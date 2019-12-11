import os
import pygame
from math import sin, radians, degrees, copysign, cos, pi
import random
import time
from pygame.math import Vector2

# Game parameters
game_width = 200
game_height = 200
dt = 0.3
player_width = 50
player_height = 50
goal_width = 67
goal_height = 67


class Circle:
    def __init__(self):
        # fetch circle image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "agent.png")

        self.max_velocity = 5

        # initialize position, velocity, and rect object
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center = self.position)

    def update(self, dt, u):
        # update x direction
        if (self.position.x < 0 and self.velocity.x < 0 and u[0] <= 0) or \
            (self.position.x > game_width - player_width and self.velocity.x > 0 and u[0] >= 0):
            self.velocity.x = 0
        else:
            self.position.x += self.velocity.x * dt
            self.velocity.x += dt*u[0]

        # update y direction
        if (self.position.y < 0 and self.velocity.y < 0 and u[1] <= 0) or \
            (self.position.y > game_height - player_height and self.velocity.y > 0 and u[1] >= 0):
            self.velocity.y = 0
        else:
            self.position.y += self.velocity.y * dt
            self.velocity.y += dt*u[1]

    def get_state(self):
        return self.position

class Player(Circle):
    def __init__(self):
        # fetch circle image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "player.png")

        self.accel = 0.2
        self.max_velocity = 10

        # initialize position, velocity, and rect object
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.position)

class Game:
    def __init__(self):
        # pygame.init()
        # pygame.display.set_caption("Car tutorial")

        self.count = 0
        self.t = 0
        self.width = game_width
        self.height = game_height
        self.clock = pygame.time.Clock()
        self.ticks = 60
        # self.screen = pygame.display.set_mode((self.width, self.height))
        self.exit = False
        
        # set up player
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.player = Player()

        # set up goal
        goal_image_path = os.path.join(current_dir, "goal.png")
        self.goal_image = pygame.image.load(goal_image_path)
        self.goal_position = Vector2(self.width - 50, self.height - 50)
        self.goal_rect = (self.goal_image).get_rect(center = self.goal_position)

    def get_reward(self):
        player_position = (self.player).get_state()
        return -1 * player_position.distance_to(self.goal_position)

    def get_done(self):
        # player is inside of goal
        goal_x = self.goal_position.x
        goal_y = self.goal_position.y

        player_x = self.player.position.x
        player_y = self.player.position.y

        inside_x = (player_x - player_width / 2 > goal_x - goal_width / 2) and \
            (player_x + player_width / 2 < goal_x + goal_width / 2)
        inside_y = (player_y - player_height / 2 > goal_y - goal_height / 2) and \
            (player_y + player_height / 2 < goal_y + goal_height / 2)

        return inside_x and inside_y
        
    def reset(self):
        self.player.position = Vector2(0,0)
        self.player.velocity = Vector2(0,0)

        return (self.player).get_state()

    def step(self, action):
        (self.player).update(dt, action)
        self.t = self.t + dt
        self.count = self.count + 1

        done = self.get_done()

        if done:
            self.count = 0
        
        return (self.player).get_state(), self.get_reward(), done, {}

    # def run(self):
    #     while not self.exit:
        
    #         # Event queue
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 self.exit = True
            
    #         if self.get_done():
    #             self.exit = True

    #         # User input
    #         pressed = pygame.key.get_pressed()

    #         action = [0, 0]

    #         if pressed[pygame.K_UP]:
    #             action[1] -= self.player.accel
    #         elif pressed[pygame.K_DOWN]:
    #             action[1] += self.player.accel
    #         elif pressed[pygame.K_RIGHT]:
    #             action[0] += self.player.accel
    #         elif pressed[pygame.K_LEFT]:
    #             action[0] -= self.player.accel

    #         self.player.update(dt, action)

    #         print("position", self.player.position)
    #         print("rect", self.player.rect.center)
    #         # print("velocity", self.player.velocity)
    #         # print("acceleration", action)

    #         # Render
    #         self.screen.fill((255, 255, 255))
    #         self.screen.blit(self.goal_image, self.goal_rect)
    #         self.screen.blit(self.player.image, self.player.position)
    #         pygame.display.flip()

    #         self.clock.tick(self.ticks)
    #     pygame.quit()


    