# encoding: utf-8


"""
                 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Copyright Yoann Berenguer
"""

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


class EnemyClass(Sprite):
    """
    ENEMY CLASS
    FEEL FREE TO ADD MORE METHODS TO DEFINE YOUR ENEMY BASE CLASS

    """

    def __init__(self, containers_, image_, pos_, gl_, timing_=60.0, layer_=0):
        """

        :param containers_: pygame groups; Store the sprite in specific pygame group(s), use kill() to
        remove the sprite from any group(s)
        :param image_     : Surface; Image of your enemy
        :param pos_       : tuple (x, y); Position of the enemy on the current display (x, y) positions.
        :param gl_:       : Global constants/variables; see Var.py for more details. gl_ is an instance
        :param timing_    : float; FPS to aim for (refreshing rate), default 60 FPS. If the FPS is > 60, the update
        method will slow down the refreshing speed.
        :param layer_     : Layer to display the sprite, default 0
        """
        # METHOD INHERIT FROM SPRITE
        Sprite.__init__(self, containers_)

        self.position = Vector2(pos_[0], pos_[1])
        self.vector   = Vector2(0.0, -0.0)
        self.image    = image_
        self.rect     = self.image.get_rect(center=pos_)
        self.mask     = from_surface(self.image)
        self.gl       = gl_
        self.layer    = layer_
        self.timing   = timing_
        self.angle    = 0
        self.life     = 1000
        self.max_life = 1000
        self.rotation = 0
        self._blend   = 0
        self.dt       = 0
        if gl_.MAX_FPS > timing_:
            self.timer = self.timing
        else:
            self.timer = 0.0

    def update(self, args=None):
        """
        UPDATE METHOD
        This method is called from the main loop every frames. 
        Define here what should be your enemy behaviors.
        """

        if self.dt > self.timer:
            self.rect = self.image.get_rect(center=self.position)
            # self.rect = self.rect.clamp(self.gl.SCREENRECT)
            self.position.x += self.vector.x
            self.position.y += self.vector.y
            self.position = self.position
        self.dt += self.gl.TIME_PASSED_SECONDS

    def update_position(self, mouse_pos):
        """
        UPDATE ENEMY POSITION
        This method is call from the mainloop to update the 
        instance variable self.position.
        
        """
        self.position.x = mouse_pos[0]
        self.position.y = mouse_pos[1]

    def update_rect(self, mouse_pos):
        """
        UPDATE ENEMY RECT 
        This method update the enemy pygame rect 
        :param mouse_pos: tuple (x, y), mouse position read on screen
        :return: None
        """
        self.rect.centerx = mouse_pos[0]
        self.rect.centery = mouse_pos[1]
