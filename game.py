import random

import pygame

from entity import Entity, Sword, Player, Box


LEVEL_MAPS = [
    "lvl1.txt",
    "lvl2.txt",
]

BLACK = (0, 0, 0)


class Game:
    def __init__(self) -> None:
        screen_ratio = 1.4
        y_size = 1000
        x_size = y_size * screen_ratio
        self.size = (int(x_size), int(y_size))
        self.screen = None
        self._level = 0
        self.rect_x_size = None
        self.rect_y_size = None
        self.reg_event_key = None
        self.running = True
        self.box_pulling_mode = False

        self.init_entities()
        self.setup_current_level()

    def init_entities(self) -> None:
        self.player = None
        self.walls = []
        self.door = None
        self.boxes = []
        self.monsters = []
        self.sword = None

    def on_init(self) -> None:
        """
        Initialize the game's screen, and begin running the game.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Very cool game tbh")
        while self.running:
            pygame.time.wait(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.reg_event_key = event.key
                if event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
                    self.box_pulling_mode = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    if self.sword and self.sword.is_in_hand:
                        self.sword.is_displayed = False

            self.update_player_and_box_pos()
            self.check_if_sword_killed_monster()
            self.move_monsters()
            self.check_if_sword_killed_monster()
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
        aclass: type = None,
    ) -> Entity | Sword | Player:
        rect = pygame.Rect(
            rect_x_cord,
            rect_y_cord,
            rect_x_size,
            rect_y_size,
        )

        icon = pygame.image.load(icon_file)
        icon_size = (rect.width, rect.height)
        icon = pygame.transform.scale(icon, icon_size)
        if aclass:
            return aclass(rect, icon)
        else:
            return Entity(rect, icon)

    def setup_lvl(self, data: list[list[str]]) -> None:
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
                        aclass=Player,
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
                    icon_file = "./images/monster.png"
                    monster = self.create_entity(
                        icon_file,
                        rect_x_cord,
                        rect_y_cord,
                        self.rect_x_size,
                        self.rect_y_size,
                    )
                    self.monsters.append(monster)
                elif key == "S":
                    icon_file = "./images/sword.png"
                    self.sword = self.create_entity(
                        icon_file,
                        rect_x_cord,
                        rect_y_cord,
                        self.rect_x_size,
                        self.rect_y_size,
                        aclass=Sword,
                    )
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
                            aclass=Box,
                        )
                        self.boxes.append(box)

    def setup_current_level(self) -> None:
        """
        Set up the current level of the game.
        """

        data = self.load_map("./lvl_data/" + LEVEL_MAPS[self._level])
        self.setup_lvl(data)

    def check_if_box_killed_monster(self, box: Entity) -> None:
        for monster in self.monsters:
            if monster.rect.x == box.rect.x and monster.rect.y == box.rect.y:
                self.monsters.remove(monster)

    def check_if_sword_killed_monster(self) -> None:
        if self.sword and self.sword.is_in_hand and self.sword.is_displayed:
            for monster in self.monsters:
                if (
                    monster.rect.x == self.sword.rect.x
                    and monster.rect.y == self.sword.rect.y
                ):
                    self.monsters.remove(monster)

    def check_for_win(self) -> bool:
        return not self.monsters

    def check_if_game_over(self) -> bool:
        for monster in self.monsters:
            if (
                monster.rect.x == self.player.rect.x
                and monster.rect.y == self.player.rect.y
            ):
                print("Game is over, you lose, restart")
                self.init_entities()
                self.setup_current_level()
                return True
        return False

    def update_player_and_box_pos(self) -> None:
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
            if reg_k == pygame.K_LCTRL:
                self.box_pulling_mode = True
            if reg_k == pygame.K_SPACE and self.sword and self.sword.is_in_hand:
                # todo factor out in separate func
                self.sword.rect.x = self.player.rect.x + self.player.dx
                self.sword.rect.y = self.player.rect.y + self.player.dy
                for entity in [self.door] + self.walls + self.boxes:
                    if (
                        self.sword.rect.x == entity.rect.x
                        and self.sword.rect.y == entity.rect.y
                    ):
                        break
                else:
                    self.sword.is_displayed = True
            self.reg_event_key = None

        new_player_x, new_player_y = self.player.rect.x + dx, self.player.rect.y + dy
        new_player_rect = pygame.Rect(
            new_player_x, new_player_y, self.player.rect.w, self.player.rect.h
        )
        if (
            new_player_x == self.door.rect.x
            and new_player_y == self.door.rect.y
            and self.check_for_win()
        ):
            if self._level == 1:
                print("Game if over, you won!")
                self.running = False
                return

            print("Lvl is over, you win, loading next lvl")
            self._level += 1
            self.init_entities()
            self.setup_current_level()
            return

        if self.check_if_game_over():
            return

        if self.box_pulling_mode:
            for entity in self.walls + self.boxes + [self.door]:
                if pygame.Rect.colliderect(new_player_rect, entity.rect):
                    break
            else:
                # check if there is a box next to current player pos
                for box in self.boxes:
                    if any(
                        (
                            (
                                box.rect.x == self.player.rect.x + dx
                                and box.rect.y == self.player.rect.y
                            ),
                            (
                                box.rect.x == self.player.rect.x - dx
                                and box.rect.y == self.player.rect.y
                            ),
                            (
                                box.rect.x == self.player.rect.x
                                and box.rect.y == self.player.rect.y + dy
                            ),
                            (
                                box.rect.x == self.player.rect.x
                                and box.rect.y == self.player.rect.y - dy
                            ),
                        )
                    ):
                        box.rect.x += dx
                        box.rect.y += dy
                        self.check_if_box_killed_monster(box)
                        break
                self.player.rect.x, self.player.rect.y = new_player_x, new_player_y
        else:
            for entity in self.walls + self.boxes + [self.door]:
                if pygame.Rect.colliderect(new_player_rect, entity.rect):
                    if type(entity) is Box:
                        # player will try to move this entity (box in this case)
                        box_to_move = entity
                        # next possible box coords
                        new_box_to_move_x = box_to_move.rect.x + dx
                        new_box_to_move_y = box_to_move.rect.y + dy
                        # check if our box will collide with door or wall after the move
                        for next_d_or_w in self.walls + [self.door]:
                            # if we are trying to move box into wall or door,
                            # then do nothing
                            if (
                                new_box_to_move_x == next_d_or_w.rect.x
                                and new_box_to_move_y == next_d_or_w.rect.y
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

        # save dx, dy to the player, to use it on next step to
        # determine direction of the sword
        if dx or dy:
            self.player.dx = dx
            self.player.dy = dy
        self.check_if_player_picked_up_sword(new_player_x, new_player_y)

    def check_if_player_picked_up_sword(self, new_player_x: int, new_player_y: int):
        if self.sword and not self.sword.is_in_hand:
            if new_player_x == self.sword.rect.x and new_player_y == self.sword.rect.y:
                self.sword.is_displayed = False
                self.sword.is_in_hand = True

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
            self.check_if_box_killed_monster(box)

        self.player.rect.x += dx
        self.player.rect.y += dy

    def move_monsters(self) -> None:
        for monster in self.monsters:
            random_i = random.randint(1, 8)
            if random_i == 1:
                dx = self.rect_x_size
                dy = 0
            elif random_i == 2:
                dx = -self.rect_x_size
                dy = 0
            elif random_i == 3:
                dx = 0
                dy = self.rect_y_size
            elif random_i == 4:
                dx = 0
                dy = -self.rect_y_size
            elif random_i == 5:
                dx = self.rect_x_size
                dy = self.rect_y_size
            elif random_i == 6:
                dx = -self.rect_x_size
                dy = self.rect_y_size
            elif random_i == 7:
                dx = self.rect_x_size
                dy = -self.rect_y_size
            elif random_i == 8:
                dx = -self.rect_x_size
                dy = -self.rect_y_size

            new_possible_monster_x = monster.rect.x + dx
            new_possible_monster_y = monster.rect.y + dy
            for entity in self.walls + self.boxes + [self.door]:
                if (
                    entity.rect.x == new_possible_monster_x
                    and entity.rect.y == new_possible_monster_y
                ):
                    break
            else:
                monster.rect.x = new_possible_monster_x
                monster.rect.y = new_possible_monster_y

    def update_lvl(self) -> None:
        self.screen.fill(BLACK)
        for entity in (
            self.walls
            + self.boxes
            + [self.player, self.door, self.sword]
            + self.monsters
        ):
            if entity and entity.is_displayed:
                self.screen.blit(entity.icon, entity.rect)
        pygame.display.update()
