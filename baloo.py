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