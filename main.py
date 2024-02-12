import pygame
from pygame.locals import *
import sys

pygame.init()

# colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CLEAR = (0, 0, 0, 0)

FPS = 30

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('TETRIS')
clock = pygame.time.Clock()


def main():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        win.fill(BLACK)
        pygame.display.flip()




if __name__ == '__main__':
    main()
