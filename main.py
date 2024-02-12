import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.font.init()

BASIC_FONT = pygame.font.SysFont('arial', size=20)
BOLD_FONT = pygame.font.SysFont('arial', size=20, bold=True)
ITALIC_FONT = pygame.font.SysFont('arial', size=20, italic=True)
BOLD_ITALIC_FONT = pygame.font.SysFont('arial', size=20, bold=True, italic=True)

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


def create_rectangle(width, height, color):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    return surf.convert_alpha()


def create_text(text, font, color):
    surf = pygame.font.Font.render(font, str(text), True, color)
    return surf.convert_alpha()


def create_textbox(width, height, inner_color, border_radius, border_color, border_size, font, text_color, text):
    surf = pygame.Surface((width, height))
    pygame.draw.rect(surf, inner_color, (width - border_size * 2, height - border_size * 2, border_size, border_size))
    pygame.draw.rect(surf, border_color, (width, height, 0, 0), border_size, border_radius)
    text_surf = create_text(text, font, text_color)
    surf.blit(text_surf, text_surf.get_rect(center=(width / 2, height / 2)))
    return surf.convert_alpha()


class Element(pygame.sprite.Sprite):

    def __init__(self, x, y, image, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update_rect(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        self.update_rect()
        surface.blit(self.image, self.rect)


class Text(Element):

    def __init__(self, x, y, text, font, color, *groups):
        self.image = create_text(text, font, color)
        super().__init__(x, y, self.image, *groups)


class Rectangle(Element):

    def __init__(self, x, y, width, height, color, *groups):
        self.image = create_rectangle(width, height, color)
        super().__init__(x, y, self.image, *groups)


class Button:

    def __init__(self, x, y, width, height, text, font, color, *groups):
        self.x = x
        self.y = y
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.hover_image = pygame.Surface((width, height))
        self.hover_rect = self.hover_image.get_rect(center=(self.x, self.y))
        self.hover = False

    def update(self):
        pass

    def draw(self, surface):
        self.update()
        if self.hover:
            surface.blit(self.hover_image, self.hover_rect)
        else:
            surface.blit(self.image, self.rect)


test_rectangle = Rectangle(100, 100, 100, 75, WHITE)
test_text = Text(200, 500, "Hello World!", BASIC_FONT, color=GREEN)


def draw_window():
    test_rectangle.draw(win)
    test_text.draw(win)


def main():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        win.fill(BLACK)
        draw_window()
        pygame.display.flip()


if __name__ == '__main__':
    main()
