"""

                   GNU GENERAL PUBLIC LICENSE

                       Version 3, 29 June 2007


 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>

 Everyone is permitted to copy and distribute verbatim copies

 of this license document, but changing it is not allowed.
 """
import math
from math import degrees, atan2, cos, sin, radians, pi
import pygame
from random import uniform, randint
from SpriteSheet import spread_sheet_fs8, spread_sheet_per_pixel

from Surface import reshape, make_surface, make_array
import numpy

DEG_TO_RAD = pi / 180
RAD_TO_DEG = 1 / DEG_TO_RAD

MISSILE_TRAIL = spread_sheet_per_pixel('Smoke_trail_2_64x64_alpha.png', 64, 6, 6)
last_image = MISSILE_TRAIL[len(MISSILE_TRAIL) - 1]
w, h = last_image.get_size()
MISSILE_TRAIL = pygame.transform.smoothscale(last_image, (int(w * 1.2), int(h * 1.2)))
del last_image, w, h
MISSILE_TRAIL1 = spread_sheet_fs8('Smoke_trail_2_64x64.png', 64, 6, 6)


func = numpy.linspace(0.8, 1.2, len(MISSILE_TRAIL1))
i = 0


for surface in MISSILE_TRAIL1:

    MISSILE_TRAIL1[i] = pygame.transform.smoothscale(surface,
                                           (int(surface.get_width() * func[i]),
                                            int(surface.get_height() * func[i])))
    i += 1


# pygame sprite group for missile's particles
# This Array contains all particles coming out of the
# missile exhaust, all particles will be blended to create a flame effect
# and smoke.
VERTEX_ARRAY_MP = pygame.sprite.Group()


def transparency(image_, visibility_):
        array_ = pygame.surfarray.pixels3d(image_)
        alpha_ = pygame.surfarray.pixels_alpha(image_)
        alpha_ = alpha_.astype(numpy.int16)
        alpha_ -= visibility_
        numpy.putmask(alpha_, alpha_ < 0, 0)
        return make_surface(make_array(array_, alpha_.astype(numpy.uint8))).convert_alpha()


def get_angle(
                object1 : pygame.math.Vector2,  # Target center coordinates (x, y)
                object2 : pygame.Rect           # represent the local object (reference object)
             ):
    # calculate the angle (returns angle in radians) between a parent object
    # and a target object (center to center)
    dx = object2.centerx - object1.x
    dy = object2.centery - object1.y

    return -atan2(dy, dx)


def projection(
                point_ : pygame.math.Vector2,             # Point gravitating around the object center
                rect_:   pygame.math.Vector2,             # Vector2 representing the center of the object
                target_:pygame.Rect                       # pygame.Rect representing the target's center
              ):
    # calculate a new position of a gravitating point after a given rotate_inplace.
    # rect_ is the center of the parent object.
    # point_ is a tuple representing the coordinates (x, y) of a point distant from the center rect_

    p_angle = -atan2(point_.y, point_.x)
    length = point_.length()
    rotation = radians(((p_angle * RAD_TO_DEG) % 360 + (get_angle(rect_, target_) * RAD_TO_DEG) % 360 - 90) % 360)
    p_ = pygame.math.Vector2(rect_.x + cos(rotation) * length,
                             rect_.y + sin(rotation) * length)

    # Return the point coordinates to match its position on the screen
    # eg. x = rect_.centerx + cos(theta)* length and y = rect_.centerx + sin(theta) * length
    return p_


def convert_pi_0_2pi(self, rad):
    return (rad + 2 * math.pi) % (2 * math.pi)


def projection_1(
                  point_ : pygame.math.Vector2,             # Point gravitating around the parent object center
                  rect_  : pygame.math.Vector2,             # Vector2 representing the parent object center
                  angle_ : int                              # Already calculated angle of the parent object (in degrees)
                ):

    # calculate a new position of a gravitating point after a given rotate_inplace.
    # rect_ is the center of the parent object.
    # point_ is a tuple representing the coordinates (x, y) of a point distant from the center rect_
    # angle represent the rotate_inplace.
    p_angle = -atan2(point_.y, point_.x)
    length = point_.length()
    rotation = radians(((p_angle * RAD_TO_DEG) % 360 + angle_ - 90) % 360)
    p_ = pygame.math.Vector2(rect_.x + cos(rotation) * length,
                             rect_.y - sin(rotation) * length)
    # Return the point coordinates to match its position on the screen
    # eg. x = rect_.x + cos(theta)* length and y = rect_.y + sin(theta) * length
    return p_


def missile_particles(screen):
    """ display all the particles onto the screen bitmap."""
    for sprite in VERTEX_ARRAY_MP:
        if sprite.rect.colliderect(screen.get_rect()):
            if sprite.index < len(sprite.images) -1:

                sprite.image = sprite.images[sprite.index].convert()
                sprite.rect = sprite.image.get_rect(center=sprite.position)

                # Blending effect & center the sprite (blit always display the sprite from the left corner)
                screen.blit(sprite.image, (sprite.rect.centerx - sprite.rect.w // 2,
                                           sprite.rect.centery - sprite.rect.h // 2 - 2),
                            special_flags=pygame.BLEND_RGB_ADD)

                sprite.rect.move_ip(sprite.vector)
                sprite.position += sprite.vector

                # Kill the instance and remove the particle from
                # the vertex_array when the index reach the end of the sprite animation.
                sprite.index += 2
            else:
                sprite.kill()
        else:
            sprite.kill()


def MissileParticleFx_improve(rect_:pygame.math.Vector2,            # Vector2 representing the center of
                                                                    # the reference of the parent object
                              vector_:pygame.math.Vector2,          # vector2, direction of the parent object
                              layer_:int,                           # Layer used
                              angle_:int,                           # parent angle in degrees (0 to 360 degrees)
                              exhaust_pos_: pygame.math.Vector2     # tuple representing the exhaust absolute position
                              ):
    missile_sprite = pygame.sprite.Sprite()
    missile_sprite.images = MISSILE_TRAIL1.copy()                       # Sprite list
    missile_sprite.image = MISSILE_TRAIL1[0]                            # First sprite
    missile_sprite.alpha = 0                                          # alpha value
    missile_sprite.rect = \
        missile_sprite.image.get_rect(center=(rect_.x, rect_.y))        # get the rect and place the center
    missile_sprite._layer = layer_                                      # layer
    missile_sprite.vector = -vector_ * uniform(0, 0.5)
    missile_sprite.index = 0
    missile_sprite.angle = angle_ - 90                                  # The sprite image is oriented at 90 degrees
                                                                        # so the total rotate_inplace transformation is
                                                                        # angle_ - 90
    missile_sprite._blend = None
    # returns coordinates center for the sprite
    new_position = projection_1(exhaust_pos_, rect_, angle_)

    missile_sprite.position = new_position                              # sprite's center
    VERTEX_ARRAY_MP.add(missile_sprite)


if __name__ == '__main__':

    SCREENRECT = pygame.Rect(0, 0, 800, 1024)
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size,  pygame.HWSURFACE, 32)

    MISSILE_TRAIL = spread_sheet_fs8('Assets\\Graphics\\Exhaust\\2\\Hot_trail_128x128_.png', 128, 5, 5)
    # MISSILE_TRAIL = spread_sheet_per_pixel('Assets\\Graphics\\Exhaust\\2\\Hot_trail_128x128_4x8.png', 128, 8, 4)
    MISSILE_TRAIL = reshape(MISSILE_TRAIL, (50, 50))
    MISSILE_TRAIL = MISSILE_TRAIL[:13]

    a = pygame.Rect(10, 10, 10, 10)
    a.center = 0, 0
    b = pygame.Rect(10, 10, 10, 10)
    b.center = 40, 60

    angle = -degrees(atan2(60, 40)) % 360

    projection_1(pygame.math.Vector2(0, 10), pygame.math.Vector2(a.center), angle)