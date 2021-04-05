# To do:
# Pause Menu
# Volume Slider
# Find images with free usage/or make
# Main Menu
# Import Font for main menu

import pygame
import random
import time
import config
from pygame import mixer
from ButtonTester import Button
from VolumeSlider import drawSoundSlider, drawMusicSlider, updateMusicSlider, isOverMusic, isOverSound, \
    updateSoundSlider, drawContinueButton, drawExitButton, isOverContinue, isOverExit

pygame.init()
# creates the screen             width, height
screen = pygame.display.set_mode((800, 600))
# Background
background = pygame.image.load("Space Background.png")
# Background music
mixer.music.load("Space Background Music.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)  # plays music on loop

# Title and Icon
pygame.display.set_caption("Subspace Sector")
icon = pygame.image.load("Space Icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("Player Ship.png")
playerX = 370
playerY = 480
# Enemy
enemyImg = pygame.image.load("Space Invader(Updated).png")
fastEnemyImg = pygame.image.load("Fast Ship.png")
enemyX = []
enemyY = []
numOfEnemies = 5
enemyX_change = []


def newEnemy(enemyNum):
    enemyX.append(random.randint(0, 734))
    enemyY.append(random.randint(50, 200))
    # Random direction
    if random.random() < 0.5:
        newEnemyDirection = 1
    else:
        newEnemyDirection = -1
    if enemyNum < len(enemyX_change):
        if enemyNum % 4 == 0:
            enemyX_change[enemyNum] = 1.5 * newEnemyDirection
        else:
            enemyX_change[enemyNum] = newEnemyDirection
    else:
        if enemyNum % 4 == 0:
            enemyX_change.append(1.5 * newEnemyDirection)
        else:
            enemyX_change.append(1 * newEnemyDirection)


for i in range(numOfEnemies):
    newEnemy(i)

# player shot
playerShot = pygame.image.load("Player Shot.png")
playerShotX = 0
playerShotY = 490
playerShot_state = False

# other
enemyKillstreakX = 0
enemyKillstreakY = 0
setKillsteakData = False
tick = 0
killstreak = 0
kills = 0
score = 0
highscore = 0
font = pygame.font.Font("freesansbold.ttf", 32)
# pause button as button class
pauseButton = Button((100, 100, 100), 760, 10, 30, 30)
# pause button image to load
PauseButton = pygame.image.load("PauseButton.png")


def drawPlayer():
    # blip means draw
    screen.blit(playerImg, (int(playerX), int(playerY)))


def drawEnemies():
    global numOfEnemies
    for i in range(numOfEnemies):
        if i % 4 != 0:
            screen.blit(enemyImg, (int(enemyX[i]), enemyY[i]))
        else:
            screen.blit(fastEnemyImg, (int(enemyX[i]), enemyY[i]))


def scoreDisplay():
    highscoreDisplay = font.render("Highscore: " + str(highscore), True, (10, 210, 10))
    scoreDisplay = font.render("Score: " + str(score), True, (10, 210, 10))
    screen.blit(scoreDisplay, (10, 65))
    screen.blit(highscoreDisplay, (10, 10))


def drawBullet():
    screen.blit(playerShot, (int(playerShotX), int(playerShotY)))


def isCollision():
    global kills
    global hitEnemy
    for i in range(numOfEnemies):
        if 64 - 7 > playerShotX - enemyX[i] > -7:
            if 55 > playerShotY - enemyY[i] > 12 - 16:
                newEnemy(i)  # respawns enemy
                kills += 1
                hitEnemy = i
                return True
    return False


def killstreakDisplay():
    global setKillsteakData
    global tick
    if setKillsteakData and tick == 0:
        global enemyKillstreakX
        global enemyKillstreakY
        enemyKillstreakX = enemyX[hitEnemy]
        enemyKillstreakY = enemyY[hitEnemy]
        tick = 200
    if tick > 0:  # score displays for 200 frames
        killsteakScore = pygame.font.Font("freesansbold.ttf", 32)
        screen.blit(killsteakScore.render(str(killstreak), True, (10, 210, 10)),
                    (int(enemyKillstreakX), enemyKillstreakY - 10))
        setKillsteakData = False
        tick -= 1


def gameOver():
    gameEndFont = pygame.font.Font("freesansbold.ttf", 64)
    screen.fill((0, 0, 0))
    screen.blit(gameEndFont.render("GAME OVER", True, (210, 10, 10)), (215, 250))
    pygame.display.update()
    mixer.music.load("Gameover.mp3")
    mixer.music.play(0)
    voice = mixer.Sound("GameOverVoice.wav")
    voice.set_volume(config.soundPercent)
    voice.play()
    time.sleep(3)
    gameEndFont = pygame.font.Font("freesansbold.ttf", 32)
    screen.blit(gameEndFont.render("Press SPACE to play again", True, (255, 255, 255)), (215, 320))
    screen.blit(gameEndFont.render("Press ESCAPE to exit", True, (255, 255, 255)), (215, 360))
    global tick
    tick = 0
    pygame.display.update()
    global PlayingGame
    PlayingGame = True


def gamePaused():
    pygame.mixer.music.pause()
    isPaused = True
    global playerX_change
    global playerShot_state
    while isPaused:
        pygame.time.Clock().tick(120)  # locks game to 120fps so the program isn't intensive on game paused screen
        # draws pause menu
        pygame.draw.rect(screen, (82, 116, 168), (250, 100, 300, 400))
        text = font.render('Paused', True, (0, 255, 0), (82, 116, 168))
        textRect = text.get_rect()
        textRect.center = (400, 150)
        screen.blit(text, textRect)
        drawMusicSlider()
        drawSoundSlider()
        drawContinueButton()
        drawExitButton()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # quit button quits the game even in pause menu
            if event.type == pygame.MOUSEBUTTONDOWN and pauseButton.isOver(pygame.mouse.get_pos()):
                isPaused = False
                playerX_change = 0
                pygame.mixer.music.unpause()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    playerX_change -= 1
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    playerX_change += 1
            if pygame.mouse.get_pressed()[0] and isOverMusic(pygame.mouse.get_pos()):
                updateMusicSlider()
            elif pygame.mouse.get_pressed()[0] and isOverSound(pygame.mouse.get_pos()):
                updateSoundSlider()
            elif event.type == pygame.MOUSEBUTTONDOWN and isOverContinue():
                isPaused = False
                playerX_change = 0
                pygame.mixer.music.unpause()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    playerX_change -= 1
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    playerX_change += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and isOverExit():
                quit()
        exitKeys = pygame.key.get_pressed()     # pygame.key.get_pressed() is assigned to not call it 3 times each frame
        if exitKeys[pygame.K_RCTRL] or exitKeys[pygame.K_LCTRL] and exitKeys[pygame.K_q]:
            quit()




playerX_change = 0
PlayAgain = True
PlayingGame = True
PlayAgain = True
while PlayAgain:
    running = True
    while running:
        pygame.time.Clock().tick(
            5000)  # locks game to 5000fps so the program isn't vastly different on different computers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # quit button quits the game
            if event.type == pygame.MOUSEBUTTONDOWN and pauseButton.isOver(pygame.mouse.get_pos()):
                gamePaused()

        keys = pygame.key.get_pressed()
        # movement keys
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # both left and right are pressed
                playerX_change = 0
            else:   # only left is pressed
                playerX_change = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # only right is pressed
            playerX_change = 1
        else:   # neither left or right are pressed
            playerX_change = 0
        # exit keys
        if keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL] and keys[pygame.K_q]:
            quit()
        # shoot key
        if keys[pygame.K_SPACE] and not playerShot_state:
            playerShotX = playerX + 25
            playerShot_state = True
            drawBullet()
            x = mixer.Sound("Laser1.wav")  # plays shot as soon as bullet spawns
            x.set_volume(config.soundPercent)
            x.play()

        # RGB - Red Green Blue
        screen.blit(background, (0, 0))
        playerXspeed = playerX_change
        # Set speed cap
        if playerX_change > 1:
            playerXspeed = 1
        if playerX_change < -1:
            playerXspeed = -1
        # apply player speed
        playerX += playerXspeed
        # player boundaries
        if playerX < 0:
            playerX = 0
        elif playerX > 736:
            playerX = 736
        # enemy movement
        for i in range(numOfEnemies):
            if enemyY[i] > 440:
                for j in range(numOfEnemies):
                    enemyY[i] = 2000
                gameOver()
                running = False
            enemyX[i] += enemyX_change[i]
            if enemyX[i] < 0:
                enemyX_change[i] = -1 * enemyX_change[i]
                enemyY[i] += 30
            elif enemyX[i] > 736:
                enemyX_change[i] = -1 * enemyX_change[i]
                enemyY[i] += 30
        if not running:
            break
        # Bullet Movement
        if playerShotY < 0:
            playerShotY = 490
            killstreak = 0
            playerShot_state = False
        if playerShot_state:
            playerShot_state = True
            drawBullet()
            playerShotY -= 1.5
            if isCollision():
                playerShot_state = False
                playerShotY = 490
                killstreak += 100
                score += killstreak
                if highscore < score:
                    highscore = score
                boom = mixer.Sound("boom.wav")
                boom.set_volume(config.soundPercent*.4)
                boom.play()
                setKillsteakData = True
                killstreakDisplay()
                enemyX[hitEnemy] = random.randint(0, 734)
                enemyY[hitEnemy] = random.randint(40, 200)
                if kills == 5:
                    newEnemy(numOfEnemies)
                    kills = 0
                    numOfEnemies += 1
        # starts redrawing everything
        drawPlayer()
        drawEnemies()
        # pauseButton.draw(screen, (0, 0, 0))     # gray button
        screen.blit(PauseButton, (760, 10))
        # playerImg = pygame.image.load("Player Ship.png")

        scoreDisplay()
        killstreakDisplay()
        pygame.display.update()

    while PlayingGame:
        pygame.time.Clock().tick(30)  # locks game to 60fps so the program isn't intensive on game over screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    PlayingGame = False
                elif event.key == pygame.K_ESCAPE:
                    PlayAgain = False
                    PlayingGame = False
            if event.type == pygame.QUIT:
                PlayAgain = False
                PlayingGame = False
    background = pygame.image.load("Space Background.png")
    # Background music
    mixer.music.load("Space Background Music.mp3")
    mixer.music.play(-1)  # plays music on loop
    # Title and Icon
    pygame.display.set_icon(icon)

    # Player
    playerX = 370
    playerY = 480
    playerX_change = 0
    # Enemy
    enemyX = []
    enemyY = []
    numOfEnemies = 5
    enemyX_change = []
    for i in range(numOfEnemies):
        newEnemy(i)
    # enemyY_change = 0
    # player shot
    playerShotX = 0
    playerShotY = 490
    playerShot_state = False
    # other
    enemyKillstreakX = 0
    enemyKillstreakY = 0
    setKillsteakData = False
    tick = 0
    killstreak = 0
    font = pygame.font.Font("freesansbold.ttf", 32)
    if highscore < score:
        highscore = score
    score = 0
    kills = 0
