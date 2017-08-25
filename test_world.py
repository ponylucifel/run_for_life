__author__ = 'Thanapon Sathirathiwat'

import pygame
from pygame import *
from test_player import *
from sprite_functions import *
import constants

def main():
    pygame.init()
    # screen created
    screen = pygame.display.set_mode(constants.DISPLAY, constants.FLAGS, constants.DEPTH)

    sound = pygame.mixer.Sound('10-shining-hotarunicus-stage.wav')
    sound.play()
    # set the screen title
    pygame.display.set_caption("RUN FOR YOUR LIFE!!")
    # flag for game exit
    gameExit = False

    timer = pygame.time.Clock()

    # loading background image and scale to fit the screen size
    backgroundImage = pygame.image.load("res/16-bit-horizon-15093.png")
    backgroundImage = pygame.transform.scale(backgroundImage, (constants.WIN_WIDTH, constants.WIN_HEIGHT))

    player = Player()

    x_pos = constants.ORIGIN_X
    y_pos = constants.ORIGIN_Y

    x_vel = 0
    y_vel = 0

    #directions
    left, right, up, down, idle, face = False, False, False, False, True, True
    onGround = True
    while not gameExit:
        for e in pygame.event.get():
            if e.type == QUIT:
                gameExit = True
            if e.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    right, face, left = True, True, False
                    x_vel = 5
                if keys[pygame.K_LEFT]:
                    right, face, left = False, False, True
                    x_vel = -5
                if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                    up, down = True, False
                    y_vel = -80
                    x_vel = 0
                    onGround = False
                    if keys[pygame.K_RIGHT]:
                        right, face, left = True, True, False
                        x_vel = 7
                    elif keys[pygame.K_LEFT]:
                        right, face, left = False, False, True
                        x_vel = -7
                if keys[pygame.K_DOWN]:
                    y_vel = 0
                    x_vel = 12
                    if keys[pygame.K_LEFT] or not face:
                        x_vel = -12
                    up, down = False, True
            if e.type == KEYUP:# restore the default value if no buttons are pressed on
                x_vel = 0
                y_vel = 0
                left, right, up, down = False, False, False, False

        if y_pos < constants.ORIGIN_Y and not onGround:
            y_vel = 5

        if x_pos <= 0:
            x_pos = 0
        elif x_pos > constants.WIN_WIDTH - 43:
            x_pos = constants.WIN_WIDTH - 43
            x_vel = 0
        if y_pos <= 0:
            y_pos = 0
        elif y_pos > constants.WIN_HEIGHT - 70:
            y_pos = constants.WIN_HEIGHT - 70
            y_vel = 0

        x_pos += x_vel
        y_pos += y_vel

        # player will be able to jump if they're on ground again.
        if y_pos >= constants.ORIGIN_Y and not onGround:
            onGround = True
            y_vel = 0
            y_pos = constants.ORIGIN_Y

        screen.blit(backgroundImage, (0, 0))
        screen.blit(player.update(left, right, up, down, idle, face, onGround), (x_pos, y_pos))
        timer.tick(120)
        pygame.display.update()
    pygame.quit()
    quit()

main()