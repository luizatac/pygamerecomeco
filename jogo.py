import os
import pygame
from pygame.locals import *
import random as Random
import pygame.mixer 
import sys

from comidas import imcomidas
from baloo import Baloo, JogadorXPStatus, JogadorLifeStatus
from pygame.mixer import Sound

class Background:

    image = None
    pos   = None

    def __init__(self, image):
        image = pygame.image.load(image).convert()

        self.isize  = image.get_size()
        self.pos    = [0, -1 * self.isize[1]]
        screen      = pygame.display.get_surface()
        screen_size = screen.get_size()

        from math import ceil
        w = (ceil(float(screen_size[0]) / self.isize[0]) + 1) * self.isize[0]
        h = (ceil(float(screen_size[1]) / self.isize[1]) + 1) * self.isize[1]

        back = pygame.Surface((w, h))

        for i in range(int((back.get_size()[0] / self.isize[0]))):
            for j in range(int((back.get_size()[1] / self.isize[1]))):
                back.blit(image, (i * self.isize[0], j * self.isize[1]))

        self.image = back 

    def update(self, tempo):
        self.pos[1] += 1
        if (self.pos[1] > 0):
            self.pos[1] -= self.isize[1]

    def draw(self, screen):
        screen.blit(self.image, self.pos)