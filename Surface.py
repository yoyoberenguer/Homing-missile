# encoding: utf-8
"""

                   GNU GENERAL PUBLIC LICENSE

                       Version 3, 29 June 2007


 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>

 Everyone is permitted to copy and distribute verbatim copies

 of this license document, but changing it is not allowed.
 """
from numpy import dstack, ndarray, uint8, int16, putmask

__author__ = "Yoann Berenguer"
__copyright__ = "Copyright 2007, Cobra Project"
__credits__ = ["Yoann Berenguer"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Yoann Berenguer"
__email__ = "yoyoberenguer@hotmail.com"

import pygame
import warnings
import math
warnings.simplefilter(action='ignore')


class ERROR(BaseException):
    pass


def make_array(rgb_array_: ndarray, alpha_: ndarray) -> ndarray:
    """
    This function is used for 24-32 bit pygame surface with pixel alphas transparency layer

    make_array(RGB array, alpha array) -> RGBA array

    Return a 3D numpy (numpy.uint8) array representing (R, G, B, A)
    values of all pixels in a pygame surface.

    :param rgb_array_: 3D array that directly references the pixel values in a Surface.
                       Only work on Surfaces that have 24-bit or 32-bit formats.
    :param alpha_:     2D array that directly references the alpha values (degree of transparency) in a Surface.
                       alpha_ is created from a 32-bit Surfaces with a per-pixel alpha value.
    :return:           Return a numpy 3D array (numpy.uint8) storing a transparency value for every pixel
                       This allow the most precise transparency effects, but it is also the slowest.
                       Per pixel alphas cannot be mixed with pygame method set_colorkey (this will have
                       no effect).
    """
    """
    assert isinstance(rgb_array_, numpy.ndarray), \
        'Expecting numpy.ndarray for argument rgb_array_ got %s ' % type(rgb_array_)
    assert isinstance(alpha_, numpy.ndarray), \
        'Expecting numpy.ndarray for argument alpha_ got %s ' % type(alpha_)
    """
    return dstack((rgb_array_, alpha_))


def make_surface(rgba_array: ndarray) -> pygame.Surface:
    """
    This function is used for 24-32 bit pygame surface with pixel alphas transparency layer

    make_surface(RGBA array) -> Surface

    Argument rgba_array is a 3d numpy array like (width, height, RGBA)
    This method create a 32 bit pygame surface that combines RGB values and alpha layer.

    :param rgba_array: 3D numpy array created with the method surface.make_array.
                       Combine RGB values and alpha values.
    :return:           Return a pixels alpha surface.This surface contains a transparency value
                       for each pixels.
    """
    return pygame.image.frombuffer((rgba_array.transpose(1, 0, 2)).copy(order='C').astype(uint8),
                                   (rgba_array.shape[:2][0], rgba_array.shape[:2][1]), 'RGBA').convert_alpha()


# Add transparency value to all pixels including black pixels
def add_transparency_all(rgb_array: ndarray, alpha_: ndarray, value: int) -> pygame.Surface:
    """
    Increase transparency of a surface
    This method is equivalent to pygame.Surface.set_alpha() but conserve the per-pixel properties of a texture
    ALL pixels will be update with a new transparency value.
    If you need to increase transparency on visible pixels only, prefer the method add_transparency instead.
    :param rgb_array:
    :param alpha_:
    :param value:
    :return:
    """
    alpha_ = alpha_.astype(int16)
    alpha_ -= value
    putmask(alpha_, alpha_ < 0, 0)

    return make_surface(make_array(rgb_array, alpha_.astype(uint8))).convert_alpha()


# Add transparency value to all pixels including black pixels
def add_transparency_all(rgb_array: ndarray, alpha_: ndarray, value: int) -> pygame.Surface:
    """
    Increase transparency of a surface
    This method is equivalent to pygame.Surface.set_alpha() but conserve the per-pixel properties of a texture
    ALL pixels will be update with a new transparency value.
    If you need to increase transparency on visible pixels only, prefer the method add_transparency instead.
    :param rgb_array:
    :param alpha_:
    :param value:
    :return:
    """
    # method 1
    """
    mask = (alpha_ >= value)
    mask_zero = (alpha_ < value)
    alpha_[:][mask_zero] = 0
    alpha_[:][mask] -= value
    return make_surface(make_array(rgb_array, alpha_.astype(numpy.uint8)))
    """
    # method 2
    alpha_ = alpha_.astype(int16)
    alpha_ -= value
    putmask(alpha_, alpha_ < 0, 0)

    return make_surface(make_array(rgb_array, alpha_.astype(uint8))).convert_alpha()


def reshape(sprite_, factor_=1.0):
    """
    Reshape a surface or every surfaces from a given array
    :param sprite_: Array full of pygame surface
    :param factor_:  can be a float (width * factor_, height * factor_) or a tuple representing the surface size
    :return: return a python array (array of surface). Surfaces conserve their transparency
    mode and bit depth
    """
    assert isinstance(sprite_, (list, pygame.Surface)), 'Argument sprite_ should be a list or a pygame.Surface.'
    assert isinstance(factor_, (tuple, float, int)), \
        'Argument factor_ should be a float, int or tuple got %s ' % type(factor_)

    if isinstance(factor_, (float, int)):
        if float(factor_) == 1.0:
            return sprite_
    else:
        assert factor_ > (0, 0)

    sprite_copy = sprite_.copy()
    if isinstance(sprite_copy, list):
        i = 0
        for surface in sprite_copy:
            w, h = sprite_[i].get_size()
            sprite_copy[i] = pygame.transform.smoothscale(surface,
                (int(w * factor_), int(h * factor_)) if isinstance(factor_, (float, int)) else factor_)
            i += 1
    else:
        w, h = sprite_.get_size()
        sprite_copy = pygame.transform.smoothscale(sprite_copy,
                (int(w * factor_), int(h * factor_)) if isinstance(factor_, (float, int)) else factor_)
    return sprite_copy


