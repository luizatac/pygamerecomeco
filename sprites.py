import pygame
from pygame.locals import *


class Sprite(pygame.sprite.Sprite):

    def __init__(self, image, position, speed=None):
        pygame.sprite.Sprite.__init__(self)

        self.image  = pygame.image.load(image)
        self.rect   = self.image.get_rect()
        screen      = pygame.display.get_surface()
        self.area   = screen.get_rect()

        self.set_pos(position)
        self.set_speed(speed or (0, 2))

    def update(self, tempo):
        move_speed = (self.speed[0] * tempo / 16, self.speed[1] * tempo / 16)
        self.rect  = self.rect.move(move_speed)

        if (self.rect.left > self.area.right) or (self.rect.top >= self.area.bottom) or (self.rect.right < 0):
            self.kill()

        if (self.rect.bottom < -40):
            self.kill()

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_pos(self):
        return (self.rect.center[0], self.rect.bottom)

    def set_pos(self, pos):
        self.rect.center = (pos[0], pos[1])

    def get_size(self):
        return self.image.get_size()