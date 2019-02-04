import pygame
from pygame.locals import *
from game.config import size_cfg
from game.scenes import TestScene


def main():
    pygame.init()
    res_x = size_cfg.get('resolution').get('x')
    res_y = size_cfg.get('resolution').get('y')
    screen = pygame.display.set_mode((res_x, res_y))
    sparkle_scene = TestScene(screen)
    pygame.display.flip()

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
                    sparkle_scene.bar.move_left()
                elif event.key == K_RIGHT:
                    sparkle_scene.bar.move_right()
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    sparkle_scene.bar.move_pos = [0, 0]
                    sparkle_scene.bar.state = "still"

        pygame.event.pump()

        sparkle_scene.update_scene()

        sparkle_scene.draw_scene()


if __name__ == '__main__': main()
