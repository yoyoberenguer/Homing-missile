#cython: boundscheck=False, wraparound=False, nonecheck=False, optimize.use_switch=True


try:
    from MissileParticleFx import MissileParticleFx_improve
except ImportError:
    raise ImportError("\n<MissileParticleFx> library is missing on your system.")

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

try:
   from Sprites cimport Sprite
except ImportError:
    raise ImportError("\nSprites.pyd missing!.Build the project first.")

# C LIBRARY
from libc.math cimport sqrt

# --------------- CONSTANTS --------------------
DEF M_PI = 3.14159265359
DEF DEG_TO_RAD = M_PI/180.0
DEF RAD_TO_DEG = 1.0/DEG_TO_RAD
# ----------------------------------------------

# --------------- C DECLARATION ----------------
cdef extern from 'vector.c':

    struct vector2d:
       float x;
       float y;

    struct mla_pack:
       vector2d vector;
       vector2d collision;

    mla_pack trajectory(vector2d p1, vector2d p2, vector2d v1, vector2d v2)nogil;
    void subv_inplace(vector2d *v1, vector2d v2)nogil;
    void addv_inplace(vector2d *v1, vector2d v2)nogil;
    float vlength(vector2d *v)nogil;
    float distance_to(vector2d v1, vector2d v2)nogil;
    void vecinit(vector2d *v, float x, float y)nogil;
    vector2d addcomponents(vector2d v1, vector2d v2)nogil;
    vector2d subcomponents(vector2d v1, vector2d v2)nogil;
    void scalevector2d_self(float c, vector2d *v)nogil;
    vector2d scalevector2d(float c, vector2d *v)nogil;
    float dot(vector2d *v1, vector2d *v2)nogil;
# ----------------------------------------------

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef missile_lead_angle_c(p1, p2, v1, v2):
    """
    C VERSION OF MISSILE LEAD ANGLE 
    
    :param p1: 
    :param p2: 
    :param v1: 
    :param v2: 
    :return: 
    """
    cdef mla_pack package
    cdef vector2d p1_, p2_, v1_, v2_
    p1_.x, p1_.y= p1.x, p1.y
    p2_.x, p2_.y = p2.x, p2.y
    v1_.x, v1_.y = v1.x, v1.y
    v2_.x, v2_.y = v2.x, v2.y
    package = trajectory(p1_, p2_, v1_, v2_)
    return package.vector, package.collision

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef missile_lead_angle_cython(p1, p2, v1, v2):
    """
    CYTHON VERSION OF MISSILE LEAD ANGLE 
    :param p1: 
    :param p2: 
    :param v1: 
    :param v2: 
    :return: 
    """
    cdef vector2d p1_, p2_, v1_, v2_
    p1_.x, p1_.y= p1.x, p1.y
    p2_.x, p2_.y = p2.x, p2.y
    v1_.x, v1_.y = v1.x, v1.y
    v2_.x, v2_.y = v2.x, v2.y
    return missile_lead_angle_cython_c(p1_, p2_, v1_, v2_)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef missile_lead_angle_cython_c(vector2d p1, vector2d p2, vector2d v1, vector2d v2):
    """
    Determine the collision missile lead angle
    :param p1: Point1
    :param p2: Point2
    :param v1: missile vector
    :param v2: target vector
    :return: Returns missile vector and collision point
    In computer geometry, always use vectors if possible!
    Code gets more complicated if you try to work with Cartesian co-ordinates
    (x,y) or with line equations y=mx+b.
    Here, for example, you have special cases for horizontal lines, m=0, and vertical lines, m=∞.
    So let's try to program this, sticking to vectors throughout.
    First, let's review the problem. We have a line segment from p1.p to p2.p and we want to find
    the points of intersection with a circle centred at self.p and radius self.r. I'm going to write these as
    p1, p2, q, and r respectively.

    Any point on the line segment can be written p1+t(p2−p1)for a
    scalar parameter t between 0 and 1. We'll be using p2−p1 often, so let's write v=p2−p1.
    Let's set this up in Python. I'm assuming that all the points are pygame.math.Vector2 objects,
    so that we can add them and take dot products and so on.
    I'm also assuming that we're using Python 3, so that division returns a float

    Q is the centre of circle (pygame.math.Vector2)
    r is the radius           (scalar)
    p1 constraint.point1      (pygame.math.Vector2), start of the line segment
    v constraint.point2 - p1  (pygame.math.Vector2), vector along line segment
    Now, a point x is on the circle if its distance from the centre of the circle is equal
    to the circle's radius, that is, if
    |x - q| = r
    So the line intersects the circle when
    |p1 + tv - q| = r
    Squaring both sides gives
    |p1 + tv - q| **2 = r ** 2
    Expanding the dot product and collecting powers of t gives
    t ** 2 (v.v) + 2t(v.(p1 - q)) + (p1.p1 + q.q - 2p1.q - r**2) = 0
    which is a quadratic equation in t with coefficients
    a = v.v
    b = 2(v.(p1 - q))
    c = p1.p1 + q.q - 2p1.q - r ** 2
    and solutions
    t = (-b +/- math.sqrt(b ** 2 - 4 * a * c)) / 2 * a

    a = V.dot(V)
    b = 2 * V.dot(P1 - Q)
    c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r ** 2
    The value b2−4ac inside the square root is known as the discriminant.
    If this is negative, then there are no real solutions to the quadratic equation;
    that means that the line misses the circle entirely.

    disc = b**2 - 4 * a * c
    if disc < 0:
        return False, None

    Otherwise, let's call the two solutions t1 and t2.
    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)

    If neither of these is between 0 and 1, then the line segment misses the circle (but would hit it if extended):
    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
    return False, None

    Now, the closest point on the extended line to the centre of the circle is
    p1+tv where
    t= ((q−p1)⋅v) / (|v| ** 2) = −b / 2a

    But we want to ensure that the point is on the line segment, so we must clamp
    t to lie between 0 and 1.
    t = max(0, min(1, - b / (2 * a)))
    return True, P1 + t * V

    """

    cdef vector2d v = subcomponents(p2, p1)
    cdef vector2d q = addcomponents(p2, v2) ;
    cdef float r = vlength(&v1);
    cdef float a = dot(&v, &v);
    cdef float double_a = 2 * a
    if a == 0:
        return None, None

    cdef vector2d tmp = subcomponents(p1, q);
    cdef float b = 2 * dot(&v, &tmp);
    cdef float c = (dot(&p1, &p1) + dot(&q, &q)) - (2 * dot(&p1, &q)) - (r * r);
    cdef float disc = (b * b) - (double_a * 2 * c);

    if disc < 0:
        return None, None

    cdef float disc_sqrt = sqrt(disc);
    # first intersection between the line and circle
    cdef float t1 = (-b + disc_sqrt) / double_a;
    # second intersection between the line and circle
    cdef float t2 = (-b - disc_sqrt) / double_a;
    # If neither of these is between 0 and 1, then the line segment
    # misses the circle (but would hit it if extended)

    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
        return None, None

    cdef vector2d i1 =  addcomponents(p1, scalevector2d(t1, &v));
    cdef vector2d i2 =  addcomponents(p1, scalevector2d(t2, &v));

    cdef vector2d intersection;
    if distance_to(p1, i1) > distance_to(p1, i2):
        vecinit(&intersection, i2.x, i2.y)
    else:
        vecinit(&intersection, i1.x, i1.y)

    cdef vector2d vector = subcomponents(q, intersection)
    cdef float dist1 = distance_to(intersection, p2);   # scalar distance between intersection and p2
    cdef float dist2 = distance_to(p1, p2);             # scalar distance between p1 and p2
    cdef float ratio;

    if dist1==0.0:
        ratio = 1.0
    else:
        ratio = dist2 / dist1  # ratio

    cdef vector2d collision = addcomponents(p1, scalevector2d(ratio, &vector));

    return vector, collision

