import time
import pygame
import random
from firework import Firework


class Launcher:
    WIDTH = 20
    HEIGHT = 20
    COLOR = "Grey"

    def __init__(self, x, y, frequency):
        self.x = x
        self.y = y
        self.frequency = frequency  # ms
        self.start_time = time.time()
        self.fireworks = []

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR,
                         (self.x, self.y, self.WIDTH, self.HEIGHT))

        for firework in self.fireworks:
            firework.draw(window)

    def loop(self, max_width, max_height):
        current_time = time.time()
        time_elapsed = current_time - self.start_time

        if time_elapsed * 1000 >= self.frequency:
            self.start_time = current_time
            self.launch()

        fireworks_to_remove = []
        for firework in self.fireworks:
            firework.move(max_width, max_height)

            if firework.exploded and len(firework.projectiles) == 0:
                fireworks_to_remove.append(firework)

        for firework in fireworks_to_remove:
            self.fireworks.remove(firework)

    def launch(self):
        color = random.choice(Firework.COLORS)
        explode_height = random.randint(50, 400)  # randint

        firework = Firework(self.x + self.WIDTH/2, self.y, -
                            5, explode_height, color)

        self.fireworks.append(firework)
