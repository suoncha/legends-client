import pygame
from config import *

# Initialize sound
class SoundManager:
    def __init__(self):
        self.theme = pygame.mixer.Sound(SOUND + 'theme.wav')
        self.theme.set_volume(0.4)
        self.theme.play(loops = -1)
        self.state = 1

    def playTheme(self):
        if self.state:
            self.state = 0
            pygame.mixer.pause()
        else:
            self.state = 1
            pygame.mixer.unpause()