import pygame
from .. import Tools, setup
from .. import Constants as C

class FlashingCoin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frames_index = 0
        frame_rect = [(1, 160, 5, 8), (9, 160, 5, 8), (17, 160, 5, 8), (9, 160, 5, 8)]      # blink~
        self.load_frames(frame_rect)
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect()
        self.rect.x = 280
        self.rect.y = 60
        self.timer = 0

    def load_frames(self, frame_rect):
        sheet = setup.PICTURE['item_objects']
        for frame_rect in frame_rect:
            self.frames.append(Tools.get_image(sheet, *frame_rect, (0,0,0), C.BG_MULTI))

    def update(self):
        self.current_time = pygame.time.get_ticks()
        frame_duration = [375, 125, 125, 125]

        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > frame_duration[self.frames_index]:
            self.frames_index += 1
            self.frames_index %= 4
            self.timer = self.current_time

        self.image = self.frames[self.frames_index]