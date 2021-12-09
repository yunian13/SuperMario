# -*- ecoding: utf-8 -*-
# @ModuleName: brick
# @Function: 
# @Author: Kylo
# @Time: 2021/12/7 23:45

import pygame
from .. import Tools, setup
from .. import Constants as C

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, brick_type, color = None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.brick_type = brick_type
        bright_rect_frames = [(16, 0, 16, 16), (48, 0, 16, 16)]
        dark_rect_frames = [(16, 32, 16, 16), (48, 32, 16, 16)]

        if not color:
            self.frame_rects = bright_rect_frames
        else:
            self.frame_rects = dark_rect_frames

        self.frames = []
        for frame_rect in self.frame_rects:
            self.frames.append(Tools.get_image(setup.PICTURE['tile_set'], *frame_rect, (0, 0, 0), C.BRICK_MULTI))

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y