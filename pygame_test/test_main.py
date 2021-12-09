import pygame
pygame.init()   #初始化

w,h = 500,500   #宽和高变量
pygame.display.set_mode((w,h))  #定义屏幕大小
screen = pygame.display.get_surface()   #做图层，画布0

#载入背景图并且缩放到w,h
bgpic = pygame.image.load('images.jfif')
bgpic = pygame.transform.scale(bgpic,(w,h))     #缩放

#加载人物图像
personpic = pygame.image.load('Isaac.png')

#创建精灵（所有元素都是精灵）
mario = pygame.sprite.Sprite()
mario.image = personpic
mario.rect = mario.image.get_rect()     #获得精灵的轮廓、位置等信息
mario.rect.x, mario.rect.y = w/2, h/2       #更改精灵的位置坐标

#玩家组（添加精灵->方便管理）
player_group = pygame.sprite.Group()
player_group.add(mario)

#开始游戏
while True :    #持续更新角色的状态再画图
    for event in pygame.event.get():    #从pygame中不断获取鼠标的事件event
        if event.type == pygame.QUIT:   #如果事件类型为退出则退出游戏
            pygame.display.quit()
            quit()
        if event.type == pygame.KEYDOWN:    #如果是keydown，证明有按键被按下了
            keys = pygame.key.get_pressed()     #首先获得此刻按键们的状态；get_press会返回一个装满0101010...的列表（记录各个按键的此刻状态）
            if keys[pygame.K_DOWN]:     #k_down是向下键的索引值，在列表中查找这个，是否被按下
                mario.rect.y += 10
            if keys[pygame.K_UP]:
                mario.rect.y -= 10
            if keys[pygame.K_LEFT]:
                mario.rect.x -= 10
            if keys[pygame.K_RIGHT]:
                mario.rect.x += 10

    #画图
    screen.blit(bgpic,(0,0))        #贴上背景图；0，0是从左上角起
    player_group.draw(screen)
    pygame.display.update()
