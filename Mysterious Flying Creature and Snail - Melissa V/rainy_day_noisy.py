# Computer Programming 1
# Unit 11 - Graphics
#
# A stormy day


# Imports
import pygame
import random
import ctypes
import time
shot_fired = False

while True:
    ctypes.windll.user32.MessageBoxW(0, "W to shoot, SPACE to change day and night, L to change lights in house,  use arrow buttons to move snail.", "Commands", 1)
    time.sleep(0.5)
    break

# Initialize game engine
pygame.mixer.pre_init()
pygame.init()

# Window
SIZE = (800, 600)
TITLE = "Rainy Day"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
GREEN = (100, 125, 75)
WHITE = (255, 255, 255)
BLUE = (75, 200, 255)
DARK_BLUE = (0, 0, 100)
GRAY = (150, 150, 150)
DARK_GRAY = (75, 75, 75)
NOT_QUITE_DARK_GRAY = (100, 100, 100)
YELLOW = (255, 248, 193)
RED = (242, 62, 16)
YELLOWW = (250, 255, 0)
BLOOD = (119, 2, 2)
BLACK = (0, 0, 0)

def draw_cloud(loc, color):
    x = loc[0]
    y = loc[1]
    
    pygame.draw.ellipse(screen, color, [x, y + 20, 40 , 40])
    pygame.draw.ellipse(screen, color, [x + 60, y + 20, 40 , 40])
    pygame.draw.ellipse(screen, color, [x + 20, y + 10, 25, 25])
    pygame.draw.ellipse(screen, color, [x + 35, y, 50, 50])
    pygame.draw.rect(screen, color, [x + 20, y + 20, 60, 40])

def draw_line():
    y = 240
    for y in range(240,500,10):
        pygame.draw.line(screen, WHITE, [400, y + 10], [700, y + 10], 2)

def draw_window(x,y):
    pygame.draw.rect(screen, window_color, [x + 20, y + 20,60,70])
    
def draw_raindrop(drop):
    rect = drop[:4]
    pygame.draw.ellipse(screen, DARK_BLUE, rect)

def draw_snail(loc, facing_right):
    x = loc[0]
    y = loc[1]

    if facing_right:
        pygame.draw.line(screen, YELLOWW, [x + 60,y + 25],[x + 55, y],2)
        pygame.draw.line(screen, YELLOWW, [x + 65,y + 25],[x + 70, y],2)
        pygame.draw.ellipse(screen, BLACK,[x + 50,y + 15,25,35])
        pygame.draw.ellipse(screen, BLACK,[x,y + 25,70,30])
        pygame.draw.ellipse(screen, WHITE,[x,y +5,50,45])
    else:
        pygame.draw.line(screen, YELLOWW, [x - 11,y + 25],[x - 6, y],2)
        pygame.draw.line(screen, YELLOWW, [x - 16,y + 25],[x - 19, y],2)
        pygame.draw.ellipse(screen, BLACK,[x - 22,y + 15,25,35])
        pygame.draw.ellipse(screen, BLACK,[x - 20,y + 25,70,30])
        pygame.draw.ellipse(screen, WHITE,[x,y +5,50,45])

''' Make clouds '''
num_clouds = 30
near_clouds = []

for i in range(num_clouds):
    x = random.randrange(0, 1600)
    y = random.randrange(-50, 100)
    loc = [x, y]
    near_clouds.append(loc)

num_clouds = 50
far_clouds = []

for i in range(num_clouds):
    x = random.randrange(0, 1600)
    y = random.randrange(-50, 300)
    loc = [x, y]
    far_clouds.append(loc)

daytime = True
lights_on = False

''' Make rain '''
num_drops = 700
rain = []

for i in range(num_drops):
    x = random.randrange(0, 1000)
    y = random.randrange(-100, 600)
    r = random.randrange(1, 5)
    stop = random.randrange(400, 700)
    drop = [x, y, r, r, stop]
    rain.append(drop)


# Enemies stuff
man = []
man.append(pygame.image.load('animations/wingMan1.png'))
man.append(pygame.image.load('animations/wingMan2.png'))
man.append(pygame.image.load('animations/wingMan3.png'))
man.append(pygame.image.load('animations/wingMan4.png'))
man.append(pygame.image.load('animations/wingMan5.png'))

ticks = 0
frame = 0

# Lightning stuff
lightning_prob = 300 # (higher is less frequent)
lightning_timer = 0

# Sound Effects
pygame.mixer.music.load("sounds1/wii-theme.ogg")
meow = pygame.mixer.Sound("sounds1/gary.ogg")
thunder = pygame.mixer.Sound("sounds/thunder.ogg")

meow.set_volume(1)
# Snail stuff
snail_loc = [50, 500]
vel =[0, 0]
speed = 3
facing_right = True

# Make Bullets
bullets = []

def draw_bullet(loc):
    x = loc[0]
    y = loc[1]

    pygame.draw.rect(screen, WHITE, [x, y, 5, 15])

# Game loop
pygame.mixer.music.play(-1)

done = False

while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True     
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                daytime = not daytime
            elif event.key == pygame.K_l:
                lights_on = not lights_on
            elif event.key == pygame.K_RIGHT:
                vel[0] = speed
                facing_right = True
            elif event.key == pygame.K_LEFT:
                vel[0] = -1 * speed
                facing_right = False
            elif event.key == pygame.K_UP:
                vel[1] = -1 * speed
            elif event.key == pygame.K_DOWN:
                vel[1] = speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                vel[0] = 0
            elif event.key == pygame.K_LEFT:
                vel[0] = 0
            elif event.key == pygame.K_UP:
                vel[1] = 0
            elif event.key == pygame.K_DOWN:
                vel[1] = 0
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    shot_fired = True
                
    # Game logic
    snail_loc[0] += vel[0]
    snail_loc[1] += vel[1]

    if shot_fired == True:
        meow.play()
        bullets.append([snail_loc[0] + 17.5, snail_loc[1]])
        shot_fired = False
        
    for b in bullets:
        b[1] -= 24
    if ticks % 3 == 0:
        frame += 1
        if frame > 4: 
            frame = 0

    ticks += 1
    
    ''' move clouds '''
    for c in far_clouds:
        c[0] -= 1

        if c[0] < -100:
            c[0] = random.randrange(800, 1600)
            c[1] = random.randrange(-50, 200)

    for c in near_clouds:
        c[0] -= 2

        if c[0] < -100:
            c[0] = random.randrange(800, 1600)
            c[1] = random.randrange(-50, 200)

    ''' set sky color '''
    if daytime:
        sky = GRAY
    else:
        sky = BLACK

    ''' set window color (if there was a house)'''
    if lights_on:
        window_color = YELLOWW
    else:
        window_color = WHITE

    ''' move rain '''
    for r in rain:
        r[0] -= 1
        r[1] += 4

        if r[1] > r[4]:
            r[0] = random.randrange(0, 1000)
            r[1] = random.randrange(-100, 0)

    ''' flash lighting '''
    if random.randrange(0, 300) == 0:
        lightning_timer = 5
        thunder.play()
    else:
        lightning_timer -= 1
    
    # Drawing code
    ''' sky '''
    if lightning_timer > 0:
        screen.fill(YELLOW)
    else:
        screen.fill(sky)

    ''' sun '''
    pygame.draw.ellipse(screen, YELLOW, [575, 75, 100, 100])

    ''' grass '''
    pygame.draw.rect(screen, GREEN, [0, 400, 800, 200])

    ''' fence '''
    y = 380
    for x in range(5, 800, 30):
        pygame.draw.polygon(screen, WHITE, [[x+5, y], [x+10, y+5],
                                            [x+10, y+40], [x, y+40],
                                            [x, y+5]])
    pygame.draw.line(screen, WHITE, [0, 390], [800, 390], 5)
    pygame.draw.line(screen, WHITE, [0, 410], [800, 410], 5)

    ''' clouds '''
    for c in far_clouds:
        draw_cloud(c, NOT_QUITE_DARK_GRAY)

    ''' house '''
    pygame.draw.polygon(screen, RED, ((700,250),(400,250),(550,150)))
    pygame.draw.rect(screen, BLOOD, [400, 250, 300, 250])
    pygame.draw.rect(screen, WHITE, [530, 440, 40, 60])
    draw_line()
    draw_window(430,270)
    draw_window(570,270)

    ''' snail '''
    draw_snail(snail_loc, facing_right)
    for b in bullets:
        draw_bullet(b)

    ''' enemies '''
    screen.blit(man[frame], [200,200])
    
    ''' rain ''' 
    for r in rain:
        draw_raindrop(r)

    ''' clouds '''
    for c in near_clouds:
        draw_cloud(c, DARK_GRAY)


    # Update screen
    pygame.display.flip()
    clock.tick(refresh_rate)

# Close window on quit
pygame.quit()
