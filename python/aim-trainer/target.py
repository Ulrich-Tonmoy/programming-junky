import math
import pygame


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.4

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE > self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, "white", (self.x, self.y), self.size)
        pygame.draw.circle(win, "red", (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, "white", (self.x, self.y), self.size * 0.5)
        pygame.draw.circle(win, "red", (self.x, self.y), self.size * 0.3)

    def collision(self, x, y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size
