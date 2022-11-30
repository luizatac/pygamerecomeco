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