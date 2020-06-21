###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True

try:
    cimport cython
    from cpython.dict cimport PyDict_DelItem, PyDict_Clear, PyDict_GetItem, PyDict_SetItem, \
        PyDict_Values, PyDict_Keys, PyDict_Items, PyDict_SetItemString
    from cpython cimport PyObject, PyObject_HasAttr, PyObject_IsInstance
except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")

try:
    from pygame.math import Vector2
except ImportError:
    raise ImportError("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class CONSTANTS:
    """
    DEFINE YOUR GAME VARIABLES AND CONSTANT

    To access your variables
    1) Create first an instance of the class
        GL = CONSTANTS()
    2) Access the variable
        GL.MAX_FPS      -> point to MAX_FPS VAR

    PS: TO MAKE YOUR VARIABLE VISIBLE FROM AN EXTERNAL ACCESS USE
        cdef public
        If the variable is not public, an attribute error will be raised
    """

    # METHOD 2
    # cdef dict __dict__

    cdef:
        public object SC_EXPLOSION, SCREENRECT, RATIO
        public object SCREEN, ALL, PLAYER_GROUP, PLAYER_PROJECTILE, GROUP_UNION, ENEMY_GROUP
        public object ENEMY_PROJECTILE, MIXER_PLAYER, MIXER_EXPLOSION, PLAYER
        public float SOUND_LEVEL, TIME_PASSED_SECONDS
        public int MAX_FPS
        public int FRAME
        public bint PAUSE



    def __cinit__(self):
        self.MAX_FPS                 = 60
        self.SC_EXPLOSION            = None
        self.SOUND_LEVEL             = 1.0
        try:
            self.TIME_PASSED_SECONDS     = 1000.0/self.MAX_FPS
        except ZeroDivisionError:
            raise ValueError('\nMAX_FPS cannot be zero !')
        self.FRAME                   = 0
        self.SCREENRECT              = None
        self.RATIO                   = Vector2(1.0, 1.0)
        self.PAUSE                   = False
        self.SCREEN                  = None
        self.ALL                     = None
        self.PLAYER_GROUP            = None
        self.PLAYER_PROJECTILE       = None
        self.GROUP_UNION             = None
        self.ENEMY_GROUP             = None
        self.ENEMY_PROJECTILE        = None
        self.MIXER_EXPLOSION         = None
        self.PLAYER                  = None

        # METHOD 2
        # self.__dict__ = {}

        # PyDict_SetItem(self.__dict__, 'SC_EXPLOSION', None)
        # PyDict_SetItem(self.__dict__, 'SOUND_LEVEL', 1.0)
        # PyDict_SetItem(self.__dict__, 'TIME_PASSED_SECONDS', 0)
        # PyDict_SetItem(self.__dict__, 'FRAME', 0)
        # PyDict_SetItem(self.__dict__, 'SCREENRECT', None)
        # PyDict_SetItem(self.__dict__, 'RATIO', Vector2(1.0, 1.0))
        # PyDict_SetItem(self.__dict__, 'MAX_FPS', 60)
        # PyDict_SetItem(self.__dict__, 'PAUSE', False)


    cpdef show_all_attributes(self):
        return self.__dict__