import pygame

black = (0, 0, 0)
red = (255, 0, 0)

LEVEL_MAPS = [
    "lvl1.txt",
]


class Game:
    def __init__(self) -> None:
        self.size = (1024, 768)
        self._level = 0

    def on_init(self) -> None:
        """
        Initialize the game's screen, and begin running the game.
        """
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        screen.fill(black)
        pygame.display.update()
        pygame.display.set_caption("Hello World")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.setup_current_level())
                    pygame.quit()
                    exit()
            pygame.draw.rect(screen, red, pygame.Rect(100, 30, 60, 60))
            pygame.display.update()

    def load_map(self, filename: str) -> list[list[str]]:
        """
        Load the map data from the given filename and return as a list of lists.
        """

        with open(filename) as f:
            map_data = [line.split() for line in f]
        return map_data

    def setup_current_level(self):
        """
        Set up the current level of the game.
        """

        data = self.load_map("./lvl_data/" + LEVEL_MAPS[self._level])

        if self._level == 0:
            print(data)
