import pygame
from launcher import Launcher

pygame.init()

WIDTH, HEIGHT = 800, 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks!!")

FPS = 60


def draw(launchers):
    window.fill((20, 2, 54))

    for launcher in launchers:
        launcher.draw(window)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    launchers = [Launcher(100, HEIGHT - Launcher.HEIGHT, 3000),
                 Launcher(300, HEIGHT - Launcher.HEIGHT, 4000),
                 Launcher(500, HEIGHT - Launcher.HEIGHT, 2000),
                 Launcher(700, HEIGHT - Launcher.HEIGHT, 5000)]

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for launcher in launchers:
            launcher.loop(WIDTH, HEIGHT)

        draw(launchers)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
