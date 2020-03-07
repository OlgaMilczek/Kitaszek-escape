import arcade
import engine


MAP_FILE = 'pustynia2.kmap'
RESOLUTION = 1920, 1080

WALL_COLOR = (100, 100, 100)
KITASZEK_COLOR = (0, 106, 78)
BACKGROUND_COLOR = (60, 60, 60)
TEXT_COLOR = (255, 245, 205)
ZBIGGY_COLOR = (255, 30, 50)
MOVE_TIME = 0.1
MOVE_DELAY = 0.5


class Game_labirynth (arcade.Window):
    def __init__(self, map_filename, resolution):
        width, height = resolution
        super().__init__(width, height, 'Uciekajacy Kitaszek!', fullscreen=True)

        self.engine = engine.Engine(map_filename)
        self.SQUARE_WIDTH = width / self.engine.width
        self.SQUARE_HEIGHT = height / self.engine.height

        self.set_mouse_visible(False)
        self.board_width = width
        self.board_height = height
        self.direction = None
        self.text_color = TEXT_COLOR
        self.time = 0.0
        self.Kitaszek = None
        self.Zbiggi = arcade.ShapeElementList()
        self.do_move = None

        points = []
        colors = []
        for x, y in self.engine.get_walls():
            wall_x = self.SQUARE_WIDTH * x
            wall_y = self.SQUARE_HEIGHT * y
            points.append((wall_x, wall_y))
            points.append((wall_x + self.SQUARE_WIDTH, wall_y))
            points.append((wall_x + self.SQUARE_WIDTH, wall_y + self.SQUARE_HEIGHT))
            points.append((wall_x, wall_y + self.SQUARE_HEIGHT))
            colors.append(WALL_COLOR)
            colors.append(WALL_COLOR)
            colors.append(WALL_COLOR)
            colors.append(WALL_COLOR)
        self.walls = arcade.create_rectangles_filled_with_colors(points, colors)

        self.setup()

    def setup(self):
        arcade.set_background_color(BACKGROUND_COLOR)
        self.create_Kitaszek()

    def create_Kitaszek(self):
        x, y = self.engine.position
        self.Kitaszek = arcade.create_ellipse_filled((x+0.5) * self.SQUARE_WIDTH, (y+0.5) * self.SQUARE_HEIGHT,
                                                     self.SQUARE_WIDTH/2, self.SQUARE_HEIGHT/2, KITASZEK_COLOR)

    def create_Zbiggy(self):
        self.Zbiggi = arcade.ShapeElementList()
        for ex, ey in self.engine.enemies:
            self.Zbiggi.append(arcade.create_ellipse_filled((ex+0.5) * self.SQUARE_WIDTH, (ey+0.5) * self.SQUARE_HEIGHT,
                                                     self.SQUARE_WIDTH/2, self.SQUARE_HEIGHT/2, ZBIGGY_COLOR))

    def on_draw(self):
        arcade.start_render()
        self.walls.draw()
        self.Kitaszek.draw()
        self.Zbiggi.draw()
        if self.engine.game_over:
            arcade.draw_text('GAME OVER!', 0.5 * self.width, 0.5 * self.height, color=self.text_color,
                             font_size=96, align='center', anchor_x='center', anchor_y='center', bold=True)
        elif not self.engine.game_continues:
            arcade.draw_text('Kitaszek escaped!', 0.5 * self.width, 0.5 * self.height, color=self.text_color,
                             font_size=96, align='center', anchor_x='center', anchor_y='center', bold=True)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()
        if symbol == arcade.key.LEFT:
            self.engine.make_move(engine.LEFT)
            self.do_move = engine.LEFT
            self.time = -MOVE_DELAY
        if symbol == arcade.key.RIGHT:
            self.engine.make_move(engine.RIGHT)
            self.do_move = engine.RIGHT
            self.time = -MOVE_DELAY
        if symbol == arcade.key.UP:
            self.engine.make_move(engine.UP)
            self.do_move = engine.UP
            self.time = -MOVE_DELAY
        if symbol == arcade.key.DOWN:
            self.engine.make_move(engine.DOWN)
            self.do_move = engine.DOWN
            self.time = -MOVE_DELAY

    def on_key_release(self, symbol: int, modifiers: int):
        if arcade.key.LEFT or arcade.key.RIGHT or arcade.key.UP or arcade.key.DOWN:
            self.do_move = None

    def on_update(self, delta_time: float):
        self.create_Kitaszek()
        self.create_Zbiggy()
        self.time += delta_time
        if self.time >= MOVE_TIME:
            if self.do_move is not None:
                self.engine.make_move(self.do_move)
            self.time = 0


if __name__ == '__main__':
    game = Game_labirynth(MAP_FILE, RESOLUTION)
    arcade.run()





