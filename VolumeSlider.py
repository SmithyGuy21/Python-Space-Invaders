import pygame
import config
from pygame import mixer
import math

# initialize pygame
from ButtonTester import Button

pygame.init()
# creates the screen             width, height
screen = pygame.display.set_mode((800, 600))
# Background
background = pygame.image.load("Space Background.png")
# Background music
mixer.music.load("Space Background Music.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)  # plays music on loop
font = pygame.font.Font("freesansbold.ttf", 32)

# pause button as button class
pauseButton = Button((100, 100, 100), 760, 10, 30, 30)
# pause button image to load
PauseButtonImage = pygame.image.load("PauseButton.png")

# continue button
continueButton = Button((0, 255, 0), 280, 365, 250, 35)
# exit button
exitButton = Button((0, 255, 0), 280, 435, 250, 35)


# set slider to default 50%
musicSliderX = 345 + 180//2
soundSliderX = 345 + 180//2
musicPercent = 0.5
soundPercent = 0.5
config.soundPercent = 0.5   # used to update slider in TestingGameStuff.py


def drawContinueButton():
    continueButton.draw(screen, 5)
    text = font.render('Continue', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (400, 383)
    screen.blit(text, textRect)


def isOverContinue():
    return continueButton.isOver(pygame.mouse.get_pos())


def drawExitButton():
    exitButton.draw(screen, 5)
    text = font.render('Exit', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (400, 454)
    screen.blit(text, textRect)


def isOverExit():
    return exitButton.isOver(pygame.mouse.get_pos())


def drawMusicSlider():
    musicNote = pygame.image.load("Music Note.png")
    screen.blit(musicNote, (270, 280))
    pygame.draw.rect(screen, (0, 0, 0), (345, 300, 180, 7))
    pygame.draw.circle(screen, (0, 255, 0), (musicSliderX, 300 + 7 // 2), 8)


def updateMusicSlider():
    global musicSliderX
    global musicPercent
    cursorX = pygame.mouse.get_pos()[0]
    cursorXonBar = min(max(cursorX, 345), 345 + 180)
    musicSliderX = cursorXonBar
    musicPercent = (cursorXonBar - 345) / 180
    mixer.music.set_volume(musicPercent)


def isOverMusic(Pos):
    distance = math.sqrt(((musicSliderX - Pos[0]) ** 2 + ((300 + 7 // 2) - Pos[1]) ** 2))
    if distance < 13:
        return True
    return False


def drawSoundSlider():
    soundIcon = pygame.image.load("Sound Icon.png")
    screen.blit(soundIcon, (280, 205))
    pygame.draw.rect(screen, (0, 0, 0), (345, 220, 180, 7))
    pygame.draw.circle(screen, (0, 255, 0), (soundSliderX, 220 + 7 // 2), 8)


def updateSoundSlider():
    global soundSliderX
    global soundPercent
    cursorX = pygame.mouse.get_pos()[0]
    cursorXonBar = min(max(cursorX, 345), 345 + 180)
    soundSliderX = cursorXonBar
    soundPercent = (cursorXonBar - 345) / 180
    config.soundPercent = soundPercent


def isOverSound(Pos):
    distance = math.sqrt(((soundSliderX - Pos[0]) ** 2 + ((220 + 7 // 2) - Pos[1]) ** 2))
    if distance < 13:
        return True
    return False


def gamePaused():
    pygame.mixer.music.pause()
    isPaused = True
    while isPaused:
        pygame.time.Clock().tick(120)  # locks game to 30fps so the program isn't intensive on game over screen
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
                quit()  # quit button quits the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pauseButton.isOver(pygame.mouse.get_pos()):
                    isPaused = False
                    pygame.mixer.music.unpause()
                    break
            if pygame.mouse.get_pressed()[0] and isOverMusic(pygame.mouse.get_pos()):
                updateMusicSlider()
            elif pygame.mouse.get_pressed()[0] and isOverSound(pygame.mouse.get_pos()):
                updateSoundSlider()
        exitKeys = pygame.key.get_pressed()  # pygame.key.get_pressed() is assigned to not call it 3 times each frame
        if exitKeys[pygame.K_RCTRL] or exitKeys[pygame.K_LCTRL] and exitKeys[pygame.K_q]:
            quit()


# PlayAgain = True
# while PlayAgain:
#     pygame.time.Clock().tick(
#         20)  # locks game to 20fps so the program isn't vastly different on different computers
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             quit()  # quit button quits the game
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if pauseButton.isOver(pygame.mouse.get_pos()):
#                 print("Pause")
#                 gamePaused()
