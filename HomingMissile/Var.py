# encoding: utf-8


"""
                 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Copyright Yoann Berenguer
"""


from pygame import SCALED, FULLSCREEN

try:
    import pygame
except ImportError:
    raise ImportError("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")

pygame.display.init()
pygame.mixer.init()

# Load missile sound effect (launch)

try:
    STINGER_EXHAUST_SOUND = pygame.mixer.Sound('Assets\\sd_weapon_missile_heavy_01.wav')
except (FileExistsError, FileNotFoundError, ImportError):
    print("\nSound file sd_weapon_missile_heavy_01.wav is missing from Assets directory")

VERTEX_ARRAY_MP = []

DEG_TO_RAD = 3.14159265358979323846 / 180.0
RAD_TO_DEG = 1.0 / DEG_TO_RAD
M_PI = 3.14159265358979323846
M_PI2 = 3.14159265358979323846 / 2.0


class CONSTANTS:
    """
    DEFINE YOUR GAME VARIABLES AND CONSTANT

    To access your variables
    1) Create first an instance of the class
        GL = CONSTANTS()
    2) Access the variable
        GL.MAX_FPS      -> point to MAX_FPS VAR

    """

    def __init__(self):
        self.MAX_FPS                 = 65
        self.SC_EXPLOSION            = None
        self.SOUND_LEVEL             = 1.0
        try:
            self.TIME_PASSED_SECONDS     = 1000.0/self.MAX_FPS
        except ZeroDivisionError:
            raise ValueError('\nMAX_FPS cannot be zero !')
        self.FRAME                   = 0
        self.SCREENRECT              = pygame.Rect(0, 0, 800, 600)
        self.PAUSE                   = False
        self.SCREEN                  = pygame.display.set_mode(self.SCREENRECT.size, SCALED, 32)
        self.ALL                     = None
        self.PLAYER_GROUP            = None
        self.PLAYER_PROJECTILE       = None
        self.GROUP_UNION             = None
        self.ENEMY_GROUP             = None
        self.ENEMY_PROJECTILE        = None
        self.MIXER_EXPLOSION         = None
        self.PLAYER                  = None

        # MIXER SETTINGS
        self.FREQUENCY               = 48000
        self.FORMAT                  = -16
        self.CHANNELS                = 2

    def show_all_attributes(self):
        return self.__dict__