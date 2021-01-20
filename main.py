import math
import pygame
from background import *

pygame.init()

#Window settings
screen_width = 800
screen_heigth = 600
screen = pygame.display.set_mode((screen_width, screen_heigth))
pygame.display.set_caption('Spider Man Atari 2600')

#Sprites
spiderman = pygame.image.load('Images/spiderman.png')
spd_right = pygame.image.load('Images/swing_right.png')
spd_left = pygame.image.load('Images/swing_left.png')
# goblin = pygame.image.load('Images/goblin.png')

#Initial conditions
x = screen_width/2 + spiderman.get_width()/2
y = screen_heigth/2 + spiderman.get_height()/2

#Keys
up_key = False
down_key = False
right_key = False
left_key = False

#Web controls
web_shooting = False
web_distance = 0
shot_up = False
shot_right = False
shot_left = False
web_active = False

#Colours
col_sky = pygame.Color(56,146,215)
build_sky = pygame.Color(232,216,73)

#Background
col_sky = pygame.Color(56,146,215)
build_sky = pygame.Color(232,216,73)
obj_color = (col_sky, build_sky)
# scroll = len(level) - (600//25)



running = True
while running:
    for ev in pygame.event.get():
        
        if ev.type == pygame.QUIT:
            running = False
        
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                running = False
                
            if ev.key == pygame.K_SPACE:
                web_shooting = True
                web_active = False
            if ev.key == pygame.K_LEFT:
                left_key = True
            if ev.key == pygame.K_RIGHT:
                right_key = True
            if ev.key == pygame.K_UP:
                up_key = True
            if ev.key == pygame.K_DOWN:
                down_key = True
        
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_SPACE:
                web_shooting = False
                web_active = True                
            if ev.key == pygame.K_LEFT:
                left_key = False
            if ev.key == pygame.K_RIGHT:
                right_key = False
            if ev.key == pygame.K_UP:
                up_key = False
            if ev.key == pygame.K_DOWN:
                down_key = False
    
    if web_shooting:
        if web_distance == 0:
            anchor = (x-29,y-40)
            if up_key:
                shot_up = True
                shot_right = False
                shot_left = False
            if right_key:
                shot_up = False
                shot_right = True
                shot_left = False
            if left_key:
                shot_up = False
                shot_right = False
                shot_left = True
                
        if web_distance < 150:
            if up_key and shot_up:
                web_distance += 1               
                anchor = (x-29, y -40- web_distance)
            elif right_key and shot_right:
                direction = 1
                web_distance += 1               
                anchor = (x-29 + web_distance, y -40- web_distance)
            elif left_key and shot_left:
                direction = -1
                web_distance += 1               
                anchor = (x-29-web_distance, y -40- web_distance)
                
    if web_active:
        if web_distance != 0:
            if shot_up:
                web_hptn = web_distance
            else:
                web_hptn = math.sqrt(2*web_distance**2)
            web_distance = 0
        
        
        
        
        if origin[1] <= anchor[1]:
            web_distance = 0
            web_active = False
        
        if shot_up:
            if up_key:
                y -= 1
                web_distance -= 1                
            elif down_key and web_hptn < 150:
                y += 1
                web_hptn += 1
            
        else:
            swing_x = abs(origin[0]-anchor[0])
            swing_y = abs(origin[1]-anchor[1])
            if web_distance != 0:
                web_hptn = math.sqrt(2*web_distance**2)
                web_distance = 0
            
            if up_key:
                cos = swing_x / web_hptn
                sin = swing_y / web_hptn
                y -= sin
                if origin[0] - anchor[0] > 0:
                    x -= cos
                else:
                    x += cos
                web_hptn -= math.sqrt(sin**2+cos**2)
            elif down_key and web_hptn < 150:
                cos = swing_x / web_hptn
                sin = swing_y / web_hptn
                y += sin
                if origin[0] - anchor[0] > 0:
                    x -= cos
                else:
                    x += cos
                web_hptn += math.sqrt(sin**2+cos**2)
            else:
                if swing_x >= swing_y and \
                    ((direction == 1 and origin[0] > anchor[0]) or \
                    (direction == -1 and origin[0] < anchor[0])):                    
                    direction = direction * (-1)
                if direction == 1:
                    x += 0.25
                elif direction == -1:
                    x -= 0.25
                origin = (x-29,y-40)
                swing_x = abs(origin[0]-anchor[0])  
                y += math.sqrt(web_hptn**2-swing_x**2) - swing_y
    
    #Draw
    screen.fill('black')            
    if web_active or web_shooting:
        origin = (x-29,y-40)
        pygame.draw.line(screen,(255,255,255),origin,anchor,5)
    if web_active:
        if origin[0] - anchor[0] >= 0:
            screen.blit(spd_left,(x - int(spiderman.get_width()/2), y - int(spiderman.get_width()/2)))
        else:
            screen.blit(spd_right,(x - int(spiderman.get_width()/2), y - int(spiderman.get_width()/2)))
    else:
        screen.blit(spiderman, (x - int(spiderman.get_width()/2), y - int(spiderman.get_width()/2)))
    pygame.display.flip()
        
pygame.quit()