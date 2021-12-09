from ..element import info
import pygame
from PlaneGame import PlaneGame
import time

class LoadScreen:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'level'
        self.duration = 2000
        self.timer = 0
        self.info = info.Info('load', self.game_info)

    def update(self, surface, keys):
        self.draw(surface)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished = True
            self.timer = 0

    def draw(self, surface):
        surface.fill((0,0,0))
        self.info.draw(surface)


class Game_Over(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'menu'
        self.duration = 4000
        self.timer = 0
        self.info = info.Info('game_over', self.game_info)



class Success(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'plane_game'
        self.duration = 4000
        self.timer = 0
        self.info = info.Info('Next Pass', self.game_info)

        #PlaneGame().startGame()


class plane_game(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = None
        self.info = info.Info('Next Pass', self.game_info)
        PlaneGame().startGame()