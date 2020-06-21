import pygame
from pygame.image import tostring
from pygame.transform import rotate, smoothscale
import timeit
import sys

SCREENRECT = pygame.Rect(0, 0, 800, 1024)
pygame.display.init()
SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWACCEL, 32)
im = pygame.image.load("Assets\\A2.png").convert(32)
im = pygame.transform.smoothscale(im, (800, 1024))

print(timeit.timeit("im.get_view('3')", "from __main__ import im", number=100000))
print(timeit.timeit("im.get_view('2')", "from __main__ import im", number=100000))
print(timeit.timeit("tostring(SCREEN, 'RGB', False)", "from __main__ import im, SCREEN, tostring", number=1000))
pygame.quit()

TRANSFORM_BUFFER = [None for r in range(360)]

TB = {}


# BUFFERING ON THE FLY
def rot_center_b(image_, angle_, rect_centre_x, rect_centre_y):

    zero_to_360 = angle_ % 360
    new_image = TRANSFORM_BUFFER[zero_to_360]
    if new_image is None:
        new_image = rotate(image_, angle_)
        TRANSFORM_BUFFER[zero_to_360] = new_image
    return new_image, new_image.get_rect(center=(rect_centre_x, rect_centre_y))


# UNBUFFERED
def rot_center(image_, angle_, rect_centre_x, rect_centre_y):
    new_image = rotate(image_, angle_)
    return new_image, new_image.get_rect(center=(rect_centre_x, rect_centre_y))


SCREENRECT = pygame.Rect(0, 0, 800, 1024)
pygame.display.init()
SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWACCEL, 32)

STINGER_IMAGE = pygame.image.load('Assets\\MISSILE1_.png').convert_alpha()
w, h = STINGER_IMAGE.get_size()
STINGER_IMAGE = smoothscale(STINGER_IMAGE, (w * 5, h * 5))
for r in range(360):
    TRANSFORM_BUFFER[r] = rotate(STINGER_IMAGE, r)
    image = rotate(STINGER_IMAGE, r)
    TB[r] = [image.copy(), image.get_rect()]

# FULL BUFFERED
def rot_center_bb(angle_, rect_centre_x, rect_centre_y):
    new_image, rect = TB[angle_]
    rect.center = (rect_centre_x, rect_centre_y)
    return new_image, rect

#
# print(sys.getsizeof(TB))
# import random
# image = STINGER_IMAGE
# print(timeit.timeit("rot_center_b(image, random.randint(0, 360), 10, 10)",
#                     "from __main__ import rot_center_b, image, random", number=100000))
#
# print(timeit.timeit("rot_center(image, random.randint(0, 360), 10, 10)",
#                     "from __main__ import rot_center, image, random", number=100000))
#
# print(timeit.timeit("rot_center_bb(random.randint(0, 359), 10, 10)",
#                     "from __main__ import rot_center_bb, random", number=100000))


R = pygame.Rect(0, 0, 100, 100)
R.center = 250, 250

print(timeit.timeit("SCREENRECT.contains(R)", "from __main__ import SCREENRECT, R", number=100000000))
print(timeit.timeit("SCREENRECT.colliderect(R)", "from __main__ import SCREENRECT, R", number=100000000))

