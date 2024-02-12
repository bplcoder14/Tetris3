import pygame
from pygame.locals import *
from enum import Enum
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
GRAY = (125, 125, 125)
CLEAR = (0, 0, 0, 0)

FPS = 30

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('TETRIS')
clock = pygame.time.Clock()
actions = []


def create_rectangle(width, height, color):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    return surf.convert_alpha()


def create_text(text, font, color):
    surf = pygame.font.Font.render(font, str(text), True, color)
    return surf.convert_alpha()


def create_textbox(width, height, inner_color, border_color, border_radius, border_size, font, text_color, text):
    surf = pygame.Surface((width, height))
    pygame.draw.rect(surf, inner_color, (border_size, border_size, width - border_size * 2, height - border_size * 2))
    pygame.draw.rect(surf, border_color, (0, 0, width, height), border_size, border_radius)
    text_surf = create_text(text, font, text_color)
    surf.blit(text_surf, text_surf.get_rect(center=(width / 2, height / 2)))
    return surf.convert_alpha()


class Actions(Enum):
    TEST = 0


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


class Textbox(Element):

    def __init__(self, x, y, width, height, inner_color, border_color, border_radius, border_size, font, text_color,
                 text, *groups):
        self.image = create_textbox(width, height, inner_color, border_color, border_radius, border_size, font,
                                    text_color, text)
        super().__init__(x, y, self.image, *groups)


class Button:

    def __init__(self, x, y, width, height, color, border_color, hover_color, border_size, border_radius, text, font,
                 text_color, action, *groups):
        self.x = x
        self.y = y
        self.image = create_textbox(width, height, color, border_color, border_radius, border_size, font, text_color,
                                    text)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.hover_image = create_textbox(width, height, hover_color, border_color, border_radius, border_size, font,
                                          text_color, text)
        self.hover_rect = self.hover_image.get_rect(center=(self.x, self.y))
        self.hover = True
        self.action = action

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False

    def draw(self, surface):
        self.update()
        if self.hover:
            surface.blit(self.hover_image, self.hover_rect)
            if self.hover and pygame.mouse.get_pressed()[0]:
                return self.action
        else:
            surface.blit(self.image, self.rect)
            return


def say_hello():
    print("hello")


test_rectangle = Rectangle(100, 100, 100, 75, WHITE)
test_text = Text(200, 500, "Hello World!", BASIC_FONT, color=GREEN)
test_button = Button(300, 300, 150, 100, BLACK, WHITE, GRAY, 5, 3, "test 1", BASIC_FONT, GREEN, Actions.TEST)
test_textbox = Textbox(400, 600, 150, 100, GRAY, WHITE, 3, 5,  BASIC_FONT, GREEN, "test 1")


def handle_actions():
    for action in actions:
        if action == Actions.TEST:
            say_hello()


def draw_window():
    actions.clear()
    test_rectangle.draw(win)
    test_text.draw(win)
    test_textbox.draw(win)
    actions.append(test_button.draw(win))
    handle_actions()


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
