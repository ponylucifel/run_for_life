__author__ = 'Thanapon Sathirathiwat'

"""
Main method to test all other classes
"""

from player import *
from platform import *
from camera import *
import constants
import pygame.mixer

def getTileMapList(fileName):
    tileList =[]
    sprite_sheet = SpriteSheet(fileName)

    # W platform Tile
    image = sprite_sheet.get_image(2, 2, 16, 16)
    image = pygame.transform.scale(image, (32, 32))
    tileList.append(image)

    # ExitBlock Tile
    image = sprite_sheet.get_image(2, 362, 16, 16)
    image = pygame.transform.scale(image, (32, 32))
    tileList.append(image)

    # T platform Tile
    image = sprite_sheet.get_image(344, 290, 16, 16)
    image = pygame.transform.scale(image, (32, 32))
    tileList.append(image)

    # P platform Tile
    image = sprite_sheet.get_image(344, 308, 16, 16)
    image = pygame.transform.scale(image, (32, 32))
    tileList.append(image)

    # B platform Tile
    image = sprite_sheet.get_image(344, 326, 16, 16)
    image = pygame.transform.scale(image, (32, 32))
    tileList.append(image)

    # R platform Tile
    image = sprite_sheet.get_image(344, 344, 16, 16)
    image = pygame.transform.scale(image, (32, 32))
    tileList.append(image)

    # V platform Tile
    image = sprite_sheet.get_image(344, 272, 16, 16)
    image = pygame.transform.scale(image, (32, 32))
    tileList.append(image)

    # A platform Tile
    image = sprite_sheet.get_image(326, 272, 16, 16)
    image = pygame.transform.scale(image, (32, 32))
    tileList.append(image)
    return tileList

def main():
    pygame.init()
    # screen created
    screen = pygame.display.set_mode(constants.DISPLAY, constants.FLAGS, constants.DEPTH)

    #load background music
    sound = pygame.mixer.Sound('10-shining-hotarunicus-stage.wav')
    sound.play()

    # set the screen title
    pygame.display.set_caption("RUN FOR YOUR LIFE!!")
    # flag for game exit
    gameExit = False
    tileMap = getTileMapList("res/sma4_tiles.png")
    timer = pygame.time.Clock()

    # player object created
    player = Player(56, 71)

    backgroundImage = pygame.image.load("res/starscape.png")
    backgroundImage = pygame.transform.scale(backgroundImage, (constants.WIN_WIDTH, constants.WIN_HEIGHT))

    x = y = 0
    entities = pygame.sprite.Group()
    platforms = []

    #directions
    left, right, up, down, idle, face = False, False, False, False, True, True

    # build the level
    for row in constants.stage1:
        for col in row:
            if col == "W":
                p = Platform(x, y, tileMap[0])
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y, tileMap[1])
                platforms.append(e)
                entities.add(e)
            if col == "T":
                p = Platform(x, y, tileMap[2])
                platforms.append(p)
                entities.add(p)
            if col == "P":
                p = Platform(x, y, tileMap[3])
                platforms.append(p)
                entities.add(p)
            if col == "B":
                p = Platform(x, y, tileMap[4])
                platforms.append(p)
                entities.add(p)
            if col == "R":
                p = Platform(x, y, tileMap[5])
                platforms.append(p)
                entities.add(p)
            if col == "V":
                p = SpikeBlock(x, y, tileMap[6])
                platforms.append(p)
                entities.add(p)
            if col == "A":
                p = SpikeBlock(x, y, tileMap[7])
                platforms.append(p)
                entities.add(p)
            x += 32
        y += 32
        x = 0

    total_level_width = len(constants.stage1[0]*32)
    total_level_height = len(constants.stage1)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while not gameExit:
        timer.tick(45)

        for e in pygame.event.get():
            if e.type == QUIT:
                gameExit = True
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                gameExit = True
            if e.type == KEYDOWN and (e.key == K_UP or e.key == K_SPACE):
                up = True
                idle = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
                face = False
                idle = False
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
                face = True
                idle = False

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        # draw background
        screen.blit(backgroundImage, (0, 0))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, platforms, face, idle)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
    pygame.quit()
    quit()

main()