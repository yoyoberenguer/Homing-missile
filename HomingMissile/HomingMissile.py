# encoding: utf-8


"""
                 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Copyright Yoann Berenguer
"""

import math
import time

try:
    import pygame
except ImportError:
    raise ImportError("\npygame library is missing on your system."
                      "\nTry: \n   C:\\pip install pygame on a window command prompt.")

from pygame import freetype

try:
    import numpy
except ImportError:
    raise ImportError("\nnumpy library is missing on your system."
                      "\nTry: \n   C:\\pip install numpy on a window command prompt.")


pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4095)

freetype.init(cache_size=64, resolution=72)
from SoundServer import SoundControl      # --> require the pygame.mixer to be init first
from Var import CONSTANTS, STINGER_EXHAUST_SOUND, VERTEX_ARRAY_MP, RAD_TO_DEG

from Sprites import Sprite, LayeredUpdatesModified, Group
from Enemy import EnemyClass
from Player import PlayerClass
from Weapon import HomingMissile, ExtraAttributes, InterceptMissile, AdaptiveMissile
from XML_parsing import xml_get_weapon


GL = CONSTANTS()
SCREENRECT = GL.SCREENRECT
SCREEN = GL.SCREEN


from Textures import *                    # --> require pygame display mode to be init first


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
                weapon_features[key] = eval(value).copy()
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


FONT = pygame.font.SysFont("Arial", 15)


def show_fps(screen_, fps_, avg_) -> list:
    """ Show framerate in upper left corner """

    fps = str(f"CPU fps:{fps_:.3f}")
    av = sum(avg_)/len(avg_) if len(avg_) > 0 else 0

    fps_text = FONT.render(fps, 1, pygame.Color("green"))
    screen_.blit(fps_text, (10, 0))
    if av != 0:
        av = str(f"avg:{av:.3f}")
        avg_text = FONT.render(av, 1, pygame.Color("green"))
        screen_.blit(avg_text, (120, 0))
    if len(avg_) > 200:
        avg_ = avg_[200:]
    return avg_


def show_heading(screen_, heading, target_angle) -> None:
    """ Show framerate in upper left corner """

    mh = str(f"Mis heading:{heading:.3f}")
    mh_text = FONT.render(mh, 1, pygame.Color("red"))

    th = str(f"Tar heading:{target_angle:.3f}")
    th_text = FONT.render(th, 1, pygame.Color("green"))

    zh = str(f"px :{len(VERTEX_ARRAY_MP):.1f}")
    zh_text = FONT.render(zh, 1, pygame.Color("green"))

    screen_.blit(mh_text, (10, 20))
    screen_.blit(th_text, (10, 40))
    screen_.blit(zh_text, (10, 60))


def get_angle(target_centre, missile_centre):
    dx = target_centre.x - missile_centre.x
    dy = target_centre.y - missile_centre.y
    return -int(RAD_TO_DEG * math.atan2(dy, dx)) % 360


if __name__ == '__main__':
    import os
    screen_position = (0, 0)
    os.environ['SDL_VIDEODRIVER'] = 'directx'
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(screen_position[0]) + "," + str(screen_position[1])
    print(pygame.display.Info())
    clock = pygame.time.Clock()
    GL.TIME_PASSED_SECONDS = clock.tick(GL.MAX_FPS)

    All = LayeredUpdatesModified()

    GL.ALL = All
    GL.PLAYER_GROUP = Group()
    GL.PLAYER_PROJECTILE = Group()
    GL.GROUP_UNION = Group()
    GL.ENEMY_GROUP = Group()
    GL.ENEMY_PROJECTILE = Group()
    GL.MIXER_PLAYER = SoundControl(GL.SCREENRECT, 10)
    GL.MIXER_EXPLOSION = SoundControl(GL.SCREENRECT, 10)
    GL.SOUND_LEVEL = 1.0

    # Load the missile from xml file
    STINGER_XML = dict(xml_get_weapon('Weapon.xml', 'STINGER'))
    BUMBLEBEE_XML = dict(xml_get_weapon('Weapon.xml', 'BUMBLEBEE'))
    WASP_XML = dict(xml_get_weapon('Weapon.xml', 'WASP'))
    HORNET_XML = dict(xml_get_weapon('Weapon.xml', 'HORNET'))

    # Parse the values into dictionaries
    STINGER_FEATURES = xml_parsing(STINGER_XML)
    BUMBLEBEE_FEATURES = xml_parsing(BUMBLEBEE_XML)
    WASP_FEATURES = xml_parsing(WASP_XML)
    HORNET_FEATURES = xml_parsing(HORNET_XML)

    # Init the player instance
    GL.PLAYER = PlayerClass(containers_ = (GL.ALL, GL.PLAYER_GROUP),
                            image_      = PLAYER_AIRCRAFT,
                            pos_        = (SCREENRECT.centerx, SCREENRECT.bottom - 50),
                            gl_         = GL,
                            timing_     = 60.0,
                            layer_      = 0,
                            _blend      = 0)

    # Init the enemy (missile target)
    target = EnemyClass(containers_ = (GL.ALL, GL.GROUP_UNION),
                        image_      = SPACE_FIGHTER_SPRITE,
                        pos_        = (SCREENRECT.centerx, SCREENRECT.top + 100),
                        gl_         = GL,
                        timing_     = 60.0,
                        layer_      = 0)

    GL.GROUP_UNION.add(target)

    STOP_GAME = False
    QUIT = False
    GL.PAUSE = False

    FPS_AVG = []

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
    s = None
    lock = 0
    while not STOP_GAME:

        pygame.event.pump()

        ratio = GL.TIME_PASSED_SECONDS / 16.667

        keys = pygame.key.get_pressed()

        if keys[pygame.K_PAUSE]:
            lock = time.time()

        while time.time() - lock < 2:
            ...

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
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

        if keys[pygame.K_SPACE]:

            if GL.PLAYER.rect.colliderect(SCREENRECT):

                player = GL.PLAYER
                if not player.is_missile_reloading(
                        STINGER_FEATURES['reloading_time'] * 1000 / GL.TIME_PASSED_SECONDS):

                    extra = ExtraAttributes(
                        {'target': target,
                         'shoot_angle': 90,
                         'ignition': False,
                         'offset': (-30, 0)})

                    s = HomingMissile(
                        gl_=GL,
                        group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                        weapon_features_=BUMBLEBEE_FEATURES,
                        extra_attributes=extra,
                        timing_=800,
                        )

                    extra = ExtraAttributes(
                        {'target': target,
                         'shoot_angle': 90,
                         'ignition': False,
                         'offset': (30, 0)})

                    s = InterceptMissile(
                        gl_=GL,
                        group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                        weapon_features_=BUMBLEBEE_FEATURES,
                        extra_attributes=extra,
                        timing_=800,
                    )

                    # extra = ExtraAttributes(
                    #     {'target': target,
                    #      'shoot_angle': -90,
                    #      'ignition': False,
                    #      'offset': (30, 0)})
                    #
                    # s = HomingMissile(
                    #     gl_=GL,
                    #     group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                    #     weapon_features_=STINGER_FEATURES,
                    #     extra_attributes=extra,
                    #     timing_=800,
                    # )
                    #
                    # extra = ExtraAttributes(
                    #     {'target': target,
                    #      'shoot_angle': -90,
                    #      'ignition': False,
                    #      'offset': (-30, 0)})
                    #
                    # s = HomingMissile(
                    #     gl_=GL,
                    #     group_=(GL.ALL, GL.PLAYER_PROJECTILE),
                    #     weapon_features_=STINGER_FEATURES,
                    #     extra_attributes=extra,
                    #     timing_=800,
                    # )

                    player.launch_missile()  # --> player fire the missile (hook method)



        SCREEN.blit(BACKGROUND, (0, 0))

        GL_ALL_update()

        # display the all missile particles
        # if any in the VERTEX_ARRAY_MP

        if len(VERTEX_ARRAY_MP) > 0:
            for particle in VERTEX_ARRAY_MP:
                particle.update(SCREEN, SCREENRECT)

        GL.ALL.draw(SCREEN)

        GL.TIME_PASSED_SECONDS = clock.tick_busy_loop(GL.MAX_FPS)
        t = clock.get_fps()

        if t != 0:
            FPS_AVG.append(t)

        FPS_AVG = show_fps(GL.SCREEN, t, FPS_AVG)

        # if s is not None:
        #     show_heading(GL.SCREEN, s.heading, get_angle(
        #         pygame.Vector2(s.target.rect.centerx, target.rect.centery),
        #         pygame.Vector2(s.rect.centerx, s.rect.centery)))

        pygame_display_flip()
        GL.MIXER_PLAYER.update()
        GL.MIXER_EXPLOSION.update()
        GL.FRAME += 1
        GL.SCREEN = SCREEN
        DT += GL.TIME_PASSED_SECONDS

    pygame.quit()
