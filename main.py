from tkinter import font
# Technical debt? more like this file (not kidding)
import sys
import pygame
import random
import sheep
import farmer


# 1. Initialize Pygame
pygame.init()


# 2. Setup the game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 536
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wolf")

herd = []
for i in range(28):
    if (random.randint(1,5) >= 2):
        shp = sheep.Sheep([random.randint(0, 800), random.randint(0, 600)], screen, 'me')
    else:
        shp = sheep.suicidalSheep([random.randint(0, 800), random.randint(0, 600)], screen, 'me')
    shp.assignColor()
    herd.append(shp)

wolfSprite = pygame.transform.scale(pygame.image.load('pixil-frame-0 (1).png'), (350, 350))
nakedWolfSprite = pygame.transform.scale(pygame.image.load('pixil-frame-0.png'), (350, 350))
craterSprite = pygame.transform.scale2x(pygame.image.load('crater.png'))
background = pygame.transform.scale(pygame.image.load('background.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
landmine = pygame.transform.scale2x(pygame.image.load('landmine.png'))
explosion = pygame.transform.scale(pygame.image.load('explosion.png'), (75, 75))
farmerSprite = pygame.image.load('farmer.png')

farmers = []

testCrater = pygame.Rect(100, 100, 25, 25)
craters = []
landmines = []
explosionRects = []
#craters.append(testCrater)
# 3. Define Colors (RGB)
BG_COLOR = (30, 30, 40)
PLAYER_COLOR = (0, 200, 150)

# 4. Player Variables
# pygame.Rect(x, y, width, height)
player = pygame.Rect(375, 275, 50, 50)
player_speed = 5

visionRect = pygame.Rect(100, 50, 0, 0)
testFarmer = farmer.Farmer([SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], screen, 'calm', 'up', visionRect)
farmers.append(testFarmer)
# 5. Game Clock (Controls frame rate)
clock = pygame.time.Clock()
FPS = 60
direction = -1
wool = 1
biting = False
mines = 15
lt = 0
lastRightClick = False
explosionTicks = 0
font = pygame.font.Font(None, 50)
scoreShow = font.render(str(wool), True, (0, 0, 0))
woolShow = font.render(str(wool), True, (0, 0, 0))
score = 0
clothed = True
safeTicks = 0

if (pygame.joystick.get_count() > 0):
  controller = pygame.joystick.Joystick(0)
  controller.init()
# 6. Main Game Loop

def manageSpawn():
    if (pygame.time.get_ticks() % 100 == 0):
        global score
        r = random.randint(1, 10000)
        if (r < score * 50):
            guy = farmer.Farmer([random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 20)], screen, 'calm', 'up', 0)
            farmers.append(guy)
        else:
            for i in range(5):
                if (random.randint(1,5) >= 2):
                    shp = sheep.Sheep([random.randint(0, 800), random.randint(0, 600)], screen, 'me')
                else:
                    shp = sheep.suicidalSheep([random.randint(0, 800), random.randint(0, 600)], screen, 'me')
                shp.assignColor()
                herd.append(shp)

running = True
while running:
    manageSpawn()
    clothed = wool > 0
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    # --- Input Handling (Continuous Movement) ---
    if (pygame.joystick.get_count() > 0):
        if (event.type == pygame.JOYAXISMOTION):
            lastLt = lt
            lx = controller.get_axis(0)
            #print(lx)
            ly = controller.get_axis(1)
            rx = controller.get_axis(2)
            ry = controller.get_axis(3)
            lt = controller.get_axis(4)
            rt = controller.get_axis(5)
            if (abs(lx) > 0.07):
                player.x += player_speed * lx
                if (lx > 0):
                    for crater in craters:
                        if (player.colliderect(crater)):
                            player.right = crater.left
                else:
                    for crater in craters:
                        if (player.colliderect(crater)):
                            player.left = crater.right
            if (abs(ly) > 0.07):
                player.y += player_speed * ly
                if (ly > 0):
                    for crater in craters:
                        if (player.colliderect(crater)):
                            player.bottom = crater.top
                else:
                    for crater in craters:
                        if (player.colliderect(crater)):
                            player.top = crater.bottom

            if (abs(rx) > abs(ry)):
                if (rx > 0):
                    direction = 'right'
                else:
                    direction = 'left'
            else:
                if (ry < 0):
                    direction = 'up'
                else: 
                    direction = 'down'

            biting = rt > 0.9

            if (lt > 0.9 and lastLt < 0.9):
                if (mines > 0):
                    mines -= 1
                    landmines.append(player_pos)
        if (controller.get_button(4) or controller.get_button(0)):
            for mine in landmines:
                explosionRects.append(pygame.Rect(mine[0], mine[1], 75, 75))
            landmines.clear()
            explosionTicks = 34

                    
        if (controller.get_button(6)):
            for i in range(10000):
                if (random.randint(1,5) >= 2):
                    shp = sheep.Sheep([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)], screen, 'me')
                else:
                    shp = sheep.suicidalSheep([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)], screen, 'me')
                shp.assignColor()
                herd.append(shp)           
    else:
        keys = pygame.key.get_pressed()

        # Horizontal movement (Arrow keys + WASD support)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
            for crater in craters:
                if (player.colliderect(crater)):
                    player.left = crater.right

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed
            for crater in craters:
                if (player.colliderect(crater)):
                    player.right = crater.left
        
        # Vertical movement (Pygame top-left is 0,0; down increases Y)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= player_speed
            for crater in craters:
                if (player.colliderect(crater)):
                    player.top = crater.bottom

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += player_speed
            for crater in craters:
                if (player.colliderect(crater)):
                    player.bottom = crater.top

        mouse_pos = pygame.mouse.get_pos()
        if (abs(mouse_pos[0] - SCREEN_WIDTH / 2) > abs(mouse_pos[1] - SCREEN_HEIGHT / 2)):
            if (mouse_pos[0] >= SCREEN_WIDTH / 2):
                direction = 'right'
            else:
                direction = 'left'
        else:
            if (mouse_pos[1] < SCREEN_HEIGHT / 2):
                direction = 'up'
            else:
                direction = 'down'
        biting = keys[pygame.K_LSHIFT] or pygame.mouse.get_pressed()[0]
        if (pygame.mouse.get_pressed()[2] and not lastRightClick):
            if (mines > 0):
                mines -= 1
                landmines.append(player_pos)
        if (pygame.mouse.get_pressed()[1]):
            for mine in landmines:
                explosionRects.append(pygame.Rect(mine[0], mine[1], 25, 25))
            explosionTicks = 49   
            landmines.clear()
        
    biteBoxLength = 50
    biteBoxWidth = 80
      
    if (direction == 'down'):
        if (biteBoxLength < biteBoxWidth):
            player_pos = [player.left + 0.5 * (50 - biteBoxWidth), player.top + biteBoxLength]
        else:
            player_pos = [player.left + 0.5 * (50 - biteBoxLength), player.top + biteBoxWidth]
    elif (direction == 'up'):
        if (biteBoxLength < biteBoxWidth):
            player_pos = [player.left + 0.5 * (50 - biteBoxWidth), player.top - biteBoxLength]
        else:
            player_pos = [player.left + 0.5 * (50 - biteBoxLength), player.top - biteBoxWidth]
    elif (direction == 'left'):
        if (biteBoxWidth <= biteBoxLength):
            player_pos = [player.left - biteBoxWidth, player.top + 0.5 * (50 - biteBoxLength)]
        else:
            player_pos = [player.left - biteBoxLength, player.top + 0.5 * (50 - biteBoxWidth)]
    else:
        if (biteBoxWidth <= biteBoxLength):
            player_pos = [player.left + biteBoxWidth, player.top + 0.5 * (50 - biteBoxLength)]
        else:
            player_pos = [player.left + biteBoxLength, player.top + 0.5 * (50 - biteBoxWidth)]

    if (biting):
        if (direction == 'down' or direction == 'up'):
            if (biteBoxWidth > biteBoxLength):
                biteBox = pygame.Rect(player_pos[0], player_pos[1], biteBoxWidth, biteBoxLength)
            else:
                biteBox = pygame.Rect(player_pos[0], player_pos[1], biteBoxLength, biteBoxWidth)
        else:
            if (biteBoxLength > biteBoxWidth):
                biteBox = pygame.Rect(player_pos[0], player_pos[1], biteBoxWidth, biteBoxLength)
            else:
                biteBox = pygame.Rect(player_pos[0], player_pos[1], biteBoxLength, biteBoxWidth)
    else:
        biteBox = pygame.Rect(0, 0, 0, 0)

    if (biting):
        for shp in herd:
            if (biteBox.colliderect(shp.hitbox)):
                if (shp.color in ['white', 'black', 'scrawny']):
                    if (wool < 5):
                        wool += 1
                    score += 1
                elif (shp.color == 'pink'):
                    if (wool < 5):
                        wool += 3
                    score += 3
                    if (random.randint(1,2) == 1):
                        mines += 1
                else:
                    score += 100
                    wool += 10
                    mines += 5
                herd.remove(shp)
    for shp in herd:
        if (shp.hitbox.collidelist(explosionRects) >= 0):
            if (shp.color in ['tung', 'me']):
                mines += 10
            else:
                if (random.randint(1,5)):
                    mines += 1
            herd.remove(shp)



    for guy in farmers:
        guy.move(player_pos)
        if (guy.hitbox.bottom > SCREEN_HEIGHT):
            guy.hitbox.bottom = SCREEN_HEIGHT
        elif (guy.hitbox.top < 0):
            guy.hitbox.top = 0
        if (guy.hitbox.left < 0):
            guy.hitbox.left = 0
        elif (guy.hitbox.right > SCREEN_WIDTH):
            guy.hitbox.right = SCREEN_WIDTH
                
    for guy in farmers:
        if (guy.vision.colliderect(player) and (biting or not clothed)):
            guy.state = 'chase'

    for guy in farmers[:]:
        for rect in explosionRects:
            if (guy.hitbox.colliderect(rect)):
                farmers.remove(guy)
                break

    # --- Screen Boundary Collision (Optional but recommended) ---
    if player.left < 0:
        player.left = 0
    if player.right > SCREEN_WIDTH:
        player.right = SCREEN_WIDTH
    if player.top < 0:
        player.top = 0
    if player.bottom > SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

    # --- Drawing ---
   
    screen.blit(background, (0,0))
    scoreShow = font.render(str(score), True, (0, 0, 0))
    screen.blit(scoreShow, (SCREEN_WIDTH - 75, 50))
    # Draw the player rectangle onto our screen surface
    if (biting):
        pygame.draw.rect(screen, (255, 0, 0), biteBox)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    for guy in farmers:
        if (player.colliderect(guy.hitbox) and safeTicks == 0):
            if (wool > 0):
                wool -= 1
                safeTicks = 35
            else:
                pygame.draw.rect(screen, [255, 0, 0], (SCREEN_HEIGHT, SCREEN_WIDTH, 0, 0))
                pygame.time.delay(5000)
                running = False
    safeTicks -= 1
    print(safeTicks)
    if (safeTicks < 0):
        safeTicks = 0
    #if (pygame.time.get_ticks() % 100 == 0):
    for shp in herd:
        shp.draw()
        if (isinstance(shp, sheep.suicidalSheep)):
            shp.move(player_pos)
        elif (isinstance(shp, sheep.Sheep)): # this sucks fix this
            if (pygame.time.get_ticks() % 10 == 0):
                shp.move()
        if (shp.hitbox.bottom > SCREEN_HEIGHT):
            shp.hitbox.bottom = SCREEN_HEIGHT
        elif (shp.hitbox.top < 0):
            shp.hitbox.top = 0
        if (shp.hitbox.right > SCREEN_WIDTH):
            shp.hitbox.right = SCREEN_WIDTH
        elif (shp.hitbox.left < 0):
            shp.hitbox.left = 0

    explosionTicks -= 1
    for rct in explosionRects:
        #pygame.draw.rect(screen, [255, 0, 0], rct)
        screen.blit(explosion, rct.topleft)
        if (explosionTicks < 0):
            craters.append(rct)
    if (explosionTicks < 0):
        explosionRects.clear()
    for crater in craters:
        screen.blit(craterSprite, (crater.left - 9, crater.top - 5))
    
    for mine in landmines:
        screen.blit(landmine, mine)
    if (clothed):
        screen.blit(wolfSprite, (player.centerx - 125, player.centery - 182))
    else:
        screen.blit(nakedWolfSprite, (player.centerx - 125, player.centery - 182))
    woolShow = font.render(str(wool), True, (0, 0, 0))
    screen.blit(woolShow, (player.centerx, player.centery))

    for guy in farmers:
        guy.draw()
    # Render the updated graphics to the screen
    pygame.display.flip()

    # Maintain fixed FPS
    clock.tick(FPS)

# Clean exit
pygame.quit()
sys.exit()
