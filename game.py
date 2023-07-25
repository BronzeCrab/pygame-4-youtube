import pygame

black = (0, 0, 0)
red = (255, 0, 0)


class Game:
    def __init__(self) -> None:
        self.size = (1024, 768)

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
            pygame.time.wait(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.draw.rect(screen, red, pygame.Rect(100, 30, 60, 60))
            pygame.display.update()
