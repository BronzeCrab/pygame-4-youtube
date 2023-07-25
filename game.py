import pygame

LEVEL_MAPS = [
    "lvl1.txt",
]


class Game:
    def __init__(self) -> None:
        ratio = 1.33
        y_size = 1000
        x_size = y_size * ratio
        self.size = (x_size, y_size)
        self._level = 0
        self.screen = None

    def on_init(self) -> None:
        """
        Initialize the game's screen, and begin running the game.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.update()
        pygame.display.set_caption("Hello World")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.setup_current_level()

    def load_map(self, filename: str) -> list[list[str]]:
        """
        Load the map data from the given filename and return as a list of lists.
        """

        with open(filename) as f:
            map_data = [line.split() for line in f]
        return map_data

    def setup_first_lvl(self, data: list[list[str]]):
        """
        Drawing first level of the game.
        """
        row_range = len(data)
        col_range = len(data[0])
        for row_ind in range(row_range):
            for col_ind in range(col_range):
                key = data[row_ind][col_ind]
                if key == "X":
                    row_frac = row_ind / row_range
                    col_frac = col_ind / col_range
                    rect_x_cord = col_frac * self.size[0]
                    rect_x_size = self.size[0] / col_range
                    rect_y_cord = row_frac * self.size[1]
                    rect_y_size = self.size[1] / row_range

                    rect = pygame.Rect(
                        rect_x_cord,
                        rect_y_cord,
                        rect_x_size,
                        rect_y_size,
                    )

                    icon_file = "./images/wall.jpg"
                    icon = pygame.image.load(icon_file)
                    icon_size = (rect.width, rect.height)
                    icon = pygame.transform.scale(icon, icon_size)
                    self.screen.blit(icon, rect)

        pygame.display.update()

    def setup_current_level(self):
        """
        Set up the current level of the game.
        """

        data = self.load_map("./lvl_data/" + LEVEL_MAPS[self._level])

        if self._level == 0:
            self.setup_first_lvl(data)
