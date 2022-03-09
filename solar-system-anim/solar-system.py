import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1400, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Animation")

WHITE = (255, 255, 255)
SUN = (249, 215, 28)
MERCURY = (173, 168, 165)
VENUS = (248, 226, 176)
EARTH = (100, 149, 237)
MARS = (161, 37, 27)
JUPITER = (200, 139, 58)
SATURN = (227, 224, 192)
URANUS = (79, 208, 231)
NEPTUNE = (62, 84, 232)

FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    AU = 149.6e6*1000  # ASTRONOMICAL_UNITS
    G = 6.67408e-11  # GRAVITATIONAL_CONSTANT
    SCALE = 250 / AU  # 1AU = 100px
    TIMESTAMP = 3600*24  # 1day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(window, self.color, False, updated_points, 2)

        pygame.draw.circle(window, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(
                f"{self.name} -> {round(self.distance_to_sun/1000,1)}km", 1, WHITE)
            window.blit(distance_text, (x - distance_text.get_width() /
                                        2, y - distance_text.get_height() / 2))

    def rotation_angle(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x-self.x
        distance_y = other_y-self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_force_x = total_force_y = 0

        for planet in planets:
            if self == planet:
                continue

            force_x, force_y = self.rotation_angle(planet)
            total_force_x += force_x
            total_force_y += force_y

        self.x_vel += total_force_x / self.mass * self.TIMESTAMP
        self.y_vel += total_force_y / self.mass * self.TIMESTAMP

        self.x += self.x_vel * self.TIMESTAMP
        self.y += self.y_vel * self.TIMESTAMP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, SUN, 1.98892 * 10**30, "Sun")
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, MERCURY,
                     3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, VENUS, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, EARTH, 5.9742 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, MARS, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-1.8 * Planet.AU, 0, 12,
                     JUPITER, 1.898 * 10**27, "Jupiter")
    jupiter.y_vel = 13.06 * 1000
    saturn = Planet(-2 * Planet.AU,  0, 17, SATURN, 5.683 * 10**26, "Saturn")
    saturn.y_vel = 9.68 * 1000
    uranus = Planet(-2.2 * Planet.AU, 0,   14,
                    URANUS, 8.681 * 10**25, "Uranus")
    uranus.y_vel = 6.80 * 1000
    neptune = Planet(-2.5 * Planet.AU, 0,  14,
                     NEPTUNE, 1.024 * 10**26, "Neptune")
    neptune.y_vel = 5.43 * 1000

    planets = [sun, mercury, venus, earth,
               mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #     run = False
                return

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        pygame.display.update()

    # pygame.quit()


main()
