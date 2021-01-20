import pygame
import math

from simple_functions import distance


pygame.init()
running = True

#Background and sprites
screen_width = 800
screen_heigth = 600
screen = pygame.display.set_mode((screen_width, screen_heigth))
pygame.display.set_caption('Spider Man Atari 2600')
spiderman = pygame.image.load('Images/spiderman.png')
spd_right = pygame.image.load('Images/swing_right.png')
spd_left = pygame.image.load('Images/swing_left.png')
# goblin = pygame.image.load('Images/goblin.png')

x = screen_width/2 + spiderman.get_width()/2
y = screen_heigth/2 + spiderman.get_height()/2
web_shooting = False
web_active = False
web_first_shot = True

shot_up = False
shot_right = False
shot_left = False

up_key = False
down_key = False
right_key = False
left_key = False

y_direction = -1

level = (
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    # visible at the beginning
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 2, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 2, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 2, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1),
#
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0),
    (0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0),#base v
#    
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0),
    (0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
)
col_sky = pygame.Color(56,146,215)
build_sky = pygame.Color(232,216,73)
obj_color = (col_sky, build_sky, 'red', 'yellow')
scroll_y = len(level) - (600//40)

def level2screen(row, col):  # -> (x, y)
    return col*40, (row-scroll_y)*40

def screen2level(x, y):  # -> (row, col)
    return y/40+scroll_y, x/40

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

    # Disparo da teia    
    if web_shooting:
        if web_first_shot:
            anchor = (x-29,y-40)
            web_distance = 0
            first_swing = True
            if up_key:
                shot_up = True
                shot_right = False
                shot_left = False
                web_first_shot = False
            if right_key:
                shot_up = False
                shot_right = True
                shot_left = False
                web_first_shot = False
            if left_key:
                shot_up = False
                shot_right = False
                shot_left = True
                web_first_shot = False
                
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

    # Movimento    
    if web_active:
        web_first_shot = True
        #Swing
        if not shot_up:
            if first_swing:
                web_hip = math.sqrt((web_distance**2)*2)
            if up_key:
                cos = abs(swing_x) / web_hip
                sin = abs(swing_y) / web_hip
                if anchor[0] == origin[0]:
                    y -= 1/5
                elif origin[0] - anchor[0] > 0:
                    x -= cos
                    y -= sin
                else:
                    x += cos
                    y -= sin
                web_hip -= 1
            elif down_key:
                cos = abs(swing_x) / web_hip
                sin = abs(swing_y) / web_hip
                if anchor[0] == origin[0]:
                    y += 1/5
                elif origin[0] - anchor[0] > 0:
                    x += cos
                    y += sin
                else:
                    x -= cos
                    y += sin
                web_hip += 1
            else:
                origin = (x-29,y-40)
                swing_x = abs(origin[0]-anchor[0])
                swing_y = abs(origin[1]-anchor[1])
                if swing_x >= swing_y and \
                    ((direction == 1 and origin[0] > anchor[0]) or \
                    (direction == -1 and origin[0] < anchor[0])):
                    if first_swing:
                        first_swing = False
                    else:
                        direction = direction * (-1)
                if direction == 1:
                    x += 0.25
                elif direction == -1:
                    x -= 0.25
                origin = (x-29,y-40)
                swing_x = abs(origin[0]-anchor[0])  
                y += math.sqrt(web_hip**2-swing_x**2) - swing_y
                swing_y = math.sqrt(web_hip**2-swing_x**2)
        
        # Movement
        if origin[1] <= anchor[1]:
            web_active = False
        if shot_up:
            if up_key:
                y -= 1                
            elif down_key:
                y += 1

    # Draw
    screen.fill('black')
    for row in range(len(level)):
        for col in range(len(level[0])):
            color = obj_color[level[row][col]]
            rect = (*level2screen(row, col), 40, 40)
            pygame.draw.rect(screen, color, rect)
    
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