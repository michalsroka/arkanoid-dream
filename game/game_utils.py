import os
import pygame
from pygame.locals import *
import numpy as np
import pandas as pd

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


def load_image(name, width=-1, height=-1, colorkey=None):
    fullname = os.path.join('game_files/images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', name)
        raise SystemExit
    image = image.convert()
    if width != -1 and height != -1:
        image = resize_image(image, width, height)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('game_files/sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound')
        raise SystemExit
    return sound


def darken_image(surface, lvl, colorkey):
    if lvl < 0:
        lvl = 0
    elif lvl > 10:
        lvl = 10
    arr = pygame.surfarray.pixels3d(surface)
    src = np.array(arr)
    dest = np.zeros(arr.shape)
    # TODO check other values
    dest[:] = 20, 50, 100
    diff = (dest - src) * 0.10 * lvl
    darkened = src + diff.astype(np.uint)
    pygame.surfarray.blit_array(surface, darkened)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = surface.get_at((0, 0))
        surface.set_colorkey(colorkey, RLEACCEL)
    return surface


def resize_image(surface, width, height):
    return pygame.transform.scale(surface, (width, height))


def read_tiles_csv(file_name):
    fullname = os.path.join('game_files/tiles_layout', file_name)
    return pd.read_csv(fullname).values
