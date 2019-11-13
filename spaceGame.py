# Siin on suht head disainid jne. https://opengameart.org/content/space-shooter-redux
import pygame
import time
import math
import random

FPS = 120
wind_laius = 600
wind_kõrgus = 600
padding = 10
scoreboard_kõrgus = 100
font_size = 36

kiirus = 5
x = padding
y = wind_kõrgus-padding-scoreboard_kõrgus

# Värvid
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
nice_b = (66, 126, 245)
background = (31, 31, 31)


# SETUP
pygame.init()
pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font(pygame.font.get_default_font(), font_size)

window = pygame.display.set_mode((wind_laius,wind_kõrgus))
pygame.display.set_caption("Spacers Invade")
aeg = pygame.time.Clock()


# Pilt
laev = pygame.image.load("playerShip1_green.png").convert()
laius = laev.get_width()
kõrgus = laev.get_height()

x = padding
y = wind_kõrgus-2*padding-scoreboard_kõrgus - kõrgus

# Heli
pygame.mixer.music.load("DigitalZen.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.3)

def delay(n = 0.15):
    time.sleep(n)

# Mängja 
def redraw():  
    window.blit(laev,(x,y)) # Ajutine
    

#Meteoriidid nendega on see jama, et ma pole piire pannud, et kui läheb window piiridest välja ss peaks uuesti ülevalt alla tulema
meteoriit_image = []
meteoriitX = []
meteoriitY = []
meteoriitY_change = []
meteoriitide_arv = 4
for i in range(meteoriitide_arv):
    meteoriit_image.append(pygame.image.load("asteroid.png").convert())
    meteoriitX.append (random.randint(0,530))
    meteoriitY.append (random.randint(9,9))
    meteoriitY_change.append (40)

def meteoriit(x,y,i):
    window.blit(meteoriit_image[i],(x,y))
#Meteoriitide liikumine
def meteoriitide_liikumine():
    global laserY
    for i in range(meteoriitide_arv):
        meteoriitY [i]+= meteoriitY_change [i]
        if meteoriitY [i] > 0:
            meteoriitY_change[i] = 1
            kokkupõrge = collision(meteoriitX[i],meteoriitY[i],laserX,laserY)
        if kokkupõrge:
            laserY = y
            laser_state = "ready"
            meteoriitX[i] = random.randint(0,560)
            meteoriitY[i] = random.randint(9,9)
        meteoriit(meteoriitX[i],meteoriitY[i], i)
#Laskmine
laser_image = pygame.image.load("laserBlue03.png").convert()
laserX = 0
laserY = y
laserY_change = 5
laser_state = "ready"

def laskmine(x,y):
    global laser_state
    laser_state = "fire"
    window.blit(laser_image,(x+16,y+10))

def laseri_liikumine():
    global laserY
    global laser_state
    if laserY < 0:
        laserY = y
        laser_state = "ready"
    if laser_state is "fire":
        laskmine(laserX,laserY)
        laserY -= laserY_change
#Collision
def collision(meteoriitX,meteoriitY,laserX,laserY):
    vahemaa = math.sqrt((math.pow(meteoriitX-laserX,2))+(math.pow(meteoriitY-laserY,2)))
    if vahemaa < 17:
        return True
    else:
        return False
        
    
def draw_elem():
    window.fill(RED)
    pygame.draw.rect(window, background, (padding/2, padding/2, wind_laius-padding , wind_kõrgus-padding))
    pygame.draw.rect(window, BLUE, (padding,wind_kõrgus-padding-scoreboard_kõrgus, wind_laius-2*padding,scoreboard_kõrgus))
    
    
menüü_valik = 0
def draw_pausil():
    global font_size
    x = [250,300,350,400,450,500]
    y = [0]
    global menüü_valik
    
    window.fill(background)
    jätka = font.render("Continue", True, (230,230,230))
    välju = font.render("Quit", True, (230,230,230))
    stats = font.render("Statistics", True, (230,230,230))
    
    y = (wind_laius - jätka.get_width())/2
    window.blit(jätka, dest = (y,x[0]))
    window.blit(stats, dest = (y,x[1]))
    window.blit(välju, dest = (y,x[2]))
    
    pygame.draw.rect(window, RED, (y-padding, x[menüü_valik]-padding, y, font_size+2*padding), 3)
    pygame.display.update()
    

def main_menu():
    window.fill((66, 126, 245))
    start = font.render("Press ENTER to START", True, BLACK)
    y = int(wind_laius - start.get_width())/2
    pygame.draw.rect(window, (230,0,0), (y-padding, 250-padding, y*4.4, font_size+2*padding))
    window.blit(start, dest = (y, 250))
    pygame.display.update() 
    

# Kõik inputiga seonduv
def nupud():
    global x
    global y
    global pause
    global run
    
    nupud = pygame.key.get_pressed()

    if nupud[pygame.K_LEFT] and x >= kiirus + padding: # Fixed 
        x -= kiirus
    if nupud[pygame.K_RIGHT] and x < wind_laius - laius - padding: # Fixed
        x += kiirus
    if nupud[pygame.K_SPACE]:
        if laser_state is "ready":
            global laserX
            laserX = x
            laskmine(x,laserY)
    if nupud[pygame.K_ESCAPE]:
        pause = not pause
        delay()        
def nupud_pausil():
    global pause
    global run
    global menüü_valik
    
    nupud = pygame.key.get_pressed()
    
    if nupud[pygame.K_ESCAPE]:
        pause = not pause
        delay()
    if nupud[pygame.K_DOWN]:
        menüü_valik += 1
        if menüü_valik > 2:
            menüü_valik = 0
        delay()
    if nupud[pygame.K_UP]:
        menüü_valik -= 1
        if menüü_valik < 0:
            menüü_valik = 2
        delay()     
    if nupud[pygame.K_RETURN]:
        if menüü_valik == 0:
            pause = not pause
            delay()
        if menüü_valik == 2:
            run = False

def nupud_alguses():
    global pause
    global run_menu
    
    nupud = pygame.key.get_pressed()
    if nupud[pygame.K_RETURN]:
        run_menu = False
        pause = False
        delay()



    
# Main loop
run_menu = True
run = True
pause = True
stats = False

while run:
    if pause == False:
        aeg.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        nupud()
        draw_elem()
        redraw()
        meteoriitide_liikumine()
        laseri_liikumine()
    pygame.display.update()    
    if pause == True:
        if not run_menu:
            if not stats:
                aeg.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False        
                draw_pausil()
                nupud_pausil()
            if stats: # TODO Implement Stats
                run = False
        if run_menu: # TO DO
            aeg.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            main_menu()
            nupud_alguses()
            
pygame.quit()