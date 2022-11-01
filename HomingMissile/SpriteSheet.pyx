# encoding: utf-8


"""
                 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Copyright Yoann Berenguer
"""


# NUMPY IS REQUIRED
try:
    import numpy
except ImportError:
    raise("\n<numpy> library is missing on your system."
          "\nTry: \n   C:\\pip install numpy on a window command prompt.")

from numpy import  empty, uint8, asarray, ascontiguousarray
cimport numpy as np


# CYTHON IS REQUIRED
try:
    cimport cython

except ImportError:
    raise("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")

from cython.parallel cimport prange
from cpython cimport PyObject_IsInstance
from cpython.list cimport PyList_Append

# PYGAME IS REQUIRED
try:
    import pygame
except ImportError:
    raise("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")

from pygame import RLEACCEL
from pygame.surfarray import pixels3d


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef unsigned char[:, :, :] bgra_to_rgba(unsigned char[:, :, :] bgra_array):
    """
    CONVERT AN BGRA COLOR ARRAY INTO AN RGBA

    :param bgra_array: numpy.ndarray (w, h, 4) uint8 with value BGRA to convert into RGBA
    :return: numpy.ndarray (w, h, 4) with RGBA values (uint8)
    """
    cdef int w, h

    try:
        w, h = (<object>bgra_array).shape[:2]
    except (ValueError, pygame.error) as e:
        raise ValueError('\nArray shape not understood.')

    cdef:
        int i, j
        unsigned char [:, :, ::1] rgba_array = empty((w, h, 4), uint8)

    with nogil:
        for i in prange(w, schedule='static', num_threads=8):
            for j in range(h):
                rgba_array[i, j, 0] = bgra_array[i, j, 2]   # red
                rgba_array[i, j, 1] = bgra_array[i, j, 1]   # green
                rgba_array[i, j, 2] = bgra_array[i, j, 0]   # blue
                rgba_array[i, j, 3] = bgra_array[i, j, 3]   # alpha
    return rgba_array


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef sprite_sheet_per_pixel(
        str file,
        int chunk,
        int columns_,
        int rows_,
        tweak_  =False,
        args    =None):
    """
    EXTRACT ALL SPRITES FROM A SPRITE SHEET.
   
    Compatible with 32-bit surface format 
   

    :param file     : str, full path to the texture/surface
    :param chunk    : int, Size of a sprite e.g chunk=64 for sprite 64x64
    :param rows_    : int, number of rows
    :param columns_ : int, number of column
    :param tweak_   : bool, modify the chunk sizes (in bytes) in order to process
        data with non equal width and height e.g 320x200
    :param args     : tuple, used with tweak_, args is a tuple containing the new chunk size,
        e.g (320, 200)
    :return         : list, Return textures (pygame surface) containing per-pixel transparency into a
        python list

    """

    assert PyObject_IsInstance(file, str), \
        'Expecting string for argument file got %s: ' % type(file)
    assert PyObject_IsInstance(chunk, int), \
        'Expecting int for argument number got %s: ' % type(chunk)
    assert PyObject_IsInstance(rows_, int) and PyObject_IsInstance(columns_, int), \
        'Expecting int for argument rows_ and columns_ ' \
        'got %s, %s ' % (type(rows_), type(columns_))
    assert PyObject_IsInstance(tweak_, bool), \
        "Expecting boolean for argument tweak_ got %s " % type(tweak_)

    cdef int width, height

    try:
        surface = pygame.image.load(file).convert_alpha()
        width, height = surface.get_size()
        buf = surface.get_view('2')
        bgra_array = numpy.frombuffer(buf, dtype=numpy.uint8).reshape(width, height, 4)

    except Exception:
        raise FileNotFoundError('\npImage %s is not found ' % file)

    cdef int dim
    try:
        width, height, dim = bgra_array.shape[:3]
    except (ValueError, pygame.error) as e:
        raise ValueError('\nArray shape not understood.')

    if width == 0 or height == 0 or dim != 4:
        raise ValueError('image with incorrect dimensions must'
                         ' be (w>0, h>0, 4) got (w:%s, h:%s, %s) ' % (width, height, dim))

    cdef:
        np.ndarray [np.uint8_t, ndim=3] rgba_array = asarray(bgra_to_rgba(bgra_array))
        np.ndarray [np.uint8_t, ndim=3] array1     = empty((chunk, chunk, 4), dtype=uint8)
        int chunk_x = 0, chunk_y = 0, rows = 0, columns = 0
        list animation = []

    # modify the chunk size
    if tweak_ and args is not None:

        if PyObject_IsInstance(args, tuple):
            try:
                chunk_x = args[0][0]
                chunky = args[0][1]
            except IndexError:
                raise IndexError('Parse argument not understood.')
            if chunk_x==0 or chunky==0:
                raise ValueError('Chunk_x and chunky cannot be equal to zero.')
            if (width % chunk_x) != 0:
                raise ValueError('Chunk_x size value is not a correct fraction of %s ' % width)
            if (height % chunky) != 0:
                raise ValueError('Chunky size value is not a correct fraction of %s ' % height)
        else:
            raise ValueError('Parse argument not understood.')
    else:
        chunk_x, chunky = chunk, chunk

    cdef image_frombuffer = pygame.image.frombuffer
    # get all the sprites
    for rows in range(rows_):
        for columns in range(columns_):
            array1 = rgba_array[rows * chunky:(rows + 1) * chunky, columns * chunk_x:(columns + 1) * chunk_x, :]
            image  = image_frombuffer(ascontiguousarray(array1), (chunk_x, chunky), 'RGBA').convert_alpha()
            PyList_Append(animation, image)
    return animation


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef sprite_sheet_fs8(
        str file,
        int chunk,
        int columns_,
        int rows_,
        tweak_= False,
        args=None):
    """
    Retrieve all sprites from a sprite sheets.
    All individual sprite will contains transparency set by the colorkey value (default black)
    This will only work on Surfaces that have 24-bit or 32-bit formats.

    :param file: str,  full path to the texture
    :param chunk: int, size of a single image in bytes e.g 64x64 (equal
    :param rows_: int, number of rows
    :param columns_: int, number of column
    :param tweak_: bool, modify the chunk sizes (in bytes) in order to process
                   data with non equal width and height e.g 320x200
    :param args: tuple, used with theak_, args is a tuple containing the new chunk size,
                 e.g (320, 200)
    :return: list, Return textures (pygame surface) containing per-pixel transparency into a
            python list

    """
    assert PyObject_IsInstance(file, str), \
        'Expecting string for argument file got %s: ' % type(file)
    assert PyObject_IsInstance(chunk, int),\
        'Expecting int for argument number got %s: ' % type(chunk)
    assert PyObject_IsInstance(rows_, int) and PyObject_IsInstance(columns_, int), \
        'Expecting int for argument rows_ and columns_ ' \
        'got %s, %s ' % (type(rows_), type(columns_))

    cdef int width, height

    try:
        image_ = pygame.image.load(file)
        width, height = image_.get_size()

    except (pygame.error, ValueError):
        raise FileNotFoundError('\nFile %s is not found ' % file)

    if width==0 or height==0:
        raise ValueError(
            'Surface dimensions is not correct, must be: (w>0, h>0) got (w:%s, h:%s) ' % (width, height))

    try:
        # Reference pixels into a 3d array
        # pixels3d(Surface) -> array
        # Create a new 3D array that directly references the pixel values
        # in a Surface. Any changes to the array will affect the pixels in
        # the Surface. This is a fast operation since no data is copied.
        # This will only work on Surfaces that have 24-bit or 32-bit formats.
        # Lower pixel formats cannot be referenced.
        rgb_array_ = pixels3d(image_)

    except (pygame.error, ValueError):
        # Copy pixels into a 3d array
        # array3d(Surface) -> array
        # Copy the pixels from a Surface into a 3D array.
        # The bit depth of the surface will control the size of the integer values,
        # and will work for any type of pixel format.
        # This function will temporarily lock the Surface as
        # pixels are copied (see the Surface.lock()
        # lock the Surface memory for pixel access
        # - lock the Surface memory for pixel access method).
        try:
            rgb_array_ = pygame.surfarray.array3d(image_)
        except (pygame.error, ValueError):
            raise ValueError('\nIncompatible pixel format.')


    cdef:
        np.ndarray[np.uint8_t, ndim=3] rgb_array = rgb_array_
        np.ndarray[np.uint8_t, ndim=3] array1    = empty((chunk, chunk, 3), dtype=uint8)
        int chunkx, chunky, rows = 0, columns = 0

    # modify the chunk size
    if tweak_ and args is not None:

        if PyObject_IsInstance(args, tuple):
            try:
                chunkx = args[0][0]
                chunky = args[0][1]
            except IndexError:
                raise IndexError('Parse argument not understood.')
            if chunkx==0 or chunky==0:
                raise ValueError('Chunkx and chunky cannot be equal to zero.')
            if (width % chunkx) != 0:
                raise ValueError('Chunkx size value is not a correct fraction of %s ' % width)
            if (height % chunky) != 0:
                raise ValueError('Chunky size value is not a correct fraction of %s ' % height)
        else:
            raise ValueError('Parse argument not understood.')
    else:
        chunkx, chunky = chunk, chunk

    cdef:
        list animation = []
        make_surface   = pygame.pixelcopy.make_surface

    # split sprite-sheet into many sprites
    for rows in range(rows_):
        for columns in range(columns_):
            array1   = rgb_array[columns * chunkx:(columns + 1) * chunkx, rows * chunky:(rows + 1) * chunky, :]
            surface_ = make_surface(array1).convert()
            surface_.set_colorkey((0, 0, 0, 0), RLEACCEL)
            PyList_Append(animation, surface_)

    return animation

