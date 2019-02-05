
class Judge:

    def __init__(self, scene):
        self.scene = scene
        self.lives = self.scene.lives

    def init_menu(self):
        pass

    def start_game(self):
        pass

    def restart_game(self):
        pass

    def recover_ball(self):
        self.scene.set_ball_on_bar()

    def start_ball(self):
        self.scene.set_ball_off_bar()

    def check_point_lost(self):
        if self.scene.ball.rect.center[1] > self.scene.screen.get_rect().bottom:
            self.lives -= 1
            self.scene.life_icon_sprites.sprites()[0].kill()
            return True
        return False

    def check_game_lost(self):
        return self.lives == 0

    def check_game_won(self):
        if len(self.scene.tile_sprites.sprites()) <= 0:
            print("Game won!")
            return True
        return False
