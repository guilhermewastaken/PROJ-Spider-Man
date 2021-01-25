import math
import random
import pygame
from background import *

pygame.init()

#Window settings
screen_width = 792
screen_heigth = 576
screen = pygame.display.set_mode((screen_width, screen_heigth))
pygame.display.set_caption('Spider Man Atari 2600')

#Sprites
spiderman = pygame.image.load('Images/spiderman2.png')
spd_right = pygame.image.load('Images/swing_right2.png')
spd_left = pygame.image.load('Images/swing_left2.png')
spd_fall = pygame.image.load('Images/falling.png')
life = pygame.image.load('Images/life.png')

goblin = pygame.image.load('Images/goblin.png')
bomb = pygame.image.load('Images/bomb.png')
criminal = pygame.image.load('Images/criminal.png')

#Initial conditions
x = screen_width/2 + spiderman.get_width()/2
y = screen_heigth/2 + spiderman.get_height()/2
lives = 3

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
obj_color = (col_sky, build_sky)

#Background
scroll = len(level) - (screen_heigth//12)
def collision(spd,crm):
    max_x = math.ceil(spd[1]+spd[3])
    min_x = int(spd[0]-spd[2])
    max_y = math.ceil(spd[0]+spd[2])    
    min_y = int(spd[1]-spd[3])
    spd_hitbox = [set(range(min_x, max_x+1)), set(range(min_y, max_y+1))]        
    min_x = int(crm[0])
    max_x = math.ceil(min_x + ENEMY_WIDTH)
    min_x = int(crm[1])
    max_x = math.ceil(min_x + ENEMY_HEIGHT)
    crm_hitbox = [set(range(min_x, max_x+1)), set(range(min_y, max_y+1))]
    col = []
    col.append(spd_hitbox[0].intersection(crm_hitbox[0]))
    col.append(spd_hitbox[1].intersection(crm_hitbox[1]))
    if len(col[0]) != 0 and len(col[1]) != 0:
        return True
    return False

def level_to_screen(row, col):  # -> (x, y)
    return col*12, (row-scroll)*12

def screen_to_level(x, y):  # -> (row, col)
    return y/12+scroll,x/12

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

#Dead?
clock = pygame.time.Clock()
falling = False
running = True

ENEMY_WIDTH = 24
ENEMY_HEIGHT = 36
enemies_cols = [0]*len(enemies_rows)
enemies_times = [0]*len(enemies_rows)

while running:
    ########## Events #########
    dt = clock.tick(60)

    if lives == 0:
        running = False
    if y > screen_heigth:
        lives -= 1
        x = screen_width/2 + spiderman.get_width()/2
        y = screen_heigth/2 + spiderman.get_height()/2
        falling = False
        web_active = False
        web_shooting = False
    
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

    ########## Updates #########
    
    # update enemy positions
    
    enemies_times = [t-dt for t in enemies_times]
    for i, t in enumerate(enemies_times):
        if t <= 0:
            enemies_cols[i] = random.choice([i*6+10 for i in range(8)])
            enemies_times[i] = random.randint(1000, 2000)
    
    if web_shooting:
        if web_distance == 0:
            anchor = (x-20,y-30)
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
                anchor = (x-20, y -30- web_distance)
            elif right_key and shot_right:
                direction = 1
                web_distance += 1               
                anchor = (x-20 + web_distance, y -30- web_distance)
            elif left_key and shot_left:
                direction = -1
                web_distance += 1               
                anchor = (x-20-web_distance, y -30- web_distance)
                
    if web_active:
        falling = False
        temp = screen_to_level(anchor[0],anchor[1])        
        if level[int(temp[0])][int(temp[1])] == 0:
            web_active = False
            falling = True
            web_distance = 0
        
        else:
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
                    origin = (x-20,y-40)
                    swing_x = abs(origin[0]-anchor[0])  
                    y += math.sqrt(web_hptn**2-swing_x**2) - swing_y
    if falling:
        y += 3
        
    # Background (scroll)
    while y > screen_heigth/3:
        if scroll >= len(level) - (screen_heigth//12):
            break
        scroll += 1
        y -= 12
        if web_active:
            anchor = (anchor[0],anchor[1]-12)
    while y < screen_heigth/2:
        if scroll <= 0:
            break
        scroll -= 1
        y += 12
        if web_active:
            anchor = (anchor[0],anchor[1]+12) 

    if web_active or web_shooting:
        origin = (x-20,y-30)

    ########## Collisions #########
    
    # collision between web and enemy
    if web_shooting or web_active:
        for enemy_row, enemy_col in zip(enemies_rows, enemies_cols):
            ex, ey = level_to_screen(enemy_row, enemy_col)
            ey -= ENEMY_HEIGHT
            if intersect(origin, anchor, (ex, ey), (ex+ENEMY_WIDTH, ey)) or \
                intersect(origin, anchor, (ex+ENEMY_WIDTH, ey), (ex+ENEMY_WIDTH, ey+ENEMY_HEIGHT)) or \
                intersect(origin, anchor, (ex, ey+ENEMY_HEIGHT), (ex+ENEMY_WIDTH, ey+ENEMY_HEIGHT)) or \
                intersect(origin, anchor, (ex, ey), (ex, ey+ENEMY_HEIGHT)):
                    web_active = False
                    falling = True
                    web_distance = 0            

    # collision between player and enemy
    for i in range(len(enemies_rows)):
        ex, ey = level_to_screen(enemies_rows[i], enemies_cols[i])
        ey -= ENEMY_HEIGHT
        # x, y - jogador
        spd_width = spiderman.get_width()
        spd_height = spiderman.get_height()
        if collision((x, y, spd_width/2, spd_height/2), (ex, ey, ENEMY_WIDTH, ENEMY_HEIGHT)):
            del enemies_rows[i]
            del enemies_cols[i]
            del enemies_times[i]
            break
            

    ########## Draw #########
    screen.fill('black')
    
    for row in range(len(level)):
        for col in range(len(level[0])):
            color = obj_color[level[row][col]]
            rect = (*level_to_screen(row, col), 12, 12)
            pygame.draw.rect(screen, color, rect)
    
    for enemy_row, enemy_col in zip(enemies_rows, enemies_cols):
        ex, ey = level_to_screen(enemy_row, enemy_col)
        ey -= ENEMY_HEIGHT
        # pygame.draw.rect(screen, 'brown', (ex, ey, ENEMY_WIDTH, ENEMY_HEIGHT))
        # pygame.draw.rect(screen, 'blue', (ex, ey, ENEMY_WIDTH/2, ENEMY_HEIGHT/2))
        screen.blit(criminal,(ex-12,ey-13))
    
    if web_active or web_shooting:
        pygame.draw.line(  screen,(255,255,255),origin,anchor,5)        
    if web_active:        
        if origin[0] - anchor[0] >= 0:
            screen.blit(spd_left,(x - int(spiderman.get_width()/2), y - int(spiderman.get_width()/2)))
        else:
            screen.blit(spd_right,(x - int(spiderman.get_width()/2), y - int(spiderman.get_width()/2)))
    elif falling:
        screen.blit(spd_fall, (x - int(spiderman.get_width()/2), y - int(spiderman.get_width()/2)))
    else:
        screen.blit(spiderman, (x - int(spiderman.get_width()/2), y - int(spiderman.get_width()/2)))
    
    if lives == 3:
        screen.blit(life, (35,538))
        screen.blit(life, (0,538))
    elif lives == 2:
        screen.blit(life, (0,538))
    pygame.display.flip()
        
pygame.quit()