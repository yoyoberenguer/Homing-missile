# encoding: utf-8
"""

                   GNU GENERAL PUBLIC LICENSE

                       Version 3, 29 June 2007


 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>

 Everyone is permitted to copy and distribute verbatim copies

 of this license document, but changing it is not allowed.
 """

__author__ = "Yoann Berenguer"
__copyright__ = "Copyright 2007, Cobra Project"
__credits__ = ["Yoann Berenguer"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Yoann Berenguer"
__email__ = "yoyoberenguer@hotmail.com"
__status__ = "Alpha Demo"

import pygame
import numpy

import warnings

warnings.simplefilter(action='ignore')


class ERROR(BaseException):
    pass


def spread_sheet_per_pixel(file_: str, chunk: int, rows_: int, columns_: int) -> list:
    """ Not to be used with asymetric surface """
    surface = pygame.image.load(file_)
    buffer_ = surface.get_view('2')

    w, h = surface.get_size()
    source_array = numpy.frombuffer(buffer_, dtype=numpy.uint8).reshape((h, w, 4))
    animation = []

    for rows in range(rows_):
        for columns in range(columns_):
            array1 = source_array[rows * chunk:(rows + 1) * chunk,
                     columns * chunk:(columns + 1) * chunk, :]

            surface_ = pygame.image.frombuffer(array1.copy(order='C'),
                                               (tuple(array1.shape[:2])), 'RGBA').convert_alpha()
            animation.append(surface_.convert(32, pygame.SWSURFACE | pygame.RLEACCEL | pygame.SRCALPHA))

    return animation


def spread_sheet_fs8(file: str, chunk: int, rows_: int, columns_: int, tweak_: bool = False, *args) -> list:
    """ surface fs8 without per pixel alpha channel """
    assert isinstance(file, str), 'Expecting string for argument file got %s: ' % type(file)
    assert isinstance(chunk, int), 'Expecting int for argument number got %s: ' % type(chunk)
    assert isinstance(rows_, int) and isinstance(columns_, int), 'Expecting int for argument rows_ and columns_ ' \
                                                                 'got %s, %s ' % (type(rows_), type(columns_))
    image_ = pygame.image.load(file)
    array = pygame.surfarray.array3d(image_)

    animation = []
    # split sprite-sheet into many sprites
    for rows in range(rows_):
        for columns in range(columns_):
            if tweak_:
                chunkx = args[0]
                chunky = args[1]
                array1 = array[columns * chunkx:(columns + 1) * chunkx, rows * chunky:(rows + 1) * chunky, :]
            else:
                array1 = array[columns * chunk:(columns + 1) * chunk, rows * chunk:(rows + 1) * chunk, :]
            surface_ = pygame.surfarray.make_surface(array1)
            animation.append(surface_.convert())
    return animation
