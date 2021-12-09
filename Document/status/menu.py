import pygame
from .. import setup
from .. import Tools
from .. import Constants as C
from ..element import info

class Menu:
    def __init__(self):
        game_info = {
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'normal'
        }
        self.start(game_info)

    def start(self, game_info):
        """
        重置，如果放在init里面就无法反复调用了
        还需要在各个关卡、状态间进行信息传递
        :param game_info:
        :return:
        """
        self.game_info = game_info
        self.setup_background()
        self.setup_player()
        self.setup_cursor()
        self.info = info.Info('menu', self.game_info)
        self.finished = False
        self.next = 'load'

    def setup_background(self):
        self.background = setup.PICTURE['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background,
                                                 (int(self.background_rect.width * C.BG_MULTI),
                                                  int(self.background_rect.height * C.BG_MULTI)))
        self.viewport = setup.SCREEN.get_rect()
        self.caption = Tools.get_image(setup.PICTURE['title_screen'], 1, 60, 176, 88, (255, 0, 220),C.BG_MULTI)

    def setup_player(self):
        self.player_image = Tools.get_image(setup.PICTURE['mario_bros'], 178, 32, 12, 16, (0,0,0), C.PLAYER_MULTI)

    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        # self.cursor.image = Tools.get_image(setup.PICTURE['item_objects'], 24, 160, 8, 8, (0,0,0), C.PLAYER_MULTI)
        self.cursor.image = Tools.get_image(setup.PICTURE['Thor'], 0, 0, 50, 57, (0, 0, 0), 1)        #Thor~
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = (200, 360)
        self.cursor.rect = rect
        self.cursor.state = '1P'    #状态机

    def update_cursor(self, keys):
        if keys[pygame.K_UP]:
            self.cursor.state = '1P'
            self.cursor.rect.y = 360
        elif keys[pygame.K_DOWN]:
            self.cursor.state = '2P'
            self.cursor.rect.y = 405
        elif keys[pygame.K_RETURN]:
            self.rest_game_info()
            if self.cursor.state == '1P':
                self.finished = True
            elif self.cursor.state == '2P':
                self.finished = True


    def update(self, surface, keys):

        self.update_cursor(keys)

        # import random
        # surface.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        surface.blit(self.background, self.viewport)
        surface.blit(self.caption, (170, 100))
        surface.blit(self.player_image, (110, 490))
        # surface.blit(self.cursor, (220, 360))
        surface.blit(self.cursor.image, self.cursor.rect)

        self.info.update()
        self.info.draw(surface)

    def rest_game_info(self):
        """
        死亡三次就重置游戏
        :return:
        """
        self.game_info.update({
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'normal'
        })