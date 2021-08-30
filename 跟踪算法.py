import pygame, sys
from math import *

pygame.init()
font1 = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 23)
textc = font1.render('*', True, (250, 0, 0))
screen = pygame.display.set_mode((800, 700), 0, 32)
missile = pygame.image.load(r'C:\Users\T480S\Desktop/640.png').convert_alpha()
height = missile.get_height()
width = missile.get_width()
pygame.mouse.set_visible(0)
x1, y1 = 100, 600  # 导弹的初始发射位置
velocity = 800  # 导弹速度
time = 1 / 1000  # 每个时间片的长度
clock = pygame.time.Clock()
A = ()
B = ()
C = ()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(300)
    x, y = pygame.mouse.get_pos()  # 获取鼠标位置，鼠标就是需要打击的目标
    distance = sqrt(pow(x1 - x, 2) + pow(y1 - y, 2))  # 两点距离公式
    section = velocity * time  # 每个时间片需要移动的距离
    sina = (y1 - y) / distance
    cosa = (x - x1) / distance
    angle = atan2(y - y1, x - x1)  # 两点间线段的弧度值
    fangle = degrees(angle)  # 弧度转角度
    x1, y1 = (x1 + section * cosa, y1 - section * sina)
    missiled = pygame.transform.rotate(missile, -(fangle))
    if 0 <= -fangle <= 90:
        A = (width * cosa + x1 - width, y1 - height / 2)
        B = (A[0] + height * sina, A[1] + height * cosa)

    if 90 < -fangle <= 180:
        A = (x1 - width, y1 - height / 2 + height * (-cosa))
        B = (x1 - width + height * sina, y1 - height / 2)

    if -90 <= -fangle < 0:
        A = (x1 - width + missiled.get_width(), y1 - height / 2 + missiled.get_height() - height * cosa)
        B = (A[0] + height * sina, y1 - height / 2 + missiled.get_height())

    if -180 < -fangle < -90:
        A = (x1 - width - height * sina, y1 - height / 2 + missiled.get_height())
        B = (x1 - width, A[1] + height * cosa)

    C = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)

    screen.fill((0, 0, 0))
    screen.blit(missiled, (x1 - width + (x1 - C[0]), y1 - height / 2 + (y1 - C[1])))
    screen.blit(textc, (x, y))  # 鼠标用一个红色*代替
    pygame.display.update()
