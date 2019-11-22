import os
import pygame
from math import sin, radians, degrees, copysign, cos, pi
import random
import time
from pygame.math import Vector2

agent_speed = 3
player_speed = 3
player_velocity = [0, 0]
game_height = 400
game_width = 600
num_agents = 4

def generate_position():
    return (random.random() * game_width, random.random() * game_height)

def generate_velocity():
    angle = (2 * pi) * random.uniform(-1, 1)
    return [agent_speed * cos(angle), agent_speed * sin(angle)]

class Circle:
    def __init__(self):
        # fetch circle image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "agent.png")

        # initialize position, velocity, and rect object
        self.position = generate_position()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.position)
        self.velocity = generate_velocity()

    def update(self):
        self.rect = self.rect.move(self.velocity)
        self.update_velocity()

    def update_velocity(self):
        if self.rect.left < 0 or self.rect.right > game_width:
            self.velocity[0] = -self.velocity[0]
        if self.rect.top < 0 or self.rect.bottom > game_height:
            self.velocity[1] = -self.velocity[1]

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Circle Game")
        self.width = game_width
        self.height = game_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.collisions = 0
        self.max_collisions = 3
        self.collision_occurring = 0
        self.exit = False
        self.agents = []

    # generate n agents and store them in a list
    def generate_agents(self, n):
        for i in range(n):
            agent = Circle()
            self.agents.append(agent)
    
    def update_agents(self):
        for agent in self.agents:
            agent.update()

    def render_agents(self):
        for agent in self.agents:
            self.screen.blit(agent.image, agent.rect)

    def run(self):
        self.generate_agents(num_agents)

        # set up player
        current_dir = os.path.dirname(os.path.abspath(__file__))
        player_image_path = os.path.join(current_dir, "player.png")
        player_image = pygame.image.load(player_image_path)
        player_rect = player_image.get_rect()

        # set up goal
        goal_image_path = os.path.join(current_dir, "goal.png")
        goal_image = pygame.image.load(goal_image_path)
        goal_rect = goal_image.get_rect(center = (self.width - 50, self.height - 50))

        # display number of collisions
        font = pygame.font.Font('freesansbold.ttf', 16) 
        text = font.render('Collisions: 0', True, (0, 0, 0), (255, 255, 255)) 
        textRect = text.get_rect()

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            
            if self.collisions >= self.max_collisions:
                self.exit = True

            if goal_rect.contains(player_rect):
                self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            self.update_agents()

            # update player position and velocity
            player_rect = player_rect.move(player_velocity)

            if pressed[pygame.K_UP] and not (player_rect.top < 0):
                player_velocity[1] = -player_speed
            elif pressed[pygame.K_DOWN] and not (player_rect.bottom > self.height):
                player_velocity[1] = player_speed
            elif pressed[pygame.K_RIGHT] and not (player_rect.right > self.width):
                player_velocity[0] = player_speed
            elif pressed[pygame.K_LEFT] and not (player_rect.left < 0):
                player_velocity[0] = -player_speed
            else:
                player_velocity[0] = 0
                player_velocity[1] = 0

            # check for collisions
            if player_rect.collidelist([agent.rect for agent in self.agents]) != -1:
                if self.collision_occurring == 0:
                    self.collisions += 1
                    self.collision_occurring = 1
                    text = font.render('Collisions: ' + str(self.collisions), True, (0, 0, 0), (255, 255, 255)) 
            else:
                self.collision_occurring = 0

            # Render
            self.screen.fill((255, 255, 255))
            self.screen.blit(goal_image, goal_rect)
            self.render_agents()
            self.screen.blit(player_image, player_rect)
            self.screen.blit(text, textRect) 
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()