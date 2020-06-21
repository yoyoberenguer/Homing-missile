###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8

# PYGAME IS REQUIRED
import pygame

try:
    from pygame.mask import from_surface
    from pygame.math import Vector2
except ImportError:
    raise ImportError("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")


try:
   from Sprites cimport Sprite
except ImportError:
    raise ImportError("\nSprites.pyd missing!.Build the project first.")

# CYTHON IS REQUIRED
try:
    cimport cython
    from cpython cimport PyObject, PyObject_HasAttr, PyObject_IsInstance
except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class PlayerClass(Sprite):
    """
    PLAYER BASE CLASS
    FEEL FREE TO ADD MORE METHODS TO DEFINE YOUR PLAYER BASE CLASS
    """

    cdef:
        public object image, rect, mask,
        object gl
        public int layer, angle, life, max_life, _rotation, _blend
        float timing, dt, timer

        float reloading_time
        float timestamp, c

    def __init__(self, containers_, image_, tuple pos_, gl_, float timing_=60.0, int layer_=0, int _blend=0):
        """

        :param containers_: pygame groups; Store the sprite in specific pygame group(s), use kill() to
        remove the sprite from any group(s)
        :param image_     : Surface; Player image
        :param pos_       : tuple (x, y) or Vector2; Player position on the current display (x, y) positions.
        :param gl_        : Global constants/variables; see CythonGlobalVar.pyx for more details. gl_ is an instance
        :param timing_    : float; FPS to aim for (refreshing rate), default 60 FPS. If the FPS is > 60, the update
        method will slow down the refreshing speed.
        :param layer_     : integer; Layer to display the sprite default 0
        :param _blend     : integer; Additive mode to use
        """

        # METHOD INHERIT FROM SPRITE
        Sprite.__init__(self, containers_)
        assert PyObject_IsInstance(pos_, (tuple, Vector2)), \
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

    # EXTERNAL ACCESS (KEEP THE CPDEF)
    cpdef center(self):
        """
        RETURN THE SPRITE LOCATION (TUPLE X, Y)
        :return: tuple; Player position on the current display
        """
        return self.rect.center

    cpdef bint is_missile_reloading(self, float reload, bint force = False):
        """
        CHECK IF A WEAPON IS RELOADED AND READY.
        Returns False when the weapon is ready to shoot else return True
        :return: bool; True | False
        """
        # DON'T ASK ..SHOOT
        if force:
            self.timestamp = 0
            return False

        if abs(self.gl.FRAME - self.timestamp) > reload:
            # READY TO SHOOT
            self.timestamp = 0
            return False

        # RELOADING
        return True

    cpdef void launch_missile(self):
        """
        SET THE WEAPON TIMESTAMP VARIABLE (SHOT FRAME NUMBER)
        This method must be call every shots.

        :return: None 
        """
        self.timestamp = self.gl.FRAME


    # EXTERNAL ACCESS (KEEP THE CPDEF)
    cpdef update(self, args=None):
        cdef:
            float dt = self.dt
            object rect = self.rect
            object gl = self.gl

        if dt > self.timer:
            rect = rect.clamp(gl.SCREENRECT)
            dt = 0

        dt += gl.TIME_PASSED_SECONDS
        self.dt = dt
        self.rect = rect
