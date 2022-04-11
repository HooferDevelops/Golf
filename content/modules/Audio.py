import pygame, random

import content.modules.Util as Util

class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = []

    def loadSound(self, fileName):
        sound = pygame.mixer.Sound(fileName)
        self.sounds.append(sound)

    def playSound(self):
        self.sounds[random.randint(0, len(self.sounds)-1)].play()
    
    def stopSound(self):
        for sound in self.sounds:
            sound.stop()

    def loopPlaySound(self):
        self.sounds[random.randint(0, len(self.sounds)-1)].play(-1)