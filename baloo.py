import copy
import pygame
from pygame.locals import *

from sprites import Sprite


class Player(Sprite):
    
    def _init_(self, position, lives=0, speed=[0, 0], image=None):
        self.acceleration = [5, 5]

        Sprite._init_(self, image, position, speed)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives

    def do_collision(self):
        if self.get_lives() == 0:
            self.kill()
        else:
            pass

    def is_dead(self):
        return self.get_lives() == 0

    def accel_left(self):
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0],speed[1]))

class Baloo(Player):
    
    def __init__(self, position, lives=10):
        image = './imagens/baloot.png'

        Player.__init__(self, position, lives, [0, 0], image)
        self.set_XP(0)

    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16, self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right
        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom
        elif (self.rect.top < 0):
            self.rect.top = 0

    def get_pos(self):
        return (self.rect.center[0], self.rect.top)

    def get_XP(self):
        return self.XP

    def set_XP(self, XP):
        self.XP = XP

class JogadorXPStatus:

    font    = None
    last_xp = -1
    fgcolor = None
    bgcolor = None
    image   = None

    def _init_(self, player, pos=None, font=None, ptsize=30, fgcolor="0xffff00", bgcolor=None):
        self.player  = player
        self.fgcolor = pygame.color.Color(fgcolor)
        if bgcolor:
            self.bgcolor = pygame.color.Color(bgcolor)
        self.pos     = pos or [0, 0]
        self.font    = pygame.font.Font(font, ptsize)

        self.last_rect = None

    def update(self, dt):
        pass

    def draw(self, screen):
        text = "Score: % 4d" % self.player.get_XP()
        if self.bgcolor:
            self.image = self.font.render(text, False, self.fgcolor, self.bgcolor)
        else:
            self.image = self.font.render(text, False, self.fgcolor, (255, 0, 255))
            self.image.set_colorkey((255, 0, 255), RLEACCEL)

        self.last_rect = Rect(self.pos, self.image.get_size())

        screen.blit(self.image, self.pos)

    def clear(self, screen, background):
        if self.last_rect:
            screen.blit(background, self.last_rect)


class JogadorLifeStatus:
    player     = None
    pos        = None
    image      = None
    size_image = None
    spacing    = 5
    def _init_(self, player, pos=None, image=None):
        image = './imagens/vidasc.png'
        self.image = pygame.image.load(image)

        self.player     = player
        self.pos        = pos or [ 5, 5 ]
        self.size_image = self.image.get_size()
        self.last_rect  = None

    def update(self, tempo):
        pass

    def draw(self, screen):
        pos = copy.copy(self.pos)
        for i in range(self.player.get_lives()):
            pos[0] += self.size_image[0] + self.spacing
            screen.blit(self.image, pos)

        pos[1] = self.size_image[1]
        self.last_rect = Rect(self.pos, pos)

    def clear(self, screen, background):
        if self.last_rect:
            screen.blit(background,self.last_rect)