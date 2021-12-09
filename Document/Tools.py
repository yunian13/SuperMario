import os

import pygame
import random

class Game:
    def __init__(self, state_dict, start_state):
    # ---> setup.py
        # PlaneGame.init()
        # PlaneGame.display.set_mode((800,600))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start(game_info)
        self.state.update(self.screen, self.keys)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()

            pygame.display.update()
            self.clock.tick(60)

def load_picture(path, accept=('.jpg','.png','.gif','.bmp')):
    picture = {}        #建立空字典
    for img in os.listdir(path):        #遍历文件夹
        name, ext = os.path.splitext(img)       #拆分函数：拆分成文件名和后缀
        if ext.lower() in accept:       #如果符合上述格式
            t = pygame.image.load(os.path.join(path,img))
            if t.get_alpha():       #如果有alpha图层，需要扣掉
                t = t.convert_alpha()
            else:
                t = t.convert()
            picture[name] = t
    return picture

def get_image(sheet, x, y, width, height, colorkey, scale):     #colorkey是图像底色，用于图像扣掉底色     scale是放大倍数
    image = pygame.Surface((width, height))
    image.blit(sheet,(0, 0), (x, y, width, height))      # 0,0是画到哪了，xywh是sheet里哪个区域要取出来
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
    return image
