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

class Game:
    screen = None
    screen_size = None
    run = True
    menu_open = True
    list = None
    player = None
    player_life = None
    player_xp = None
    background = None
    img = None
    latido = None
    choro = None
    fim = False
    nivel = 20


    def _init_(self, size):
        actors = {}
        pygame.init()
        flags = DOUBLEBUF

        self.screen = pygame.display.set_mode(size, flags)
        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('BellyBaloo') 
        self.load_images()
        pygame.mixer.init()
        self.latido = pygame.mixer.Sound(os.path.join('snd','latido.wav'))
        self.latido.set_volume(0.5)

        self.choro = pygame.mixer.Sound(os.path.join('snd','choro.wav'))
        self.choro.set_volume(0.5) 


    def load_images(self):
        def load_image(filename):
            img = pygame.image.load(os.path.join('imagens', filename))
            img.set_alpha(None, RLEACCEL) 
            img.convert()
            img.set_colorkey(( 255, 0, 255), RLEACCEL)
            return img
        self.image_player_status = load_image('vidasc.png')

    def handle_events(self):
        player = self.player

        for event in pygame.event.get():
            t = event.type
            if t in (KEYDOWN, KEYUP):
                k=event.key