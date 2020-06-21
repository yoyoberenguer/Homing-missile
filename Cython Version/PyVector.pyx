#cython: boundscheck=False, wraparound=False, nonecheck=False, optimize.use_switch=True

"""
C Vector library
This unit contains a set of easy to use vector functions that can
be imported directly in a python script.
The project need to be compiled for your system before being imported into python,
to do so, use the following command into a DOS command line prompt.
C:\>python setup_PyVector.py build_ext --inplace.

When the compilation is complete, you should see two new files in your directory
1)PyVector.c
2)PyVector.cp36-win_amd64 (name depends on your system)

To import the library in your python IDE use the following import
import PyVector

The library is similar to pygame.math.Vector2 in a slightly much faster version

"""



# CYTHON IS REQUIRED
try:
    cimport cython
    from cpython.dict cimport PyDict_DelItem, PyDict_Clear, PyDict_GetItem, PyDict_SetItem, \
        PyDict_Values, PyDict_Keys, PyDict_Items
    from cpython cimport PyObject, PyObject_HasAttr, PyObject_IsInstance
    from cython.parallel cimport prange

except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")
try:
    import pygame
    from pygame.math import Vector2
    from pygame import Surface, Rect, transform
except ImportError:
    raise ImportError("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")

from libc.stdio cimport printf

# --------------- C DECLARATION ----------------
cdef extern from 'vector.c':

    struct vector2d:
       float x;
       float y;

    struct mla_pack:
       vector2d vector;
       vector2d collision;

    mla_pack trajectory(vector2d p1, vector2d p2, vector2d v1, vector2d v2);
    void subv_inplace(vector2d *v1, vector2d v2);
    void addv_inplace(vector2d *v1, vector2d v2);
    float vlength(vector2d *v);
    float distance_to(vector2d v1, vector2d v2);
    void vecinit(vector2d *v, float x, float y)
    vector2d addcomponents(vector2d v1, vector2d v2)
    vector2d subcomponents(vector2d v1, vector2d v2)
    void scale_inplace(float c, vector2d *v)
    vector2d scalevector2d(float c, vector2d *v)
    float dot(vector2d *v1, vector2d *v2)

    float distance_squared_to(vector2d v1, vector2d v2)
    void divv_inplace(vector2d *v1, vector2d v2)
    void mulv_inplace(vector2d *v1, vector2d v2)
    vector2d mulcomponents(vector2d v1, vector2d v2)
    vector2d divcomponents(vector2d v1, vector2d v2)
    void normalize (vector2d *v)
    void scale_to_length(vector2d *v, float length)
    float length_squared(vector2d v)
    void vrotate_deg(vector2d *v, float deg)
    void vrotate_rad(vector2d *v, float rad)
    float angle_to(vector2d v1, vector2d v2)
    float vangle_rad(vector2d v)
    float vangle_deg(vector2d v)
    vector2d adjust_vector(vector2d player, vector2d rect, vector2d speed)
    vector2d RandAngleVector2d(int minimum, int maximum, float angle)
    void RandAngleVector2d_inplace(vector2d *v, int minimum, int maximum, float angle)
    vector2d RandAngleVector2df(float minimum, float maximum, float angle)
    void RandAngleVector2d_inplacef(vector2d *v, float minimum, float maximum, float angle)

# ----------------------------------------------


cpdef vector2d v_vector2d(float x, float y):
    """
    2d Vector structure with components x & y (floats)
    Use the structure vector2d to declare vector type object
    e.g struct vector2d v-> v(x, y)
    """
    cdef vector2d v;
    v.x = x
    v.y = y
    return v

cpdef vector2d v_sub_inplace(vector2d v1, vector2d v2):
    """
    Substract vector components such as v1 = v1 - v2
    v1.x = v1.x - v2.x and v1.y = v1.y - v2.y
    """
    subv_inplace(&v1, v2)
    return v1

cpdef vector2d v_add_inplace(vector2d v1, vector2d v2):
    """
    Add vector components such as v1 = v1 + v2
    v1.x = v1.x + v2.x and v1.y = v1.y + v2.y
    """
    addv_inplace(&v1, v2)
    return v1

cpdef float v_length(vector2d v):
    """
    Returns the Euclidean width of the vector (vector magnitude).
    e.g:
      float width = vlength(&v1);
    """
    return vlength(&v)

cpdef float v_distance_to(vector2d v1, vector2d v2):
    """
    Calculate the distance between two vectors ex v1 & v2
    Return a float representing the cartesian distance between v1 and v2
    timing : 0.182s for 10 millions iterations.
    e.g:
      struct vector2d v1, v2;
      vecinit(&v1, -1.0, 2.0);
      vecinit(&v2, 5.0, -5.0);
      float distance = distance_to(v1, v2);
    
    """
    return distance_to(v1, v2)

cpdef vector2d v_init(vector2d v, float x, float y):
    """
    Use this function to initialized a vector
    timing : 0.161s for 10 millions iterations.
    e.g:
      vecinit(v, 0.0, 0.0)  --> v(0.0, 0.0)
      vecinit(v, cos(90), sin(90))
    """
    vecinit(&v, x, y)
    return v

cpdef vector2d v_add_components(vector2d v1, vector2d v2):
    """
    Add components of 2 vectors (v1 + v2).
    Return a new 2d vector v with components vx = v1.x + v2.x and vy = v1.y + v2.y
    """
    return addcomponents(v1, v2)

cpdef vector2d v_sub_components(vector2d v1, vector2d v2):
    """
    Substract components of 2 vectors (v1 - v2).
    Return a new 2d vector v with components vx = v1.x - v2.x and vy = v1.y - v2.y
    """
    return subcomponents(v1, v2)

# TODO CHECK FOR THE REST
cpdef void v_scale_inplace(float c, vector2d v):
    """
    Multiply a vector with a scalar c (scaling a vector)
    Return a re-scale vector v with components vx = vx * (scalar c) and vy = vy * (scalar c)
    """
    scale_inplace(c, &v)


cpdef vector2d v_scale(float c, vector2d v):
    """
    Multiply a vector with a scalar c (scaling a vector)
    Return a re-scale vector v with components vx = vx * (scalar c) and vy = vy * (scalar c)
    """
    scalevector2d(c, &v)
    return v

cpdef float v_dot(vector2d v1, vector2d v2):
    """
    dot product (scalar product).
    a · b = |a| × |b| × cos(θ)
    |a| is the magnitude (width) of vector a
    |b| is the magnitude (width) of vector b
    θ is the angle between a and b
    or -> a · b = ax × bx + ay × by
    """
    return dot(&v1, &v2)

cpdef float v_distance_squared_to(vector2d v1, vector2d v2):
    """
    Calculate distance between two vectors ex v1 & v2
    Return a float representing the square distance between v1 & v2
    timing : 0.099s for 10 millions iterations
    e.g:
      float distance = distance_to(v1, v2); 
    """
    return distance_squared_to(v1, v2)

cpdef vector2d v_div_inplace(vector2d v1, vector2d v2):
    """
    Divide vector components such as v1 = v1 / v2
    v1.x = v1.x / v2.x and v1.y = v1.y / v2.y  (with v2.x and v2.y !=0)
    """
    divv_inplace(&v1, v2)
    return v1

cpdef vector2d v_mul_inplace(vector2d v1, vector2d v2):
    """
    Multiply vector components such as v1 = v1 * v2
    v1.x = v1.x * v2.x and v1.y = v1.y * v2.y
    """
    mulv_inplace(&v1, v2)
    return v1

cpdef vector2d v_mul_components(vector2d v1, vector2d v2):
    """
    multiply components of 2 vectors (v1 * v2).
    Return a new 2d vector v with components vx = v1.x * v2.x and vy = v1.y * v2.y
    """
    return mulcomponents(v1, v2)

cpdef vector2d v_div_components(vector2d v1, vector2d v2):
    """
    divide components of 2 vectors (v1 / v2).
    Return a new 2d vector v with components vx = v1.x / v2.x and vy = v1.y / v2.y
    Return a vector with magnitude equal zero when division by zero.
    """
    return divcomponents(v1, v2)

cpdef vector2d v_normalize (vector2d v):
    """
    Vector normalisation (dividing components x&y by vector magnitude) v / |v|
    """
    normalize(&v)
    return v

cpdef vector2d v_scale_to_length(vector2d v, float c):
    """
    Normalize a 2d vector and rescale it to a given width. (v / |v|) * scalar
    """
    scale_to_length(&v, c)
    return v

cpdef float v_length_squared(vector2d v):
    """
    Returns the squared Euclidean width of a vector (vector magnitude).
    """
    return length_squared(v)


cpdef vector2d v_rotate_deg(vector2d v, float deg):
    """
    Rotates a vector by a given angle in degrees.
    """
    vrotate_deg(&v, deg)
    return v

cpdef vector2d v_rotate_rad(vector2d v, float rad):
    """
    Rotates a vector by a given angle in radians.
    """
    vrotate_deg(&v, rad)
    return v

cpdef float v_angle_to(vector2d v1, vector2d v2):
    """
    Calculates the angle to a given vector in degrees (v2 angle - v1 angle)
    """
    return angle_to(v1, v2)

cpdef float v_angle_rad(vector2d v):
    """
    Return the vector angle in radians.
    """
    return vangle_rad(v)

cpdef float v_angle_deg(vector2d v):
    """
    Return the vector angle in degrees.
    """
    return vangle_deg(v)

cpdef vector2d angle_vector(vector2d player, vector2d rect, vector2d speed):
    """
    Determine the angle between player vector and rect vector. 
    The angle is projected on both axis (x, y) and scale to width speed 
    :param player: vector2d; player position 
    :param rect: vector2d; other location 
    :param speed: vector2d; vector magnitude 
    :return: vector2d orepresenting the angle between the player and rect with magnitude <speed>
    """
    return adjust_vector(player, rect, speed)

cpdef vector2d rand_angle(int minimum, int maximum, float angle):
    """
    Scale a vector to a random width (int) and toward a given angle
    angle is in radian.

    :param minimum: int; minimum value for the re-scale
    :param maximum: int; maximum value for the re-scale
    :param angle: float; angle in radian
    :return: vector2d; new vector
    """
    return RandAngleVector2d(minimum, maximum, angle)

cpdef vector2d rand_angle_inplace(vector2d v, int minimum, int maximum, float angle):
    """
    Scale a vector inplace to a random width (int) and toward a given angle
    angle is in radian.

    :param v: vector2d; vector to be re-scale inplace
    :param minimum: int; min re-scale value
    :param maximum: int; max re-scale value
    :param angle: float; angle in radians
    :return: return vector v
    """
    RandAngleVector2d_inplace(&v, minimum, maximum, angle)
    return v

cpdef vector2d rand_angle_f(float minimum, float maximum, float angle):
    """
    Scale a new vector to a random width (float) and toward a given angle
    angle is in radian.

    :param minimum: float; minimum value for re-scaling
    :param maximum: float; maximum value for re-scaling
    :param angle: float; angle in radian
    :return: vector2d; new vector
    """
    return RandAngleVector2df(minimum, maximum, angle)

cpdef vector2d rand_angle_inplacef(vector2d v, float minimum, float maximum, float angle):
    """
    # Scale a vector inplace to a random width (float) and toward a given angle
    # angle is in radian.

    :param v: vector2d; vector to change
    :param minimum: float; min re-scale value
    :param maximum: float; max re-scale value
    :param angle: float; angle in radian
    :return: vector2d
    """
    RandAngleVector2d_inplacef(&v, minimum, maximum, angle)
    return v

# TODO WHEN TIME ALLOW IT
#
# cdef class PyVector2(object):
#
#     cdef dict __dict__
#
#     def __init__(self, float x, float y):
#         cdef vector2d v
#         self.v.x = x
#         self.v.y = y
#
#     def __add__(self, vector2d other):
#         self.v.x += other.x
#         self.v.y += other.y
#
#     def __neg__(self):
#         self.v.x = -self.v.x
#         self.v.y = -self.v.y
#
#     def __mul__(self, vector2d other):
#         self.v.x *= other.x
#         self.v.y *= other.y
#
#     def __divmod__(self, vector2d other):
#         self.v.x /= other.x
#         self.v.y /= other.y
#
#     def __sub__(self, vector2d other):
#         self.v.x -= other.x
#         self.v.y -= other.y

