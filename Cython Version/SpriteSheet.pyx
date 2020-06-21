
import cv2

# NUMPY IS REQUIRED
try:
    import numpy
    from numpy import ndarray, zeros, empty, uint8, int32, float64, float32, dstack, full, ones,\
    asarray, ascontiguousarray
except ImportError:
    print("\n<numpy> library is missing on your system."
          "\nTry: \n   C:\\pip install numpy on a window command prompt.")
    raise SystemExit

cimport numpy as np


# CYTHON IS REQUIRED
try:
    cimport cython
    from cython.parallel cimport prange
    from cpython cimport PyObject, PyObject_HasAttr, PyObject_IsInstance
    from cpython.list cimport PyList_Append, PyList_GetItem, PyList_Size
except ImportError:
    print("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")
    raise SystemExit


# PYGAME IS REQUIRED
try:
    import pygame
    from pygame import Color, Surface, SRCALPHA, RLEACCEL, BufferProxy
    from pygame.surfarray import pixels3d, array_alpha, pixels_alpha, array3d
    from pygame.image import frombuffer

except ImportError:
    print("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")
    raise SystemExit


DEF OPENMP = True

# num_threads – The num_threads argument indicates how many threads the team should consist of.
# If not given, OpenMP will decide how many threads to use.
# Typically this is the number of cores available on the machine. However,
# this may be controlled through the omp_set_num_threads() function,
# or through the OMP_NUM_THREADS environment variable.
if OPENMP:
    DEF THREAD_NUMBER = 8
else:
    DEF THREAD_NUMNER = 1

DEF SCHEDULE = 'static'

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef unsigned char[:, :, :] array_bgra2rgba_c(unsigned char[:, :, :] bgra_array):
    """
    Convert an BGRA color array into an RGBA

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
        for i in prange(w, schedule=SCHEDULE, num_threads=THREAD_NUMBER):
            for j in range(h):
                rgba_array[i, j, 0] = bgra_array[i, j, 2]   # red
                rgba_array[i, j, 1] = bgra_array[i, j, 1]   # green
                rgba_array[i, j, 2] = bgra_array[i, j, 0]   # blue
                rgba_array[i, j, 3] = bgra_array[i, j, 3]   # alpha
    return rgba_array


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cpdef sprite_sheet_per_pixel(str file, int chunk, int columns_, int rows_, tweak_=False, args=None):
    """
    Extract all sprites from a sprite sheet.
    This method is using OpencCV to open the spritesheet (much faster than Pygame)

    All sprites will contain per-pixel transparency information,
    Surface without per-pixel information will raise a ValueError
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

    TEST:
        32bit : 3.2746867 0.32746867
        24bit : FAIL
         8bit : FAIL

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

    try:
        # load an image with alpha channel numpy.array (w, h, 4) uint 8
        # imread() decodes the image into a matrix with the color channels
        # stored in the order of Blue, Green and Red respectively.

        bgra_array = (cv2.imread(file, cv2.IMREAD_UNCHANGED)).astype(dtype=numpy.uint8)
        if bgra_array is None:
            raise ValueError

    except Exception:
        raise FileNotFoundError('\npImage %s is not found ' % file)

    cdef int width, height, dim
    try:
        width, height, dim = bgra_array.shape[:3]
    except (ValueError, pygame.error) as e:
        raise ValueError('\nArray shape not understood.')

    if width == 0 or height == 0 or dim != 4:
        raise ValueError('image with incorrect dimensions must'
                         ' be (w>0, h>0, 4) got (w:%s, h:%s, %s) ' % (width, height, dim))

    cdef:
        np.ndarray [np.uint8_t, ndim=3] rgba_array = asarray(array_bgra2rgba_c(bgra_array))
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
cpdef sprite_sheet_fs8(str file, int chunk, int columns_, int rows_, tweak_= False, args=None):
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

    TEST:
        32bit :  im1 7.4495958 0.74495958
        24bit :  im2 9.024994 0.9024994
         8bit :  im3 4.5625514 0.45625514
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


#
# from numpy import frombuffer, uint8
# def sprite_sheet_per_pixel(file_: str, chunk: int, rows_: int, columns_: int) -> list:
#     """ Not to be used with asymetric surface """
#     surface = pygame.image.load(file_)
#     buffer_ = surface.get_view('2')
#
#     w, h = surface.get_size()
#     source_array = frombuffer(buffer_, dtype=uint8).reshape((h, w, 4))
#     animation = []
#
#     for rows in range(rows_):
#         for columns in range(columns_):
#             array1 = source_array[rows * chunk:(rows + 1) * chunk,
#                      columns * chunk:(columns + 1) * chunk, :]
#
#             surface_ = pygame.image.frombuffer(array1.copy(order='C'),
#                                                (tuple(array1.shape[:2])), 'RGBA').convert_alpha()
#             animation.append(surface_.convert(32, pygame.SWSURFACE | pygame.RLEACCEL | pygame.SRCALPHA))
#
#     return animation
#
#
# def spread_sheet_fs8(file: str, chunk: int, rows_: int, columns_: int, tweak_: bool = False, *args) -> list:
#     """ surface fs8 without per pixel alpha channel """
#     assert isinstance(file, str), 'Expecting string for argument file got %s: ' % type(file)
#     assert isinstance(chunk, int), 'Expecting int for argument number got %s: ' % type(chunk)
#     assert isinstance(rows_, int) and isinstance(columns_, int), 'Expecting int for argument rows_ and columns_ ' \
#                                                                  'got %s, %s ' % (type(rows_), type(columns_))
#     image_ = pygame.image.load(file)
#     array = pygame.surfarray.array3d(image_)
#
#     animation = []
#     # split sprite-sheet into many sprites
#     for rows in range(rows_):
#         for columns in range(columns_):
#             if tweak_:
#                 chunkx = args[0]
#                 chunky = args[1]
#                 array1 = array[columns * chunkx:(columns + 1) * chunkx, rows * chunky:(rows + 1) * chunky, :]
#             else:
#                 array1 = array[columns * chunk:(columns + 1) * chunk, rows * chunk:(rows + 1) * chunk, :]
#             surface_ = pygame.surfarray.make_surface(array1)
#             animation.append(surface_.convert())
#     return animation
