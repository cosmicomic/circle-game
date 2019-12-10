import os
import pygame
from math import sin, radians, degrees, copysign, cos, pi
import random
import time
from pygame.math import Vector2

# Game parameters
game_width = 500
game_height = 500
dt = 0.5

class Circle:
    def __init__(self):
        # fetch circle image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "agent.png")
        
        self.max_velocity = 10

        # initialize position, velocity, and rect object
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, u):
        self.position[0] += self.velocity.x * dt
        self.position[1] += self.velocity.y * dt

        self.velocity.x += dt*u[0]
        self.velocity.y += dt*u[1]
        self.velocity.x = max(-self.max_velocity,
                              min(self.velocity.x, self.max_velocity))
        self.velocity.y = max(-self.max_velocity,
                              min(self.velocity.y, self.max_velocity))

    def getState(self):
        return self.position, self.velocity

class Player(Circle):
    def __init__(self):
        # fetch circle image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "player.png")

        self.accel = 0.5
        self.max_velocity = 10

        # initialize position, velocity, and rect object
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0,0)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.position)


class Game:
    def __init__(self):
        self.width = game_width
        self.height = game_height
        
        # set up player
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.player = Player()

        # set up goal
        goal_image_path = os.path.join(current_dir, "goal.png")
        self.goal_image = pygame.image.load(goal_image_path)
        self.goal_position = Vector2(self.width - 50, self.height - 50)
        self.goal_rect = (self.goal_image).get_rect(center = self.goal_position)

    def get_reward(self):
        player_position, _ = (self.player).getState()
        return -1 * player_position.distance_to(self.goal_position)

    def get_done(self):
        # player is inside of goal
        return (self.goal_rect).contains(self.player)

    def reset(self):
        (self.player).position = Vector2(0,0)

    def step(self, action):
        (self.player).update(dt, action)
