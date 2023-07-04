import math
import random
import time
import pygame

from target import Target

pygame.init()
WIDTH, HEIGHT = 800, 600
TARGET_SPAWN_DELAY = 600
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0, 25, 40)
LIFE = 3
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_hit = 0
    clicks = 0
    missed = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_SPAWN_DELAY)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH-TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT-TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                missed += 1

            if click and target.collision(*mouse_pos):
                targets.remove(target)
                targets_hit += 1

        if missed >= LIFE:
            end_screen(WIN, elapsed_time, targets_hit, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_hit, missed)
        pygame.display.update()

    pygame.quit()


def end_screen(win, elapsed_time, targets_hit, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")

    hps = round(targets_hit / elapsed_time, 1)
    hps_label = LABEL_FONT.render(f"Hits/Sec: {hps} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_hit}", 1, "white")

    accuracy = round(targets_hit / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_mid_screen_height(time_label), 100))
    win.blit(hps_label, (get_mid_screen_height(hps_label), 200))
    win.blit(hits_label, (get_mid_screen_height(hits_label), 300))
    win.blit(accuracy_label, (get_mid_screen_height(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def get_mid_screen_height(surface):
    return WIDTH / 2 - surface.get_width() / 2


def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)


def format_time(seconds):
    milli = math.floor(int(seconds * 1000 % 1000) / 100)
    secs = int(round(seconds % 60, 1))
    minutes = int(seconds // 60)

    return f"{minutes:02d}: {secs:02d}: {milli}"


def draw_top_bar(win, elapsed_time, targets_hit, missed):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")

    hps = round(targets_hit / elapsed_time, 1)
    hps_label = LABEL_FONT.render(f"Hits/Sec: {hps} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_hit}", 1, "black")

    life_label = LABEL_FONT.render(f"Life: {LIFE - missed}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(hps_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(life_label, (650, 5))


if __name__ == "__main__":
    main()
