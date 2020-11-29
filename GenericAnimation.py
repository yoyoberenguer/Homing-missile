import pygame


class GenericAnimation(pygame.sprite.Sprite):
    images = None
    containers = None

    def __init__(self, timing_, gl_, center_, layer_: int = -1):

        self._layer = layer_
        self._blend = None
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.GL = gl_

        if isinstance(self.GL.All, pygame.sprite.LayeredUpdates):
                self.GL.All.change_layer(self, layer_)

        self.timing = timing_
        self.image = self.images
        self.rect = self.image.get_rect(center=center_)
        self.dt = 0

    def update(self):

        if self.dt > self.timing:

            if self.GL.SCREENRECT .contains(self.rect):
                self.rect.move_ip(self.GL.BACKGROUND_VECTOR)
            else:
                self.kill()

            self.dt = 0

        self.dt += self.GL.TIME_PASSED_SECONDS

