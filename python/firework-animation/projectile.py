import pygame


class Projectile:
    WIDTH = 5
    HEIGHT = 10
    ALPHA_DECREMENT = 1

    def __init__(self, x, y, x_velocity, y_velocity, color):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.color = color
        self.alpha = 255

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.alpha = max(0, self.alpha - self.ALPHA_DECREMENT)

    def draw(self, window):
        self.draw_rect_alpha(window, self.color + (self.alpha,),
                             (self.x, self.y, self.WIDTH, self.HEIGHT))

    @staticmethod
    def draw_rect_alpha(surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)
