__author__ = 'ponylucifel'

import pygame
from sprite_functions import *

class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player
    controls.
    """

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []
    standing_frames = []
    jumping_frames = []
    dash_frames = []

    current_frame = 0

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        sprite_sheet = SpriteSheet("res/megamansprite.png")
        # graphic attributes for standing_frames for when player stand idle
        image = sprite_sheet.get_image(56, 355, 56, 71)
        self.standing_frames.append(image)
        image = sprite_sheet.get_image(56, 355, 56, 71)
        image = pygame.transform.flip(image, True, False)
        self.standing_frames.append(image)

        # graphic attributes for walking to the right
        for i in range(11):
            image = sprite_sheet.get_image(i*56, 142, 56, 71)
            self.walking_frames_r.append(image)

        # graphic attributes for walking to the left
        # Load all the right facing images, then flip them
        # to face left.
        for i in range(11):
            image = sprite_sheet.get_image(i*56, 142, 56, 71)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

        # graphic attributes for jumping to the right and left
        image = sprite_sheet.get_image(224, 213, 56, 71)
        self.jumping_frames.append(image)

        image = sprite_sheet.get_image(224, 213, 56, 71)
        image = pygame.transform.flip(image, True, False)
        self.jumping_frames.append(image)

        # graphic attributes for dashing to the right and left
        image = sprite_sheet.get_image(56, 213, 56, 71)
        self.dash_frames.append(image)

        image = sprite_sheet.get_image(56, 213, 56, 71)
        image = pygame.transform.flip(image, True, False)
        self.dash_frames.append(image)

    def update(self, backward=False, forward=False, upward=False, downward=False, idle=False, face=True, onGround=True):
        pygame.time.Clock().tick(75)
        image = None
        if forward and not backward and not upward and not downward:
            image = self.walk()
        elif upward:
            image = self.jump(face=face)
        elif downward:
            image = self.dash(face)
        elif backward and not forward and not upward and not downward:
            image = self.walk(forward=False)
        elif idle and not face and not forward and not backward and not upward and not downward:
            # stand idle and face to the right
            image = self.idle(face)
        else:# Default case triggered if no direction is given.  Stand idle and face to the right
            image = self.idle(face)

        return image

    def idle(self, face=True):
        if face:
            return self.standing_frames[0]
        else:
            return self.standing_frames[1]

    def walk(self, forward=True):
        if forward:
            image = self.walking_frames_r[self.current_frame]
        else:
            image = self.walking_frames_l[self.current_frame]

        if self.current_frame >= len(self.walking_frames_r)-1:
            self.current_frame = 0
        else:
            self.current_frame += 1
        return image

    def jump(self, face=True, onGround=True):
        if face:
            image = self.jumping_frames[0] #facing towards the right
        else:
            image = self.jumping_frames[1] #facing towards the left
        return image

    def dash(self, face=True):
        if face:
            image = self.dash_frames[0] #facing towards the right
        else:
            image = self.dash_frames[1] #facing towards the left
        return image