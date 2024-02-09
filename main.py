import pyglet
from pyglet import shapes
from pyglet.text import Label

background = pyglet.graphics.Group(order=0)
middle_ground_0 = pyglet.graphics.Group(order=1)
middle_ground_1 = pyglet.graphics.Group(order=2)
middle_ground_2 = pyglet.graphics.Group(order=3)
foreground = pyglet.graphics.Group(order=4)


class Button:

    def __init__(self, x, y, width, height, border_size, color, border_color, text, batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color
        self.border_size = border_size
        self.text = text
        self.batch = batch
        self.border_rectangle = shapes.Rectangle(self.x, self.y, self.width,
                                                 self.height, color=self.border_color,
                                                 group=middle_ground_0, batch=self.batch)
        self.inner_rectangle = shapes.Rectangle(self.x, self.y, self.width - self.border_size,
                                                self.height - self.border_size, color=self.color, group=middle_ground_1
                                                , batch=self.batch)
        self.label = Label(text=self.text, x=self.x, y=self.y, width=self.width, height=self.height, multiline=True,
                           group=middle_ground_2, batch=self.batch, anchor_x='center', anchor_y='center')

    def set_display(self):
        pass


class MainWindow(pyglet.window.Window):

    def __init__(self):
        super().__init__(width=1000, height=800, caption='Tetris')
        self.batch = pyglet.graphics.Batch()
        self.buttons = [Button(500, 400, 100, 75, 3, (255, 0, 0), (255, 255, 255), "button 1", self.batch)]

    def on_draw(self):
        self.clear()
        self.batch.draw()


if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
