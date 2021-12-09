import pygame
from . import Constants as C
from . import Tools

pygame.init()
# PlaneGame.display.set_mode((800,600))
SCREEN = pygame.display.set_mode((C.SCREEN_W, C.SCREEN_H))

PICTURE = Tools.load_picture('Material/picture')