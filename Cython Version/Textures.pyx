import pygame
from pygame.transform import rotozoom, smoothscale

from pygame import freetype


try:
    cimport cython
    from cpython.dict cimport PyDict_DelItem, PyDict_Clear, PyDict_GetItem, PyDict_SetItem, \
        PyDict_Values, PyDict_Keys, PyDict_Items, PyDict_SetItemString
    from cpython cimport PyObject, PyObject_HasAttr, PyObject_IsInstance
    from cpython.list cimport PyList_Append, PyList_GetItem, PyList_Size
except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")

from SpriteSheet import sprite_sheet_per_pixel, sprite_sheet_fs8

SCREENRECT = pygame.Rect(0, 0, 800, 1024)


# cdef list MISSILE_TRAIL = sprite_sheet_per_pixel('Assets\\Smoke_trail_2_64x64_alpha.png', 64, 6, 6)
cdef:
    list MISSILE_TRAIL = sprite_sheet_fs8('Assets\\Smoke_trail_2_64x64.png', 64, 6, 6)
    int i = 0
    int w, h
    float f =0

MISSILE_TRAIL_DICT = {}
w, h = MISSILE_TRAIL[0].get_size()
for image in MISSILE_TRAIL:

    f = i / 20.0
    image = MISSILE_TRAIL[i]
    image = \
        pygame.transform.smoothscale(
            image, (int(w * (1 + f)),
                               int(h * (1 + f)))).convert(32, pygame.RLEACCEL)
    # PyDict_SetItem(MISSILE_TRAIL_DICT, i, [MISSILE_TRAIL[i], MISSILE_TRAIL[i].get_rect()])
    MISSILE_TRAIL_DICT[i] = [image, image.get_rect()]
    i += 1

cdef list MISSILE_TRAIL1 = sprite_sheet_per_pixel('Assets\\Smoke_trail_2_64x64_alpha.png', 64, 6, 6)
MISSILE_TRAIL_DICT1 = {}
w, h = MISSILE_TRAIL1[0].get_size()
i = 0
for image in MISSILE_TRAIL1:
    f = i / 20.0
    image = MISSILE_TRAIL1[i]
    image = \
        pygame.transform.smoothscale(
             image, (int(w * (1 + f)),
                                 int(h * (1 + f))))
    MISSILE_TRAIL_DICT1[i] = [image, image.get_rect()]
    i += 1


cdef list MISSILE_TRAIL2 = sprite_sheet_fs8('Assets\\Explosion12_256x256_.png', 256, 7, 6)
w, h = image.get_size()
w /= 4
h /= 4
MISSILE_TRAIL_DICT2 = {}
i = 0
for image in MISSILE_TRAIL2:
    # USE 20.0 IF IMAGES ARE BLEND WITH BLEND_RGB_MAX MODE
    # OTHERWISE USE 50.0 FOR BLEND_RGB_ADD
    f = i / 20.0
    image = MISSILE_TRAIL2[i]
    image = \
        pygame.transform.smoothscale(
            MISSILE_TRAIL2[i], (int(w * (1 + f)),
                                int(h * (1 + f)))).convert(32, pygame.RLEACCEL)
    MISSILE_TRAIL_DICT2[i] = [image, image.get_rect()]
    i += 1


cdef list MISSILE_TRAIL3 = sprite_sheet_fs8('Assets\\LaserExplosion128x128_.png', 128, 8, 6)
w, h = MISSILE_TRAIL3[0].get_size()
w /= 2
h /= 2
MISSILE_TRAIL_DICT3 = {}
i = 0
for image in MISSILE_TRAIL3:

    # USE 20.0 IF IMAGES ARE BLEND WITH BLEND_RGB_MAX MODE
    # OTHERWISE USE 50.0 FOR BLEND_RGB_ADD
    f = i / 20.0
    image = MISSILE_TRAIL3[i]
    image = \
        pygame.transform.smoothscale(
            image, (int(w * (1 + f)),
                    int(h * (1 + f)))).convert(32, pygame.RLEACCEL)
    MISSILE_TRAIL_DICT3[i] = [image, image.get_rect()]
    i += 1

SPACE_FIGHTER_SPRITE  = pygame.image.load('Assets\\illumDefault11.png').convert_alpha()
SPACE_FIGHTER_SPRITE  = smoothscale(SPACE_FIGHTER_SPRITE, (80, 55))

# MISSILE IMAGE
STINGER_IMAGE         = pygame.image.load('Assets\\MISSILE1_.png').convert_alpha()
BUMBLEBEE_IMAGE       = pygame.image.load('Assets\\MISSILE2_.png')
BUMBLEBEE_IMAGE.set_colorkey((0, 0, 0), pygame.RLEACCEL)
WASP_IMAGE            = pygame.image.load('Assets\\MISSILE3.png').convert_alpha()
HORNET_IMAGE          = pygame.image.load('Assets\\MISSILE4.png').convert_alpha()

# MISSILE PRE-CALCULATED ROTATION
STINGER_ROTATE_BUFFER = {}
cdef int a
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

# -----------------------RECORD_FRAMES RECORDER
LEVEL_ICON = pygame.image.load('Assets\\switchGreen04.png').convert_alpha()
LEVEL_ICON = pygame.transform.rotozoom(LEVEL_ICON, 90, 0.7)

VIDEO_ICON = pygame.image.load('Assets\\video1_.png').convert(32)
VIDEO_ICON.set_colorkey((0, 0, 0, 0), pygame.RLEACCEL)
VIDEO_ICON = pygame.transform.smoothscale(VIDEO_ICON, (64, 64))

FONT = freetype.Font('Assets\\ARCADE_R.ttf', size=15)
RECT1 = FONT.get_rect("Video capture, please wait...ESC to stop", style=freetype.STYLE_NORMAL, size=15)
RECT1.center = (SCREENRECT.centerx - RECT1.w // 2, SCREENRECT.centery - RECT1.h // 2)
# ----------------------- RECORD_FRAMES RECORDER


COBRA = pygame.image.load('Assets\\SpaceShip.png').convert_alpha()