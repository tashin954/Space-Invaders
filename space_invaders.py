# Here we will create a rule so that if the enemy reaches the bottom of the screen
# near the spaceship then "Game Over" text is displayed

import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Souund
mixer.music.load('background.wav')      # Because we want to play this sound contineously so we used music.load
mixer.music.play(-1)                    # and to play this in a loop we put -1 within bracket

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemy = 6

for i in range(no_of_enemy):  # Above we made a list of everything a single enemy needed, so
    enemyImg.append(pygame.image.load('enemy.png'))  # that using this list now we can create 6 enemy at a time
    enemyX.append(random.randint(0, 735))  # using the for loop which runs from 0 to 5 we created & stored
    enemyY.append(random.randint(50, 150))  # details of 6 enemies i.e we appended each time the for loop
    enemyX_change.append(2)  # ran
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

# Score
score_value = 0  # Here we defined score_value as 0 and made a font object with font
font = pygame.font.Font('freesansbold.ttf', 25)  # type and size

textX = 10  # Here we assign the x and y co-ordinate
textY = 10  # of the text we want to show on screen

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


# Here we define show_text function so 1st we neend to render and then blit
def show_text(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))  # Here we pass str, antialising as True
    screen.blit(score, (x, y))  # RGB values and then blit it


# Game over text display function
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Player Draw
def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy Draw
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Here we define a collision function if distance is less than 27 is returns True
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2) + (math.pow((enemyY - bulletY), 2))))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
runing = True

while runing:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

        # If keystroke is pressed we check whether it is right or left arrow key

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3

            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')        # We use mixer.Sound here because our file is small
                    bullet_sound.play()                            # and not large
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key - - pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Checking condition so that the spaceship donot go out of the Game Window
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Making our enemy move
    for i in range(no_of_enemy):

        if enemyY[i] > 440:
            for i in range(no_of_enemy):
                enemyY[i] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')  # We use mixer.Sound here because our file is small
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 5
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Resetting the position and state of bullet once the bullet goes out of the screen so we can fire multiple bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Moving or Firing our bullet
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)  # Here also we are using the previous saved bulletX value
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_text(textX, textY)  # Here we call show_text and pass co-ordinate
    pygame.display.update()
