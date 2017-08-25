__author__ = 'Thanapon Sathirathiwat'



from pygame import *
from sprite_functions import *

class Platform(pygame.sprite.Sprite):
    """
    This class create a 32 by 32 platform of the image found in the loaded image in tileImage
    With the x, y coordinates, the class saves position to be displayed on the final project.
    """
    def __init__(self, x, y, tileImage=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = tileImage
        self.rect = Rect(x, y, 32, 32)


class ExitBlock(Platform):
    """
    Other obstacle class
    """
    def __init__(self, x, y, tileImage):
        Platform.__init__(self, x, y, tileImage)

class SpikeBlock(Platform):
    """
    Othee obstacle class
    """
    def __init__(self, x, y, tileImage):
        Platform.__init__(self, x, y, tileImage)