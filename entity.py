import pygame


class Entity:
    def __init__(self, rect: pygame.Rect, icon: pygame.Surface) -> None:
        self.rect = rect
        self.icon = icon
