import pygame, os

import content.modules.Util as Util
from content.modules.Audio import Audio

class GolfHole(pygame.sprite.Sprite):
    def __init__(self, canvas, world, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Util.rootDirectory, "content/assets/sprites/hole.png"))
        self.rect = self.image.get_rect()
        self.canvas = canvas
        self.world = world

        self.rect.x = x
        self.rect.y = y

        self.holeSounds = Audio()
        self.holeSounds.loadSound("content/assets/sounds/hole/hole-1.mp3")
        
    def attemptDraw(self):
        self.canvas.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        for i, obj in enumerate(self.world.objectClasses):
            if (type(obj).__name__ == "GolfBall"):
                if (obj.rect.colliderect(self.rect) and not obj.targetHole):
                    self.holeSounds.playSound()
                    obj.targetHole = self