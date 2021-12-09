from ..element import info
import pygame
from .. import Tools, setup
from .. import Constants as C
from ..element import player, stuff, brick, pro_box, enemy
import os
import json

class Level:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'game_over'
        self.info = info.Info('level', self.game_info)
        self.load_map_data()        # 加载地图
        self.setup_background()
        self.setup_start_positions()        # 设置起始位置
        self.setup_player()
        self.setup_ground_items()
        self.setup_bricks_AND_boxes()
        self.setup_enemies()
        self.setup_checkpoints()

    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = os.path.join('Document/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

    def setup_background(self):
        # self.background = setup.PICTURE['level_1']      # 硬编码不提倡
        self.image_name = self.map_data['image_name']
        self.background = setup.PICTURE[self.image_name]
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BG_MULTI),
                                                                   int(rect.height * C.BG_MULTI)))
        self.background_rect = self.background.get_rect()
        self.game_window = setup.SCREEN.get_rect()

        # 让人物越过1/3的画面时，窗口跟着移动
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]

    def setup_player(self):
        self.player = player.Player('mario')
        # self.player.rect.x = 300
        # self.player.rect.y = 490        # 站在了地上
        self.player.rect.x = self.game_window.x + self.player_x     # 窗口的x + 玩家相对的x
        self.player.rect.bottom = self.player_y     # player_y是人物脚所在的位置

    def update(self, surface, keys):
        """
        在if的过程中对于死亡等不同的状态做分支处理
        :param surface:
        :param keys:
        :return:
        """
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys)
        if self.player.dead:
            if self.current_time - self.player.dead_timer > 3000:
                self.finished = True
                self.update_game_info()
        else:
            self.update_player_position()
            self.check_check_points()
            self.check_ifgoto_die()
            self.update_game_window()
            self.info.update()
            self.bricks_group.update()
            self.boxes_group.update()
            self.enemy_group.update(self)
            self.die_group.update(self)
            self.shell_K_group.update(self)

        self.draw(surface)

    def update_player_position(self):
        """
        主角位置更新的代码，改用update_game_window窗口
        :return:
        """
        # x 方向
        self.player.rect.x += self.player.x_vel   #人物正常移动
        # if self.player.rect.x < 0:
        #     self.player.rect.x = 0
        # if self.player.rect.x > C.SCREEN_W - 16 * C.PLAYER_MULTI:
        #     self.player.rect.x = C.SCREEN_W - 16 * C.PLAYER_MULTI
             # 上面注释是以前人物移动而非窗口移动的编码
        # 下面防止人物超出地图，跑到别的“关卡”中
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        self.check_x_collisions()

        # y 方向
        if not self.player.dead:
            self.player.rect.y += self.player.y_vel
            self.check_y_collisions()

    def update_game_window(self):       # 滑动的移动窗口
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_vel     # 不能走出地图，看65行最后的注释
            self.start_x = self.game_window.x       # 不能回头走出窗口

    def draw(self, surface):
        self.game_ground.blit(self.background, self.game_window, self.game_window)      # 新建空图层用于画出1/3移动窗口的效果
        self.game_ground.blit(self.player.image, self.player.rect)
        self.bricks_group.draw(self.game_ground)
        self.boxes_group.draw(self.game_ground)
        self.enemy_group.draw(self.game_ground)
        self.die_group.draw(self.game_ground)
        self.shell_K_group.draw(self.game_ground)

        surface.blit(self.game_ground, (0,0), self.game_window)      # blit方法用于将目标图层的特定位置画到指定图层，第二个参数是目标图层的左上角放到原图层的哪个位置
        self.info.draw(surface)

    def setup_ground_items(self):
        """
        通过读取json文件，获取每个物体的坐标和名字，大小
        并且用item类实例化出来
        :return:
        """
        self.ground_items_groups = pygame.sprite.Group()        # 这里用了精灵组...
        for name in ['step','pipe','ground']:
            for item in self.map_data[name]:
                self.ground_items_groups.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def check_x_collisions(self):
        """
        x方向的碰撞检测
        用精灵类中的碰撞检测：检查一个精灵是否与精灵组中的任意一个精灵发生碰撞
        :return:
        """
        check_group = pygame.sprite.Group(self.ground_items_groups, self.bricks_group, self.boxes_group)
        coll_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if coll_sprite:
            self.adjust_player_x(coll_sprite)
        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy:
            self.player.todie()

        shell = pygame.sprite.spritecollideany(self.player, self.shell_K_group)
        if shell:
            if shell.state == 'slide':
                self.player.todie()
            else:
                if self.player.rect.x < shell.rect.x:
                    shell.x_vel = 10
                    shell.rect.x += 40
                    shell.direction = 1
                else:
                    shell.x_vel = -10
                    shell.rect.x -= 40
                    shell.direction = 0
                shell.state = 'slide'

    def adjust_player_x(self, sprite):
        """
        对目标碰撞后的x位置调整
        :return:
        """
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left       # 从左碰撞，位置变成物体的右边
        else:
            self.player.rect.left < sprite.rect.right
        self.player.x_vel = 0


    def check_y_collisions(self):
        """
        y 方向上的碰撞检测
        :return:
        """
        check_group = pygame.sprite.Group(self.ground_items_groups, self.bricks_group, self.boxes_group)
        coll_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if coll_sprite:
            self.adjust_player_y(coll_sprite)

        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy:
            self.enemy_group.remove(enemy)
            if enemy.name == 'koopa':
                self.shell_K_group.add(enemy)
            else:
                self.die_group.add(enemy)

            if self.player.y_vel < 0:       # 如果碰撞时的速度小于0，产生不同死法
                how =  'bumped'
            else:
                how = 'trampled'
                self.player.state = 'jump'
                self.player.rect.bottom = enemy.rect.top
                self.player.y_vel = self.player.jump_vel * 0.8
            enemy.todie(how)
        self.check_need_fall(self.player)

    def adjust_player_y(self, sprite):
        """
        对目标碰撞后的y位置调整
        if  从上面碰撞，撞头=白撞
        if  从下面碰撞，有个小回弹
        :param sprite:
        :return:
        """
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.rect.bottom = sprite.rect.top
            self.player.y_vel = 0
            self.player.state = 'walk'
        else:
            self.player.y_vel = 7
            self.player.rect.top = self.player.rect.bottom
            self.player.state = 'fall'

    def check_need_fall(self, sprite):
        """
        确保从物体上跳下时能落回地面
        :param sprite:
        :return:
        """
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_groups, self.bricks_group, self.boxes_group)
        coll_sprite = pygame.sprite.spritecollideany(sprite, check_group)
        if not coll_sprite and sprite.state != 'jump':     # 防止jump的时候也下落
            sprite.state = 'fall'
        sprite.rect.y -= 1

    def check_ifgoto_die(self):     # 判断马里奥是否掉到窗口外了
        if self.player.rect.y > C.SCREEN_H:
            self.player.todie()

    def update_game_info(self):
        """
        每当人物死亡一次，就生命数减一
        如果生命数为0，下一个阶段就是‘game-over’
            否则就是加载’load‘的screen
        :return:
        """
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next = 'game_over'
        else:
            self.next = 'load'

    def setup_bricks_AND_boxes(self):
        """
        在地图中添加 bricks-砖块 和 box宝箱
        :return:
        """
        self.bricks_group = pygame.sprite.Group()
        self.boxes_group = pygame.sprite.Group()
        if 'brick' in self.map_data:
            for bricks_data in self.map_data['brick']:
                x, y = bricks_data['x'], bricks_data['y']
                brick_type = bricks_data['type']
                if 'brick_num' in bricks_data:
                    #TODO 水管世界
                    pass
                else:
                    self.bricks_group.add(brick.Brick(x, y, brick_type))

        if 'box' in self.map_data:
            for boxes_data in self.map_data['box']:
                x, y = boxes_data['x'], boxes_data['y']
                box_type = boxes_data['type']
                self.boxes_group.add(pro_box.Box(x, y, box_type))

    def setup_enemies(self):
        self.die_group = pygame.sprite.Group()
        self.shell_K_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id, enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data))
                self.enemy_group_dict[enemy_group_id] = group

    def setup_checkpoints(self):
        self.checkpoints_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x, y, w, h = item['x'], item['y'], item['width'], item['height']
            checkpoint_type = item['type']
            enemy_groupid = item.get('enemy_groupid')
            self.checkpoints_group.add(stuff.Checkpoint(x, y, w, h, checkpoint_type, enemy_groupid))

    def check_check_points(self):
        """
        如果检查点被玩家触碰，且检查点的类型是0
            则释放野怪
        :return:
        """
        checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoints_group)
        if checkpoint:
            if checkpoint.checkpoint_type == 0:
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])
            checkpoint.kill()
