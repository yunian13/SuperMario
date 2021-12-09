import pygame
import random

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60

CREATE_ENEMY_EVENT = pygame.USEREVENT

CREATE_MONEY_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=1, speed_y=0):

        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.speed_y = speed_y

    def update(self):

        self.rect.y += self.speed


class Background(GameSprite):


    def __init__(self, is_alt = False):

        super().__init__("./Test_version/pygame_test/background.png")

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height






class Enemy(GameSprite):

    def __init__(self):

        super().__init__("./Test_version/pygame_test/enemy1.png")

        self.speed = random.randint(4, 6)

        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            print("delete")

            self.kill()

    def __del__(self):
        print("die {}".format(self.rect))

class Money(GameSprite):

    def __init__(self):

        super().__init__("./Test_version/pygame_test/bullet_supply.png")

        self.speed = random.randint(3, 5)

        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)


    def update(self):
        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            print("delete")

            self.kill()

    def __del__(self):
        print("die {}".format(self.rect))


class Hero(GameSprite):

    def __init__(self):

        super().__init__("./Test_version/pygame_test/life.png", 0)

        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom -120

    def update(self):

        self.rect.x += self.speed
        self.rect.y += self.speed_y

        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        elif self.rect.bottom > SCREEN_RECT.height:
            self.rect.bottom = SCREEN_RECT.height

        elif self.rect.y < 0:
            self.rect.y = 0
