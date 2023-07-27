import random

import pygame

from entity import Entity


LEVEL_MAPS = [
    "lvl1.txt",
]

BLACK = (0, 0, 0)


class Game:
    def __init__(self) -> None:
        screen_ratio = 1.4
        y_size = 1000
        x_size = y_size * screen_ratio
        self.size = (int(x_size), int(y_size))
        self._level = 0
        self.player = None
        self.screen = None
        self.walls = []
        self.reg_event_key = None
        self.rect_x_size = None
        self.rect_y_size = None
        self.door = None
        self.boxes = []
        self.setup_current_level()

    def on_init(self) -> None:
        """
        Initialize the game's screen, and begin running the game.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Hello World")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.reg_event_key = event.key
            self.update_player_and_box_pos()
            self.update_lvl()

    def load_map(self, filename: str) -> list[list[str]]:
        """
        Load the map data from the given filename and return as a list of lists.
        """

        with open(filename) as f:
            map_data = [line.split() for line in f]
        return map_data

    def create_entity(
        self,
        icon_file: str,
        rect_x_cord: float,
        rect_y_cord: float,
        rect_x_size: float,
        rect_y_size: float,
    ) -> Entity:
        rect = pygame.Rect(
            rect_x_cord,
            rect_y_cord,
            rect_x_size,
            rect_y_size,
        )

        icon = pygame.image.load(icon_file)
        icon_size = (rect.width, rect.height)
        icon = pygame.transform.scale(icon, icon_size)
        return Entity(rect, icon)

    def setup_first_lvl(self, data: list[list[str]]) -> None:
        """
        Drawing first level of the game.
        """
        row_range = len(data)
        col_range = len(data[0])
        self.rect_x_size = self.size[0] / col_range
        self.rect_y_size = self.size[1] / row_range

        for row_ind in range(row_range):
            for col_ind in range(col_range):
                key = data[row_ind][col_ind]

                row_frac = row_ind / row_range
                col_frac = col_ind / col_range
                rect_x_cord = round(col_frac * self.size[0])
                rect_y_cord = round(row_frac * self.size[1])

                if key == "X":
                    icon_file = "./images/wall.jpg"
                    wall = self.create_entity(
                        icon_file,
                        rect_x_cord,
                        rect_y_cord,
                        self.rect_x_size,
                        self.rect_y_size,
                    )
                    self.walls.append(wall)
                elif key == "C":
                    icon_file = "./images/player.png"
                    self.player = self.create_entity(
                        icon_file,
                        rect_x_cord,
                        rect_y_cord,
                        self.rect_x_size,
                        self.rect_y_size,
                    )

                elif key == "D":
                    icon_file = "./images/door.png"
                    self.door = self.create_entity(
                        icon_file,
                        rect_x_cord,
                        rect_y_cord,
                        self.rect_x_size,
                        self.rect_y_size,
                    )
                elif key == "M":
                    pass
                else:
                    r = random.randint(0, 10)
                    if r == 0:
                        icon_file = "./images/box.png"
                        box = self.create_entity(
                            icon_file,
                            rect_x_cord,
                            rect_y_cord,
                            self.rect_x_size,
                            self.rect_y_size,
                        )
                        self.boxes.append(box)

    def setup_current_level(self) -> None:
        """
        Set up the current level of the game.
        """

        data = self.load_map("./lvl_data/" + LEVEL_MAPS[self._level])

        if self._level == 0:
            self.setup_first_lvl(data)

    def update_player_and_box_pos(self) -> None:
        keys_pressed = pygame.key.get_pressed()
        dx, dy = 0, 0
        if self.reg_event_key:
            reg_k = self.reg_event_key
            if reg_k == pygame.K_LEFT or reg_k == pygame.K_a:
                dx -= self.rect_x_size
            if reg_k == pygame.K_RIGHT or reg_k == pygame.K_d:
                dx += self.rect_x_size
            if reg_k == pygame.K_UP or reg_k == pygame.K_w:
                dy -= self.rect_y_size
            if reg_k == pygame.K_DOWN or reg_k == pygame.K_s:
                dy += self.rect_y_size
            self.reg_event_key = None

        new_player_x, new_player_y = self.player.rect.x + dx, self.player.rect.y + dy
        new_player_rect = pygame.Rect(
            new_player_x, new_player_y, self.player.rect.w, self.player.rect.h
        )
        for entity in self.walls + self.boxes + [self.door]:
            if pygame.Rect.colliderect(new_player_rect, entity.rect):
                if entity in self.boxes:
                    # player will try to move this entity (box in this case)
                    box_to_move = entity
                    # next possible box coords
                    new_box_to_move_x = box_to_move.rect.x + dx
                    new_box_to_move_y = box_to_move.rect.y + dy
                    # check if our box will collide after the move
                    for next_b_d_or_w in self.walls + self.boxes + [self.door]:
                        # if we are trying to move box into wall or dor,
                        # then do nothing
                        if (
                            new_box_to_move_x == next_b_d_or_w.rect.x
                            and new_box_to_move_y == next_b_d_or_w.rect.y
                            and next_b_d_or_w not in self.boxes
                        ):
                            break
                    # we try to move box into other box
                    else:
                        pot_moved_boxes = self.get_potential_moved_boxes(
                            box_to_move.rect.x, box_to_move.rect.y, dx, dy
                        )
                        self.move_some_or_not(pot_moved_boxes, dx, dy)
                break
        else:
            self.player.rect.x, self.player.rect.y = new_player_x, new_player_y

    def is_box_near_the_wall(self, box: Entity, dx: int, dy: int) -> bool:
        for wall in self.walls:
            if wall.rect.x == box.rect.x + dx and wall.rect.y == box.rect.y + dy:
                return True
        return False

    def get_potential_moved_boxes(
        self,
        a_box_x: int,
        a_box_y: int,
        dx: int,
        dy: int,
        potential_moved_boxes=None,
    ) -> None:
        if potential_moved_boxes is None:
            potential_moved_boxes = []

        for box in self.boxes:
            if (
                box.rect.x == a_box_x
                and box.rect.y == a_box_y
                and box not in potential_moved_boxes
            ):
                potential_moved_boxes.append(box)
                self.get_potential_moved_boxes(
                    box.rect.x + dx, box.rect.y + dy, dx, dy, potential_moved_boxes
                )
                break
        return potential_moved_boxes

    def move_some_or_not(self, pot_moved_boxes: list[Entity], dx: int, dy: int) -> None:
        for box in pot_moved_boxes:
            if self.is_box_near_the_wall(box, dx, dy):
                return

        for box in pot_moved_boxes:
            box.rect.x += dx
            box.rect.y += dy

        self.player.rect.x += dx
        self.player.rect.y += dy

    def update_lvl(self) -> None:
        self.screen.fill(BLACK)
        for entity in self.walls + self.boxes + [self.player, self.door]:
            self.screen.blit(entity.icon, entity.rect)
        pygame.display.update()
