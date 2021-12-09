import pygame
from sprite import *
pygame.init()

screen = pygame.display.set_mode((480, 700))
# 绘制背景图像

bg = pygame.image.load("./Test_version/pygame_test/background.png") # 加载
screen.blit(bg, (0, 0)) # 绘制
# PlaneGame.display.update()
hero = pygame.image.load("./Test_version/pygame_test/Isaac.png")
screen.blit(hero, (200, 500))
pygame.display.update()
clock = pygame.time.Clock() # 创建时钟
hero_rect = pygame.Rect(150, 300, 102, 126)

enemy = GameSprite("./Test_version/pygame_test/enemy1.png", 2)
enemy_group = pygame.sprite.Group(enemy)
money = GameSprite("./Test_version/pygame_test/bullet_supply.png")
money_group = pygame.sprite.Group(money)


while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("game over")
            pygame.quit()
            exit()

    hero_rect.y -= 3

    if hero_rect.y <= 0:
        hero_rect.y = 700

    screen.blit(bg, (0, 0))

    screen.blit(hero, hero_rect)

    enemy_group.update()

    enemy_group.draw(screen)

    money_group.update()

    money_group.draw(screen)

    pygame.display.update()

pygame.quit()
