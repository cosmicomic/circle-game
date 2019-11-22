import os
import pygame
from math import sin, radians, degrees, copysign, cos, pi
import random
from pygame.math import Vector2

random.seed()

def generate_position(width, height):
    return (random.random() * width, random.random() * height)

def generate_velocity(speed):
    angle = (2 * pi) * random.uniform(-1, 1)
    return [speed * cos(angle), speed * sin(angle)]

speed = generate_velocity(3)
speed2 = generate_velocity(3)
speed3 = generate_velocity(3)

player_speed = [0, 0]

def update_velocity(agentrect, speed, width, height):
    if agentrect.left < 0 or agentrect.right > width:
        speed[0] = -speed[0]
    if agentrect.top < 0 or agentrect.bottom > height:
        speed[1] = -speed[1]

class Circle:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)

    def update(self):
        pass


# class Car:
#     def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
#         self.position = Vector2(x, y)
#         self.velocity = Vector2(0.0, 0.0)
#         self.angle = angle
#         self.length = length
#         self.max_acceleration = max_acceleration
#         self.max_steering = max_steering
#         self.max_velocity = 20
#         self.brake_deceleration = 10
#         self.free_deceleration = 2

#         self.acceleration = 0.0
#         self.steering = 0.0

#     def update(self, dt):
#         self.velocity += (self.acceleration * dt, 0)
#         self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

#         if self.steering:
#             turning_radius = self.length / sin(radians(self.steering))
#             angular_velocity = self.velocity.x / turning_radius
#         else:
#             angular_velocity = 0

#         self.position += self.velocity.rotate(-self.angle) * dt
#         self.angle += degrees(angular_velocity) * dt


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Circle Game")
        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.collisions = 0
        self.max_collisions = 3
        self.collision_occurring = 0
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "agent.png")
        agent_image = pygame.image.load(image_path)
        # agentrect = agent_image.get_rect(center=(self.width / 4, self.height / 4))
        # agentrect2 = agent_image.get_rect(center=(self.width / 2, self.height / 2))
        # agentrect3 = agent_image.get_rect(center=(self.width / 3, self.height / 3))
        agentrect = agent_image.get_rect(center=generate_position(self.width, self.height))
        agentrect2 = agent_image.get_rect(center=generate_position(self.width, self.height))
        agentrect3 = agent_image.get_rect(center=generate_position(self.width, self.height))

        player_image_path = os.path.join(current_dir, "player.png")
        player_image = pygame.image.load(player_image_path)
        player_rect = player_image.get_rect()

        # goal
        goal_image_path = os.path.join(current_dir, "goal.png")
        goal_image = pygame.image.load(goal_image_path)
        goal_rect = goal_image.get_rect(center = (self.width - 50, self.height - 50))

        # display number of collisions
        font = pygame.font.Font('freesansbold.ttf', 16) 
        text = font.render('Collisions: 0', True, (0, 0, 0), (255, 255, 255)) 
        textRect = text.get_rect()

        # car = Car(0, 0)
        ppu = 32

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

            agentrect = agentrect.move(speed)
            update_velocity(agentrect, speed, self.width, self.height)

            agentrect2 = agentrect2.move(speed2)
            update_velocity(agentrect2, speed2, self.width, self.height)

            agentrect3 = agentrect3.move(speed3)
            update_velocity(agentrect3, speed3, self.width, self.height)

            player_rect = player_rect.move(player_speed)


            if pressed[pygame.K_UP] and not (player_rect.top < 0):
                player_speed[1] = -2
            elif pressed[pygame.K_DOWN] and not (player_rect.bottom > self.height):
                player_speed[1] = 2
            elif pressed[pygame.K_RIGHT] and not (player_rect.right > self.width):
                player_speed[0] = 2
            elif pressed[pygame.K_LEFT] and not (player_rect.left < 0):
                player_speed[0] = -2
            else:
                player_speed[0] = 0
                player_speed[1] = 0


            if player_rect.collidelist([agentrect, agentrect2, agentrect3]) != -1:
                if self.collision_occurring == 0:
                    self.collisions += 1
                    self.collision_occurring = 1
                    text = font.render('Collisions: ' + str(self.collisions), True, (0, 0, 0), (255, 255, 255)) 
            else:
                self.collision_occurring = 0

            # Logic
            # car.update(dt)

            # Drawing
            self.screen.fill((255, 255, 255))
            self.screen.blit(goal_image, goal_rect)
            self.screen.blit(agent_image, agentrect)
            self.screen.blit(agent_image, agentrect2)
            self.screen.blit(agent_image, agentrect3)
            self.screen.blit(player_image, player_rect)
            self.screen.blit(text, textRect) 
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()