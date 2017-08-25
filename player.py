__author__ = 'Thanapon Sathirathiwat'

from platform import *
from sprite_functions import *

class Player(pygame.sprite.Sprite):
    """
    This Player classs will load a lot of frame image to be used within the class to display sprite animation.
    Plus, it will keep track of the current x and y position of the player object as well as the cartesian coordinates' velocity
    """

    PLAYER_SPRITE_WIDTH = 56
    PLAYER_SPRITE_HEIGHT = 71

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []
    standing_frames = []
    jumping_frames = []
    dash_frames = []

    current_frame = 0

    def __init__(self, x, y):
        super().__init__()

        sprite_sheet = SpriteSheet("res/megamansprite.png")
        # graphic attributes for standing_frames for when player stand idle
        image = sprite_sheet.get_image(56, 355, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
        self.standing_frames.append(image)
        image = sprite_sheet.get_image(56, 355, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
        image = pygame.transform.flip(image, True, False)
        self.standing_frames.append(image)

        # graphic attributes for walking to the right
        for i in range(11):
            image = sprite_sheet.get_image(i*56, 142, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
            self.walking_frames_r.append(image)

        # graphic attributes for walking to the left
        # Load all the right facing images, then flip them
        # to face left.
        for i in range(11):
            image = sprite_sheet.get_image(i*56, 142, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

        # graphic attributes for jumping to the right and left
        image = sprite_sheet.get_image(224, 213, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
        self.jumping_frames.append(image)

        image = sprite_sheet.get_image(224, 213, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
        image = pygame.transform.flip(image, True, False)
        self.jumping_frames.append(image)

        # graphic attributes for dashing to the right and left
        image = sprite_sheet.get_image(56, 213, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
        self.dash_frames.append(image)

        image = sprite_sheet.get_image(56, 213, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
        image = pygame.transform.flip(image, True, False)
        self.dash_frames.append(image)

        self.x_vel = 0
        self.y_vel = 0
        self.onGround = False

        self.rect = Rect(x, y, self.PLAYER_SPRITE_WIDTH, self.PLAYER_SPRITE_HEIGHT)
        self.image = None

    def update(self, up, down, left, right, platforms, face, idle):
        if up:
            # only jump if on the ground
            self.image = self.jump(face)
            if self.onGround:
                self.y_vel -= 10
                # self.image = self.jump(face)
        elif down:
            if self.onGround:
                self.image = self.dash(face)
                if right:
                    self.x_vel = 15
                elif left:
                    self.x_vel = -15

        elif left:
            self.x_vel = -5
            if self.onGround:
                self.image = self.walk(face)
        elif right:
            self.x_vel = 5
            if self.onGround:
                self.image = self.walk(face)
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.y_vel += 0.3
            # max falling speed
            if self.y_vel > 100:
                self.y_vel = 100
        if not(left or right):
            self.x_vel = 0
            self.image = self.idle(face)
        # increment in x direction
        self.rect.left += self.x_vel
        # do x-axis collisions
        self.collide(self.x_vel, 0, platforms)
        # increment in y direction
        self.rect.top += self.y_vel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.y_vel, platforms)

    def collide(self, x_vel, y_vel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if x_vel > 0:
                    self.rect.right = p.rect.left
                    # print("collide right")
                if x_vel < 0:
                    self.rect.left = p.rect.right
                    # print("collide left")
                if y_vel > 0:
                    # print("collide bottom")
                    if isinstance(p, SpikeBlock):
                        pygame.event.post(pygame.event.Event(QUIT))
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.y_vel = 0
                if y_vel < 0:
                    self.rect.top = p.rect.bottom
                    if isinstance(p, SpikeBlock):
                        pygame.event.post(pygame.event.Event(QUIT))
                    # print("collide upper")

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