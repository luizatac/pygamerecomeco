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

#Sai do jogo
            if t == QUIT:
                self.run = False
                exit(0)

            #O baloo só se move pra direita ou esquerda
            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                    exit(0)
                elif k == K_RIGHT:
                    player.accel_right()
                elif k == K_LEFT:
                    player.accel_left()
                elif k == K_SPACE and self.menu_open:
                    self.menu_open = False

            elif t == KEYUP:
                if   k == K_LEFT:
                    player.accel_right()
                elif k == K_RIGHT:
                    player.accel_left()

    def actors_update(self, tempo):
        for actor in self.list.values(): 
            actor.update(tempo)

        self.player_life.update(tempo)
        self.player_xp.update(tempo)

    def actors_draw(self):
        self.background.draw(self.screen)
        
        for actor in self.list.values():
            actor.draw(self.screen)

        self.player_life.draw(self.screen)
        self.player_xp.draw(self.screen)

    def actor_check_hit(self, jogador, list, action):
        if isinstance(jogador, pygame.sprite.RenderPlain):
            hitted = pygame.sprite.groupcollide(jogador, list, 1, 0)
            for v in hitted.values():
                for o in v:
                    action(o)
            return hitted

        elif isinstance(jogador, pygame.sprite.Sprite):
            if pygame.sprite.spritecollide(jogador, list, 1):
                if(self.nivel >= 5):
                    if(self.player.get_XP() % 10 == 0):
                        self.nivel = self.nivel - 1
                self.player.set_XP(self.player.get_XP() + 1)
                self.latido.play()
            return jogador.is_dead()

    def actors_act( self ):
        self.actor_check_hit(self.player, self.list['food'], self.player.do_collision)

        if self.player.is_dead():
            self.menu_open = True 
            self.fim = True
            self.nivel = 20
            self.choro.play()
            return

    def food_check_pos(self):

        for sprite in self.list['food'].sprites():
            if sprite.is_lost():
                self.list['food'].remove(sprite)
                self.player.set_lives(self.player.get_lives() -1)

    def manage(self):
        r = Random.randint( 0, 60 )
        x = Random.randint( 200, 600 )
        if (r > (self.nivel * len(self.list['food']))): 
            food = imcomidas([0, 0])
            size  = food.get_size()
            food.set_pos([x , - size[1]])
            self.list['food'].add(food)

    def menu(self):
        self.background = Background('./imagens/ceuu.png')
        self.background.draw(self.screen)

        img = pygame.image.load('imagens/baloop.png').convert_alpha() 
        img = pygame.transform.scale(img, (350, 400))
        self.screen.blit(img, (200, 115))

        if(self.fim):
            self.font = pygame.font.Font(None, 50)
            self.write_on_screen(u'VOCÊ PERDEU :(', (0, 0, 0), (290, 60))

            self.font = pygame.font.Font(None, 50)
            self.write_on_screen(u'Pontuação: % 4d' % self.player.get_XP(), (0, 0, 0), (280, 100))
                
            self.font = pygame.font.Font(None, 30)
            self.write_on_screen(u'Pressione a tecla ESPAÇO para recomeçar!', (0, 0, 0), (235, 560))
        else:          
            self.font = pygame.font.Font(None, 50)
            self.write_on_screen(u'BELLY BALOO', (0, 0, 0), (290, 60))

            self.font = pygame.font.Font(None, 30)
            self.write_on_screen(u'Pressione a tecla ESPAÇO para começar!', (0, 0, 0), (235, 560))


    def write_on_screen(self, text_out, color, position):
        text = self.font.render(text_out, 0, color)
        text_rect = text.get_rect()
        text_rect.move_ip(position)
        self.screen.blit(text, text_rect)

    def loop( self ):
        clock = pygame.time.Clock()
        tempo = 16

        while self.run and self.menu_open:
            clock.tick(1000 / tempo)
            
            self.menu()

            self.handle_events()

            pygame.display.flip()


        #Começa o jogo 
        self.background = Background('./imagens/ceuu.png')

        pos         = [self.screen_size[0] / 2, self.screen_size[1]]
        self.player = Baloo(pos, lives=4)

        self.player_life = JogadorLifeStatus(self.player, [5, 5], image=self.image_player_status)
        self.player_xp   = JogadorXPStatus(self.player, [self.screen_size[0] - 100, 5], fgcolor="0xff0000")
        
        self.list = {
            'food'  : pygame.sprite.RenderPlain(imcomidas([Random.randint(200, 600), 0])),
            'player' : pygame.sprite.RenderPlain(self.player),
        }