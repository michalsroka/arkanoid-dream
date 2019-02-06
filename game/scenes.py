from game.objects import *
from game.game_utils import read_tiles_csv
from game.config import tile_cfg


class Menu:
    # TODO menu should have buttons which one choses with arrow keys. They have an effect of being pushed when chosen.
    # TODO after choosing start one can choose a level/scene which has different graphics and tile layouts
    pass


class Scene:
    def __init__(self, screen, bar, ball, life_icons, lives, tiles, background_objects=None, background=None):
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

        self.life_icons = life_icons

        # grouping objects TODO: check if needed here
        self.bar_sprites = pygame.sprite.RenderUpdates(self.bar)
        self.ball_sprites = pygame.sprite.RenderUpdates(self.ball)
        self.tile_sprites = pygame.sprite.RenderUpdates(self.tiles)
        self.life_icon_sprites = pygame.sprite.RenderUpdates(self.life_icons)
        self.background_object_sprites_2d = list()
        # if background_objects are not None the array should be 2D (each row is a new lvl)
        if self.background_objects is not None:
            for lvl_objects in self.background_objects:
                self.background_object_sprites_2d.append(pygame.sprite.RenderUpdates(lvl_objects))
        self.background_object_sprites_2d.reverse()
        self.screen.blit(self.background, (0, 0))
        if self.background_objects is not None:
            for lvl_sprites in self.background_object_sprites_2d:
                lvl_sprites.draw(screen)
        self.bar_sprites.draw(self.screen)
        self.ball_sprites.draw(self.screen)
        self.tile_sprites.draw(self.screen)
        self.life_icon_sprites.draw(self.screen)
        self.ball_on_bar = True
        self.lives = lives

    def update_scene(self):
        if not self.ball.collide_bar(self.bar_sprites):
            self.ball.left_bar = True
        if not self.ball.collide_tile(self.tile_sprites):
            self.ball.left_tile = True
        if self.background_objects is not None:
            for lvl_sprites in self.background_object_sprites_2d:
                lvl_sprites.update()
        self.life_icon_sprites.update()
        self.bar_sprites.update()
        self.ball_sprites.update(self.bar.rect.midtop[0], self.bar.rect.midtop[1])
        self.tile_sprites.update()

    def draw_scene(self):
        self.screen.blit(self.background, (0, 0))
        if self.background_objects is not None:
            for lvl_sprites in self.background_object_sprites_2d:
                lvl_sprites.draw(self.screen)
        self.bar_sprites.draw(self.screen)
        self.ball_sprites.draw(self.screen)
        self.tile_sprites.draw(self.screen)
        self.life_icon_sprites.draw(self.screen)
        pygame.display.flip()

    def set_ball_on_bar(self):
        self.ball.on_bar = True
        self.ball.left_bar = False

    def set_ball_off_bar(self):
        self.ball.on_bar = False
        self.ball.vector = (3 / 2 * math.pi, self.ball.speed)

    def get_tiles_from_layout2(self, file_name, screen, row_gap=30, tile_shift=40):
        layout_arr = read_tiles_csv(file_name)
        screen_x = screen.get_rect().right - 2 * tile_shift
        tiles = list()
        for y, row in enumerate(layout_arr):
            y_coord = row_gap + y * row_gap
            for x, val in enumerate(row):
                x_coord = tile_shift + (screen_x / len(row)) * x
                tmp_tile = self.pick_tile(val)
                if tmp_tile is not None:
                    tmp_tile.rect = tmp_tile.rect.move(x_coord, y_coord)
                    tiles.append(tmp_tile)
        return tiles

    def get_tiles_from_layout(self, file_name, screen):
        layout_arr = read_tiles_csv(file_name)
        screen_center_x = screen.get_rect().centerx
        tiles = list()
        num_of_columns = len(layout_arr[0])
        tile_x_size, tile_y_size = self.pick_tile(1).rect.size
        tiles_len_x = num_of_columns * tile_x_size
        left_x = screen_center_x - (tiles_len_x / 2)
        assert left_x > 0, "Too many columns of tiles. Change layout."
        for y, row in enumerate(layout_arr):
            y_coord = 2 * tile_y_size + y * tile_y_size
            for x, val in enumerate(row):
                x_coord = left_x + (tile_x_size * x)
                tmp_tile = self.pick_tile(val)
                if tmp_tile is not None:
                    tmp_tile.rect = tmp_tile.rect.move(x_coord, y_coord)
                    tiles.append(tmp_tile)
        return tiles

    def pick_tile(self, num):
        if num == 0:
            return None
        elif num == 1:
            return Tile()
        elif num == 2:
            return TestStrongTile()


class TestScene(Scene):
    def __init__(self, screen, lives=3):
        screen_x, screen_y = screen.get_size()
        bar = Bar()
        bar.rect.midbottom = screen.get_rect().midbottom
        bar.rect = bar.rect.move(0, -5)
        ball = Ball()
        ball.rect.midbottom = bar.rect.midbottom
        ball.rect = ball.rect.move(0, -5)
        tiles = list()
        for i in range(34):
            if i % 17 != 0 and (i - 16) % 17 != 0:
                tmp_tile = Tile()
                tile_x = (screen_x / 17) * (i % 17)
                row = (i - (i % 17)) / 17
                initial_shift = 30
                tile_y = initial_shift + (row * 60)
                tmp_tile.rect = tmp_tile.rect.move(tile_x, tile_y)
                tiles.append(tmp_tile)
        life_icons = list()
        for i in range(lives):
            tmp_life_icon = LifeIcon()
            life_icon_y = 30
            life_icon_x = screen_x - 30 - (i * tmp_life_icon.rect.size[0])
            tmp_life_icon.rect = tmp_life_icon.rect.move(life_icon_x, life_icon_y)
            life_icons.append(tmp_life_icon)
        Scene.__init__(self, screen, bar, ball, life_icons, lives, tiles)


class TestSceneLayout(Scene):
    def __init__(self, screen, lives=3):
        screen_x, screen_y = screen.get_size()
        bar = Bar()
        bar.rect.midbottom = screen.get_rect().midbottom
        bar.rect = bar.rect.move(0, -5)
        ball = Ball()
        ball.rect.midbottom = bar.rect.midbottom
        ball.rect = ball.rect.move(0, -5)
        tiles_layout_file = tile_cfg.get('tiles-layout').get('test')
        tiles = Scene.get_tiles_from_layout(self, tiles_layout_file, screen)
        life_icons = list()
        for i in range(lives):
            tmp_life_icon = LifeIcon()
            life_icon_y = 30
            life_icon_x = screen_x - 30 - (i * tmp_life_icon.rect.size[0])
            tmp_life_icon.rect = tmp_life_icon.rect.move(life_icon_x, life_icon_y)
            life_icons.append(tmp_life_icon)
        sparkles = list()
        for lvl in range(4, 8):
            lvl_sparkles = list()
            for i in range(lvl * 2):
                x_coord = np.random.rand() * screen.get_rect().right
                y_coord = np.random.rand() * screen.get_rect().bottom
                sparkle = Sparkle(lvl=lvl)
                sparkle.rect = sparkle.rect.move(x_coord, y_coord)
                lvl_sparkles.append(sparkle)
            sparkles.append(lvl_sparkles)
        Scene.__init__(self, screen, bar, ball, life_icons, lives, tiles, background_objects=sparkles)


class EarthScene(Scene):
    def __init__(self, screen, lives=3):
        background_img_name = img_cfg.get('background').get('earth-background-image')
        screen_x, screen_y = screen.get_size()
        background_surface, background_rect = load_image(background_img_name, width=screen_x, height=screen_y)
        bar = EarthBar()
        bar.rect.midbottom = screen.get_rect().midbottom
        bar.rect = bar.rect.move(0, -5)
        ball = EarthBall()
        ball.rect.midbottom = bar.rect.midbottom
        ball.rect = ball.rect.move(0, -5)
        tiles_layout_file = tile_cfg.get('tiles-layout').get('earth')
        tiles = Scene.get_tiles_from_layout(self, tiles_layout_file, screen)
        life_icons = list()
        for i in range(lives):
            tmp_life_icon = LifeIcon2()
            life_icon_y = 30
            life_icon_x = screen_x - 30 - (i * tmp_life_icon.rect.size[0])
            tmp_life_icon.rect = tmp_life_icon.rect.move(life_icon_x, life_icon_y)
            life_icons.append(tmp_life_icon)
        sparkles = list()
        for lvl in range(4, 8):
            lvl_sparkles = list()
            for i in range(lvl * 2):
                x_coord = np.random.rand() * screen.get_rect().right
                y_coord = np.random.rand() * screen.get_rect().bottom
                sparkle = EarthBackground(lvl=lvl)
                sparkle.rect = sparkle.rect.move(x_coord, y_coord)
                lvl_sparkles.append(sparkle)
            sparkles.append(lvl_sparkles)
        Scene.__init__(self, screen, bar, ball, life_icons, lives, tiles,
                       background_objects=sparkles, background=background_surface)

    def pick_tile(self, num):
        if num == 0:
            return None
        elif num == 1:
            return EarthTile1()
        elif num == 2:
            return EarthTile2()


class MetalScene(Scene):
    def __init__(self, screen, lives=3):
        background_img_name = img_cfg.get('background').get('metal-background-image')
        screen_x, screen_y = screen.get_size()
        background_surface, background_rect = load_image(background_img_name, width=screen_x, height=screen_y)
        bar = MetalBar()
        bar.rect.midbottom = screen.get_rect().midbottom
        bar.rect = bar.rect.move(0, -5)
        ball = MetalBall()
        ball.rect.midbottom = bar.rect.midbottom
        ball.rect = ball.rect.move(0, -5)
        tiles_layout_file = tile_cfg.get('tiles-layout').get('metal')
        tiles = Scene.get_tiles_from_layout(self, tiles_layout_file, screen)
        life_icons = list()
        for i in range(lives):
            tmp_life_icon = LifeIcon2()
            life_icon_y = 30
            life_icon_x = screen_x - 30 - (i * tmp_life_icon.rect.size[0])
            tmp_life_icon.rect = tmp_life_icon.rect.move(life_icon_x, life_icon_y)
            life_icons.append(tmp_life_icon)
        sparkles = list()
        for lvl in range(4, 8):
            lvl_sparkles = list()
            for i in range(lvl * 2):
                x_coord = np.random.rand() * screen.get_rect().right
                y_coord = np.random.rand() * screen.get_rect().bottom
                sparkle = MetalBackground(lvl=lvl)
                sparkle.rect = sparkle.rect.move(x_coord, y_coord)
                lvl_sparkles.append(sparkle)
            sparkles.append(lvl_sparkles)
        Scene.__init__(self, screen, bar, ball, life_icons, lives, tiles,
                       background_objects=sparkles, background=background_surface)

    def pick_tile(self, num):
        if num == 0:
            return None
        elif num == 1:
            return MetalTile1()
        elif num == 2:
            return MetalTile2()
        elif num == 3:
            return MetalTile3()
