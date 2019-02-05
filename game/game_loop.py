import pygame
from pygame.locals import *
from game.config import size_cfg
from game.scenes import TestScene, TestSceneLayout
from game.judge import Judge


def main():
    pygame.init()
    res_x = size_cfg.get('resolution').get('x')
    res_y = size_cfg.get('resolution').get('y')
    screen = pygame.display.set_mode((res_x, res_y))
    scene = TestSceneLayout(screen)
    pygame.display.flip()

    judge = Judge(scene)

    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    scene.bar.move_left()
                elif event.key == K_RIGHT:
                    scene.bar.move_right()
                elif event.key == K_SPACE:
                    if judge.scene.ball_on_bar:
                        judge.start_ball()
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    scene.bar.move_pos = [0, 0]
                    scene.bar.state = "still"

        pygame.event.pump()

        if judge.check_point_lost():
            judge.recover_ball()
        if judge.check_game_lost():
            # TODO to implement
            return
        if judge.check_game_won():
            return

        scene.update_scene()
        scene.draw_scene()


if __name__ == '__main__':
    main()
