import pygame
from game.objects import *


class Menu:
    pass


class Scene:
    def __init__(self, screen, bar, ball, tiles=None, background_objects=None, background=None):
        self.screen = screen
        if background is None:
            self.background = pygame.Surface(self.screen.get_size())
            self.background = self.background.convert()
            self.background.fill((0, 0, 0))
        else:
            self.background = background
        self.bar = bar
        self.ball = ball
        # 2D array: column says about x coordinate, row about y
        # TODO: or verify if coords are given as a parameter
        self.tiles = tiles
        # 3D array: same as tiles but 1st coord. is the level: shifts an object farther
        self.background_objects = background_objects

        # grouping objects TODO: check if needed here
        self.bar_sprites = pygame.sprite.RenderUpdates(self.bar)
        self.ball_sprites = pygame.sprite.RenderUpdates(self.ball)
        self.tile_sprites = pygame.sprite.RenderUpdates(self.tiles)
        if self.background_objects is not None:
            self.background_object_sprites = pygame.sprite.RenderUpdates(self.background_objects)

        self.screen.blit(self.background, (0, 0))
        if self.background_objects is not None:
            self.background_object_sprites.draw(screen)
        self.bar_sprites.draw(self.screen)
        self.ball_sprites.draw(self.screen)
        self.tile_sprites.draw(self.screen)

    def update_scene(self):
        if not self.ball.collide_bar(self.bar_sprites):
            self.ball.left_bar = True
        if not self.ball.collide_tile(self.tile_sprites):
            self.ball.left_tile = True
        self.bar_sprites.update()
        self.ball_sprites.update()
        self.tile_sprites.update()
        if self.background_objects is not None:
            self.background_object_sprites.update()

    def draw_scene(self):
        self.screen.blit(self.background, (0, 0))
        self.bar_sprites.draw(self.screen)
        self.ball_sprites.draw(self.screen)
        self.tile_sprites.draw(self.screen)
        if self.background_objects is not None:
            self.background_object_sprites.draw(self.screen)
        pygame.display.flip()


class TestScene(Scene):
    def __init__(self, screen):
        screen_x, screen_y = screen.get_size()
        bar = Bar()
        bar.rect.midbottom = screen.get_rect().midbottom
        bar.rect = bar.rect.move(0, -5)
        ball = Ball()
        ball.rect.midbottom = bar.rect.midbottom
        ball.rect = ball.rect.move(0, -5)
        tiles = []
        for i in range(34):
            if i % 17 != 0 and (i - 16) % 17 != 0:
                tmp_tile = Tile()
                tile_x = (screen_x / 17) * (i % 17)
                row = (i - (i % 17)) / 17
                initial_shift = 30
                tile_y = initial_shift + (row * 60)
                tmp_tile.rect = tmp_tile.rect.move(tile_x, tile_y)
                tiles.append(tmp_tile)
        # TODO add sparkles
        Scene.__init__(self, screen, bar, ball, tiles)
