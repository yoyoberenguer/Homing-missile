
import multiprocessing
from multiprocessing import Process, Queue, freeze_support
import time

import numpy
import pygame
from random import randint


class DrawSpriteMultiprocess(Process):

    def __init__(self, listener_name_, input_, output_, event_, background_, size_):

        super(Process, self).__init__()

        self.listener_name = listener_name_
        self.event = event_
        self.stop = False
        self.input = input_
        self.output = output_
        self.background = background_
        self.size = size_



    def draw(self):
        # print(self.listener_name)
        ...

    def run(self):
        while not self.event.is_set():
            bck = pygame.image.frombuffer(self.background, self.size, 'RGB')
            if self.input[self.listener_name] is not None:
                sprite = self.input[self.listener_name]
                for spr in sprite:
                    image = pygame.image.frombuffer(spr.image, (spr.rect.w, spr.rect.h), 'RGB')
                    bck.blit(image, spr.rect)#, special_flags=pygame.BLEND_RGB_ADD)

                    ...
                out_bck = pygame.image.tostring(bck, 'RGB', False)
                self.output.put({self.listener_name: out_bck})
                self.input[self.listener_name] = None
            else:
                time.sleep(0.0001)

        print('DrawSpriteMultiprocess %s is dead.' % self.listener_name)


if __name__ == '__main__':
    SIZE = (800, 600)
    SCREENRECT = pygame.Rect((0, 0), SIZE)
    pygame.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.RESIZABLE, 32)
    BACKGROUND = pygame.image.load('Assets\\A2.png').convert(32, pygame.RLEACCEL)
    BACKGROUND = pygame.transform.smoothscale(BACKGROUND, SIZE)
    BACKGROUND.set_alpha(None)

    sprite_number = 1000
    sprites = numpy.array([pygame.sprite.Sprite() for r in range(sprite_number)])
    for s in sprites:
        image = pygame.image.load('Assets\\SpaceShip.png').convert(32, pygame.RLEACCEL)
        s.image = pygame.image.tostring(image, 'RGB', False)
        s.rect = image.get_rect()
        s.rect.center = (randint(0, SIZE[0]), randint(0, SIZE[1]))

    PROCESS = 10
    QUEUE = multiprocessing.Queue()
    EVENT = multiprocessing.Event()
    MANAGER = multiprocessing.Manager()
    DATA = MANAGER.dict()

    # SPLIT SPRITES INTO CHUNKS
    chunks = numpy.split(sprites, PROCESS)

    i = 0
    for c in chunks:
        DATA[i] = list(c)
        i += 1
    i = 0
    # for i in range(len(chunks)):
    #     print(i, DATA[i])

    BCK = pygame.image.tostring(BACKGROUND, 'RGB', False)

    for i in range(PROCESS):
        DrawSpriteMultiprocess(i, DATA, QUEUE, EVENT, BCK, SIZE).start()

    FRAME = 0
    CLOCK = pygame.time.Clock()
    STOP_GAME = False
    PAUSE = False

    index = 0
    while not STOP_GAME:

        pygame.event.pump()

        while PAUSE:
            event = pygame.event.wait()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_PAUSE]:
                PAUSE = False
                pygame.event.clear()
                keys = None
            break

        for event in pygame.event.get():

            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                print('Quitting')
                STOP_GAME = True

            elif event.type == pygame.MOUSEMOTION:
                MOUSE_POS = event.pos

            elif keys[pygame.K_PAUSE]:
                PAUSE = True
                print('Paused')

        temp = {}
        for i in range(PROCESS):
            for key, value in QUEUE.get().items():
                temp[str(key)] = value
        msort = []
        for key, value in sorted(temp.items(), key=lambda item: (int(item[0]), item[1])):
            msort.append(value)

        for r in msort:
            SCREEN.fill((0, 0, 0))
            im = pygame.image.frombuffer(r, SIZE, 'RGB')
            SCREEN.blit(im, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            pygame.display.flip()

        SCREEN.fill((0, 0, 0, 0))
        SCREEN.blit(BACKGROUND, (0, 0))
        pygame.display.flip()
        TIME_PASSED_SECONDS = CLOCK.tick(800)
        print(CLOCK.get_fps())
        FRAME += 1

        i = 0
        for c in chunks:
            DATA[i] = c
            i += 1

    EVENT.set()


    pygame.quit()
