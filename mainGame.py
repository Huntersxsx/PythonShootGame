# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013
@author: Leo
Modified on Mon Dec 17 19:05:00 2018
@Annotation added by Huntersx

"""
from sys import exit
from pygame.locals import *
from gameRole import *
import random

#####   mainGame   #####
# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))   #界面大小
pygame.display.set_caption('Aircraft Battle')

# 载入游戏音乐
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')   #pygame.mixer.Sound用来播放声音片段
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)       #set_volume用来控制音量
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')    #播放音乐文件
pygame.mixer.music.play(-1, 0.0)   #-1表示循环播放
pygame.mixer.music.set_volume(0.25)

# 载入背景图
background = pygame.image.load('resources/image/background.png').convert()   #普通的转换，相同于display
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

# 设置玩家相关参数
player_rect = []
#pygame.Rect(left, top, width, height)，可用来剪切图片
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家图片区域，两种尾气喷射状态
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸图片区域，4种静态图片合成动态
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))     #对应的是灰烬
player_pos = [200, 600]                          # 玩家左上角初始化在屏幕的位置
player = Player(plane_img, player_rect, player_pos)   #玩家类

# 定义子弹对象使用的surface相关参数
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)    #截取获得子弹图片

# 定义敌机对象使用的surface相关参数
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)    #截取获得敌机图片
#敌机被击落的图片，4种静态合成动态
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))   #爆炸
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))   #灰烬

enemies1 = pygame.sprite.Group()

# 存储被击毁的飞机，用来渲染击毁动画
enemies_down = pygame.sprite.Group()

shoot_frequency = 0    #射击的频率
enemy_frequency = 0    #敌机出现的频率

player_down_index = 16

score = 0    #得分

clock = pygame.time.Clock()    #Pygame.time.Clock()可以控制每个循环多长时间运行一次

running = True

while running:
    # 控制游戏最大帧率为60
    clock.tick(60)    #每秒内循环要运行的次数

    # 控制发射子弹频率,并发射子弹
    if not player.is_hit:
        if shoot_frequency % 15 == 0:    #1s发射4次子弹
            bullet_sound.play()
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:    #控制在0-15，目的是让玩家的图片索引值为0和1
            shoot_frequency = 0

    # 生成敌机
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]   #随机初始化敌机左上角的位置
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)     #敌机类
        enemies1.add(enemy1)      #添加到敌机集合中
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # 移动子弹，若超出窗口范围则删除
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:    #玩家的子弹超出屏幕
            player.bullets.remove(bullet)   #删除

    # 移动敌机，若超出窗口范围则删除
    for enemy in enemies1:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)   #被撞到的敌机也爆炸
            player.is_hit = True    #flag置1
            game_over_sound.play()   #播放game over声效
            break
        if enemy.rect.top > SCREEN_HEIGHT:   #敌机飞行超过窗口，删除
            enemies1.remove(enemy)

    # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency // 8   #索引值为0、1
    else:
        player.img_index = player_down_index // 8   #player_down_index的初始值为16
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:    #控制player_down_index在16-47，目的是让玩家图片索引值为2，3，4，5，形成爆炸效果
            running = False

    # 绘制击毁动画
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 绘制子弹和敌机
    player.bullets.draw(screen)
    enemies1.draw(screen)

    # 绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # 监听键盘事件
    key_pressed = pygame.key.get_pressed()
    # 若玩家被击中，则无效
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:  #w或者上剪头
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:  #s或者下剪头
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:   #a或者左剪头
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:   #d或者右剪头
            player.moveRight()


font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
