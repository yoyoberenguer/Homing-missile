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
except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")



# LOAD EXTERNAL VECTOR LIBRARY
cdef extern from 'vector.c':

    struct vector2d:
       float x;
       float y;

    void subv_inplace(vector2d *v1, vector2d v2);
    void addv_inplace(vector2d *v1, vector2d v2);
    float vlength(vector2d *v);
    float distance_to(vector2d v1, vector2d v2);
    void vecinit(vector2d *v, float x, float y)
    vector2d addcomponents(vector2d v1, vector2d v2)
    vector2d subcomponents(vector2d v1, vector2d v2)
    void scalevector2d_self(float c, vector2d *v)
    vector2d scalevector2d(float c, vector2d *v)
    float dot(vector2d *v1, vector2d *v2)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class EnemyClass(Sprite):
    """
    ENEMY CLASS
    FEEL FREE TO ADD MORE METHODS TO DEFINE YOUR ENEMY BASE CLASS

    """

    cdef:
        public object rect, mask, image
        object gl
        public position, vector
        public int layer, angle, life, \
            max_life, rotation, _blend
        float dt, timer, timing

    def __init__(self, containers_, image_, pos_, gl_, timing_=60.0, layer_=0):
        """

        :param containers_: pygame groups; Store the sprite in specific pygame group(s), use kill() to
        remove the sprite from any group(s)
        :param image_     : Surface; Image of your enemy
        :param pos_       : tuple (x, y); Position of the enemy on the current display (x, y) positions.
        :param gl_:       : Global constants/variables; see CythonGlobalVar.pyx for more details. gl_ is an instance
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

    # EXTERNAL ACCESS (KEEP THE CPDEF)
    cpdef update(self, args=None):
        """
        UPDATE METHOD
        This method is called from the main loop every frames. 
        Define here what should be your enemy behaviors.
        """
        cdef:
            position = self.position
            vector   = self.vector
            float dt = self.dt

        if dt > self.timer:
                self.rect = self.image.get_rect(center=position)
                # self.rect = self.rect.clamp(self.gl.SCREENRECT)
                position.x += vector.x
                position.y += vector.y
                dt = 0
                self.position = position
        dt += self.gl.TIME_PASSED_SECONDS
        self.dt = dt

    # EXTERNAL ACCESS (KEEP THE CPDEF)
    cpdef void update_position(self, mouse_pos):
        """
        UPDATE ENEMY POSITION
        This method is call from the mainloop to update the 
        instance variable self.position.
        
        """
        cdef position = self.position
        position.x = mouse_pos[0]
        position.y = mouse_pos[1]
        self.position = position

    # EXTERNAL ACCESS (KEEP THE CPDEF)
    cpdef void update_rect(self, mouse_pos):
        """
        UPDATE ENEMY RECT 
        This method update the enemy pygame rect 
        :param mouse_pos: tuple (x, y), mouse position read on screen
        :return: None
        """
        cdef rect = self.rect
        rect.centerx = mouse_pos[0]
        rect.centery = mouse_pos[1]
        self.rect = rect

