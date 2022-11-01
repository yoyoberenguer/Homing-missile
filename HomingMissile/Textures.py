# encoding: utf-8


"""
                 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Copyright Yoann Berenguer
"""

import pygame
from PygameShader import blur, saturation
from pygame.transform import rotozoom, smoothscale


from SpriteSheet import sprite_sheet_per_pixel, sprite_sheet_fs8
from Var import CONSTANTS

GL = CONSTANTS()

MISSILE_TRAIL = []
try:
    MISSILE_TRAIL = sprite_sheet_fs8('Assets\\Smoke_trail_2_64x64.png', 64, 6, 6)
    # MISSILE_TRAIL = sprite_sheet_fs8('Assets\\Smoke_trail_2_64x64_alpha.png', 64, 6, 6)
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile Smoke_trail_2_64x64.png is missing from Assets directory")


MISSILE_TRAIL_DICT = {}
w, h = MISSILE_TRAIL[0].get_size()
i = 0
b = -1.0
for image in MISSILE_TRAIL:
    f = i / 20.0

    saturation(image, b)
    if b < 1.0 - 0.038:
        b += +0.038
    else:
        b = 1.0
    blur(image, t_=i+1)

    image = pygame.transform.smoothscale(image, (int(w * (1 + f)), int(h * (1 + f)))).convert()
    MISSILE_TRAIL_DICT[i] = [image, image.get_rect()]
    i += 1

MISSILE_TRAIL1 = []
try:
    MISSILE_TRAIL1 = sprite_sheet_per_pixel('Assets\\Smoke_trail_2_64x64_alpha.png', 64, 6, 6)
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile Smoke_trail_2_64x64_alpha.png is missing from Assets directory")

MISSILE_TRAIL_DICT1 = {}
w, h = MISSILE_TRAIL1[0].get_size()
i = 0
for image in MISSILE_TRAIL1:
    f = i / 20.0
    image = pygame.transform.smoothscale(image, (int(w * (1 + f)), int(h * (1 + f))))
    MISSILE_TRAIL_DICT1[i] = [image, image.get_rect()]
    i += 1

MISSILE_TRAIL2 = []
try:
    MISSILE_TRAIL2 = sprite_sheet_fs8('Assets\\Smoke_trail_3_256x256_.png', 256, 7, 6)
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile Explosion12_256x256_.png is missing from Assets directory")

# REMOVING THE FIRST 5 SPRITES
MISSILE_TRAIL2 = MISSILE_TRAIL2[4:]
w, h = MISSILE_TRAIL2[4].get_size()
w /= 3
h /= 3
MISSILE_TRAIL_DICT2 = {}
i = 0
b = 1.0
for image in MISSILE_TRAIL2:
    f = i / 20.0
    saturation(image, b)
    if b > -0.035:
        b += -0.035
    else:
        b = -1.0

    blur(image, t_=i+1)

    image = pygame.transform.smoothscale(MISSILE_TRAIL2[i], (int(w * (1 + f)), int(h * (1 + f)))).convert()
    MISSILE_TRAIL_DICT2[i] = [image, image.get_rect()]
    i += 1

MISSILE_TRAIL3 = []
try:
    MISSILE_TRAIL3 = sprite_sheet_fs8('Assets\\Smoke_trail_4_128x128_.png', 128, 8, 6)
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile Smoke_trail_4_128x128_.png is missing from Assets directory")

w, h = MISSILE_TRAIL3[0].get_size()
w /= 2
h /= 2
MISSILE_TRAIL_DICT3 = {}
i = 0
b = 1.0
for image in MISSILE_TRAIL3:
    f = i / 20.0
    saturation(image, b)
    if b > -0.035:
        b += -0.035
    else:
        b = -1.0

    blur(image, t_=i + 1)

    image = \
        pygame.transform.smoothscale(image, (int(w * (1 + f)), int(h * (1 + f)))).convert()
    MISSILE_TRAIL_DICT3[i] = [image, image.get_rect()]
    i += 1


SPACE_FIGHTER_SPRITE = None
try:
    SPACE_FIGHTER_SPRITE  = pygame.image.load('Assets\\illumDefault11.png').convert_alpha()
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile illumDefault11.png is missing from Assets directory")

SPACE_FIGHTER_SPRITE  = smoothscale(SPACE_FIGHTER_SPRITE, (80, 55))

STINGER_IMAGE = None
try:
    # MISSILE IMAGE
    STINGER_IMAGE         = pygame.image.load('Assets\\MISSILE1_.png').convert_alpha()
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile MISSILE1_.png is missing from Assets directory")

BUMBLEBEE_IMAGE = None
try:
    BUMBLEBEE_IMAGE       = pygame.image.load('Assets\\MISSILE2_.png')
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile MISSILE2_.png is missing from Assets directory")
BUMBLEBEE_IMAGE.set_colorkey((0, 0, 0), pygame.RLEACCEL)

WASP_IMAGE = None
try:
    WASP_IMAGE            = pygame.image.load('Assets\\MISSILE3.png').convert_alpha()
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile MISSILE3.png is missing from Assets directory")

HORNET_IMAGE = None
try:
    HORNET_IMAGE          = pygame.image.load('Assets\\MISSILE4.png').convert_alpha()
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile MISSILE4.png is missing from Assets directory")

# MISSILE PRE-CALCULATED ROTATION
STINGER_ROTATE_BUFFER = {}

for a in range(360):
    image = rotozoom(STINGER_IMAGE, a, 0.9)
    rect  = image.get_rect()
    STINGER_ROTATE_BUFFER[a] = [image, rect]

BUMBLEBEE_ROTATE_BUFFER = {}
for a in range(360):
    image = rotozoom(BUMBLEBEE_IMAGE, a, 0.8)
    rect  = image.get_rect()
    BUMBLEBEE_ROTATE_BUFFER[a] = [image, rect]

WASP_ROTATE_BUFFER = {}
for a in range(360):
    image = rotozoom(WASP_IMAGE, a, 0.9)
    rect = image.get_rect()
    WASP_ROTATE_BUFFER[a] = [image, rect]

HORNET_ROTATE_BUFFER = {}
for a in range(360):
    image = rotozoom(HORNET_IMAGE, a, 0.9)
    rect = image.get_rect()
    HORNET_ROTATE_BUFFER[a] = [image, rect]

try:
    PLAYER_AIRCRAFT = pygame.image.load('Assets\\SpaceShip.png').convert_alpha()
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile SpaceShip.png is missing from Assets directory")

BACKGROUND = None
try:
    BACKGROUND = pygame.image.load('Assets\\bck1.jpg').convert()
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nFile A2.png is missing from Assets directory")

BACKGROUND = pygame.transform.smoothscale(BACKGROUND, GL.SCREENRECT.size)
BACKGROUND.set_alpha(None)
