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


def create_circle(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
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
    TEST2 = 1


class AppScene(Enum):
    MAIN_MENU = 0
    PLAY = 1


class Mouse:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.left = False
        self.right = False
        self.middle = False
        self.scroll = 0
        self.scroll_up = False
        self.scroll_down = False
        self.held = True

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        if self.left:
            self.held = True
        else:
            self.held = False
        self.left, self.middle, self.right = pygame.mouse.get_pressed()
        self.scroll = pygame.mouse.get_rel()[1]
        if self.scroll > 0:
            self.scroll_up = True
            self.scroll_down = False
        elif self.scroll < 0:
            self.scroll_up = False
            self.scroll_down = True
        else:
            self.scroll_up = False
            self.scroll_down = False


mouse = Mouse()


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
        return


class Text(Element):

    def __init__(self, x, y, text, font, color, *groups):
        self.image = create_text(text, font, color)
        super().__init__(x, y, self.image, *groups)


class Circle(Element):

    def __init__(self, x, y, radius, color, *groups):
        self.image = create_circle(radius, color)
        super().__init__(x, y, self.image, *groups)
        self.rect = self.image.get_rect(center=(self.x, self.y))


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
            if pygame.mouse.get_pressed()[0] and not mouse.held:
                return self.action
            else:
                return
        else:
            surface.blit(self.image, self.rect)
            return


class Scene:

    def __init__(self, elements=None):
        self.elements = []
        if elements is not None:
            self.elements = elements
        self.actions = []

    def add_element(self, element):
        self.elements.append(element)

    def draw(self, surface):
        self.actions.clear()
        for element in self.elements:
            self.actions.append(element.draw(surface))
        return self.actions


app_scene = AppScene.MAIN_MENU

test_rectangle = Rectangle(100, 100, 100, 75, WHITE)
test_text = Text(200, 500, "Hello World!", BASIC_FONT, color=GREEN)
test_button = Button(300, 300, 150, 100, BLACK, WHITE, GRAY, 5, 3, "test 1", BASIC_FONT, GREEN, Actions.TEST)
test_textbox = Textbox(400, 600, 150, 100, GRAY, WHITE, 3, 5, BASIC_FONT, GREEN, "test 1")
test_circle = Circle(500, 500, 50, RED)

test_scene = Scene()
test_scene.add_element(test_rectangle)
test_scene.add_element(test_text)
test_scene.add_element(test_button)
test_scene.add_element(test_textbox)
test_scene.add_element(test_circle)

main_menu_scene = test_scene
play_scene = Scene()
play_scene.add_element(Rectangle(100, 100, 100, 75, WHITE))
play_scene.add_element(Button(300, 300, 150, 100, BLACK, WHITE, GRAY, 5, 3, "test 1", BASIC_FONT, GREEN, Actions.TEST2))


def handle_actions():
    global app_scene
    for action in actions:
        if action == Actions.TEST:
            print("test")
            app_scene = AppScene.PLAY
        elif action == Actions.TEST2:
            print("test2")
            app_scene = AppScene.MAIN_MENU


def draw_window():
    global actions
    if app_scene == AppScene.MAIN_MENU:
        actions = main_menu_scene.draw(win)
    elif app_scene == AppScene.PLAY:
        actions = play_scene.draw(win)
    handle_actions()


def main():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        win.fill(BLACK)
        mouse.update()
        draw_window()
        pygame.display.flip()


if __name__ == '__main__':
    main()
