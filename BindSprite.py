# encoding: utf-8
"""

                   GNU GENERAL PUBLIC LICENSE

                       Version 3, 29 June 2007


 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>

 Everyone is permitted to copy and distribute verbatim copies

 of this license document, but changing it is not allowed.
 """

__author__ = "Yoann Berenguer"
__copyright__ = "Copyright 2007, Cobra Project"
__credits__ = ["Yoann Berenguer"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Yoann Berenguer"
__email__ = "yoyoberenguer@hotmail.com"

import pygame
from math import cos, sin, radians, hypot, degrees, acos, atan, copysign


# Bind a sprite to an object optionally with an offset
# if offset is not None, use object position with added offset
# else use the object location.

# This class does not check if the object is still alive if you are
# not using the flag dependency.
# The class does not check the SCREEN boundaries, so you can display
# the sprite at any locations.
# More than one sprite animation can be played around the same object, the class
# will not check the number of instance already running.
# The sprite is killed eventually when all sprites have been blit onto the SCREEN
# except is the option loop is used.
# Setting the dependency flag will allow the method update to check each iteration
# if the parent object is still alive and interact with the sprite accordingly.

class BindSprite(pygame.sprite.Sprite):
    images = None
    containers = None

    def __init__(self,
                 object_,              # Parent object to use
                 gl_,                  # class global variable
                 offset_=None,         # offset default is None
                 timing_=15,           # timing default is 15
                 layer_=0,             # display sprite on layer 0 by default
                 loop_=False,          # loop sprite animation, default False
                 dependency_ = False,  # if the object is not alive, kill the sprite
                 follow_ = False,      # Tell the sprite to follow parent rotate_inplace
                 blend_ = None,        # Blend mode default None
                 event_ =None          # Event type
                 ):
        """

        :param object_:
        :param gl_:
        :param offset_:
        :param timing_:
        :param layer_:
        :param loop_:
        :param dependency_:
        :param follow_:
        :param blend_:
        :param event_:
        """
        self._blend = blend_

        assert BindSprite.images is not None, \
            'class variable images should be a pygame surface or a list.'
        assert BindSprite.containers is not None, \
            'class variable containers should be a given pygame.sprite.Group.'
        self._layer = layer_

        pygame.sprite.Sprite.__init__(self, self.containers)

        if isinstance(gl_.All, pygame.sprite.LayeredUpdates):
            gl_.All.change_layer(self, layer_)

        self.images_copy = self.images.copy()
        self.image = self.images_copy[0] if \
            isinstance(self.images, list) else self.images_copy
        self.object = object_               # Parent object
        self.offset = offset_               # Offset from the center
        if offset_ is not None:
            self.rect = self.image.get_rect(center=(object_.rect.centerx + offset_[0],
                                                    object_.rect.centery + offset_[1]))
        else:
            self.rect = self.image.get_rect(center=object_.rect.center)
        self.dt = 0                         # time constant
        self.timing = timing_               # Refresh in ms
        self.index = 0                      # Matrix indices (next sprite)
        self.loop = loop_                   # if True, loop back to the first frame
        self.gl = gl_                       # Global constants
        self.dependency = dependency_       # if True, kill the sprite when the parent is killed
        self.event = event_                 # Define special event
        self.follow = follow_               # Allow sprite to follow parent rotate_inplace

    @classmethod
    def kill_instance(cls, instance_):
        """ Kill a given instance """
        if isinstance(instance_, BindSprite):
            if hasattr(instance_, 'kill'):
                instance_.kill()


    def update(self):

        # object and sprite are connected together, if
        # object dies, the sprite is killed.
        if self.dependency and not self.object.alive():
            self.kill()
            self.gl.All.remove(self)

        if self.dt > self.timing:

            if isinstance(self.images_copy, list):

                self.image = self.images_copy[self.index % len(self.images_copy)]
                if self.follow:
                    self.image, self.rect = \
                        self.object.rot_center(self.image.copy(),
                            self.object._rotation + 90, self.rect)

                if not self.loop:
                    if self.index > len(self.images_copy) - 1:
                        self.kill()
            else:
                self.image = self.images_copy
                if not self.loop:
                    self.kill()

            self.index += 1
            self.dt = 0

        # Sprite has an offset from the center
        if self.offset is not None:
            # sprite follow parent rotate_inplace
            if self.follow:
                hypo = hypot(*self.offset)
                if self.offset[0] != 0:
                    angle = degrees(atan(self.offset[1] / self.offset[0]))
                else:
                    angle = degrees(atan(self.offset[1] /
                                         (copysign(1, self.offset[0]) * 0.0000000000001)))
                angle %= 360

                if 0 < angle <= 180:
                    t = radians(-180 + self.object._rotation)
                    offset_=(cos(t) * hypo,
                            -sin(t) * hypo)
                else:
                    offset_=(cos(radians(self.object._rotation)) * hypo,
                            -sin(radians(self.object._rotation)) * hypo)

                self.rect = self.rect = self.image.get_rect(
                    center=(self.object.rect.centerx + offset_[0],
                            self.object.rect.centery + offset_[1]))

            else:
                self.rect = self.image.get_rect(
                    center=(self.object.rect.centerx + self.offset[0],
                            self.object.rect.centery + self.offset[1]))
        else:
            self.rect = self.image.get_rect(
                center=self.object.rect.center)

        # self.rect = self.rect.clamp(self.gl.SCREENRECT)

        self.dt += self.gl.TIME_PASSED_SECONDS
