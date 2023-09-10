import pygame


class Entity:
    is_displayed: bool = True

    def __init__(self, rect: pygame.Rect, icon: pygame.Surface) -> None:
        self.rect = rect
        self.icon = icon


class Player(Entity):
    dx: int = 0
    dy: int = 0


class Sword(Entity):
    is_in_hand: bool = False
