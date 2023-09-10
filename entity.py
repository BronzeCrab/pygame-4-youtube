import pygame


class Entity:
    is_displayed = True

    def __init__(self, rect: pygame.Rect, icon: pygame.Surface) -> None:
        self.rect = rect
        self.icon = icon


class Sword(Entity):
    is_in_hand = False
