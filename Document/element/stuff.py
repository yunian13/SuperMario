# -*- ecoding: utf-8 -*-
# @ModuleName: stuff
# @Function: 
# @Author: Kylo
# @Time: 2021/12/7 21:44

import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h)).convert()       # 这个图层是给物体添加了轮廓
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name

class Checkpoint(Item):
    def __init__(self,x, y, w, h, checkpoint_type, enemy_groupid = None, name = 'checkpoint'):
        Item.__init__(self, x, y, w, h, name)
        self.checkpoint_type = checkpoint_type
        self.enemy_groupid = enemy_groupid