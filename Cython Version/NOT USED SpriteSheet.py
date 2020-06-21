
from numpy import uint8, frombuffer
import pygame


class ERROR(BaseException):
    pass


def load_per_pixel(file: str) -> pygame.Surface:
    """ Not compatible with 8 bit depth color surface"""

    assert isinstance(file, str), 'Expecting path for argument <file> got %s: ' % type(file)
    try:
        surface = pygame.image.load(file)
        buffer_ = surface.get_view('2')
        w, h = surface.get_size()
        source_array = frombuffer(buffer_, dtype=uint8).reshape((w, h, 4))

        surface_ = pygame.image.frombuffer(source_array.copy(order='C'),
                                   (tuple(source_array.shape[:2])), 'RGBA').convert_alpha()
        return surface_
    except pygame.error:
        raise SystemExit('\n[-] Error : Could not load image %s %s ' % (file, pygame.get_error()))


def spread_sheet_per_pixel(file_: str, chunk: int, rows_: int, columns_: int) -> list:
    """ Not to be used with asymetric surface """
    surface = pygame.image.load(file_)
    buffer_ = surface.get_view('2')

    w, h = surface.get_size()
    source_array = frombuffer(buffer_, dtype=uint8).reshape((h, w, 4))
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
