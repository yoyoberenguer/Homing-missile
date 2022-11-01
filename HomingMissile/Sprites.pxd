
# PYGAME IS REQUIRED
try:
    import pygame
    from pygame import Color, Surface, SRCALPHA, RLEACCEL, BufferProxy, gfxdraw
    from pygame.surfarray import pixels3d, array_alpha, pixels_alpha, array3d
    from pygame.image import frombuffer
    from pygame import Rect
    from pygame.time import get_ticks

except ImportError:
    raise ImportError("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")

try:
    cimport cython
    from cython.parallel cimport prange
    from cpython cimport PyObject_CallFunctionObjArgs, PyObject, \
        PyList_SetSlice, PyObject_HasAttr, PyObject_IsInstance, \
        PyObject_CallMethod, PyObject_CallObject
    from cpython.dict cimport PyDict_DelItem, PyDict_Clear, PyDict_GetItem, PyDict_SetItem, \
        PyDict_Values, PyDict_Keys, PyDict_Items
    from cpython.list cimport PyList_Append, PyList_GetItem, PyList_Size
    from cpython.object cimport PyObject_SetAttr

except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class Sprite(object):

    cdef dict __dict__

    cpdef add_internal(self, object group);

    cpdef remove_internal(self, object group);

    cpdef update(self, args=*);

    cpdef kill(self);

    cpdef list groups(self);

    cpdef bint alive(self);


#
# @cython.boundscheck(False)
# @cython.wraparound(False)
# @cython.nonecheck(False)
# @cython.cdivision(True)
# cdef class AbstractGroup(object):
#
#     cpdef list sprites(self)
#
#     cpdef void add_internal(self, sprite)
#
#     cpdef void remove_internal(self, object sprite)
#
#     cpdef bint has_internal(self, object sprite)
#
#     cpdef copy(self)
#
#     cpdef void update(self, args=*)
#
#     cpdef draw(self, object surface)
#
#     cpdef void clear(self, object surface, object bgd)
#
#     cpdef void empty(self)


