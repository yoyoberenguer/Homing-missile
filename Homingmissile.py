"""
				   GNU GENERAL PUBLIC LICENSE

					   Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>

 Everyone is permitted to copy and distribute verbatim copies

 of this license document, but changing it is not allowed.
 """

import pygame

class GL:
    SC_explosion = None
    SOUND_LEVEL = 1.0
    TIME_PASSED_SECONDS = None
    FRAME = 0
    SCREENRECT = None
    RATIO = pygame.math.Vector2(1, 1)

import random

SCREENRECT = pygame.Rect(0, 0, 800, 1024)
GL.SCREENRECT = SCREENRECT
pygame.display.init()
SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWSURFACE, 32)
GL.screen = SCREEN
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4095)
import math
from math import atan2, cos, sin, pi, degrees, radians
from MissileParticleFx import MissileParticleFx_improve, VERTEX_ARRAY_MP, missile_particles
from SoundServer import SoundControl
from pygame import freetype

DEG_TO_RAD = pi / 180
RAD_TO_DEG = 1 / DEG_TO_RAD
MAXFPS = 60


def missile_lead_angle(p1: pygame.math.Vector2,  # Start of vector1 position
                       p2: pygame.math.Vector2,  # start of vector2 position

                       v1: pygame.math.Vector2,  # Euclidean vector, vector projections representing the missile
                       # vector.
                       v2: pygame.math.Vector2):  # Euclidean vector, vector projections representing the target
    # vector.
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
    # todo check if v1 and v2 should be normalised
    v = p2 - p1
    q = p2 + v2  # circle centre
    r = v1.length()  # circle radius

    a = v.dot(v)
    if a == 0:
        return None, None, None

    b = 2 * v.dot(p1 - q)
    c = p1.dot(p1) + q.dot(q) - 2 * p1.dot(q) - r ** 2
    disc = b ** 2 - 4 * a * c

    if disc < 0:
        return None, None, None

    disc_sqrt = math.sqrt(disc)
    t1 = (-b + disc_sqrt) / (2 * a)  # first intersection between the line and circle
    t2 = (-b - disc_sqrt) / (2 * a)  # second intersection between the line and circle

    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
        return None, None, None

    i1 = p1 + t1 * v  # intersection 1 in the Cartesian plane
    i2 = p1 + t2 * v  # intersection 2 in the Cartesian plane

    # Determine the closest point from p1 (missile).
    if p1.distance_to(i1) > p1.distance_to(i2):
        intersection = i2
    else:
        intersection = i1

    vector = q - intersection
    angle = math.degrees(math.atan2(vector.y, vector.x))

    dist1 = intersection.distance_to(p2)  # scalar distance from p2 and intersection
    dist2 = p1.distance_to(p2)  # scalar distance between p1 and p2
    # todo div zero
    ratio = dist2 / dist1  # ratio

    collision = p1 + ratio * vector
    # parametric equation
    # p1 + t * vector

    return p1, vector, collision


class HomingMissile(pygame.sprite.Sprite):
    """
        PURE PURSUIT ALGORITHM
        Homing missile (guided missile) with automatic tracking path correction.
        The projectile is capable of very sharp angle to follow target.
        This missile will hit the target as long as the target speed is inferior to the missile speed.
        The missile has a fuel attribute lowering down the effectiveness range of the ballistic missile.
        This Missile class is reserved for the Player class.
        Sprite will be killed if it goes outside the screen limits (except for nuke missile).
    """
    containers = None
    images = None
    screenrect = None

    def __init__(self,
                 player_,  # Player class
                 target_,  # pygame.Rect for the target position
                 weapon_,  # Weapon class
                 gl_,  # global variable
                 offset_=None,  # Offset from the center
                 nuke_=False,  # Missile is a nuke when flag is raised True
                 shoot_angle_=90,  # missile aiming toward by default
                 timing_=15,  # Refreshing time default 33ms
                 propulsion_=False,  # missile propulsion delay True | False
                 layer_=-2):  # Layer used

        pygame.sprite.Sprite.__init__(self, self.containers)

        if layer_:
            if isinstance(gl_.All, pygame.sprite.LayeredUpdates):
                gl_.All.change_layer(self, layer_)

        # missile speed
        self.speed = pygame.math.Vector2(0, float(weapon_.velocity.y))  # missile speed vector
        self.magnitude = self.speed.length()  # missile speed magnitude
        self.rotation = 90  # missile orientation
        self.target = target_  # target to hit
        self.images_copy = self.images.copy()
        self.image = self.images_copy[0] if isinstance(self.images_copy, list) else self.images_copy
        self.offset = player_.center() if offset_ is None else offset_
        self.rect = self.image.get_rect(center=self.offset)
        self.pos = self.rect.center  # missile position (starting position)
        self.vector = pygame.math.Vector2()  # Keep for compatibility with external class
        self.weapon = weapon_  # Weapon instance (contains all the attributes)
        self.index = 0  # surface index

        # if nuke_ is True, missile is nuke type
        # else homing missile
        if nuke_:
            self.is_nuke = True
        else:
            self.is_nuke = False

        self.timing = timing_  # Refreshing time
        self.dt = 0  # Time constant
        self.gl_ = gl_  # Global variables
        self.player = player_  # player instance
        self.angle_degrees = 0
        self.layer_ = layer_
        self.bingo = random.randint(90, 110)  # random counter (quantity of fuel)
        self.propulsion = propulsion_  # True | False (delay propulsion)

        # Exhaust coordinates (absolute values from the center,
        # center of the object is the reference point for any transformation.
        self.exhaust_abs_position = pygame.math.Vector2(
            self.rect.midbottom[0] - self.rect.centerx, \
            self.rect.midbottom[1] - self.rect.centery)
        self.sound = weapon_.sound_effect  # extract sound fx
        self._id = id(self)
        self.start = self.gl_.FRAME  # Stating frame
        if self.gl_.SC_explosion is not None and \
                self.gl_.SC_spaceship is not None:
            self.sound_fx()  # play sound fx
        self.heading = shoot_angle_  # Mis
        self.angle_degrees = self.heading - self.rotation  # Angle value to pass to method rot_center.
        # correspond considering the bitmap orientation
        self.image, self.rect = self.rot_center(
            self.images_copy, self.angle_degrees, self.rect)  # Draw the missile and initialised the rectangle size

        # Apply 60FPS to the missile if MAXFPS is over 60fps
        if MAXFPS > 60:
            self.timing = 16.0
        else:
            self.timing = 0.0

    def sound_fx(self):
        """ Play sound fx using SC_spaceship sound server"""
        if not any(self.gl_.SC_spaceship.get_identical_id(self._id)):
            self.gl_.SC_spaceship.play(sound_=self.sound,
                                       loop_=False, priority_=0,
                                       volume_=self.gl_.SOUND_LEVEL,
                                       fade_out_ms=0, panning_=True,
                                       name_='MISSILE FLIGHT',
                                       x_=self.rect.centerx, object_id_=self._id)

    def sound_fx_stop(self):
        """ Stop missile sound fx """
        if self.gl_.SC_spaceship is not None:
            self.gl_.SC_spaceship.stop_object(self._id)

    @staticmethod
    def rot_center(image_: pygame.Surface, angle_, rect_) -> (pygame.Surface, pygame.Rect):
        """ rotate an image while keeping its center and size (only for symmetric surface)
            argument angle_ has to be in degres
        """
        new_image = pygame.transform.rotate(image_, angle_)
        return new_image, new_image.get_rect(center=rect_.center)

    def get_angle(self):
        """ Returns the angle  between the shooter and the target."""
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        # return angle (in degrees) difference between the missile and the target object
        return -int(degrees(atan2(dy, dx)) % 360)

    def get_vector(self, angle_rad):
        """ Determine the current direction vector according to the angle angle_rad (radians)"""
        # angle_rad must in radians
        self.speed.x = cos(angle_rad)
        self.speed.y = -sin(angle_rad)
        self.speed *= self.magnitude

    def location(self):
        return self.rect

    def center(self):
        return self.rect.center

    def update(self):

        if self.dt > self.timing:

            if not isinstance(self.target, pygame.Rect):

                # Returns True when the Sprite belongs to one or more Groups.
                if self.target is not None and self.target.alive() \
                        and self.player.alive() and self.bingo > 0:

                    self.bingo -= 1

                    self.angle_degrees = self.get_angle()
                    angle_rad = radians(self.angle_degrees)

                    # The missile sprite is oriented at 90 degrees
                    angle = self.angle_degrees - self.rotation

                    self.image, self.rect = self.rot_center(
                        self.images_copy[self.index] if
                        isinstance(self.images_copy, list) else self.images_copy,
                        angle, self.rect)

                    self.get_vector(angle_rad)

                    # Particle effect
                    # create the smoke trail from the missile exhaust
                    if self.propulsion:
                        # 25 frames for a refreshing rate of 16ms.
                        # ! Change value if refreshing rate is changing.
                        if self.gl_.FRAME - self.start > 25:

                            for r in range(2):
                                MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                          vector_=self.speed, layer_=self.layer_,
                                                          angle_=self.angle_degrees,
                                                          exhaust_pos_=self.exhaust_abs_position)

                    else:
                        for r in range(2):
                            MissileParticleFx_improve(
                                rect_=pygame.math.Vector2(self.rect.center),
                                vector_=self.speed, layer_=self.layer_,
                                angle_=self.angle_degrees, exhaust_pos_=self.exhaust_abs_position)

                    self.rect.center += self.speed

                # target is destroyed or player is dead
                # missile continue its course
                else:
                    angle_rad = -atan2(self.speed.y, self.speed.x)
                    self.angle_degrees = (angle_rad * RAD_TO_DEG) % 360
                    if self.bingo > 0:
                        for r in range(1):
                            MissileParticleFx_improve(
                                rect_=pygame.math.Vector2(self.rect.center),
                                vector_=self.speed, layer_=self.layer_,
                                angle_=self.angle_degrees, exhaust_pos_=self.exhaust_abs_position)
                    self.bingo -= 1
                    self.rect.center += self.speed

            # NUCLEAR BOMB
            else:

                self.rect.center += self.speed
                self.pos = self.rect.center

            # missile is going outside the display.
            if not HomingMissile.screenrect.contains(self.rect):
                if self.is_nuke:
                    # Create a dummy target 400 pixels ahead of the spaceship
                    # Virtual rectangle that will trigger a nuke explosion after colliding with it.
                    # This sprite is passed into the group nuke_aiming_point(this group contains every
                    # virtual rectangle)
                    dummy_sprite = pygame.sprite.Sprite()
                    dummy_sprite.rect = self.rect.copy()
                    dummy_sprite.rect.center = (self.rect.centerx, self.rect.centery - 200)
                    dummy_sprite.dummy = True
                    dummy_sprite.name = self.gl_.PLAYER_NUMBER
                    self.gl_.nuke_aiming_point.add(dummy_sprite)
                else:
                    self.sound_fx_stop()
                    self.kill()

            if isinstance(self.images_copy, list):
                if self.index >= len(self.images_copy) - 1:
                    self.index = 0
                else:
                    self.index += 1

            self.dt = 0

        self.dt += self.gl_.TIME_PASSED_SECONDS


class AdaptiveHomingMissile(pygame.sprite.Sprite):
    """
        PURE PURSUIT ALGORITHM
        This class is almost identical to EnemyHomingMissile, only minor adjustment have been
        made in order to conserve symmetrical aspect when more than one missile is shot.

        Guided ballistic missile
        This missile adjust its direction by incrementing/decrementing the aiming angle
        in order to reach the target with the minimum distance traveled.
        It has also a fuel attribute decreasing its effectiveness in time.
        The missile can be shot in any direction from the player position.
        The propulsion engine can be trigger at a later stage using the variable propulsion.
        A launch offset can be added to the starting missile position.
        When the missile is launched, it will curve and travel toward the position of a virtual rectangle
        placed ahead of the player position until it reached 25 frames, time when the propulsion engine
        is triggered. This allow the missiles to curve symmetrically around the spaceship in both directions
        clockwise and anti-clockwise.
        The missile will follow its path when going outside the screen dimensions, this allow a shot from anywhere
        in the gaming window (as long has the missile has fuel).
        If the target is destroyed before the missile impact, the missile will resume its course ahead with
        the previous calculated vector direction.
    """

    containers = None  # Groups
    images = None  # Sprite
    is_locked = False  # missile locked True | False --> NOT USE
    screenrect = None  # Screen dimension (pygame.Rect)

    def __init__(self,
                 player_,  # player instance
                 gl_,  # global variables
                 weapon_,  # Weapon class
                 shooter_,  # shooter rectangle
                 shoot_angle_,  # shooting angle
                 target_,  # missile target
                 target_pool_,  # Target pool (pygame.sprite.Group())
                 offset_=None,  # launch offset
                 timing_=15,  # Refreshing time
                 propulsion_=False,  # True | False propulsion delay
                 particles=True,  # show particle
                 layer_=-2):  # Sprite layer

        pygame.sprite.Sprite.__init__(self, self.containers)

        if layer_:
            if isinstance(gl_.All, pygame.sprite.LayeredUpdates):
                gl_.All.change_layer(self, layer_)

        # Create a velocity vector2d, ! CANNOT WORK FROM THE ORIGINAL VECTOR, it has to be a copy
        self.velocity = pygame.math.Vector2(weapon_.velocity, weapon_.velocity)
        self.magnitude = self.velocity.length()  # projectile speed (vector magnitude)
        self.rotation = 90  # bitmap orientation (missile heading 90 degrees) by default
        self.target = target_  # target sprite (must have a rect attribute)
        self.particles = particles  # show particles
        self.images_copy = self.images.copy()  # Work from bitmap copy
        self.image = self.images_copy[0] if \
            isinstance(self.images_copy, list) else self.images_copy

        self.rect = self.image.get_rect(midbottom=shooter_.center)  # missile rectangle
        self.position = pygame.math.Vector2(self.rect.center)  # missile position (pygame.vector2
        self.vector = pygame.math.Vector2()  # attribute vector for compatibility with other class
        self.shooter_rect = pygame.math.Vector2(shooter_.center)  # Original position when missile triggered
        # EnemyHomingMissile.is_locked = True                       # NOT USE
        self.index = 0
        self.timing = timing_  # Refreshing rate in ms (16ms equivalent to 60fps)
        self.dt = 0  # Time constant
        self.time_passed_seconds = gl_.TIME_PASSED_SECONDS  # Time constant
        self.gl_ = gl_  # Global variables
        self.target_pool = target_pool_  # Enemy pool
        self.screenrect = AdaptiveHomingMissile.screenrect  # screen rectangle to check borders
        self.weapon = weapon_  # weapon class (missile attributes and settings)
        self.damage = weapon_.damage  # Amount of damages transfer to target after collision
        self.collision_damage = weapon_.damage  # attribute for compatibility with other class
        self.max_rotation = weapon_.max_rotation  # Maximal rotation in degrees (max turn in degrees, in
        # 1 second at 60fps)
        self.shoot_angle = shoot_angle_  # Angle where the missile is aiming to (starting angle)
        self.heading = shoot_angle_  # direction where the missile is heading (similar to
        # to self.shoot_angle at start)
        self.angle = self.heading - self.rotation  # Angle value to pass to method rot_center.
        # correspond considering the bitmap orientation
        self.image, self.rect = self.rot_center(
            self.images_copy, self.angle, self.rect)  # Draw the missile and initialised the rectangle size
        # matching the bitmap size.
        if offset_ is not None:
            self.rect.center += offset_ if isinstance(offset_, pygame.math.Vector2) \
                else (0, 0)  # offset to add to the position
        self.sign = 0  # Two - dimensional rotation direction indicator,
        # clockwise or anti - clockwise
        # Exhaust coordinates (absolute values from the center,
        # center of the object the reference point for any transformation.
        self.exhaust_abs_position = pygame.math.Vector2(self.rect.midbottom[0] - self.rect.centerx, \
                                                        self.rect.midbottom[1] - self.rect.centery)
        self.layer_ = layer_
        self.bingo = random.randint(100, 120)  # Randomized value (fuel counter)
        self.propulsion = propulsion_  # Delay propulsion True | False
        self.sound = weapon_.sound_effect
        self._id = id(self)
        if self.gl_.SC_explosion is not None and \
                self.gl_.SC_spaceship is not None:
            self.sound_fx()  # play sound fx
        self.get_vector()  # Get the vector corresponding to the missile direction
        self.start = self.gl_.FRAME  # catch the frame number
        self.dummy = None  # init dummy
        self.dummy_target()  # create a dummy target (pygame rect)
        self.initial_target = target_  # copy target

        # at this point the missile is aiming toward
        # the virtual rectangle (dummy rectangle)
        # The dummy rect will be substitute after 25 frames
        # with the initial target (self.initial_target) see below for more
        # details
        self.target = self.dummy  # first target is the dummy rect
        self.player = player_  # player instance (who is shooting)
        # Apply 60FPS to the missile if MAXFPS is over 60fps
        if MAXFPS > 60:
            self.timing = 16.0
        else:
            self.timing = 0.0

    def dummy_target(self):
        self.dummy = pygame.sprite.Sprite()
        self.dummy.image = pygame.Surface((10, 10)).convert()
        self.dummy.rect = self.dummy.image.get_rect(center=(self.shooter_rect.x, 0))
        self.dummy.vector = pygame.math.Vector2(-1, 1)
        self.dummy.dummy = True
        self.dummy.invincible = True
        self.target_pool.add(self.dummy)  # add the dummy rectangle to the enemy pool

    def sound_fx(self):
        if not any(self.gl_.SC_explosion.get_identical_id(self._id)):
            self.gl_.SC_explosion.play(sound_=self.sound,
                                       loop_=False, priority_=0,
                                       volume_=self.gl_.SOUND_LEVEL,
                                       fade_out_ms=0, panning_=True,
                                       name_='MISSILE FLIGHT',
                                       x_=self.rect.centerx, object_id_=self._id)

    def sound_fx_stop(self):
        if self.gl_.SC_explosion is not None:
            self.gl_.SC_explosion.stop_object(self._id)

    # kept for compatibility with other class.
    def hit(self, *args, **kwargs):
        """ The missile got hit by a projectile, kill the sprite"""
        self.sound_fx_stop()
        # Remove the dummy rectangle from the enemy pool
        if self.dummy in self.target_pool:
            self.dummy.kill()
        self.kill()

    # kept for compatibility with other class.
    def location(self):
        """ Return the center position (tuple) of the missile """
        return self.rect

    def get_angle(self):
        # determines the angle between the shooter and the target position
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        # angle (in degrees) difference between the missile and the target object
        return -int(degrees(atan2(dy, dx)) % 360)

    def get_vector(self):
        self.velocity.x, self.velocity.y = cos(radians(self.heading)), \
                                           -sin(radians(self.heading))
        self.velocity *= self.magnitude

    @staticmethod
    def rot_center(image_: pygame.Surface, angle_, rect_) -> (pygame.Surface, pygame.Rect):
        """ rotate an image while keeping its center and size (only for symmetric surface)
            argument angle_ has to be in degres
        """
        new_image = pygame.transform.rotate(image_, angle_)
        return new_image, new_image.get_rect(center=rect_.center)

    def update(self):

        if self.dt > self.timing:

            # if one of the player is alive (sprite alive)
            if self.target is not None and \
                    self.target.alive() and self.bingo > 0:

                self.bingo -= 1

                rotation_degrees = self.get_angle()
                self.angle = rotation_degrees - self.heading

                if self.angle != 0:

                    self.angle %= 360
                    sign = 0
                    clockwise = self.angle
                    anticlockwise = 360 - clockwise
                    # equidistant, choose a direction
                    if anticlockwise == clockwise:
                        sign = random.choice((-1, 1))
                    # equidistant 0 % 360 degrees same angle.
                    elif abs(anticlockwise - clockwise) == 360:
                        sign = 0
                    # anticlockwise is shortest angular rotation
                    elif anticlockwise < clockwise:
                        sign = -1
                    elif anticlockwise > clockwise:
                        sign = +1

                    delta = rotation_degrees % 360 - self.heading % 360
                    # print(rotation_degrees, self.heading, self.angle,
                    #      rotation_degrees % 360 - self.heading % 360)
                    if abs(delta) - abs(self.max_rotation * sign) >= 1:
                        self.heading += (self.max_rotation * sign)
                    else:
                        self.heading += delta

                self.image, self.rect = self.rot_center(
                    self.images_copy, self.heading - self.rotation, self.rect)

                self.get_vector()

                if self.propulsion:
                    # 25 frames for a refreshing rate of 16ms.
                    # ! Change value if refreshing rate is not 16ms.
                    if self.gl_.FRAME - self.start > 25:
                        # Missile is now aiming for its target
                        self.target = self.initial_target
                        if self.particles:
                            for r in range(3):
                                MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                          vector_=self.velocity, layer_=self.layer_,
                                                          angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)
                else:
                    if self.gl_.FRAME - self.start > 2:
                        # Missile is now aiming for its target
                        self.target = self.initial_target

                    if self.particles:
                        for r in range(3):
                            MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                      vector_=self.velocity, layer_=self.layer_,
                                                      angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)

                self.rect.center += self.velocity
                self.position = self.rect.center

            # missile continue in the same direction
            else:

                if self.bingo > 0:
                    if self.gl_.FRAME - self.start > 25 and self.particles:
                        for r in range(2):
                            MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                      vector_=self.velocity, layer_=self.layer_,
                                                      angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)
                self.bingo -= 1
                self.rect.center += self.velocity
                self.position = self.rect.center

            if not self.screenrect.colliderect(self.rect):
                self.sound_fx_stop()
                # Allow the missile to go outside the screen
                if self.bingo < 0:
                    # Remove the dummy rectangle from the enemy pool
                    if self.dummy in self.target_pool:
                        self.dummy.kill()
                    self.kill()

            if isinstance(self.images_copy, list):
                if self.index >= len(self.images_copy) - 1:
                    self.index = 0
                else:
                    self.index += 1

            self.dt = 0

        self.dt += self.time_passed_seconds


class InterceptHomingMissile(pygame.sprite.Sprite):
    """
        LEAD COLLISION (proportional navigation) more effective, follow an optimal path
        Intercept theorem (Thales basic proportionality theorem)
        https://www.youtube.com/watch?v=T2fPKUfmnKo
        https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm

    """

    containers = None  # Groups
    images = None  # Sprite
    is_locked = False  # missile locked True | False --> NOT USE
    screenrect = None  # Screen dimension (pygame.Rect)

    def __init__(self,
                 player_,  # player instance
                 gl_,  # global variables
                 weapon_,  # Weapon class
                 shooter_,  # shooter rectangle
                 shoot_angle_,  # shooting angle
                 target_,  # missile target
                 target_pool_,  # Target pool (pygame.sprite.Group())
                 offset_=None,  # launch offset
                 timing_=15,  # Refreshing time
                 propulsion_=False,  # True | False propulsion delay
                 particles=True,  # show particle
                 layer_=-2):  # Sprite layer

        pygame.sprite.Sprite.__init__(self, self.containers)

        if layer_:
            if isinstance(gl_.All, pygame.sprite.LayeredUpdates):
                gl_.All.change_layer(self, layer_)

        # Create a velocity vector2d, ! CANNOT WORK FROM THE ORIGINAL VECTOR, it has to be a copy
        self.velocity = pygame.math.Vector2(weapon_.velocity, weapon_.velocity)
        self.magnitude = self.velocity.length()  # projectile speed (vector magnitude)
        self.rotation = 90  # bitmap orientation (missile heading 90 degrees) by default
        self.target = target_  # target sprite (must have a rect attribute)
        self.particles = particles  # show particles
        self.images_copy = self.images.copy()  # Work from bitmap copy
        self.image = self.images_copy[0] if \
            isinstance(self.images_copy, list) else self.images_copy

        self.rect = self.image.get_rect(midbottom=shooter_.center)  # missile rectangle
        self.position = pygame.math.Vector2(self.rect.center)  # missile position (pygame.vector2
        self.vector = pygame.math.Vector2()  # attribute vector for compatibility with other class
        self.shooter_rect = pygame.math.Vector2(shooter_.center)  # Original position when missile triggered
        # EnemyHomingMissile.is_locked = True                       # NOT USE
        self.index = 0
        self.timing = timing_  # Refreshing rate in ms (16ms equivalent to 60fps)
        self.dt = 0  # Time constant
        self.time_passed_seconds = gl_.TIME_PASSED_SECONDS  # Time constant
        self.gl_ = gl_  # Global variables
        self.target_pool = target_pool_  # Enemy pool
        self.screenrect = InterceptHomingMissile.screenrect  # screen rectangle to check borders
        self.weapon = weapon_  # weapon class (missile attributes and settings)
        self.damage = weapon_.damage  # Amount of damages transfer to target after collision
        self.collision_damage = weapon_.damage  # attribute for compatibility with other class
        self.max_rotation = weapon_.max_rotation  # Maximal rotation in degrees (max turn in degrees, in
        # 1 second at 60fps)
        self.shoot_angle = shoot_angle_  # Angle where the missile is aiming to (starting angle)
        self.heading = shoot_angle_  # direction where the missile is heading (similar to
        # to self.shoot_angle at start)
        self.angle = self.heading - self.rotation  # Angle value to pass to method rot_center.
        # correspond considering the bitmap orientation
        self.image, self.rect = self.rot_center(
            self.images_copy, self.angle, self.rect)  # Draw the missile and initialised the rectangle size
        # matching the bitmap size.
        if offset_ is not None:
            self.rect.center += offset_ if isinstance(offset_, pygame.math.Vector2) \
                else (0, 0)  # offset to add to the position
        self.sign = 0  # Two - dimensional rotation direction indicator,
        # clockwise or anti - clockwise
        # Exhaust coordinates (absolute values from the center,
        # center of the object the reference point for any transformation.
        self.exhaust_abs_position = pygame.math.Vector2(self.rect.midbottom[0] - self.rect.centerx, \
                                                        self.rect.midbottom[1] - self.rect.centery)
        self.layer_ = layer_
        self.bingo = random.randint(100, 120)  # Randomized value (fuel counter)
        self.propulsion = propulsion_  # Delay propulsion True | False
        self.sound = weapon_.sound_effect
        self._id = id(self)
        if self.gl_.SC_explosion is not None and \
                self.gl_.SC_spaceship is not None:
            self.sound_fx()  # play sound fx
        self.get_vector()  # Get the vector corresponding to the missile direction
        self.start = self.gl_.FRAME  # catch the frame number
        self.dummy = None  # init dummy
        self.dummy_target()  # create a dummy target (pygame rect)
        self.initial_target = target_  # copy target

        # at this point the missile is aiming toward
        # the virtual rectangle (dummy rectangle)
        # The dummy rect will be substitute after 25 frames
        # with the initial target (self.initial_target) see below for more
        # details
        self.target = self.dummy  # first target is the dummy rect
        self.player = player_  # player instance (who is shooting)
        # Apply 60FPS to the missile if MAXFPS is over 60fps
        if MAXFPS > 60:
            self.timing = 16.0
        else:
            self.timing = 0.0

    def dummy_target(self):
        self.dummy = pygame.sprite.Sprite()
        self.dummy.image = pygame.Surface((10, 10)).convert()
        self.dummy.rect = self.dummy.image.get_rect(center=(self.shooter_rect.x, 0))
        self.dummy.vector = pygame.math.Vector2(0, 0)
        self.dummy.dummy = True
        self.dummy.invincible = True
        self.target_pool.add(self.dummy)  # add the dummy rectangle to the enemy pool

    def sound_fx(self):
        if not any(self.gl_.SC_explosion.get_identical_id(self._id)):
            self.gl_.SC_explosion.play(sound_=self.sound,
                                       loop_=False, priority_=0,
                                       volume_=self.gl_.SOUND_LEVEL,
                                       fade_out_ms=0, panning_=True,
                                       name_='MISSILE FLIGHT',
                                       x_=self.rect.centerx, object_id_=self._id)

    def sound_fx_stop(self):
        if self.gl_.SC_explosion is not None:
            self.gl_.SC_explosion.stop_object(self._id)

    # kept for compatibility with other class.
    def hit(self, *args, **kwargs):
        """ The missile got hit by a projectile, kill the sprite"""
        self.sound_fx_stop()
        # Remove the dummy rectangle from the enemy pool
        if self.dummy in self.target_pool:
            self.dummy.kill()
        self.kill()

    # kept for compatibility with other class.
    def location(self):
        """ Return the center position (tuple) of the missile """
        return self.rect

    def get_angle(self):
        # determines the angle between the shooter and the target position
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        # angle (in degrees) difference between the missile and the target object
        return -int(degrees(atan2(dy, dx)) % 360)

    def get_vector(self):
        self.velocity.x, self.velocity.y = cos(radians(self.heading)), \
                                           -sin(radians(self.heading))
        self.velocity *= self.magnitude

    @staticmethod
    def rot_center(image_: pygame.Surface, angle_, rect_) -> (pygame.Surface, pygame.Rect):
        """ rotate an image while keeping its center and size (only for symmetric surface)
            argument angle_ has to be in degres
        """
        new_image = pygame.transform.rotate(image_, angle_)
        return new_image, new_image.get_rect(center=rect_.center)

    def update(self):

        if self.dt > self.timing:

            # if one of the player is alive (sprite alive)
            if self.target is not None and \
                    self.target.alive() and self.bingo > 0:

                self.bingo -= 1

                p1, vector, collision = \
                    missile_lead_angle(p1=pygame.math.Vector2(self.rect.center),
                                       p2=pygame.math.Vector2(self.target.rect.center),
                                       v1=pygame.math.Vector2(
                                           cos(math.radians(self.heading)) * self.magnitude,
                                           sin(math.radians(self.heading)) * self.magnitude),
                                       v2=pygame.math.Vector2(self.target.vector.x,
                                                              self.target.vector.y))
                if p1 is not None:
                    self.heading = math.degrees(-math.atan2(vector.y, vector.x))
                    self.velocity = vector  # * self.magnitude

                self.image, self.rect = self.rot_center(
                    self.images_copy, self.heading - self.rotation, self.rect)

                # self.get_vector()

                if self.propulsion:
                    # 25 frames for a refreshing rate of 16ms.
                    # ! Change value if refreshing rate is not 16ms.
                    if self.gl_.FRAME - self.start > 2:
                        # Missile is now aiming for its target
                        self.target = self.initial_target
                        if self.particles:
                            for r in range(3):
                                MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                          vector_=self.velocity, layer_=self.layer_,
                                                          angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)
                else:
                    if self.gl_.FRAME - self.start > 2:
                        # Missile is now aiming for its target
                        self.target = self.initial_target

                    if self.particles:
                        for r in range(3):
                            MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                      vector_=self.velocity, layer_=self.layer_,
                                                      angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)

                self.rect.center += self.velocity
                self.position = self.rect.center

            # missile continue in the same direction
            else:

                if self.bingo > 0:
                    if self.gl_.FRAME - self.start > 2 and self.particles:
                        for r in range(2):
                            MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                      vector_=self.velocity, layer_=self.layer_,
                                                      angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)
                self.bingo -= 1
                self.rect.center += self.velocity
                self.position = self.rect.center

            if not self.screenrect.colliderect(self.rect):
                self.sound_fx_stop()
                # Allow the missile to go outside the screen
                if self.bingo < 0:
                    # Remove the dummy rectangle from the enemy pool
                    if self.dummy in self.target_pool:
                        self.dummy.kill()
                    self.kill()

            if isinstance(self.images_copy, list):
                if self.index >= len(self.images_copy) - 1:
                    self.index = 0
                else:
                    self.index += 1

            self.dt = 0

        self.dt += self.time_passed_seconds


class EnemyHomingMissile(pygame.sprite.Sprite):
    """
    This ballistic missile is reserved for the enemy class
    Functionality is almost identical to AdaptiveHomingMissile class (see class for more details).
    The missile is aiming directly toward the target choosing always the shortest path.

    """
    containers = None  # Groups
    images = None  # Sprite
    is_locked = False  # missile locked True | False --> NOT USE
    screenrect = None  # Screen dimension (pygame.Rect)

    def __init__(self, gl_,
                 weapon_,  # Weapon class
                 shooter_,  # shooter rectangle
                 shoot_angle_,  # shooting angle
                 target_,  # missile target
                 target_pool_,  # Target pool (pygame.sprite.Group())
                 offset_=None,  # launch offset
                 timing_=15,  # Refreshing time
                 propulsion_=False,  # True | False propulsion delay
                 layer_=-2):  # Sprite layer

        pygame.sprite.Sprite.__init__(self, self.containers)

        if layer_:
            if isinstance(gl_.All, pygame.sprite.LayeredUpdates):
                gl_.All.change_layer(self, layer_)

        # Create a velocity vector2d, ! CANNOT WORK FROM THE ORIGINAL VECTOR, it has to be a copy
        self.velocity = pygame.math.Vector2(weapon_.velocity, weapon_.velocity)
        self.magnitude = self.velocity.length()  # projectile speed (vector magnitude)
        self.rotation = 90  # bitmap orientation (missile heading 90 degrees) by default
        self.target = target_  # target sprite (must have a rect attribute)
        self.images_copy = self.images.copy()  # Work from bitmap copy
        self.image = self.images_copy[0] if \
            isinstance(self.images_copy, list) else self.images_copy

        self.rect = self.image.get_rect(midbottom=shooter_.center)  # missile rectangle
        self.position = pygame.math.Vector2(self.rect.center)  # missile position (pygame.vector2
        self.vector = pygame.math.Vector2()  # attribute vector for compatibility with other class
        self.shooter_rect = pygame.math.Vector2(shooter_.center)  # Original position when missile triggered
        # EnemyHomingMissile.is_locked = True                       # NOT USE
        self.index = 0
        self.timing = timing_  # Refreshing rate in ms (16ms equivalent to 60fps)
        self.dt = 0  # Time constant
        self.time_passed_seconds = gl_.TIME_PASSED_SECONDS  # Time constant
        self.gl_ = gl_  # Global variables
        self.target_pool = target_pool_  # Contains player instances (Player and Player2)
        self.screenrect = EnemyHomingMissile.screenrect  # screen rectangle to check borders
        self.weapon = weapon_  # weapon class (missile attributes and settings)
        self.damage = weapon_.damage  # Amount of damages transfer to target after collision
        self.collision_damage = weapon_.damage  # attribute for compatibility with other class
        self.max_rotation = weapon_.max_rotation  # Maximal rotation in degrees (max turn in degrees, in
        # 1 second at 60fps)
        self.shoot_angle = shoot_angle_  # Angle where the missile is aiming to (starting angle)
        self.heading = shoot_angle_  # direction where the missile is heading (similar to
        # to self.shoot_angle at start)
        self.angle = self.heading - self.rotation  # Angle value to pass to method rot_center.
        # correspond considering the bitmap orientation
        self.image, self.rect = self.rot_center(
            self.images_copy, self.angle, self.rect)  # Draw the missile and initialised the rectangle size
        # matching the bitmap size.
        if offset_ is not None:
            self.rect.center += offset_ if isinstance(offset_, pygame.math.Vector2) \
                else (0, 0)  # offset to add to the position
        self.sign = 0  # Two - dimensional rotation direction indicator,
        # clockwise or anti - clockwise
        # Exhaust coordinates (absolute values from the center,
        # center of the object the reference point for any transformation.
        self.exhaust_abs_position = pygame.math.Vector2(self.rect.midbottom[0] - self.rect.centerx, \
                                                        self.rect.midbottom[1] - self.rect.centery)
        self.layer_ = layer_
        self.bingo = random.randint(100, 120)  # Randomized value (fuel counter)
        self.propulsion = propulsion_  # Delay propulsion True | False
        self.sound = weapon_.sound_effect
        self._id = id(self)
        if self.gl_.SC_explosion is not None and \
                self.gl_.SC_spaceship is not None:
            self.sound_fx()  # play sound fx
        self.get_vector()  # Get the vector corresponding to the missile direction
        self.start = self.gl_.FRAME  # catch the frame number
        # Apply 60FPS to the missile if MAXFPS is over 60fps
        if MAXFPS > 60:
            self.timing = 16.0
        else:
            self.timing = 0.0

    def sound_fx(self):
        if not any(self.gl_.SC_explosion.get_identical_id(self._id)):
            self.gl_.SC_explosion.play(sound_=self.sound,
                                       loop_=False, priority_=0,
                                       volume_=self.gl_.SOUND_LEVEL,
                                       fade_out_ms=0, panning_=True,
                                       name_='MISSILE FLIGHT',
                                       x_=self.rect.centerx, object_id_=self._id)

    def sound_fx_stop(self):
        if self.gl_.SC_explosion is not None:
            self.gl_.SC_explosion.stop_object(self._id)

    # kept for compatibility with other class.
    def hit(self, *args, **kwargs):
        """ The missile got hit by a projectile, kill the sprite"""
        self.sound_fx_stop()
        self.kill()

    # kept for compatibility with other class.
    def location(self):
        """ Return the center position (tuple) of the missile """
        return self.rect

    def get_angle(self):
        # determines the angle between the shooter and the target position
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        # angle (in degrees) difference between the missile and the target object
        return -int(degrees(atan2(dy, dx)) % 360)

    def get_vector(self):
        self.velocity.x, self.velocity.y = cos(radians(self.heading)), \
                                           -sin(radians(self.heading))
        self.velocity *= self.magnitude

    @staticmethod
    def rot_center(image_: pygame.Surface, angle_, rect_) -> (pygame.Surface, pygame.Rect):
        """ rotate an image while keeping its center and size (only for symmetric surface)
            argument angle_ has to be in degres
        """
        new_image = pygame.transform.rotate(image_, angle_)
        return new_image, new_image.get_rect(center=rect_.center)

    def update(self):

        if self.dt > self.timing:

            # if one of the player is alive (sprite alive)
            if self.target is not None and \
                    self.target.alive() and self.bingo > 0:

                self.bingo -= 1

                rotation_degrees = self.get_angle()
                self.angle = rotation_degrees - self.heading

                if self.angle != 0:

                    self.angle %= 360
                    sign = 0
                    clockwise = self.angle
                    anticlockwise = 360 - clockwise
                    # equidistant, choose a direction
                    if anticlockwise == clockwise:
                        sign = random.choice((-1, 1))
                    # equidistant 0 % 360 degrees same angle.
                    elif abs(anticlockwise - clockwise) == 360:
                        sign = 0
                    # anticlockwise is shortest angular rotation
                    elif anticlockwise < clockwise:
                        sign = -1
                    elif anticlockwise > clockwise:
                        sign = +1

                    delta = rotation_degrees % 360 - self.heading % 360
                    # print(rotation_degrees, self.heading, self.angle,
                    #      rotation_degrees % 360 - self.heading % 360)
                    if abs(delta) - abs(self.max_rotation * sign) >= 1:
                        self.heading += (self.max_rotation * sign)
                    else:
                        self.heading += delta

                self.image, self.rect = self.rot_center(
                    self.images_copy, self.heading - self.rotation, self.rect)

                self.get_vector()

                if self.propulsion:
                    # 25 frames for a refreshing rate of 16ms.
                    # ! Change value if refreshing rate is changing.
                    if self.gl_.FRAME - self.start > 25:
                        MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                  vector_=self.velocity, layer_=self.layer_,
                                                  angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)
                else:
                    MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                              vector_=self.velocity, layer_=self.layer_,
                                              angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)

                self.rect.center += self.velocity
                self.position = self.rect.center

            # missile continue in the same direction
            else:

                if self.bingo > 0:
                    if self.gl_.FRAME - self.start > 25:
                        #  self.target.kill()
                        MissileParticleFx_improve(rect_=pygame.math.Vector2(self.rect.center),
                                                  vector_=self.velocity, layer_=self.layer_,
                                                  angle_=self.heading, exhaust_pos_=self.exhaust_abs_position)
                self.bingo -= 1
                self.rect.center += self.velocity
                self.position = self.rect.center

            if not self.screenrect.colliderect(self.rect):
                self.sound_fx_stop()
                # Allow the missile to go outside the screen
                if self.bingo < 0:
                    self.kill()

            if isinstance(self.images_copy, list):
                if self.index >= len(self.images_copy) - 1:
                    self.index = 0
                else:
                    self.index += 1

            self.dt = 0

        self.dt += self.time_passed_seconds


if __name__ == '__main__':

    freetype.init(cache_size=64, resolution=72)
    class EnemyWeapons:

        def __init__(self, name_: str, sprite_: (pygame.Surface, list), range_: int,
                     velocity_, damage_: int,
                     sound_effect_: pygame.mixer.Sound, volume_: int, reloading_time_: float,
                     animation_, offset_: tuple = (0, 0), detonation_dist_: int = None,
                     timestamp_=0, max_rotation_=None):

            self.name = name_  # Weapon system name (str)
            self.type_ = 'LASER'  # for compatibility with other class (str)
            self.sprite = sprite_  # Sprite shot (pygame.Surface)
            self.range = range_  # Maximum range (int)
            self.velocity = pygame.math.Vector2(0, velocity_)  # shot speed (pygame.math.Vector2)
            self.damage = damage_  # Damage given to the player (int)
            self.sound_effect = sound_effect_  # Shot sound effect (pygame.mixer.Sound)
            self.volume = volume_  # Sound FX volume (int)
            self.animation = animation_  # Shot animation (pygame.Surface, list)
            self.timestamp = timestamp_  # Shooting timestamp (int)
            self.reloading_time = reloading_time_ * MAXFPS  # time(in secs) x fps = (number of frames)
            self.offset = offset_  # Offset for laser shots (tuple)
            self.detonation_dist = detonation_dist_  # detonation distance (for ground turret)
            self.max_rotation = max_rotation_  # Missile max_rotation (maximal angular

        # deviation in degrees)

        def is_reloading(self, frame_):
            if frame_ - self.timestamp > self.reloading_time:
                # ready to shoot
                self.timestamp = 0
                return False
            # reloading
            else:
                return True

        def shooting(self, frame_):
            self.timestamp = frame_  # GL.FRAME


    class LayeredUpdatesModified(pygame.sprite.LayeredUpdates):

        def __init__(self):
            pygame.sprite.LayeredUpdates.__init__(self)

        def draw(self, surface_):
            """draw all sprites in the right order onto the passed surface

            LayeredUpdates.draw(surface): return Rect_list

            """
            spritedict = self.spritedict
            surface_blit = surface_.blit
            dirty = self.lostsprites
            self.lostsprites = []
            dirty_append = dirty.append
            init_rect = self._init_rect
            for spr in self.sprites():
                rec = spritedict[spr]

                if hasattr(spr, '_blend') and spr._blend is not None:
                    newrect = surface_blit(spr.image, spr.rect, special_flags=spr._blend)
                else:
                    newrect = surface_blit(spr.image, spr.rect)

                if rec is init_rect:
                    dirty_append(newrect)
                else:
                    if newrect.colliderect(rec):
                        dirty_append(newrect.union(rec))
                    else:
                        dirty_append(newrect)
                        dirty_append(rec)
                spritedict[spr] = newrect
            return dirty


    class Player(pygame.sprite.Sprite):

        images = None
        containers = None

        def __init__(self, pos_, gl_, timing_=15, layer_=0):
            pygame.sprite.Sprite.__init__(self, Player.containers)

            self.image = Player.images
            self.rect = self.image.get_rect(center=pos_)

            self.mask = pygame.mask.from_surface(self.image)
            self.gl = gl_
            self.layer_ = layer_
            self.timing = timing_
            self.angle = 0
            self.life = 1000
            self.max_life = 1000
            self._rotation = 0

        def update(self):
            self.rect = self.rect.clamp(SCREENRECT)


    class Enemy(pygame.sprite.Sprite):

        images = None
        containers = None

        def __init__(self, pos_, gl_, timing_=15, layer_=0):
            pygame.sprite.Sprite.__init__(self, Player.containers)

            self.image = Enemy.images
            self.rect = self.image.get_rect(center=pos_)
            self.position = pos_
            self.vector = pygame.math.Vector2(0, 0)
            self.mask = pygame.mask.from_surface(self.image)
            self.gl = gl_
            self.layer_ = layer_
            self.timing = timing_
            self.angle = 0
            self.life = 1000
            self.max_life = 1000
            self._rotation = 0

        def update(self):
            # self.rect = self.rect.clamp(SCREENRECT)
            self.image = Enemy.images
            self.rect = self.image.get_rect(center=self.position)
            self.position += self.vector


    SCREENRECT = pygame.Rect(0, 0, 800, 1024)
    GL.SCREENRECT = SCREENRECT
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWACCEL, 32)
    GL.screen = SCREEN
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4095)

    BACKGROUND = pygame.image.load('Assets\\A2.png').convert()

    clock = pygame.time.Clock()
    GL.TIME_PASSED_SECONDS = clock.tick(60)

    All = LayeredUpdatesModified()
    # globalisation
    GL.All = All

    GL.PLAYER_GROUP = pygame.sprite.Group()
    GL.GROUP_UNION = pygame.sprite.Group()
    GL.enemy_group = pygame.sprite.Group()
    SoundControl.SCREENRECT = SCREENRECT
    GL.SC_spaceship = SoundControl(10)
    GL.SC_explosion = SoundControl(10)
    GL.SOUND_LEVEL = 1.0

    SPACE_FIGHTER_SPRITE = pygame.image.load('Assets\\illumDefault11.png').convert_alpha()
    SPACE_FIGHTER_SPRITE = pygame.transform.smoothscale(SPACE_FIGHTER_SPRITE, (80, 55))
    MISSILE_FLIGHT_SOUND = pygame.mixer.Sound('Assets\\sd_weapon_missile_heavy_01.ogg')
    STINGER_MISSILE_SPRITE = pygame.image.load('Assets\\MISSILE0.png').convert_alpha()
    STINGER_MISSILE = EnemyWeapons(name_='Missile',
                                   sprite_=STINGER_MISSILE_SPRITE,
                                   range_=SCREENRECT.h,
                                   velocity_=-15,
                                   damage_=1050,
                                   sound_effect_=MISSILE_FLIGHT_SOUND,
                                   volume_=1.0,
                                   reloading_time_=5,
                                   animation_=None,
                                   offset_=(0, 0),
                                   detonation_dist_=None,
                                   max_rotation_=10)

    COBRA = pygame.image.load('Assets\\SpaceShip.png').convert_alpha()
    Player.images = COBRA
    Player.containers = GL.All, GL.PLAYER_GROUP
    Enemy.containers = GL.All, GL.GROUP_UNION
    Enemy.images = SPACE_FIGHTER_SPRITE
    GL.player = Player(pos_=(SCREENRECT.centerx, SCREENRECT.bottom + 100), gl_=GL, timing_=0, layer_=0)
    Player._blend = None

    target = Enemy(pos_=(SCREENRECT.centerx, SCREENRECT.top + 100), gl_=GL, timing_=0, layer_=0)
    GL.GROUP_UNION.add(target)

    # dummy = pygame.sprite.Sprite()
    # dummy.image = SPACE_FIGHTER_SPRITE
    # dummy.rect = dummy.image.get_rect(center=(200, 400))
    # dummy = Enemy(pos_=(GL.player.rect.centerx - 200, SCREENRECT.left -400), gl_=GL, timing_=0, layer_=0)
    # GL.GROUP_UNION.add(dummy)

    STOP_GAME = False
    QUIT = False
    GL.PAUSE = False
    em = pygame.sprite.Group()
    hm = pygame.sprite.Group()

    recording = False    # allow recording video
    VIDEO = []          # Capture frames

    dt = 0.0
    while not STOP_GAME:
        pygame.event.pump()

        keys = pygame.key.get_pressed()

        while GL.PAUSE:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                # print(keys)
                if keys[pygame.K_PAUSE]:
                    GL.PAUSE = False
                    pygame.event.clear()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                target.rect.center = mouse_pos
                target.position = mouse_pos
                ...

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            STOP_GAME = True

        if keys[pygame.K_RIGHT]:
            GL.player.rect.centerx += 6

        if keys[pygame.K_LEFT]:
            GL.player.rect.centerx -= 6

        if keys[pygame.K_UP]:
            GL.player.rect.centery -= 6

        if keys[pygame.K_DOWN]:
            GL.player.rect.centery += 6

        if keys[pygame.K_F8]:
            pygame.image.save(SCREEN, 'Screendump' + str(GL.FRAME) + '.png')

        if keys[pygame.K_SPACE]:
            if not (GL.GROUP_UNION.has(hm) or GL.GROUP_UNION.has(em)):
                AdaptiveHomingMissile.containers = GL.enemy_group, GL.All
                AdaptiveHomingMissile.images = STINGER_MISSILE.sprite
                AdaptiveHomingMissile.screenrect = SCREENRECT

                HomingMissile.containers = GL.All, GL.enemy_group
                HomingMissile.images = STINGER_MISSILE.sprite
                HomingMissile.screenrect = SCREENRECT
                mouse_pos = pygame.mouse.get_pos()
                target.rect.center = mouse_pos
                target.pos = mouse_pos

                hm = HomingMissile(player_=GL.player,
                                   target_=target,
                                   weapon_=STINGER_MISSILE,
                                   gl_=GL,
                                   offset_=GL.player.rect.center,
                                   nuke_=False, propulsion_=True,
                                   timing_=0)
                GL.GROUP_UNION.add(hm)

                # missile moving clockwise
                em = AdaptiveHomingMissile(
                    player_=GL.player,
                    gl_=GL,
                    weapon_=STINGER_MISSILE,  # Weapon class
                    shooter_=GL.player.rect,  # shooter rectangle
                    shoot_angle_=250,  # shooting angle
                    target_pool_=GL.PLAYER_GROUP,  # Player group as target
                    offset_=pygame.math.Vector2(-20, +30),  # launch offset
                    timing_=15,  # Refreshing time
                    target_=target,
                    propulsion_=True,  # delay propulsion
                    layer_=-2)  # Sprite layer))
                GL.GROUP_UNION.add(em)

                # missile moving anti-clockwise
                em = AdaptiveHomingMissile(
                    player_=GL.player,
                    gl_=GL,
                    weapon_=STINGER_MISSILE,  # Weapon class
                    shooter_=GL.player.rect,  # shooter rectangle
                    shoot_angle_=290,  # shooting angle
                    target_pool_=GL.PLAYER_GROUP,  # Player group as target
                    offset_=pygame.math.Vector2(20, 30),  # launch offset
                    timing_=15,  # Refreshing time
                    target_=target,
                    propulsion_=True,  # delay propulsion
                    layer_=-2)  # Sprite layer))
                GL.GROUP_UNION.add(em)

                InterceptHomingMissile.containers = GL.enemy_group, GL.All
                InterceptHomingMissile.images = STINGER_MISSILE.sprite
                InterceptHomingMissile.screenrect = SCREENRECT
                # missile going straight ahead
                em = InterceptHomingMissile(
                    player_=GL.player,
                    gl_=GL,
                    weapon_=STINGER_MISSILE,  # Weapon class
                    shooter_=GL.player.rect,  # shooter rectangle
                    shoot_angle_=90,  # shooting angle
                    target_pool_=GL.PLAYER_GROUP,  # Player group as target
                    offset_=pygame.math.Vector2(0, 0),  # launch offset
                    timing_=15,  # Refreshing time
                    target_=target,
                    propulsion_=False,  # delay propulsion
                    layer_=-2)  # Sprite layer))
                GL.GROUP_UNION.add(em)

                # missile going straight ahead
                em = AdaptiveHomingMissile(
                    player_=GL.player,
                    gl_=GL,
                    weapon_=STINGER_MISSILE,  # Weapon class
                    shooter_=GL.player.rect,  # shooter rectangle
                    shoot_angle_=90,  # shooting angle
                    target_pool_=GL.PLAYER_GROUP,  # Player group as target
                    offset_=pygame.math.Vector2(0, 0),  # launch offset
                    timing_=15,  # Refreshing time
                    target_=target,
                    propulsion_=False,  # delay propulsion
                    layer_=-2)  # Sprite layer))
                GL.GROUP_UNION.add(em)

        if keys[pygame.K_PAUSE]:
            GL.PAUSE = True
        # print('game is pause')

        SCREEN.blit(BACKGROUND, (0, 0))

        GL.All.update()


        if len(VERTEX_ARRAY_MP) > 0:
            missile_particles(GL.screen, dt)

        GL.All.draw(SCREEN)

        # Cap the speed at 60 FPS
        GL.TIME_PASSED_SECONDS = clock.tick(MAXFPS)
        dt += GL.TIME_PASSED_SECONDS
        if dt >= 16.0:
            dt = GL.TIME_PASSED_SECONDS

        pygame.display.flip()

        if recording:
            VIDEO.append(pygame.image.tostring(SCREEN, 'RGB', False))

        GL.SC_spaceship.update()
        GL.SC_explosion.update()

        # print(clock.get_fps(), len(VERTEX_ARRAY_MP), GL.FRAME)

        GL.FRAME += 1

    # Create a video
    # convert all the image into a AVI file (with 60 fps)

    if recording:
        import cv2
        from cv2 import COLOR_RGBA2BGR

        import os
        import numpy


        video = cv2.VideoWriter('Video.avi',
                                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (SCREENRECT.w, SCREENRECT.h), True)


        class BuildVideo(object):
            Video_Icon = None  # Sound icon in the volume control
            Indicator = None

            def __init__(self,
                         play_,
                         scale_=1  # Image re-scaling, scale_ = 1 no rescaling
                         ):
                self.length, self.height = 350 * scale_, 72 * scale_
                self.canvas = pygame.Surface((self.length, self.height)).convert()
                self.canvas.fill((28, 40, 32, 20))

                if scale_ != 1:
                    w, h = self.Video_Icon.get_size()
                    self.Video_Icon = pygame.transform.smoothscale(self.Video_Icon,
                                                                   (int(w * scale_), int(h * scale_)))
                    w, h = self.Indicator.get_size()
                    self.Indicator = pygame.transform.smoothscale(self.Indicator,
                                                                  (int(w * scale_), int(h * scale_)))

                w, h = self.Video_Icon.get_size()
                self.canvas.blit(self.Video_Icon, (int(2.85 * self.length / 100),
                                                   (self.canvas.get_height() - h) // 2))

                w, self.h = self.Indicator.get_size()
                self.volume = play_
                self.value = 255
                self.th = None
                self.flag = False
                self.image = None
                self.scale = scale_
                self.update_volume(play_)

            def update_volume(self, play_):
                can = self.canvas.copy()
                for level in range(int(play_ * 10)):
                    can.blit(self.Indicator,
                             (int(22.85 * self.length / 100) + (level * 25 * self.scale),
                              (self.canvas.get_height() - self.h) // 2))
                self.value = 255
                self.flag = False
                can.set_alpha(self.value)
                self.image = can


        level_icon = pygame.image.load('switchGreen04.png').convert_alpha()
        level_icon = pygame.transform.rotozoom(level_icon, 90, 0.7)

        BuildVideo.Video_Icon = pygame.image.load('video1.png').convert_alpha()
        BuildVideo.Video_Icon = pygame.transform.smoothscale(BuildVideo.Video_Icon, (64, 64))
        BuildVideo.Indicator = level_icon

        font = freetype.Font('ARCADE_R.ttf', size=15)
        rect1 = font.get_rect("Video capture, please wait...ESC to stop", style=freetype.STYLE_NORMAL, size=15)
        rect1.center = (SCREENRECT.centerx - rect1.w // 2, SCREENRECT.centery - rect1.h // 2)
        font.render_to(GL.screen, rect1.center, "Video capture, please wait...ESC to stop",
                       fgcolor=pygame.Color(255, 255, 255), size=15)
        pygame.display.flip()

        counter = 0
        video_bar = BuildVideo(0, 0.4)
        for event in pygame.event.get():
            pygame.event.clear()

        for image in VIDEO:

            video_bar.update_volume(counter / len(VIDEO))
            SCREEN.blit(video_bar.image, ((SCREENRECT.w >> 1) - 175 // 2, (SCREENRECT.h >> 1) + 25))
            image = numpy.fromstring(image, numpy.uint8).reshape(SCREENRECT.h, SCREENRECT.w, 3)
            image = cv2.cvtColor(image, COLOR_RGBA2BGR)
            video.write(image)

            counter += 1
            pygame.display.flip()

        cv2.destroyAllWindows()
        video.release()
    pygame.quit()
