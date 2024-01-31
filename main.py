import pyglet


class MainWindow(pyglet.window.Window):

    def __init__(self):
        super().__init__(width=1000, height=800, caption='Tetris')

    def on_draw(self):
        self.clear()


if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
