# -*- coding: utf-8 -*-

try:
    import pygame
except ImportError:
    raise ImportError("\npygame library is missing on your system."
                      "\nTry: \n   C:\\pip inatall pygame on a window command prompt.")

from pygame import RLEACCEL, Surface, Color
from pygame import freetype
try:
    import numpy
except ImportError:
    raise ImportError("\nnumpy library is missing on your system."
                      "\nTry: \n   C:\\pip install numpy on a window command prompt.")
from numpy import uint8, fromstring, frombuffer

try:
    from cv2 import COLOR_RGBA2BGR, cvtColor, VideoWriter, destroyAllWindows, VideoWriter_fourcc
except ImportError:
    raise ImportError("\nOpenCv library is missing on your system."
                      "\nTry: \n   C:\\pip install opencv-python on a window command prompt.")
from math import pi
try:
    from matplotlib import pyplot as plt
except ImportError:
    raise ImportError("\nmatplotlib library is missing on your system."
                      "\nTry: \n   C:\\pip install matplotlib on a window command prompt.")

try:
    from MissileParticleFx import VERTEX_ARRAY_MP
except ImportError:
    raise ImportError("\nMissileParticleFx library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")

try:
    from CythonGlobalVar import CONSTANTS
except ImportError:
    raise ImportError("\nCythonGlobalVar library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")

DEG_TO_RAD = pi / 180.0
RAD_TO_DEG = 1 / DEG_TO_RAD

GL = CONSTANTS()


SCREENRECT = pygame.Rect(0, 0, 800, 1024)
GL.SCREENRECT = SCREENRECT
pygame.display.init()
SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWSURFACE, 32)
GL.SCREEN = SCREEN
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4095)
freetype.init(cache_size=64, resolution=72)
try:
    from SoundServer import SoundControl
except ImportError:
    raise ImportError("\nSoundServer library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")
try:
    from Sprites import Sprite, LayeredUpdatesModified, Group
except ImportError:
    raise ImportError("\nSprites library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")
try:
    from Weapon import HomingMissile, ExtraAttributes, InterceptMissile, AdaptiveMissile
except ImportError:
    raise ImportError("\nWeapon library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")
try:
    from Enemy import EnemyClass
except ImportError:
    raise ImportError("\nEnemy library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")
try:
    from Player import PlayerClass
except ImportError:
    raise ImportError("\nPlayer library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")
try:
    from XML_parsing import xml_get_weapon
except ImportError:
    raise ImportError("\nXML_parsing library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")
try:
    from Textures import *
except ImportError:
    raise ImportError("\nTextures library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")
try:
    from Sounds import *
except ImportError:
    raise ImportError("\nSounds library is missing on your system or is not cynthonized."
                      "\nTry: \n   C:\\python setup_Project.py build_ext --inplace")


def xml_parsing(xml_features):
    weapon_features = {}
    for key, value in xml_features.items():

        if key == "image":
            try:
                weapon_features[key] = eval(value)
            except NameError:
                raise NameError('\nSprite %s image %s not loaded into memory!' % (key, value))

        elif key == "sprite_rotozoom":
            try:
                weapon_features[key] = eval(value)
            except NameError:
                raise NameError('\nSprite %s image %s not loaded into memory!' % (key, value))

        elif key == "propulsion_sound_fx":
            try:
                weapon_features[key] = eval(value)
            except NameError:
                raise NameError('Pygame %s sound %s not loaded into memory!' % (key, value))
        elif key == "missile_trail_fx":
            try:
                weapon_features[key] = eval(value)
            except NameError:
                raise NameError('Pygame %s is %s not loaded into memory!' % (key, value))

        elif key == "missile_trail_fx_blend":
            try:
                weapon_features[key] = eval(value)
            except NameError:
                raise NameError('Pygame %s is %s cannot be evaluated!' % (key, value))

        elif key == 'animation':
            try:
                value = int(value)
            except (ValueError, TypeError):
                value = None
            weapon_features[key] = value

        elif key == "bingo_range":
            weapon_features[key] = tuple(eval(value))

        elif key == 'range':
            weapon_features[key] = eval(value)

        elif key in ("name", "type"):
            weapon_features[key] = str(value)

        elif key == 'velocity':
            weapon_features[key] = pygame.math.Vector2(float(value), float(value))

        elif key == 'detonation_dist':
            try:
                det = int(key)
            except ValueError:
                det = None
            weapon_features[key] = det
        else:
            try:
                weapon_features[key] = int(value)
            except ValueError:
                try:
                    weapon_features[key] = float(value)
                except ValueError:
                    raise ValueError('\nData not understood %s %s ' % (key, value))
    return weapon_features


if __name__ == '__main__':
        SCREENRECT = pygame.Rect(0, 0, 800, 1024)
        GL.SCREENRECT = SCREENRECT
        pygame.display.init()
        SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWACCEL, 32)
        GL.SCREEN = SCREEN
        pygame.init()
        pygame.mixer.pre_init(44100, 16, 2, 4095)

        BACKGROUND = pygame.image.load('Assets\\A2.png').convert(32, pygame.RLEACCEL)
        BACKGROUND.set_alpha(None)

        clock = pygame.time.Clock()
        GL.TIME_PASSED_SECONDS = clock.tick(GL.MAX_FPS)

        All = LayeredUpdatesModified()

        # ALL SPRITES (class LayerUpdateModified Group)
        GL.ALL = All
        # PLAYER GROUPS (Class Group)
        GL.PLAYER_GROUP = Group()
        GL.PLAYER_PROJECTILE = Group()
        # BOTH (Class Group)
        GL.GROUP_UNION = Group()
        # ENEMY GROUPS (Class Group)
        GL.ENEMY_GROUP = Group()
        GL.ENEMY_PROJECTILE = Group()
        GL.MIXER_PLAYER = SoundControl(GL.SCREENRECT, 10)
        GL.MIXER_EXPLOSION = SoundControl(GL.SCREENRECT, 10)
        GL.SOUND_LEVEL = 1.0

        # LOAD THE WEAPON STINGER FROM XML FILE
        STINGER_XML = dict(xml_get_weapon('Weapon.xml', 'STINGER'))
        BUMBLEBEE_XML = dict(xml_get_weapon('Weapon.xml', 'BUMBLEBEE'))
        WASP_XML = dict(xml_get_weapon('Weapon.xml', 'WASP'))
        HORNET_XML = dict(xml_get_weapon('Weapon.xml', 'HORNET'))

        STINGER_FEATURES = xml_parsing(STINGER_XML)
        BUMBLEBEE_FEATURES = xml_parsing(BUMBLEBEE_XML)
        WASP_FEATURES = xml_parsing(WASP_XML)
        HORNET_FEATURES = xml_parsing(HORNET_XML)

        GL.PLAYER = PlayerClass(containers_=(GL.ALL, GL.PLAYER_GROUP),
                                image_=COBRA,
                                pos_=(SCREENRECT.centerx, SCREENRECT.bottom - 300),
                                gl_=GL, timing_=60.0, layer_=0, _blend=0)

        # CREATE AN ENEMY INSTANCE
        # The enemy will belongs to GL.ALL and GL.GROUP_UNION
        target = EnemyClass(containers_=(GL.ALL, GL.GROUP_UNION),
                            image_=SPACE_FIGHTER_SPRITE,
                            pos_=(SCREENRECT.centerx, SCREENRECT.top + 100),
                            gl_=GL, timing_=60.0, layer_=0)

        # TODO OFFSET RE-DECLARE
        extra = ExtraAttributes({'target': target,
                                 'shoot_angle': 90,
                                 'ignition': False,
                                 'offset': (0, 0)})

        # TODO CHANGE THIS RELOADING TIME IS INDEXED TO STINGER ONLY
        # missile = MissileBaseClass(GL, STINGER_FEATURES)

        GL.GROUP_UNION.add(target)

        dummy = Sprite()
        dummy.image = SPACE_FIGHTER_SPRITE
        dummy.rect = dummy.image.get_rect(center=(200, 400))
        dummy = EnemyClass(containers_=(GL.ALL, GL.GROUP_UNION),
                           image_=SPACE_FIGHTER_SPRITE,
                           pos_=(GL.PLAYER.rect.centerx - 200, SCREENRECT.left - 400),
                           gl_=GL, timing_=0, layer_=0)
        GL.GROUP_UNION.add(dummy)

        STOP_GAME = False
        QUIT = False
        GL.PAUSE = False
        em = Group()
        hm = Group()

        # ALLOW RECORDING
        recording = True

        FPS_AVG = []
        RECORD_FRAMES = []  # Capture frames
        dx_right = 0
        dx_left  = 0
        dy_up    = 0
        dy_down  = 0
        pygame.key.set_repeat(100, 3)

        pygame_display_flip = pygame.display.flip
        screen_blit = SCREEN.blit
        GL_ALL_update = GL.ALL.update
        GL_ALL_draw = GL.ALL.draw
        DT = 0

        while not STOP_GAME:
            pygame.event.pump()

            ratio = GL.TIME_PASSED_SECONDS / 16.667

            keys = pygame.key.get_pressed()

            while GL.PAUSE:
                pygame.event.pump()
                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_PAUSE]:
                        GL.PAUSE = False
                        pygame.event.clear()

            for event in pygame.event.get():

                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    # target.rect.center = mouse_pos
                    # target.position = mouse_pos
                    target.update_rect(mouse_pos)
                    target.update_position(mouse_pos)
                    ...

                if event.type == pygame.KEYDOWN:
                    ...

                if event.type == pygame.KEYUP:
                    # RESET BOOST VALUES
                    dx_right = 0
                    dx_left = 0
                    dy_up = 0
                    dy_down = 0

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                STOP_GAME = True

            if keys[pygame.K_RIGHT]:
                # LINEAR INCREMENT BOOST
                dx_right += 0.05
                GL.PLAYER.rect.centerx += ((12 + dx_right) * ratio)

            if keys[pygame.K_LEFT]:
                # LINEAR INCREMENT BOOST
                dx_left += 0.05
                GL.PLAYER.rect.centerx -= ((12 + dx_left) * ratio)

            if keys[pygame.K_UP]:
                dy_up += 0.05
                GL.PLAYER.rect.centery -= ((8 + dy_up) * ratio)

            if keys[pygame.K_DOWN]:
                dy_down += 0.05
                GL.PLAYER.rect.centery += ((8 + dy_down) * ratio)

            if keys[pygame.K_F8]:
                pygame.image.save(SCREEN, 'Screendump' + str(GL.FRAME) + '.png')

            if keys[pygame.K_SPACE]:

                if GL.PLAYER.rect.colliderect(SCREENRECT):
                    player = GL.PLAYER
                    if not player.is_missile_reloading(
                            STINGER_FEATURES['reloading_time'] * 1000 / GL.TIME_PASSED_SECONDS):

                        extra = ExtraAttributes({'target': target,
                                                 'shoot_angle': -90,
                                                 'ignition': False,
                                                 'offset': (-25, 25)})
                        HomingMissile(
                            gl_=GL,
                            group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                            weapon_features_=STINGER_FEATURES,
                            extra_attributes=extra,
                            timing_=60,
                            _blend=0
                            )

                        extra = ExtraAttributes({'target': target,
                                                 'shoot_angle': -90,
                                                 'ignition': False,
                                                 'offset': (25, 25)})
                        HomingMissile(
                            gl_=GL,
                            group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                            weapon_features_=BUMBLEBEE_FEATURES,
                            extra_attributes=extra,
                            timing_=60,
                            _blend=0
                        )
                        extra = ExtraAttributes({'target': target,
                                                 'shoot_angle': -90,
                                                 'ignition': False,
                                                 'offset': (25, 25)})
                        HomingMissile(
                            gl_=GL,
                            group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                            weapon_features_=WASP_FEATURES,
                            extra_attributes=extra,
                            timing_=60,
                            _blend=0
                        )

                        extra = ExtraAttributes({'target': target,
                                                 'shoot_angle': -90,
                                                 'ignition': False,
                                                 'offset': (25, 25)})
                        HomingMissile(
                            gl_=GL,
                            group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                            weapon_features_=HORNET_FEATURES,
                            extra_attributes=extra,
                            timing_=60,
                            _blend=0
                        )

                        #  ---------------------------------------------------------

                        # extra = ExtraAttributes({'target'     : target,
                        #                          'shoot_angle': -90,
                        #                          'ignition'   : False,
                        #                          'offset'     : (25, 25)})

                        # InterceptMissile(
                        #     gl_=GL,
                        #     group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                        #     weapon_features_=BUMBLEBEE_FEATURES,
                        #     extra_attributes=extra,
                        #     timing_=60.0,
                        #     _blend=pygame.BLEND_RGB_ADD)
                        #
                        # extra = ExtraAttributes({'target': target,
                        #                          'shoot_angle': -90,
                        #                          'ignition': False,
                        #                          'offset': (-25, 25)})
                        #
                        # InterceptMissile(
                        #     gl_=GL,
                        #     group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                        #     weapon_features_=BUMBLEBEE_FEATURES,
                        #     extra_attributes=extra,
                        #     timing_=60.0,
                        #     _blend=0)
                        #  -------------------------------------------------------

                        # extra = ExtraAttributes({'target': target,
                        #                          'shoot_angle': 90,
                        #                          'ignition': False,
                        #                          'offset': (25, 25)})
                        #
                        # AdaptiveMissile(
                        #     gl_=GL,
                        #     group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                        #     weapon_features_=BUMBLEBEE_FEATURES,
                        #     extra_attributes=extra,
                        #     timing_=60.0)
                        #
                        # extra = ExtraAttributes({'target': target,
                        #                          'shoot_angle': 90,
                        #                          'ignition': False,
                        #                          'offset': (-25, 25)
                        #                          })
                        #
                        # AdaptiveMissile(
                        #     gl_=GL,
                        #     group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                        #     weapon_features_=STINGER_FEATURES,
                        #     extra_attributes=extra,
                        #     timing_=60.0)

                        player.launch_missile()

            if keys[pygame.K_PAUSE]:
                GL.PAUSE = True

            SCREEN.blit(BACKGROUND, (0, 0))

            GL_ALL_update()

            # display the all missile particles
            # if any in the VERTEX_ARRAY_MP
            if len(VERTEX_ARRAY_MP) > 0:
                for particle in VERTEX_ARRAY_MP:
                    particle.update(SCREEN, SCREENRECT)

            GL.ALL.draw(SCREEN)

            # Cap the speed at 60 FPS
            GL.TIME_PASSED_SECONDS = clock.tick_busy_loop(GL.MAX_FPS)
            # print('TIME PASSED SECONDS : ', GL.TIME_PASSED_SECONDS)
            t = clock.get_fps()
            if t != 0:
                FPS_AVG.append(t)
            # print(clock.get_fps())
            pygame_display_flip()

            if recording:
                if GL.MAX_FPS > 60:
                    if DT >= 1000 / 60:
                        RECORD_FRAMES.append(pygame.image.tostring(SCREEN, 'RGB', False))
                        DT = 0
                else:
                    RECORD_FRAMES.append(pygame.image.tostring(SCREEN, 'RGB', False))

            GL.MIXER_PLAYER.update()
            GL.MIXER_EXPLOSION.update()

            # print(clock.get_fps()) # , len(VERTEX_ARRAY_MP), GL.FRAME)
            # print(len(GL.PLAYER_GROUP), len(GL.GROUP_UNION))
            GL.FRAME += 1
            GL.SCREEN = SCREEN

            DT += GL.TIME_PASSED_SECONDS

        # Create a video
        # convert all the image into a AVI file (with 60 fps)
        print('AVG FPS', sum(FPS_AVG)/GL.FRAME, 'MAX ', max(FPS_AVG), "MIN ", min(FPS_AVG))

        if recording:

            video = VideoWriter(
                'Video.avi', VideoWriter_fourcc('M', 'J', 'P', 'G'),
                60, (SCREENRECT.w, SCREENRECT.h), True)


            class VideoMeter(object):

                def __init__(self, video_icon_, indicator_, volume_, scale_=1, color_=Color(28, 40, 32, 20)):
                    self.video_icon  = video_icon_
                    self.indicator   = indicator_
                    self.volume      = volume_
                    self.scale       = scale_
                    self.width       = 350 * scale_
                    self.height      = 72  * scale_
                    self.canvas      = Surface(
                        (self.width, self.height)).convert(32, RLEACCEL)
                    self.canvas.fill(color_)

                    if scale_ != 1.0:
                        vw, vh = self.video_icon.get_size()
                        self.video_icon = smoothscale(
                            self.video_icon, (int(vw * scale_), int(vh * scale_)))
                        iw, ih = self.indicator.get_size()
                        self.indicator = smoothscale(
                            self.indicator, (int(iw * scale_), int(ih * scale_)))

                    vw, vh = self.video_icon.get_size()
                    self.canvas.blit(self.video_icon, (int(2.85 * self.width / 100.0),
                                                       (self.height - vh) // 2))

                    self.w, self.h = self.indicator.get_size()

                    self.value = 255
                    self.image = None
                    self.update_meter(volume_)

                def update_meter(self, vol_):

                    canvas = self.canvas.copy()
                    canvas_blit = canvas.blit
                    c1 = int(22.85 * self.width / 100.0)
                    c2 = float(25.0 * self.scale)
                    c3 = (self.height - self.h) // 2
                    for level in range(int(vol_ * 10)):
                        canvas_blit(self.indicator, (c1 + int(level * c2), c3))
                    self.value = 255
                    canvas.set_alpha(self.value)
                    self.image = canvas

            FONT.render_to(SCREEN, RECT1.center,
                           "Video capture, please wait...ESC to stop",
                           fgcolor=pygame.Color(255, 255, 255), size=15)

            pygame.display.flip()

            counter = 0
            video_bar = VideoMeter(VIDEO_ICON, LEVEL_ICON, 0, 0.4)

            c1 = len(RECORD_FRAMES)
            print(c1)
            c2 = (SCREENRECT.w >> 1) - 175 // 2
            c3 = (SCREENRECT.h >> 1) + 25

            assert c1 != 0, '\nRecorded video has no frames!.'

            pygame.event.clear()


            for image in RECORD_FRAMES:

                pygame.event.pump()


                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        raise SystemExit

                video_bar.update_meter(counter / c1)
                screen_blit(video_bar.image, (c2, c3))
                image = frombuffer(image, uint8).reshape(SCREENRECT.h, SCREENRECT.w, 3)
                # image = numpy.frombuffer(image, dtype=numpy.uint8).reshape(SCREENRECT.h, SCREENRECT.w, 4)
                # image_ = numpy.array(image, dtype=numpy.uint8).transpose(1, 0, 2)
                # SCREEN.fill((0, 0, 0, 0))
                # SCREEN.blit(pygame.image.frombuffer(image_, (SCREENRECT.w, SCREENRECT.h), 'RGB'), (0, 0))
                image = cvtColor(image, COLOR_RGBA2BGR)
                video.write(image)
                pygame_display_flip()
                counter += 1

            destroyAllWindows()
            video.release()

        plt.plot(FPS_AVG)
        plt.title("FPS AVG")
        plt.draw()
        plt.show()

        pygame.quit()


# import math
# def missile_lead_angle(p1: pygame.math.Vector2,  # Start of vector1 position
#                        p2: pygame.math.Vector2,  # start of vector2 position
#
#                        v1: pygame.math.Vector2,  # Euclidean vector, vector projections representing the missile
#                        # vector.
#                        v2: pygame.math.Vector2):  # Euclidean vector, vector projections representing the target
#     # vector.
#     """
#     Determine the collision missile lead angle
#     :param p1: Point1
#     :param p2: Point2
#     :param v1: missile vector
#     :param v2: target vector
#     :return: Returns missile vector and collision point
#     In computer geometry, always use vectors if possible!
#     Code gets more complicated if you try to work with Cartesian co-ordinates
#     (x,y) or with line equations y=mx+b.
#     Here, for example, you have special cases for horizontal lines, m=0, and vertical lines, m=∞.
#     So let's try to program this, sticking to vectors throughout.
#     First, let's review the problem. We have a line segment from p1.p to p2.p and we want to find
#     the points of intersection with a circle centred at self.p and radius self.r. I'm going to write these as
#     p1, p2, q, and r respectively.
#
#     Any point on the line segment can be written p1+t(p2−p1)for a
#     scalar parameter t between 0 and 1. We'll be using p2−p1 often, so let's write v=p2−p1.
#     Let's set this up in Python. I'm assuming that all the points are pygame.math.Vector2 objects,
#     so that we can add them and take dot products and so on.
#     I'm also assuming that we're using Python 3, so that division returns a float
#
#     Q is the centre of circle (pygame.math.Vector2)
#     r is the radius           (scalar)
#     p1 constraint.point1      (pygame.math.Vector2), start of the line segment
#     v constraint.point2 - p1  (pygame.math.Vector2), vector along line segment
#     Now, a point x is on the circle if its distance from the centre of the circle is equal
#     to the circle's radius, that is, if
#     |x - q| = r
#     So the line intersects the circle when
#     |p1 + tv - q| = r
#     Squaring both sides gives
#     |p1 + tv - q| **2 = r ** 2
#     Expanding the dot product and collecting powers of t gives
#     t ** 2 (v.v) + 2t(v.(p1 - q)) + (p1.p1 + q.q - 2p1.q - r**2) = 0
#     which is a quadratic equation in t with coefficients
#     a = v.v
#     b = 2(v.(p1 - q))
#     c = p1.p1 + q.q - 2p1.q - r ** 2
#     and solutions
#     t = (-b +/- math.sqrt(b ** 2 - 4 * a * c)) / 2 * a
#
#     a = V.dot(V)
#     b = 2 * V.dot(P1 - Q)
#     c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r ** 2
#     The value b2−4ac inside the square root is known as the discriminant.
#     If this is negative, then there are no real solutions to the quadratic equation;
#     that means that the line misses the circle entirely.
#
#     disc = b**2 - 4 * a * c
#     if disc < 0:
#         return False, None
#
#     Otherwise, let's call the two solutions t1 and t2.
#     sqrt_disc = math.sqrt(disc)
#     t1 = (-b + sqrt_disc) / (2 * a)
#     t2 = (-b - sqrt_disc) / (2 * a)
#
#     If neither of these is between 0 and 1, then the line segment misses the circle (but would hit it if extended):
#     if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
#     return False, None
#
#     Now, the closest point on the extended line to the centre of the circle is
#     p1+tv where
#     t= ((q−p1)⋅v) / (|v| ** 2) = −b / 2a
#
#     But we want to ensure that the point is on the line segment, so we must clamp
#     t to lie between 0 and 1.
#     t = max(0, min(1, - b / (2 * a)))
#     return True, P1 + t * V
#
#     """
#     # todo check if v1 and v2 should be normalised
#     v = p2 - p1
#     q = p2 + v2  # circle centre
#     r = v1.length()  # circle radius
#
#     a = v.dot(v)
#     if a == 0:
#         return None, None, None
#
#     b = 2 * v.dot(p1 - q)
#     c = p1.dot(p1) + q.dot(q) - 2 * p1.dot(q) - r ** 2
#     disc = b ** 2 - 4 * a * c
#
#     if disc < 0:
#         return None, None, None
#
#     disc_sqrt = math.sqrt(disc)
#     t1 = (-b + disc_sqrt) / (2 * a)  # first intersection between the line and circle
#     t2 = (-b - disc_sqrt) / (2 * a)  # second intersection between the line and circle
#
#     if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
#         return None, None, None
#
#     i1 = p1 + t1 * v  # intersection 1 in the Cartesian plane
#     i2 = p1 + t2 * v  # intersection 2 in the Cartesian plane
#
#     # Determine the closest point from p1 (missile).
#     if p1.distance_to(i1) > p1.distance_to(i2):
#         intersection = i2
#     else:
#         intersection = i1
#
#     vector = q - intersection
#     angle = math.degrees(math.atan2(vector.y, vector.x))
#
#     dist1 = intersection.distance_to(p2)  # scalar distance from p2 and intersection
#     dist2 = p1.distance_to(p2)  # scalar distance between p1 and p2
#     # todo div zero
#     ratio = dist2 / dist1  # ratio
#
#     collision = p1 + ratio * vector
#     # parametric equation
#     # p1 + t * vector
#
#     return p1, vector, collision


# p1 = pygame.math.Vector2(5, 1)
# p2 = pygame.math.Vector2(10, 5)
# v1 = pygame.math.Vector2(1, 1)
# v2 = pygame.math.Vector2(-1, 1)
# import timeit
# from Weapon import lead_collision, lead_collision
#
# N = 1000000
# print(timeit.timeit("lead_collision(p1.x, p1.y, p2.x, p2.y, v1.x, v1.y, v2.x, v2.y)",
#                     "from __main__ import lead_collision, p1, p2, v1, v2", number=N)/N)
#
# print(timeit.timeit("missile_lead_angle(p1, p2, v1, v2)",
#                     "from __main__ import missile_lead_angle, p1, p2, v1, v2", number=N)/N)
#
# print(timeit.timeit("lead_collision(p1.x, p1.y, p2.x, p2.y, v1.x, v1.y, v2.x, v2.y)",
#                     "from __main__ import lead_collision, p1, p2, v1, v2", number=N)/N)