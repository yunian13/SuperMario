import pygame
from sprite import *

class PlaneGame(object):

    def __init__(self):

        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        self.clock = pygame.time.Clock()

        self.__create_sprite()

        pygame.time.set_timer(CREATE_ENEMY_EVENT, 3000)
        pygame.time.set_timer(CREATE_MONEY_EVENT, 2000)

    def __create_sprite(self):

        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        self.enemy_group = pygame.sprite.Group()
        self.money_group = pygame.sprite.Group()

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("start")

        while True:
            self.clock.tick(FRAME_PER_SEC)

            self.__event_handler()

            self.__check_collide()

            self.__update_sprites()

            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                PlaneGame.__game_over()

            elif event.type == CREATE_ENEMY_EVENT:
                print("enemy show time")
                enemy = Enemy()
                self.enemy_group.add(enemy)

            elif event.type == CREATE_MONEY_EVENT:
                print("money show time")
                money = Money()
                self.money_group.add(money)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 3
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -3

        elif keys_pressed[pygame.K_UP]:
            self.hero.speed_y = -3

        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed_y = 3


        else:
            self.hero.speed = 0
            self.hero.speed_y = 0

    def __check_collide(self):

        moneys = pygame.sprite.spritecollide(self.hero, self.money_group, True)
        if len(moneys) > 0:
            score = len(moneys)
            print(score)
            if score >= 20:
                self.hero.kill()
                print("you are very good")

        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()

            PlaneGame.__game_over()

    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.money_group.update()
        self.money_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print("game over")

        pygame.quit()
        exit()

    def startGame(self):
        game = PlaneGame()

        game.start_game()

if __name__ == '__main__':
    game = PlaneGame()

    game.start_game()


