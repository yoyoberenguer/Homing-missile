###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8

# CYTHON IS REQUIRED
import math
import pygame

# TODO PYGAME SURFACE COPY IS VERY SLOW
# TODO CREATE METHOD TO KNOW IF THE MIXER IS INIT
# TODO CIMPORT
from MissileParticleFx import MParticleFX


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
    from pygame import Rect, transform
except ImportError:
    raise ImportError("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")

try:
   from Sprites cimport Sprite
   from Sprites import Group
except ImportError:
    raise ImportError("\nSprites.pyd missing!.Build the project first.")

from copy import deepcopy

from libc.stdlib cimport abs
from libc.math cimport cos, sin, atan2, sqrt, round


cdef extern from 'vector.c':

    struct vector2d:
       float x
       float y

    struct rect_p:
        int x
        int y

    struct mla_pack:
        vector2d vector
        vector2d collision


    cdef float M_PI
    cdef float M_PI2
    cdef float RAD_TO_DEG
    cdef float DEG_TO_RAD
    void vecinit(vector2d *v, float x, float y)nogil
    float vlength(vector2d *v)nogil
    void mulv_inplace(vector2d *v1, vector2d v2)nogil
    void scale_inplace(float c, vector2d *v)nogil
    vector2d addcomponents(vector2d v1, vector2d v2)nogil
    vector2d subcomponents(vector2d v1, vector2d v2)nogil
    vector2d scalevector2d(float c, vector2d *v)nogil
    float distance_to(vector2d v1, vector2d v2)nogil
    float dot(vector2d *v1, vector2d *v2)nogil
    float randRangeFloat(float lower, float upper)nogil
    int randRange(int lower, int upper)nogil


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class WeaponFeatures(Sprite):
    """
    WEAPON STRUCTURE
    """
    def __init__(self, group_, dict features_):
        """
        :param group_: Sprite Group(s)
        :param features_: Weapon settings (see XML file for more details)
        """
        Sprite.__init__(self, group_)

        for key, val in PyDict_Items(features_):
            PyDict_SetItem(self.__dict__, key, val)

    cpdef dict show_attributes(self):
        """
        SHOW ALL THE CLASS ATTRIBUTES THAT INHERIT FROM WEAPONFEATURES  
        :return: 
        """
        return self.__dict__


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class ExtraAttributes(object):

    cdef dict __dict__

    def __init__(self, dict settings_):
        for key, val in PyDict_Items(settings_):
            PyDict_SetItem(self.__dict__, key, val)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef inline int get_angle(rect_p target_centre, rect_p missile_centre)nogil:
        """
        RETURN THE ANGLE IN RADIANS BETWEEN THE MISSILE AND THE TARGET
         
        :return: integer;  
        """
        cdef int dx = target_centre.x - missile_centre.x
        cdef int dy = target_centre.y - missile_centre.y
        return -<int>((RAD_TO_DEG * atan2(dy, dx)) % 360)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef inline vector2d get_vector(int heading_, float magnitude_)nogil:
    """
    DETERMINE THE MISSILE VECTOR DIRECTION
    SHORTEST DISTANCE IN ORDER TO HIT THE TARGET 
    :return: vector2d 
    """
    # TODO TRANSFORM ANGLE TO RAD
    cdef float angle_radian = DEG_TO_RAD * heading_
    cdef vector2d vec
    vecinit(&vec, cos(angle_radian), -sin(angle_radian))
    scale_inplace(magnitude_, &vec)
    return vec



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(False)
cdef rot_center(dict rotate_buffer_, int angle_, int rect_centre_x, int rect_centre_y):
    """
    ROTATE/ALIGN THE MISSILE TO THE TRAJECTORY 
    THIS METHOD USE A BUFFER TO RECORD ON THE FLY TEXTURE TRANSFORMATION SUCH
    AS ROTATION. IT LOOKS INTO A BUFFER AND IF THE VALUE IS NONE, IT ASSUME 
    THAT THE TEXTURE HAS NOT BE TRANSFORMED. 
    THIS METHOD INCREASE THE OVERALL PERFORMANCES SINCE IT LOOKS INSIDE A BUFFER.
    PERFORMANCES INCREASE IN FUNCTION TO THE TEXTURE SIZE.
    THE LARGEST THE IMAGE THE HIGHEST THE PERFORMANCES COMPARE TO THE UN-BUFFERED VERSION. 
    THE FULL BUFFERED VERSION IS DEFINITELY THE FASTEST METHOD BUT UN-NECESSARY SINCE 
    THE TEXTURE USED FOR THE MISSILE IS RELATIVELY SMALL. HOPE TO YOU IF YOU 
    WANT TO CREATE A BUFFER WITH 360 ROTATED IMAGES INDEXED FROM 0 TO 360 DEGREES. 
    
    :param rotate_buffer_: Buffer containing sprite rotations (0 to 360)
    :param image_: pygame.Surface; Sprite image
    :param angle_: integer; Angle between missile and target
    :param rect_centre_x : integer; rect centre x 
    :param rect_centre_y : integer; rect centre y
    :return: Tuple; Return new rotated image and adjusted pygame Rect
    """
    cdef int zero_to_360 = angle_ % 360
    try:
        new_image, rect = rotate_buffer_[zero_to_360]
    except IndexError:
        # TODO
        ...
    return new_image, new_image.get_rect(center=(rect_centre_x, rect_centre_y))


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef inline int missile_guidance(
        int predictive_angle, int heading,
        int max_rotation, int angle)nogil:
    """
    RETURN THE OPTIMIZED ANGLE A MISSILE NEEDS TO FOLLOW IN ORDER TO HIT A TARGET QUICKER.
    THE MISSILE EFFICIENCY IS LIMITED WITH THE VARIABLE max_rotation ALLOWING THE MISSILE 
    TO TURN A CERTAIN AMOUNT OF DEGREES EACH FRAMES. 
    THIS FEATURES BRINGS A BIT MORE REALISM TO THE MISSILE TRAJECTORY.
    
    :param predictive_angle: integer; Predictive angle in degrees. 
    :param heading: integer; Actual missile heading in degrees
    :param max_rotation: The maximum angle in degrees the missile can turn each frames (virage)
    :param angle: integer; self.angle correspond to the real missile angle (taking account of the 
    image orientation)
    :return: Return an optimized angle in order to hit the target.
    """

    cdef int diff_angle = predictive_angle - heading
    cdef int clockwise, anticlockwise, sign, delta

    if diff_angle != 0:

        sign = 0
        clockwise = angle
        anticlockwise = 360 - clockwise
        # EQUIDISTANT, CHOOSE A DIRECTION
        if anticlockwise == clockwise:
            sign = randRange(-1, 1)
            if sign == 0:
                sign = 1
        # EQUIDISTANT 0 % 360 DEGREES SAME ANGLE.
        elif abs(anticlockwise - clockwise) == 360:
            sign = 0
        # ANTICLOCKWISE IS SHORTEST ANGULAR SPRITE_ORIENTATION
        elif anticlockwise < clockwise:
            sign = -1
        elif anticlockwise > clockwise:
            sign = +1

        delta = diff_angle % 360
        if abs(delta) - abs(max_rotation * sign) >= 1:
            heading += (max_rotation * sign)
        else:
            heading += delta
    return heading


cdef vector2d get_line_coefficient(float vx, float vy, float posx, float posy)nogil:
    """
    RETURN LINE COEFFICIENTS M, K
    LINE SEGMENT CAN BE WRITTEN P1 + T(P2 - P1) WHERE P2 - P1 IS A VECTOR

    :return: returns line coefficients m and k
    """


    # CALCULATE REGRESSION COEFFICIENT (SLOPE) AND SLOPE-INTERCEPT
    # OF A LINE (Y = MX + K OR Y = MX - K) FROM A GIVEN DIRECTION
    # AND VECTOR POSITION (X, Y).
    # M = ΔY/ΔX AND K = ΔY - M.X

    # CHECK IF THE VECTOR IS NULL,
    cdef float vector_length = sqrt(vx * vx + vy * vy)
    cdef float m, k
    cdef vector2d point2, mk
    if vector_length == 0.0:
        vecinit(&mk, 0.0, 0.0)
        return mk
    else:
        if vx != 0.0:
            m = vy / vx if vx != 0.0 else 0.0
        # NEXT POINT AFTER VECTOR INCREMENT
        vecinit(&point2, vx + posx, vy + posy)
        k = point2.y - m * point2.x
    # (Y = MX + K OR Y = MX - K)
    # NOTE: -Y = -MX -K (HEIGHT-AXIS IS INVERTED)
    vecinit(&mk, m, k)
    return mk

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class HomingMissile(WeaponFeatures):
    """
    PURE PURSUIT ALGORITHM

    Guided ballistic missile :
        This missile adjust its direction by small incremental steps always aiming toward
        the target position. This missile has a an on-board fuel tank limiting its maximal
        velocity and flying distance. It can be shot in any direction from the player position and
        fly outside the display before heading back to the playable area in order to hit the target.

        The propulsion engine can be trigger at a later stage using the variable propulsion.
        A launch offset can be added to simulate a launch under the aircraft wings.

        If the target is destroyed before the missile collision, it will resume its course
        to the latest calculated vector direction (prior target explosion)
    """
    cdef:
        object gl
        float magnitude, timing, dt, timer, c
        bint ignition
        int layer, heading, angle, bingo, _blend, start
        long long int _id

    def __init__(self,
                 gl_,
                 group_,
                 weapon_features_,
                 extra_attributes,
                 float timing_=60,
                 int layer_=-2,
                 int _blend=0):
        """
        :param gl_      : Contains all the global variables/constants
        :param group_   : Sprite group; Determine the group(s) holding the sprite. The sprite is consider alive
                          if it belongs to a group.
        :param weapon_features_: Contains all the missile settings/parameters
        :param extra_attributes: Extra attributes to load e.g
                                 ExtraAttributes({'target': target,
                                                 'shoot_angle': -90,
                                                 'ignition': True,
                                                 'offset': (-25, 10)})
        :param timing_ : float; Refresh rate is 15ms (Method update is still being called every frames but
                         changes are allowed every 15ms by the function (use of a timing constant self.dt
                         to determine if the cumulative time is over the threshold.
                         Variable self.dt is set to zero approximately every 15ms
        :param layer_  : integer; Default value is level -2. The missile sprite will always be shown on the top of
                         other sub-sprites (below level -2), but overcast by sprite layer layers >-1 .
        """

        WeaponFeatures.__init__(self, group_, weapon_features_)

        self.gl = gl_
        # VECTOR MAGNITUDE (float)
        self.magnitude = self.velocity.length()

        self.timing = 1000.0 / timing_
        self.dt = 0

        if gl_.MAX_FPS > timing_:
            self.timer = self.timing
        else:
            self.timer = 0.0


        # MISSILE TARGET INSTANCE
        self.main_target = extra_attributes.target
        self.target = extra_attributes.target
        self.target_rect = extra_attributes.target.rect

        # TODO PYGAME SURFACE COPY IS VERY SLOW
        self.image_copy = self.image.copy()
        # SPRITE IMAGE AND RECT
        self.rect = self.image.get_rect(midbottom=gl_.PLAYER.rect.center)

        # SET THE IGNITION DELAY IF ANY
        # Missile engine and exhaust particles will start after n seconds
        self.ignition = extra_attributes.ignition

        if self.ignition:
            virtual_group = Group()
            self.dummy_target = Sprite()
            self.dummy_target.rect = self.target_rect.copy()
            self.dummy_target.rect.center = (self.rect.centerx, self.rect.centery - 100)
            virtual_group.add(self.dummy_target)
            self.target = self.dummy_target

        # SET THE SPRITE LAYER
        self.layer  = layer_

        # DISPLAY SIZE IN PYGAME RECT
        self.screenrect  = gl_.SCREENRECT
        # MISSILE HEADING
        self.heading     = deepcopy(extra_attributes.shoot_angle)
        # PHASE SHIFT
        self.angle       = self.heading - self.sprite_orientation

        # INIT RECT SIZE AND ADJUST IMAGE
        self.image, self.rect = rot_center(self.sprite_rotozoom,
            self.angle, self.rect.centerx, self.rect.centery)

        # ADD OFFSET TO MISSILE POSITION
        if extra_attributes.offset is not None:
            if PyObject_IsInstance(extra_attributes.offset, tuple):
                self.rect.centerx += extra_attributes.offset[0]
                self.rect.centery += extra_attributes.offset[1]

        # EXHAUST COORDINATES
        self.exhaust_abs_position = Vector2(
            self.rect.midbottom[0] - self.rect.centerx,
            self.rect.midbottom[1] - self.rect.centery)

        # BINGO TIME (MAXIMUM FUEL TANK VALUE)
        # WHEN THE TANK IS EMPTY, THE MISSILE CANNOT TURN
        self.bingo = randRange(self.bingo_range[0], self.bingo_range[1])
        self._id = id(self)

        if gl_.MIXER_EXPLOSION is not None and \
            gl_.MIXER_PLAYER is not None:
                self.sound_fx()

        # DETERMINE THE TRAJECTORY VECTOR
        cdef vector2d vec
        vec = get_vector(self.heading, self.magnitude)
        self.velocity = Vector2(vec.x, vec.y)

        # FRAME TIMESTAMP
        self.start = gl_.FRAME

        # MISSILE START ITS PROPULSION SYSTEM AFTER X FRAMES DEPENDS ON FPS
        self.c = (1000.0 / 60.0) * 25.0

        self._blend = _blend

    cdef void sound_fx(self):
        """
        PLAY THE MISSILE SOUND USING THE MIXER <MIXER_EXPLOSION>
        :return: None 
        """
        mixer = self.gl.MIXER_EXPLOSION
        cdef _id = self._id
        if not any(mixer.get_identical_id(_id)):
            mixer.play(
                sound_=self.propulsion_sound_fx,
                loop_=0, priority_=0,
                volume_=self.gl.SOUND_LEVEL,
                fade_out_ms=0, panning_=True,
                name_='MISSILE FLIGHT',
                x_=self.rect.centerx, object_id_=_id)

    cdef void sound_fx_stop(self):
        """
        STOP THE SOUND BEING PLAYED BY THE MIXER
        :return: None 
        """
        mixer = self.gl.MIXER_EXPLOSION
        if mixer is not None:
            mixer.stop_object(self._id)

    cpdef location(self):
        """
        RETURN THE MISSILE POSITION (TUPLE VALUES) 
        """
        return self.rect.center


    cdef void hit(self):
        """ 
        THE MISSILE HIT THE TARGET OR GOT HIT
        KILL THE SPRITE.
        """
        self.sound_fx_stop()
        self.kill()

    cpdef update(self, args=None):
        """
        UPDATE THE MISSILE POSITION AND CONTROL PARTICLES EFFECT
        METHOD CALLED EVERY FRAMES FROM THE MAIN LOOP.
        
        :param args: Default None; 
        :return: None
        """
        cdef:
            target = self.target
            int max_rotation = self.max_rotation,
            int sprite_orientation = self.sprite_orientation
            int gl_frame = self.gl.FRAME
            rect_center = Vector2(self.rect.center)
            bint ignition = self.ignition
            int start = self.start, layer = self.layer
            velocity = self.velocity
            exhaust_abs_position = self.exhaust_abs_position
            dict missile_trail_fx = self.missile_trail_fx
            int missile_trail_fx_blend = self.missile_trail_fx_blend
            int heading = self.heading
            float time_passed_seconds = self.gl.TIME_PASSED_SECONDS
            float timer = self.timer
            float dt = self.dt
            float timing = self.timing, c = self.c / time_passed_seconds
            gl = self.gl
            int rotation_degrees
            vector2d vec
            int t_
            bint compiled_logic

        cdef rect_p target_c, rect_c

        if self.dt >= timer:


            t_ = gl_frame - self.start
            compiled_logic = t_ > c

            if target is not None and \
                target.alive() and self.bingo > 0:
                self.bingo -= 1

                target_c.x = target.rect.centerx
                target_c.y = target.rect.centery
                rect_c.x   = rect_center.x
                rect_c.y   = rect_center.y
                rotation_degrees = get_angle(target_c, rect_c)

                self.angle = rotation_degrees - heading
                self.angle %= 360
                heading = missile_guidance(rotation_degrees, heading, max_rotation, self.angle)
                self.heading = heading

                self.image, self.rect = rot_center(self.sprite_rotozoom,
                    heading - sprite_orientation, self.rect.centerx, self.rect.centery)

                vec = get_vector(heading, self.magnitude)
                velocity = Vector2(vec.x, vec.y)

                if ignition:
                    if compiled_logic:
                        self.target = self.main_target
                        self.dummy_target.kill()
                        MParticleFX(gl, rect_center, velocity, layer,
                            heading, exhaust_abs_position, missile_trail_fx,
                                    missile_trail_fx_blend, 60.0)

                else:
                    MParticleFX(gl, rect_center, velocity, layer,
                        heading, exhaust_abs_position, missile_trail_fx,
                                missile_trail_fx_blend, 60.0)

                rect_center += velocity
                self.rect.center = (rect_center.x, rect_center.y)

            # MISSILE IS BINGO
            # OR TARGET IS KILLED
            # MISSILE CONTINUE ITS COURSE (LINEAR TRAJECTORY)
            else:
                # IF THE TARGET IS DESTROYED THE MISSILE WILL
                # STILL HAVE FUEL IN ITS TANK.
                if self.bingo > 0:
                    if gl_frame - start > c:
                        MParticleFX(gl, rect_center, velocity, layer,
                            heading, exhaust_abs_position, missile_trail_fx,
                                    missile_trail_fx_blend, 60)
                self.bingo -= 1

                rect_center += velocity
                self.rect.center = (rect_center.x, rect_center.y)

            self.velocity = velocity
            dt = 0.0
        else:
            dt += time_passed_seconds
        self.dt = dt

        # SHUTDOWN THE MISSILE IF IT GOES OUTSIDE DISPLAYS BOUNDARIES
        if not self.screenrect.colliderect(self.rect):
            self.sound_fx_stop()
            self.kill()


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef vector2d fast_lead_collision(
        float p1_x, float p1_y,
        float p2_x, float p2_y,
        float v1_x, float v1_y,
        float v2_x, float v2_y)nogil:

    """
    DETERMINE THE COLLISION MISSILE LEAD ANGLE.
    THIS METHOD RETURNS ONLY THE VECTOR
    
    :param p1_x: float; p1 component x 
    :param p1_y: float; p1 component y
    :param p2_x: float; p2 component x 
    :param p2_y: float; p2 component y
    :param v1_x: float; v1 component x
    :param v1_y: float; v1 component y
    :param v2_x: float; v2 component x
    :param v2_y: float; v2 component y
    :return: Returns missile vector 
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

    cdef vector2d p1, p2, v1, v2, vector
    vecinit(&p1, p1_x, p1_y)
    vecinit(&p2, p2_x, p2_y)
    vecinit(&v1, v1_x, v1_y)
    vecinit(&v2, v2_x, v2_y)

    cdef:
        vector2d v = subcomponents(p2, p1)
        vector2d q = addcomponents(p2, v2)
        float r = vlength(&v1)
        float a = dot(&v, &v)
        float double_a = 2 * a

    if a == 0:
        vecinit(&vector, 0.0, 0.0)
        return vector

    cdef:
        vector2d tmp = subcomponents(p1, q)
        float b = 2 * dot(&v, &tmp)
        float c = (dot(&p1, &p1) + dot(&q, &q)) - (2 * dot(&p1, &q)) - (r * r)
        float disc = (b * b) - (double_a * 2 * c)


    if disc < 0:
        vecinit(&vector, 0.0, 0.0)
        return vector

    cdef:
        float disc_sqrt = <float>sqrt(disc)
        # FIRST INTERSECTION BETWEEN THE LINE AND CIRCLE
        float t1 = (-b + disc_sqrt) / double_a
        # SECOND INTERSECTION BETWEEN THE LINE AND CIRCLE
        float t2 = (-b - disc_sqrt) / double_a

    # IF NEITHER OF THESE IS BETWEEN 0 AND 1, THEN THE LINE SEGMENT
    # MISSES THE CIRCLE (BUT WOULD HIT IT IF EXTENDED)

    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
        vecinit(&vector, 0.0, 0.0)
        return vector

    cdef:
        vector2d i1 =  addcomponents(p1, scalevector2d(t1, &v))
        vector2d i2 =  addcomponents(p1, scalevector2d(t2, &v))
        vector2d intersection

    if distance_to(p1, i1) > distance_to(p1, i2):
        vecinit(&intersection, i2.x, i2.y)
    else:
        vecinit(&intersection, i1.x, i1.y)

    cdef:
        cdef vector2d vec = subcomponents(q, intersection)

    return vec


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef mla_pack lead_collision(
        float p1_x, float p1_y,
        float p2_x, float p2_y,
        float v1_x, float v1_y,
        float v2_x, float v2_y)nogil:

    """
    DETERMINE THE COLLISION MISSILE LEAD ANGLE
    THIS METHOD RETURN A STRUCTURE CONTAINING BOTH VECTOR AND COLLISION POINT 
    
    :param p1_x: float; p1 component x 
    :param p1_y: float; p1 component y
    :param p2_x: float; p2 component x 
    :param p2_y: float; p2 component y
    :param v1_x: float; v1 component x
    :param v1_y: float; v1 component y
    :param v2_x: float; v2 component x
    :param v2_y: float; v2 component y
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

    cdef vector2d p1, p2, v1, v2
    vecinit(&p1, p1_x, p1_y)
    vecinit(&p2, p2_x, p2_y)
    vecinit(&v1, v1_x, v1_y)
    vecinit(&v2, v2_x, v2_y)


    cdef:
        vector2d v = subcomponents(p2, p1)
        vector2d q = addcomponents(p2, v2)
        float r = vlength(&v1)
        float a = dot(&v, &v)
        float double_a = 2 * a
        mla_pack pack

    if a == 0:
        vecinit(&pack.vector, 0.0, 0.0)
        vecinit(&pack.collision, 0.0, 0.0)
        return pack

    cdef:
        vector2d tmp = subcomponents(p1, q)
        float b = 2 * dot(&v, &tmp)
        float c = (dot(&p1, &p1) + dot(&q, &q)) - (2 * dot(&p1, &q)) - (r * r)
        float disc = (b * b) - (double_a * 2 * c)


    if disc < 0:
        vecinit(&pack.vector, 0.0, 0.0)
        vecinit(&pack.collision, 0.0, 0.0)
        return pack

    cdef:
        float disc_sqrt = <float>sqrt(disc)
        # FIRST INTERSECTION BETWEEN THE LINE AND CIRCLE
        float t1 = (-b + disc_sqrt) / double_a
        # SECOND INTERSECTION BETWEEN THE LINE AND CIRCLE
        float t2 = (-b - disc_sqrt) / double_a

    # IF NEITHER OF THESE IS BETWEEN 0 AND 1, THEN THE LINE SEGMENT
    # MISSES THE CIRCLE (BUT WOULD HIT IT IF EXTENDED)

    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
        vecinit(&pack.vector, 0.0, 0.0)
        vecinit(&pack.collision, 0.0, 0.0)
        return pack

    cdef:
        vector2d i1 =  addcomponents(p1, scalevector2d(t1, &v))
        vector2d i2 =  addcomponents(p1, scalevector2d(t2, &v))
        vector2d intersection;

    if distance_to(p1, i1) > distance_to(p1, i2):
        vecinit(&intersection, i2.x, i2.y)
    else:
        vecinit(&intersection, i1.x, i1.y)

    cdef:
        vector2d vector = subcomponents(q, intersection)
        float dist1 = distance_to(intersection, p2)   # SCALAR DISTANCE BETWEEN INTERSECTION AND P2
        float dist2 = distance_to(p1, p2)             # SCALAR DISTANCE BETWEEN P1 AND P2
        float ratio

    if dist1==0.0:
        ratio = 1.0
    else:
        ratio = dist2 / dist1  # ratio

    cdef vector2d collision = addcomponents(p1, scalevector2d(ratio, &vector))

    vecinit(&pack.vector, vector.x, vector.y)
    vecinit(&pack.collision, collision.x, collision.y)
    return pack

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef class InterceptMissile(WeaponFeatures):
    """
    LEAD COLLISION (proportional navigation) more effective, follow an optimal path
        Intercept theorem (Thales basic proportionality theorem)
        https://www.youtube.com/watch?v=T2fPKUfmnKo
        https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm

    """

    cdef:
        object gl,
        float magnitude, timing, dt, timer, c
        bint ignition
        int layer, heading, angle, bingo, start, _blend
        long long int _id


    def __init__(self,
                 gl_,
                 group_,
                 weapon_features_,
                 extra_attributes,
                 float timing_=60.0,
                 int layer_=-2,
                 _blend=0):
        """
        :param gl_      : Contains all the global variables/constants
        :param group_   : Sprite group; Determine the group(s) holding the sprite. The sprite is consider alive
                          if it belongs to a group.
        :param weapon_features_: Contains all the missile settings/parameters
        :param extra_attributes: Extra attributes to load e.g
                                 ExtraAttributes({'target': target,
                                                 'shoot_angle': -90,
                                                 'ignition': True,
                                                 'offset': (-25, 10)})
        :param timing_ : float; Refresh rate is 15ms (Method update is still being called every frames but
                         changes are allowed every 15ms by the function (use of a timing constant self.dt
                         to determine if the cumulative time is over the threshold.
                         Variable self.dt is set to zero approximately every 15ms
        :param layer_  : integer; Default value is level -2. The missile sprite will always be shown on the top of
                         other sub-sprites (below level -2), but overcast by sprite layer layers >-1 .
        """

        WeaponFeatures.__init__(self, group_, weapon_features_)

        self.gl = gl_
        # VECTOR MAGNITUDE (float)
        self.magnitude = self.velocity.length()

        # MISSILE TARGET INSTANCE
        self.main_target = extra_attributes.target
        self.target = extra_attributes.target
        self.target_rect = extra_attributes.target.rect

        self.image_copy = self.image.copy()
        # SPRITE IMAGE AND RECT
        self.rect = self.image.get_rect(midbottom=gl_.PLAYER.rect.center)

        # SET THE IGNITION DELAY IF ANY
        # Missile engine and exhaust particles will start after n seconds
        self.ignition = extra_attributes.ignition

        if self.ignition:
            virtual_group = Group()
            self.dummy_target = Sprite()
            self.dummy_target.rect = self.target_rect.copy()
            self.dummy_target.rect.center = (self.rect.centerx, self.rect.centery - 100)
            self.dummy_target.vector = Vector2(0, 0)
            virtual_group.add(self.dummy_target)
            self.target = self.dummy_target

        # SET THE SPRITE LAYER
        self.layer  = layer_

        self.timing = 1000.0 / timing_
        self.dt = 0

        if gl_.MAX_FPS > timing_:
            self.timer = self.timing
        else:
            self.timer = 0.0

        # DISPLAY SIZE IN PYGAME RECT
        self.screenrect  = gl_.SCREENRECT
        # MISSILE HEADING
        self.heading     = deepcopy(extra_attributes.shoot_angle)
        # PHASE SHIFT
        self.angle       = self.heading - self.sprite_orientation

        # INIT RECT SIZE AND ADJUST IMAGE
        self.image, self.rect = rot_center(self.sprite_rotozoom,
            self.angle, self.rect.centerx, self.rect.centery)

        # ADD OFFSET TO MISSILE POSITION
        if extra_attributes.offset is not None:
            if PyObject_IsInstance(extra_attributes.offset, tuple):
                self.rect.centerx += extra_attributes.offset[0]
                self.rect.centery += extra_attributes.offset[1]

        # EXHAUST COORDINATES
        self.exhaust_abs_position = Vector2(
            self.rect.midbottom[0] - self.rect.centerx,
            self.rect.midbottom[1] - self.rect.centery)

        # BINGO TIME (MAXIMUM FUEL TANK VALUE)
        # WHEN THE TANK IS EMPTY, THE MISSILE CANNOT TURN
        self.bingo = randRange(self.bingo_range[0], self.bingo_range[1])
        self._id = id(self)

        if gl_.MIXER_EXPLOSION is not None and \
            gl_.MIXER_PLAYER is not None:
                self.sound_fx()

        # DETERMINE THE TRAJECTORY VECTOR
        vec = get_vector(self.heading, self.magnitude)
        self.velocity = Vector2(vec.x, vec.y)

        # FRAME TIMESTAMP
        self.start = gl_.FRAME

        # MISSILE START ITS PROPULSION SYSTEM AFTER X FRAMES DEPENDS ON FPS
        self.c = self.timing * 25.0

        self._blend = _blend

    cdef void sound_fx(self):
        """
        PLAY THE MISSILE SOUND USING THE MIXER <MIXER_EXPLOSION>
        :return: None 
        """
        mixer = self.gl.MIXER_EXPLOSION
        cdef _id = self._id
        if not any(mixer.get_identical_id(_id)):
            mixer.play(
                sound_=self.propulsion_sound_fx,
                loop_=0, priority_=0,
                volume_=self.gl.SOUND_LEVEL,
                fade_out_ms=0, panning_=True,
                name_='MISSILE FLIGHT',
                x_=self.rect.centerx, object_id_=_id)

    cdef void sound_fx_stop(self):
        """
        STOP THE SOUND BEING PLAYED BY THE MIXER
        :return: None 
        """
        mixer = self.gl.MIXER_EXPLOSION
        if mixer is not None:
            mixer.stop_object(self._id)

    cpdef location(self):
        """
        RETURN THE MISSILE POSITION (TUPLE VALUES) 
        """
        return self.rect.center

    cdef void hit(self):
        """ 
        THE MISSILE HIT THE TARGET OR GOT HIT
        KILL THE SPRITE.
        """
        self.sound_fx_stop()
        self.kill()

    cpdef update(self, args=None):
        """
        UPDATE THE MISSILE POSITION AND CONTROL PARTICLES EFFECT
        METHOD CALLED EVERY FRAMES FROM THE MAIN LOOP.
        
        :param args: Default None; 
        :return: None
        """
        cdef:
            float dt = self.dt
            target = self.target
            target_rect = target.rect
            rect_center = self.rect.center
            int heading = self.heading
            float magnitude = self.magnitude
            float rad_angle = 0.0, angle = self.angle
            velocity = self.velocity
            gl = self.gl
            int gl_frame = gl.FRAME
            float gl_time_passed_seconds = self.gl.TIME_PASSED_SECONDS
            float timing = self.timing, timer = self.timer
            int layer = self.layer
            exhaust = self.exhaust_abs_position
            missile_trail = self.missile_trail_fx
            missile_trail_fx_blend = self.missile_trail_fx_blend
            int t_
            bint compiled_logic = False
            max_rotation = self.max_rotation
            # mla_pack pack;
            vector2d vector
            float c = self.c / gl_time_passed_seconds


        if self.dt >= timer:

            t_ = gl_frame - self.start
            compiled_logic = t_ > c

            if target is not None and \
                target.alive() and self.bingo > 0:
                self.bingo -= 1

                rad_angle = DEG_TO_RAD * heading

                vector = fast_lead_collision(
                    rect_center[0], rect_center[1], target_rect.centerx, target_rect.centery,
                    cos(rad_angle) * magnitude, sin(rad_angle) * magnitude, target.vector.x, target.vector.y)

                # vector = Vector2(pack.vector.x, pack.vector.y)

                if vector is not None:
                    predictive_angle = <int>(-RAD_TO_DEG * atan2(vector.y, vector.x))
                    self.angle = predictive_angle - heading
                    self.angle %= 360
                    heading = missile_guidance(predictive_angle, heading, max_rotation, self.angle)
                    self.heading = heading
                    rad_angle = DEG_TO_RAD * heading
                    self.velocity = Vector2(cos(rad_angle) * magnitude, -sin(rad_angle) * magnitude)
                    velocity = self.velocity

                self.image, self.rect = rot_center(self.sprite_rotozoom,
                    heading - self.sprite_orientation, self.rect.centerx, self.rect.centery)

                if self.ignition:
                    if compiled_logic:
                        self.target = self.main_target
                        self.dummy_target.kill()
                        MParticleFX(gl, Vector2(rect_center), velocity, layer,
                            heading, exhaust, missile_trail, missile_trail_fx_blend, 15.0)

                else:
                    MParticleFX(gl, Vector2(rect_center), velocity, layer,
                        heading, exhaust, missile_trail, missile_trail_fx_blend, 15.0)

                self.rect.center += velocity


            # MISSILE IS BINGO
            # OR TARGET IS KILLED
            # MISSILE CONTINUE ITS COURSE (LINEAR TRAJECTORY)
            else:
                # IF THE TARGET IS DESTROYED THE MISSILE WILL
                # STILL HAVE FUEL IN ITS TANK.
                if self.bingo > 0:
                    if compiled_logic:
                        MParticleFX(gl, Vector2(rect_center), velocity, layer,
                            heading, exhaust, missile_trail, missile_trail_fx_blend, 15.0)
                self.bingo -= 1

                self.rect.center += velocity

            dt = 0
        else:
            dt += gl_time_passed_seconds

        self.dt = dt
        # SHUTDOWN THE MISSILE IF IT GOES OUTSIDE DISPLAYS BOUNDARIES
        if not self.screenrect.colliderect(self.rect):
            self.sound_fx_stop()
            self.kill()



cdef class AdaptiveMissile(WeaponFeatures):
    """
        PURE PURSUIT ALGORITHM
        HOMING MISSILE (GUIDED MISSILE) WITH AUTOMATIC GRADUAL ACCELERATION/DECELERATION.
        THIS PROJECTILE IS CAPABLE OF VERY SHARP ANGLE.
        IT CAN ACCELERATE IN STRAIGHT TRAJECTORY AND DECELERATE IN THE TURNS TO INCREASE MANOEUVRABILITY

    """
    cdef:
        object gl,
        float magnitude, min_magnitude, timing, dt, timer, c
        bint ignition
        int layer, heading, angle, bingo, start, _blend
        long long int _id

    def __init__(self,
                 gl_,
                 group_,
                 weapon_features_,
                 extra_attributes,
                 float timing_=60,
                 int layer_=-2,
                 _blend=0):

        WeaponFeatures.__init__(self, group_, weapon_features_)

        self.gl = gl_
        # VECTOR MAGNITUDE (float)
        self.magnitude = self.velocity.length()
        self.min_magnitude = self.magnitude

        self.timing = 1000.0 / timing_
        self.dt = 0

        if gl_.MAX_FPS > timing_:
            self.timer = self.timing
        else:
            self.timer = 0.0

        # MISSILE TARGET INSTANCE
        self.main_target = extra_attributes.target
        self.target = extra_attributes.target
        self.target_rect = extra_attributes.target.rect

        self.image_copy = self.image.copy()
        # SPRITE IMAGE AND RECT
        self.rect = self.image.get_rect(midbottom=gl_.PLAYER.rect.center)

        # SET THE IGNITION DELAY IF ANY
        # MISSILE ENGINE AND EXHAUST PARTICLES WILL START AFTER N SECONDS
        self.ignition = extra_attributes.ignition

        if self.ignition:
            virtual_group = Group()
            self.dummy_target = Sprite()
            self.dummy_target.rect = self.target_rect.copy()
            self.dummy_target.rect.center = (self.rect.centerx, self.rect.centery - 100)
            virtual_group.add(self.dummy_target)
            self.target = self.dummy_target

        # SET THE SPRITE LAYER
        self.layer  = layer_

        # DISPLAY SIZE IN PYGAME RECT
        self.screenrect  = gl_.SCREENRECT
        # MISSILE HEADING
        self.heading     = deepcopy(extra_attributes.shoot_angle)
        # PHASE SHIFT
        self.angle       = self.heading - self.sprite_orientation

        # INIT RECT SIZE AND ADJUST IMAGE
        self.image, self.rect = rot_center(self.sprite_rotozoom,
            self.angle, self.rect.centerx, self.rect.centery)

        # ADD OFFSET TO MISSILE POSITION
        if extra_attributes.offset is not None:
            if PyObject_IsInstance(extra_attributes.offset, tuple):
                self.rect.centerx += extra_attributes.offset[0]
                self.rect.centery += extra_attributes.offset[1]

        # EXHAUST COORDINATES
        self.exhaust_abs_position = Vector2(
            self.rect.midbottom[0] - self.rect.centerx,
            self.rect.midbottom[1] - self.rect.centery)

        # BINGO TIME (MAXIMUM FUEL TANK VALUE)
        # WHEN THE TANK IS EMPTY, THE MISSILE CANNOT TURN
        self.bingo = randRange(self.bingo_range[0], self.bingo_range[1])
        self._id = id(self)

        if gl_.MIXER_EXPLOSION is not None and \
            gl_.MIXER_PLAYER is not None:
                self.sound_fx()

        # DETERMINE THE TRAJECTORY VECTOR
        cdef vector2d vec
        vec = get_vector(self.heading, self.magnitude)
        self.velocity = Vector2(vec.x, vec.y)

        # FRAME TIMESTAMP
        self.start = gl_.FRAME

        # MISSILE START ITS PROPULSION SYSTEM AFTER X FRAMES DEPENDS ON FPS
        self.c = (1000.0 / 60.0) * 25.0

        self._blend = _blend

        self.adaptive_vector = []

    cdef void sound_fx(self):
        """
        PLAY THE MISSILE SOUND USING THE MIXER <MIXER_EXPLOSION>
        :return: None 
        """
        mixer = self.gl.MIXER_EXPLOSION
        cdef _id = self._id
        if not any(mixer.get_identical_id(_id)):
            mixer.play(
                sound_=self.propulsion_sound_fx,
                loop_=0, priority_=0,
                volume_=self.gl.SOUND_LEVEL,
                fade_out_ms=0, panning_=True,
                name_='MISSILE FLIGHT',
                x_=self.rect.centerx, object_id_=_id)

    cdef void sound_fx_stop(self):
        """
        STOP THE SOUND BEING PLAYED BY THE MIXER
        :return: None 
        """
        mixer = self.gl.MIXER_EXPLOSION
        if mixer is not None:
            mixer.stop_object(self._id)

    cpdef location(self):
        """
        RETURN THE MISSILE POSITION (TUPLE VALUES) 
        """
        return self.rect.center

    cdef void hit(self):
        """ 
        THE MISSILE HIT THE TARGET OR GOT HIT
        KILL THE SPRITE.
        """
        self.sound_fx_stop()
        self.kill()

    cpdef update(self, args=None):
        """
        UPDATE THE MISSILE POSITION AND CONTROL PARTICLES EFFECT
        METHOD CALLED EVERY FRAMES FROM THE MAIN LOOP.
        
        :param args: Default None; 
        :return: None
        """
        cdef:
            target = self.target
            int max_rotation = self.max_rotation,
            int sprite_orientation = self.sprite_orientation
            image_copy = self.image_copy
            int gl_frame = self.gl.FRAME
            rect_center = Vector2(self.rect.center)
            bint ignition = self.ignition
            int start = self.start, layer = self.layer
            velocity = self.velocity
            exhaust_abs_position = self.exhaust_abs_position
            int time_passed_seconds = self.gl.TIME_PASSED_SECONDS
            missile_trail_fx = self.missile_trail_fx
            missile_trail_fx_blend = self.missile_trail_fx_blend
            int heading = self.heading
            float timing = self.timing, c = self.c / time_passed_seconds, timer = self.timer
            gl = self.gl
            int rotation_degrees
            float dt = self.dt
            vector2d vec, mk1, mk2, mk3
            int t_
            bint compiled_logic
            magnitude = self.magnitude

        cdef rect_p target_c, rect_c

        if dt > timer:

            t_ = gl_frame - self.start
            compiled_logic = t_ > c

            if target is not None and \
                target.alive() and self.bingo > 0:
                self.bingo -= 1

                target_c.x = target.rect.centerx
                target_c.y = target.rect.centery
                rect_c.x   = rect_center.x
                rect_c.y   = rect_center.y
                rotation_degrees = get_angle(target_c, rect_c)

                self.angle = rotation_degrees - heading
                self.angle %= 360
                heading = missile_guidance(rotation_degrees, heading, max_rotation, self.angle)
                self.heading = heading

                self.image, self.rect = rot_center(self.sprite_rotozoom,
                    heading - sprite_orientation, self.rect.centerx, self.rect.centery)

                vec = get_vector(heading, self.magnitude)
                velocity = Vector2(vec.x, vec.y)

                # BUILDING LIST
                if len(self.adaptive_vector) < 3:
                    self.adaptive_vector.append(velocity)

                # LIST HAS 3 VECTORS
                elif len(self.adaptive_vector) == 3:

                    try:
                        mk1 = get_line_coefficient(self.adaptive_vector[0].x, self.adaptive_vector[0].y,
                                                   self.adaptive_vector[1].x, self.adaptive_vector[1].y)
                        mk2 = get_line_coefficient(self.adaptive_vector[1].x, self.adaptive_vector[1].y,
                                                   self.adaptive_vector[2].x, self.adaptive_vector[2].y)

                        if round(mk1.x) == round(mk2.x):
                            self.magnitude += 0.5
                            self.magnitude = max(30.0, self.magnitude)

                        else:
                            self.magnitude -= 0.1
                            self.magnitude = min(self.min_magnitude, self.magnitude)

                        self.adaptive_vector.append(velocity)
                        self.adaptive_vector.pop(0)
                    except IndexError:
                        # IGNORE
                        ...

                # self.get_line_coefficient()

                if ignition:
                    if compiled_logic:
                        self.target = self.main_target
                        self.dummy_target.kill()
                        MParticleFX(gl, rect_center, velocity, layer,
                            heading, exhaust_abs_position, missile_trail_fx,
                                    missile_trail_fx_blend, 15.0)

                else:
                    MParticleFX(gl, rect_center, velocity, layer,
                        heading, exhaust_abs_position, missile_trail_fx,
                                missile_trail_fx_blend, 15.0)
                    MParticleFX(gl, rect_center, velocity, layer,
                        heading, exhaust_abs_position, missile_trail_fx,
                                missile_trail_fx_blend, 15.0)

                rect_center += velocity
                self.rect.center = (rect_center.x, rect_center.y)

            # MISSILE IS BINGO
            # OR TARGET IS KILLED
            # MISSILE CONTINUE ITS COURSE (LINEAR TRAJECTORY)
            else:
                # IF THE TARGET IS DESTROYED THE MISSILE WILL
                # STILL HAVE FUEL IN ITS TANK.
                if self.bingo > 0:
                    if gl_frame - start > c:
                        MParticleFX(gl, rect_center, velocity, layer,
                            heading, exhaust_abs_position, missile_trail_fx,
                                    missile_trail_fx_blend, 15.0)
                self.bingo -= 1

                rect_center += velocity
                self.rect.center = (rect_center.x, rect_center.y)

            dt = 0
        else:
            dt += time_passed_seconds

        self.dt = dt
        self.velocity = velocity
        # SHUTDOWN THE MISSILE IF IT GOES OUTSIDE DISPLAYS BOUNDARIES
        if not self.screenrect.colliderect(self.rect):
            self.sound_fx_stop()
            self.kill()

            # # NUCLEAR BOMB
            # else:
            #
            #     self.rect.center += self.speed
            #     self.pos = self.rect.center

            # # missile is going outside the display.
            # if not self.screenrect.contains(self.rect):
            #     if self.is_nuke:
            #         # Create a dummy target 400 pixels ahead of the spaceship
            #         # Virtual rectangle that will trigger a nuke explosion after colliding with it.
            #         # This sprite is passed into the group nuke_aiming_point(this group contains every
            #         # virtual rectangle)
            #         dummy_sprite = pygame.sprite.Sprite()
            #         dummy_sprite.rect = self.rect.copy()
            #         dummy_sprite.rect.center = (self.rect.centerx, self.rect.centery - 200)
            #         dummy_sprite.dummy = True
            #         dummy_sprite.name = self.gl_.PLAYER_NUMBER
            #         self.gl_.nuke_aiming_point.add(dummy_sprite)
            #     else:
            #         self.sound_fx_stop()
            #         self.kill()







