import pygame
import math
import random
from projectile import Projectile


class Firework:
    COLORS = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 255, 255),
        (255, 165, 0),
        (255, 255, 255),
        (230, 230, 250),
        (255, 192, 203)
    ]

    RADIUS = 10
    MAX_PROJECTILE = 100
    MIN_PROJECTILE = 25
    PROJECTILE_VELOCITY = 4

    def __init__(self, x, y, y_velocity, explode_height, color):
        self.x = x
        self.y = y
        self.y_velocity = y_velocity
        self.explode_height = explode_height
        self.color = color
        self.projectiles = []
        self.exploded = False

    def draw(self, window):
        if not self.exploded:
            pygame.draw.circle(window, self.color,
                               (self.x, self.y), self.RADIUS)

        for projectile in self.projectiles:
            projectile.draw(window)

    def move(self, max_width, max_height):
        if not self.exploded:
            self.y += self.y_velocity

            if self.y <= self.explode_height:
                self.explode()

        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()

            if projectile.x >= max_width or projectile.x < 0:
                projectiles_to_remove.append(projectile)
            elif projectile.y >= max_height or projectile.y < 0:
                projectiles_to_remove.append(projectile)

        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)

    def explode(self):
        self.exploded = True
        number_of_projectiles = random.randrange(
            self.MIN_PROJECTILE, self.MAX_PROJECTILE)

        if random.randint(0, 1) == 0:
            self.create_circular_projectiles(number_of_projectiles)
        else:
            self.create_star_projectiles()

    def create_circular_projectiles(self, number_of_projectiles):
        angle_dif = math.pi*2 / number_of_projectiles
        current_angle = 0
        velocity = random.randrange(self.PROJECTILE_VELOCITY - 1,
                                    self.PROJECTILE_VELOCITY + 1)
        for _ in range(number_of_projectiles):
            x_velocity = math.sin(current_angle) * velocity
            y_velocity = math.cos(current_angle) * velocity
            color = random.choice(self.COLORS)
            self.projectiles.append(Projectile(
                self.x, self.y, x_velocity, y_velocity, color))
            current_angle += angle_dif

    def create_star_projectiles(self):
        angle_diff = math.pi/4
        current_angle = 0
        number_of_projectiles = 32
        for i in range(1, number_of_projectiles + 1):
            vel = self.PROJECTILE_VELOCITY + (i % (number_of_projectiles / 8))
            x_vel = math.sin(current_angle) * vel
            y_vel = math.cos(current_angle) * vel
            color = random.choice(self.COLORS)
            self.projectiles.append(Projectile(
                self.x, self.y, x_vel, y_vel, color))
            if i % (number_of_projectiles / 8) == 0:
                current_angle += angle_diff
