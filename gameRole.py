# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013
@author: Leo
Modified on Mon Dec 17 19:05:00 2018
@Annotation added by Huntersx

"""

import pygame


#####   gameRole   #####
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()   #子弹的初始矩形框
        self.rect.midbottom = init_pos     #子弹初始化的中底部位置
        self.speed = 10   #子弹的速度

    def move(self):
        self.rect.top -= self.speed

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 用来存储玩家对象图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())    #透明转换
        self.rect = player_rect[0]                      # 玩家初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.speed = 8                                  # 初始化玩家速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家图片索引
        self.is_hit = False                             # 玩家是否被击中

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)    # 子弹类，初始子弹的中底部位置为玩家的中顶部位置
        self.bullets.add(bullet)    #添加到子弹集合中

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0    #到达顶端
        else:
            self.rect.top -= self.speed    #向上移动

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height   #到达底端
        else:
            self.rect.top += self.speed   #向下移动

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0    #到达界面左端
        else:
            self.rect.left -= self.speed   #向左平移

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width   #到达界面右端
        else:
            self.rect.left += self.speed     #向右平移

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos     #初始化矩形的左上角坐标
       self.down_imgs = enemy_down_imgs
       self.speed = 2    #敌军的速度
       self.down_index = 0

    def move(self):
        self.rect.top += self.speed   #敌军一直往下移动