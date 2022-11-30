import pygame
from pygame.locals import *
import random

from sprites import Sprite


class Comidas(Sprite):

    def __init__(self, position, speed=[0, 0], image=None):
        self.acceleration = [4, 4]

        Sprite.__init__(self, image, position, speed)

    def accel_left(self):
        speed = self.velocidade()
        self.ajeitav(speed[0] - self.acceleration[0], speed[1])

    def accel_right(self):
        speed = self.velocidade()
        self.ajeitav(speed[0] + self.acceleration[0], speed[1])

    def is_lost(self):
        return self.get_pos()[1] >= 600


class imcomidas(Comidas):

    foods = [
        {'image': './imagens/racaoc.png', 'pontos': 1},
        {'image': './imagens/biscoitoc.png', 'pontos': 1},
        {'image': './imagens/cenoura.png', 'pontos': 1},
        {'image': './imagens/macac.png', 'pontos': 1},
        {'image': './imagens/banana.png', 'pontos': 1},
        {'image': './imagens/alface.png', 'pontos': 1},
        {'image': './imagens/brocolis.png', 'pontos': 1},
        
    ]