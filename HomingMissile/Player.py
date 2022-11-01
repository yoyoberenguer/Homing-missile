# encoding: utf-8


"""
                 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Copyright Yoann Berenguer
"""

# PYGAME IS REQUIRED
import pygame

try:
    from pygame.mask import from_surface
    from pygame.math import Vector2
except ImportError:
    raise ImportError("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")


try:
    from Sprites import Sprite
except ImportError:
    raise ImportError("\nSprites.pyd missing!.Build the project first.")


class PlayerClass(Sprite):
    """
    PLAYER BASE CLASS
    FEEL FREE TO ADD MORE METHODS TO DEFINE YOUR PLAYER BASE CLASS
    """

    def __init__(self, containers_, image_, pos_, gl_, timing_=60.0, layer_=0, _blend=0):
        """

        :param containers_: pygame groups; Store the sprite in specific pygame group(s), use kill() to
        remove the sprite from any group(s)
        :param image_     : Surface; Player image
        :param pos_       : tuple (x, y) or Vector2; Player position on the current display (x, y) positions.
        :param gl_        : Global constants/variables; see Var.py for more details. gl_ is an instance
        :param timing_    : float; FPS to aim for (refreshing rate), default 60 FPS. If the FPS is > 60, the update
        method will slow down the refreshing speed.
        :param layer_     : integer; Layer to display the sprite default 0
        :param _blend     : integer; Additive mode to use
        """

        # METHOD INHERIT FROM SPRITE
        Sprite.__init__(self, containers_)
        assert isinstance(pos_, (tuple, Vector2)), \
            "\nArgument pos_ should be a tuple | Vector2 got %s " % type(pos_)

        self.image     = image_
        self.rect      = image_.get_rect(center=pos_)
        self.mask      = pygame.mask.from_surface(self.image)
        self.gl        = gl_
        self.layer     = layer_
        self.timing    = timing_
        self.angle     = 0
        self.life      = 1000
        self.max_life  = 1000
        self._rotation = 0
        self.dt        = 0
        self._blend    = 0

        # FORCE THE CONDITION self.gl.FRAME - self.timestamp > reload
        # TO BE TRUE WHEN THE PLAYER SHOOT FOR THE FIRST TIME
        self.timestamp = 1000000

        if gl_.MAX_FPS > timing_:
            self.timer = self.timing
        else:
            self.timer = 0.0

    def center(self):
        """
        RETURN THE SPRITE LOCATION (TUPLE X, Y)
        :return: tuple; Player position on the current display
        """
        return self.rect.center

    def is_missile_reloading(self, reload, force = False):
        """
        CHECK IF A WEAPON IS RELOADED AND READY.
        Returns False when the weapon is ready to shoot else return True
        :return: bool; True | False
        """
        if force:
            self.timestamp = 0
            return False

        if abs(self.gl.FRAME - self.timestamp) > reload:
            # READY TO SHOOT
            self.timestamp = 0
            return False

        # RELOADING
        return True

    def launch_missile(self):
        """
        SET THE WEAPON TIMESTAMP VARIABLE (SHOT FRAME NUMBER)
        This method must be call every shots.

        :return: None 
        """
        self.timestamp = self.gl.FRAME

    def update(self, args=None):

        if self.dt > self.timer:
            self.rect = self.rect.clamp(self.gl.SCREENRECT)
            self.dt = 0

        self.dt += self.gl.TIME_PASSED_SECONDS
