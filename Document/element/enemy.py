# -*- ecoding: utf-8 -*-
# @ModuleName: enemy
# @Function: 
# @Author: Kylo
# @Time: 2021/12/8 0:35

import pygame
from .. import setup, Tools
from .. import Constants as C

def create_enemy(enemy_data):
    """
    根据json文件中的怪物类型，生成怪物
    :param enemy_data:
    :return:
    """
    enemy_type = enemy_data['type']
    x, bottom_y, direction, color = enemy_data['x'], enemy_data['y'], enemy_data['direction'], enemy_data['color']
    if enemy_type == 0:
        enemy = G_enemy(x, bottom_y, direction, 'goomba', color)       # 蘑菇怪
    elif enemy_type == 1:
        enemy = K_enemy(x, bottom_y, direction, 'koopa', color)       # 乌龟

    return enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, bottom_y, direction, name, frame_rects):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.name = name
        self.frame_index = 0
        self.left_frame = []
        self.right_frame = []

        self.load_frames(frame_rects)
        self.frames = self.left_frame if self.direction == 0 else self.right_frame
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = bottom_y

        self.timer = 0
        self.x_vel = -1 * C.ENEMY_SPEED if self.direction == 0 else C.ENEMY_SPEED
        self.y_vel = 0
        self.gravity = C.GRAVITY
        self.state = 'walk'


    def load_frames(self, frame_rects):
        for frame_rects in frame_rects:
            left_frame = Tools.get_image(setup.PICTURE['enemies'], *frame_rects, (0, 0, 0), C.ENEMY_MULTI)
            right_frame = pygame.transform.flip(left_frame, True, False)
            self.left_frame.append(left_frame)
            self.right_frame.append(right_frame)

    def update(self, level):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(level)
        self.update_position(level)

    def handle_states(self, level):
        if self.state == 'trampled':
            self.trampled(level)
        elif self.state == 'walk':
            self.walk()
        elif self.state == 'fall':
            self.fall()
        elif self.state == 'die':
            self.die()
        elif self.state == 'slide':
            self.slide()

        if self.direction:
            self.image = self.right_frame[self.frame_index]
        else:
            self.image = self.left_frame[self.frame_index]

    def walk(self):
        if self.current_time - self.timer > 125:
            self.frame_index = (self.frame_index + 1) % 2
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time

    def fall(self):
        if self.y_vel < 10:
            self.y_vel += self.gravity

    def update_position(self, level):
        self.rect.x += self.x_vel
        self.check_x_collision(level)
        self.rect.y += self.y_vel
        if self.state != 'die':
            self.check_y_collision(level)

    def check_x_collision(self, level):
        sprite = pygame.sprite.spritecollideany(self, level.ground_items_groups)
        if sprite:
            if self.direction:
                self.direction = 0
                self.rect.right = sprite.rect.left
            else:
                self.direction = 1
                self.rect.left = sprite.rect.right
            self.x_vel *= -1

        if self.state == 'slide':
            enemy = pygame.sprite.spritecollideany(self, level.enemy_group)
            if enemy:
                enemy.todie(how = 'slide')
                level.enemy_group.remove(enemy)
                level.die_group.add(enemy)

    def check_y_collision(self, level):
        check_group = pygame.sprite.Group(level.ground_items_groups, level.boxes_group, level.bricks_group)
        sprite = pygame.sprite.spritecollideany(self, check_group)
        if sprite:
            if self.rect.top < sprite.rect.top:
                self.rect.bottom = sprite.rect.top
                self.y_vel = 0
                self.state = 'walk'
        level.check_need_fall(self)

    def die(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.y_vel += self.gravity
        if self.rect.y > C.SCREEN_H:
            self.kill()

    def todie(self, how):
        self.dead_timer = self.current_time
        if how in ['bumped', 'slide']:
            self.y_vel = -8
            self.gravity = 0.6
            self.state = 'die'
            self.frame_index = 2
        elif how == 'trampled':
            self.state = 'trampled'

    def trampled(self, level):
        """
        如果野怪被踩踏，一个变扁，一个变成壳
        所以需要不同子类方法去实现
        :return:
        """
        pass

    def slide(self):
        pass



class G_enemy(Enemy):
    def __init__(self, x, bottom_y, direction, name, color):
        bright_rect_frames = [(0, 16, 16, 16), (16, 16, 16, 16), (32, 16, 16, 16)]
        dark_rect_frames = [(0, 48, 16, 16), (16, 48, 16, 16), (32, 48, 16, 16)]

        if not color:
            frame_rects = bright_rect_frames
        else:
            frame_rects = dark_rect_frames

        Enemy.__init__(self, x, bottom_y, direction, name, frame_rects)


    def trampled(self, level):
        """
        换个皮肤，掐个表：到点消失
        :return:
        """
        self.x_vel = 0
        self.frame_index = 2
        if self.dead_timer == 0:
            self.dead_timer = self.current_time
        if self.current_time - self.dead_timer > 500:
            self.kill()


class K_enemy(Enemy):
    def __init__(self, x, bottom_y, direction, name, color):
        bright_rect_frames = [(96, 9, 16, 22), (112, 9, 16, 22), (160, 9, 16, 22)]
        dark_rect_frames = [(96, 72, 16, 22), (112, 72, 16, 22), (160, 72, 16, 22)]

        if not color:
            frame_rects = bright_rect_frames
        else:
            frame_rects = dark_rect_frames

        Enemy.__init__(self, x, bottom_y, direction, name, frame_rects)
        self.shell_timer = 0

    def trampled(self, level):
        self.x_vel = 0
        self.frame_index = 2

        # 若龟壳不去动他，静止一段时间就会变回乌龟
        if self.shell_timer == 0:
            self.shell_timer = self.current_time
        if self.current_time - self.shell_timer > 5000:
            self.state = 'walk'
            self.x_vel = -C.ENEMY_SPEED if self.direction == 0 else C.ENEMY_SPEED
            level.enemy_group.add(self)
            level.shell_K_group.remove(self)
            self.shell_timer = 0

    def slide(self):
        pass