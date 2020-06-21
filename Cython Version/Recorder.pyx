# ###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
#
# import cv2
# from cv2 import cvtColor, COLOR_RGBA2BGR, VideoWriter_fourcc
# from numpy import fromstring, uint8
#
# # CYTHON IS REQUIRED
# try:
#     cimport cython
#     from cpython cimport PyObject, PyObject_HasAttr, PyObject_IsInstance
# except ImportError:
#     raise ImportError("\n<cython> library is missing on your system."
#           "\nTry: \n   C:\\pip install cython on a window command prompt.")
#
# try:
#     import pygame
#     from pygame import Surface, transform, freetype, RLEACCEL
# except ImportError:
#     raise ImportError("\n<Pygame> library is missing on your system."
#           "\nTry: \n   C:\\pip install pygame on a window command prompt.")
#
#
#
#
#     video = cv2.VideoWriter('Video.avi',
#                             cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (SCREENRECT.w, SCREENRECT.h), True)
#
#
# cdef class VideoMeter(object):
#
#     cdef:
#         int length
#         canvas
#
#     def __init__(self, video_icon, video_level, float vol_,
#                  float scale_ = 1.0, color_ = pygame.Color(28, 40, 32, 20)):
#
#         assert PyObject_IsInstance(color_, pygame.Color), \
#             '\nArgument color must be a pygame color type.'
#         self.length = <int>(350 * scale_)
#         cdef height = <int>(72 * scale_)
#         self.canvas = Surface((self.length, height)).convert(32, RLEACCEL)
#         self.canvas.fill(color_)
#
#         cdef:
#             int w, h
#             transform_smoothscale = transform.smoothscale
#
#         if scale_ != 1.0:
#             w, h = video_icon.get_size()
#             video_icon = transform._smoothscale(
#                 video_icon, (int(w * scale_), int(h * scale_)))
#             w, h = self.Indicator.get_size()
#             self.Indicator = transform_smoothscale(
#                 self.Indicator, (int(w * scale_), int(h * scale_)))
#
#         w, h = video_icon.get_size()
#         self.canvas.blit(video_icon, (int(2.85 * self.length / 100),
#                                            (self.canvas.get_height() - h) // 2))
#
#         w, self.h = self.Indicator.get_size()
#         self.volume = vol_
#         self.value = 255
#         self.th = None
#         self.flag = False
#         self.image = None
#         self.scale = scale_
#         self.update_volume(vol_)
#
#     def update_volume(self, float new_volume):
#         can = self.canvas.copy()
#         for level in range(<int>(new_volume * 10)):
#             can.blit(self.Indicator,
#                      (int(22.85 * self.length / 100) + (level * 25 * self.scale),
#                       (self.canvas.get_height() - self.h) // 2))
#         self.value = 255
#         self.flag = False
#         can.set_alpha(self.value)
#         self.image = can
#
#
#     LEVEL_ICON = pygame.image.load('Assets\\switchGreen04.png').convert_alpha()
#     LEVEL_ICON = pygame.transform.rotozoom(LEVEL_ICON, 90, 0.7)
#
#     VIDEO_ICON = pygame.image.load('Assets\\video1.png').convert_alpha()
#     VIDEO_ICON = pygame.transform.smoothscale(VIDEO_ICON, (64, 64))
#
#     FONT = freetype.Font('Assets\\ARCADE_R.ttf', size=15)
#     RECT1 = FONT.get_rect("Video capture, please wait...ESC to stop", style=freetype.STYLE_NORMAL, size=15)
#     RECT1.center = (SCREENRECT.centerx - RECT1.w // 2, SCREENRECT.centery - RECT1.h // 2)
#     FONT.render_to(GL.screen, RECT1.center, "Video capture, please wait...ESC to stop",
#         fgcolor=pygame.Color(255, 255, 255), size=15)
#     pygame.display.flip()
#
#     counter = 0
#     video_meter = VideoMeter(0, 0.4)
#
#     for event in pygame.event.get():
#         pygame.event.clear()
#
#     for image in VIDEO:
#
#         video_meter.update_volume(counter / len(VIDEO))
#         SCREEN.blit(video_bar.image, ((SCREENRECT.w >> 1) - 175 // 2, (SCREENRECT.h >> 1) + 25))
#         image = fromstring(image, uint8).reshape(SCREENRECT.h, SCREENRECT.w, 3)
#         image = cv2.cvtColor(image, COLOR_RGBA2BGR)
#         video.write(image)
#
#         counter += 1
#         pygame.display.flip()
#
#     cv2.destroyAllWindows()
#     video.release()
# pygame.quit()
