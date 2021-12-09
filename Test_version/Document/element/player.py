import pygame
from ..import Tools,setup
from .. import Constants as C
import json
import os

class Player (pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

    def load_data(self):        # json文件转化成字典
        file_name = self.name + '.json'
        file_path = os.path.join('Document/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    def setup_states(self):
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.big = False
        self.ispossible_jump = True

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_vel = 0
        self.y_vel = 0

        self.max_walk_vel = speed['max_walk_speed']
        self.max_run_vel = speed['max_run_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.run_accel = speed['run_accel']
        self.turn_accel = speed['turn_accel']
        self.gravity = C.GRAVITY
        self.anti_gravity = C.ANTI_GRAVITY

        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel

    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer = 0
        self.dead_timer = 0

    def load_images(self):
        sheet = setup.PICTURE['mario_bros']
        frame_rect = self.player_data['image_frames']

        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.right_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []

        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.big_fire_frames = [self.right_big_fire_frames, self.left_big_fire_frames]

        self.all_frames = [
            self.right_small_normal_frames,
            self.right_big_normal_frames,
            self.right_big_fire_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.left_big_fire_frames
        ]

        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames

        for group, group_frame_rect in frame_rect.items():
            for frame_rect in group_frame_rect:
                right_image = Tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0,0,0), C.PLAYER_MULTI)
                left_image = pygame.transform.flip(right_image, True, False)
                if group == 'right_small_normal':
                    self.left_small_normal_frames.append(left_image)
                    self.right_small_normal_frames.append(right_image)
                if group == 'right_big_normal':
                    self.left_big_normal_frames.append(left_image)
                    self.right_big_normal_frames.append(right_image)
                if group == 'right_big_fire':
                    self.left_big_fire_frames.append(left_image)
                    self.right_big_fire_frames.append(right_image)

        self.frame_index = 0
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    # def update(self, keys):
    #     self.current_time = PlaneGame.time.get_ticks()
    #     if keys[PlaneGame.K_RIGHT]:
    #         self.state = 'walk'
    #         self.x_vel = 5
    #         self.y_vel = 0
    #         self.frames = self.right_frames
    #     if keys[PlaneGame.K_LEFT]:
    #         self.state = 'walk'
    #         self.x_vel = -5
    #         self.y_vel = 0
    #         self.frames = self.left_frames
    #     # if keys[PlaneGame.K_UP]:
    #     #     self.state = 'walk'
    #     #     self.x_vel = 0
    #     #     self.y_vel = -5
    #     #     self.frames = self.up_frames
    #     # if keys[PlaneGame.K_DOWN]:
    #     #     self.state = 'walk'
    #     #     self.x_vel = 0
    #     #     self.y_vel = 5
    #     #     self.frames = self.down_frames
    #     if keys[PlaneGame.K_SPACE]:
    #         self.state = 'jump'
    #         self.y_vel = -5
    #     if self.state == 'walk':
    #         if self.current_time - self.walking_timer > 100:
    #             self.walking_timer = self.current_time
    #             self.frame_index += 1
    #             self.frame_index %= 4
    #     if self.state == 'jump':
    #         self.frame_index = 4
    #     self.image = self.frames[self.frame_index]
    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(keys)

    def handle_states(self, keys):

        self.ispossible_jump_or_cant(keys)

        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'die':
            self.die(keys)

        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    def ispossible_jump_or_cant(self, keys):
        if not keys[pygame.K_a]:
            self.ispossible_jump = True

    def stand(self, keys):
        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'
        elif keys[pygame.K_a] and self.ispossible_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel

    def jump(self, keys):
        self.frame_index = 4        # 跳跃帧是第四帧
        self.y_vel += self.anti_gravity
        self.ispossible_jump = False

        if self.y_vel >= 0:
            self.state = 'fall'

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)

        if not keys[pygame.K_a]:    # 大小跳
            self.state = 'fall'

    def fall(self, keys):
        self.y_vel = self.calc_vel(self.y_vel, self.gravity, self.max_y_vel)

        # # TODO 碰撞测试（已经更新，不用下面愣方法了）
        # if self.rect.bottom > C.GROUND_HEIGHT:
        #     self.rect.bottom = C.GROUND_HEIGHT
        #     self.y_vel = 0
        #     self.state = 'walk'

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)

    def walk(self, keys):
        if keys[pygame.K_s]:        # 如果‘s'键被按下，就变成冲刺状态
            self.max_x_vel = self.max_run_vel       # 最大速度变成最大跑步速度
            self.x_accel = self.run_accel       # 最大加速度变成jason中的最大加速度
        else:
            self.max_x_vel = self.max_walk_vel
            self.x_accel = self.walk_accel

        if keys[pygame.K_a] and self.ispossible_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel

        if self.current_time - self.walking_timer > self.calc_frame():        # 如果设计成定值就会不同速度但是有相同的摆臂，换成动态的帧数计算函数
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            # self.x_vel = 5
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)      # 人物右行，速度方向为正（加上一个加速度）同时最快不能超过最大速度
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)     # 人物左行，速度方向为正（减上一个加速度）同时最快不能小于负最大速度
        else:       # 人物从行走状态变成静止的状态
            if self.face_right:
                self.x_vel -= self.x_accel
                if self.x_vel < 0:
                    self.x_vel = 0
                    self.state = 'stand'
                else:
                    self.x_vel += self.x_accel
                    if self.x_vel > 0:
                        self.x_vel = 0
                        self.state = 'stand'

    def calc_vel(self, vel, accel, max_vel, is_positive = True):        # 速度计算函数
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)
    def calc_frame(self):
        frame = -60 / self.max_run_vel * abs(self.x_vel) + 80
        return frame

    def todie(self):
        self.dead = True
        self.y_vel = self.jump_vel
        self.frame_index = 6    # 6号帧造型
        self.state = 'die'
        self.dead_timer = self.current_time

    def die(self, keys):
        """
        开关方法，处理人物死亡
        :param keys:
        :return:
        """
        self.rect.y += self.y_vel
        self.y_vel += self.anti_gravity