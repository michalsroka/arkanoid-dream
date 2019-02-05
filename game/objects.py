import pygame
from game.game_utils import load_image, darken_image
from game.config import img_cfg, size_cfg
import math
import numpy as np


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        bar_name = img_cfg.get('bars').get('basic')
        width = size_cfg.get('bars').get('basic').get('x')
        height = size_cfg.get('bars').get('basic').get('y')
        self.image, self.rect = load_image(bar_name, width=width, height=height)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect = self.rect.move(self.area.right / 2 - self.rect.right / 2,
                                   self.area.bottom - 30)
        self.speed = 5
        self.state = "still"
        self.move_pos = [0, 0]

    def update(self):
        move_pos = self.rect.move(self.move_pos)
        if self.area.contains(move_pos):
            self.rect = move_pos

    def move_left(self):
        self.move_pos[0] = self.move_pos[0] - self.speed
        self.state = "moveleft"

    def move_right(self):
        self.move_pos[0] = self.move_pos[0] + self.speed
        self.state = "moveright"

    def set_pos(self, x, y):
        self.rect.topleft = x, y


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ball_name = img_cfg.get('balls').get('basic')
        width = size_cfg.get('balls').get('basic').get('x')
        height = size_cfg.get('balls').get('basic').get('y')
        self.image, self.rect = load_image(ball_name, width=width, height=height, colorkey=-1)

        self.speed = 7
        angle = 3 / 2 * math.pi
        self.vector = (angle, self.speed)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.left_bar = False
        self.left_tile = True
        self.on_bar = True

    def update(self, bar_x=None, bar_y=None):
        if self.on_bar:
            self.rect.midbottom = (bar_x, bar_y)
        # TODO change to vector speed
        # TODO fix collision detection
        self.rect = self.get_updated_pos()
        if self.rect.left < 0 or self.rect.right > self.area.right:
            self.side_bounce()
        if self.rect.top < 0:
            self.vertical_bounce()

    def side_bounce(self):
        new_angle = math.pi - self.vector[0]
        if new_angle < 0:
            new_angle = 2 * math.pi + new_angle
        self.vector = (new_angle, self.speed)

    def vertical_bounce(self):
        self.vector = (2 * math.pi - self.vector[0], self.speed)

    def get_updated_pos(self):
        (angle, r) = self.vector
        (dx, dy) = (r * math.cos(angle), r * math.sin(angle))
        return self.rect.move(dx, dy)

    def set_pos(self, x, y):
        self.rect.topleft = x, y

    # TODO consider only checking side collisions if not => front collision
    def collide_bar(self, bar_sprites):
        is_in_collision = False
        for bar_sprite in pygame.sprite.spritecollide(self, bar_sprites, dokill=0):
            is_in_collision = True
            if self.left_bar:
                self.vertical_bounce()
                change_x = (self.rect.center[0] - bar_sprite.rect.center[0]) / bar_sprite.rect.size[0]
                self.vector = ((1 + change_x / 4) * self.vector[0], self.speed)
                if self.vector[0] < 7 / 6 * math.pi:
                    self.vector = (7 / 6 * math.pi, self.speed)
                elif self.vector[0] > 11 / 6 * math.pi:
                    self.vector = (11 / 6 * math.pi, self.speed)
            self.left_bar = False
        return is_in_collision

    def collide_tile(self, tile_sprites):
        is_in_collision = False
        for tile in pygame.sprite.spritecollide(self, tile_sprites, dokill=1):
            is_in_collision = True
            if self.left_tile:
                if self.check_side_collision(tile):
                    self.side_bounce()
                # TODO check which variant works better
                # elif self.check_front_collision(tile):
                #     self.vertical_bounce()
                else:
                    self.vertical_bounce()
        return is_in_collision

    def check_side_collision(self, sprite):
        # TODO handle division by zero
        a = math.tan(self.vector[0])
        if 0 <= self.vector[0] < math.pi / 2 or 3 / 2 * math.pi <= self.vector[0] < 2 * math.pi:
            b = self.rect.center[1] - a * self.rect.right
            sprite_left_x = sprite.rect.left
            y_collision = a * sprite_left_x + b
            if sprite.rect.top < y_collision < sprite.rect.bottom:
                return True
        elif math.pi / 2 <= self.vector[0] < 3 / 2 * math.pi:
            b = self.rect.center[1] - a * self.rect.left
            sprite_right_x = sprite.rect.right
            y_collision = a * sprite_right_x + b
            if sprite.rect.top < y_collision < sprite.rect.bottom:
                return True
        return False

    def check_front_collision(self, sprite):
        a = math.tan(self.vector[0])
        if 0 <= self.vector[0] < math.pi:
            b = self.rect.top - a * self.rect.center[0]
            sprite_bottom_y = sprite.rect.bottom
            x_collision = (sprite_bottom_y - b) / a
            if sprite.rect.left <= x_collision <= sprite.rect.right:
                return True
        elif math.pi <= self.vector[0] < 2 * math.pi:
            b = self.rect.bottom - a * self.rect.center[0]
            sprite_top_y = sprite.rect.top
            x_collision = (sprite_top_y - b) / a
            if sprite.rect.left <= x_collision <= sprite.rect.right:
                return True
        return False


class Tile(pygame.sprite.Sprite):
    def __init__(self, lives_left=1):
        pygame.sprite.Sprite.__init__(self)
        tile_name = self.get_tile_name()
        width, height = self.get_size()
        height = size_cfg.get('tiles').get('basic').get('y')
        self.image, self.rect = load_image(tile_name, width=width, height=height)
        self.lives_left = lives_left

    def set_pos(self, x, y):
        self.rect.topleft = x, y

    def get_tile_name(self):
        return img_cfg.get('tiles').get('basic')

    def get_size(self):
        return size_cfg.get('tiles').get('basic').get('x'), size_cfg.get('tiles').get('basic').get('y')

    def kill(self):
        if self.lives_left == 1:
            pygame.sprite.Sprite.kill(self)
        else:
            # TODO change appearance after hit
            self.lives_left -= 1


class TestStrongTile(Tile):
    def __init__(self):
        Tile.__init__(self, lives_left=2)

    def get_tile_name(self):
        return img_cfg.get('tiles').get('basic-strong')


class BackgroundObject(pygame.sprite.Sprite):
    # lvl value indicates how far from the foreground the object is
    def __init__(self, bg_obj_name, width, height, lvl=1, moving=True, colorkey=None):
        pygame.sprite.Sprite.__init__(self)
        width = int(width * (0.9 ** lvl))
        height = int(height * (0.9 ** lvl))
        self.image, self.rect = load_image(bg_obj_name, width=width, height=height, colorkey=colorkey)
        self.image = darken_image(self.image, lvl, colorkey)
        self.moving = moving
        self.speed = 2
        angle = np.random.rand() * 2 * math.pi
        self.vector = (angle, self.speed)

    def update(self):
        if self.moving:
            self.rect = self.get_updated_pos()
            self.vector = (self.vector[0] + math.pi / 24, self.speed)
            if self.vector[0] > 2 * math.pi:
                self.vector = (self.vector[0] - 2 * math.pi, self.speed)

    def get_updated_pos(self):
        (angle, r) = self.vector
        (dx, dy) = (r * math.cos(angle), r * math.sin(angle))
        return self.rect.move(dx, dy)

    def set_pos(self, x, y):
        self.rect.topleft = x, y


class Sparkle(BackgroundObject):
    def __init__(self, lvl=2):
        sparkle_name = img_cfg.get('background').get('sparkle-basic')
        width = size_cfg.get('background').get('sparkle-basic').get('x')
        height = size_cfg.get('background').get('sparkle-basic').get('y')
        BackgroundObject.__init__(self, sparkle_name, width, height, lvl, colorkey=-1)


class LifeIcon(BackgroundObject):
    def __init__(self, lvl=1):
        life_icon_name = img_cfg.get('background').get('life-icon')
        width = size_cfg.get('background').get('life-icon').get('x')
        height = size_cfg.get('background').get('life-icon').get('y')
        BackgroundObject.__init__(self, life_icon_name, width, height, lvl, moving=False, colorkey=-1)
