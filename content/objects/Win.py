import pygame, math, os, random

import content.modules.Util as Util
from content.objects.GrassParticle import GrassParticle
from content.modules.Audio import Audio

class Win(pygame.sprite.Sprite):
    def __init__(self, canvas, world, x, y):
        super().__init__()

        self.defaultImage = pygame.image.load(os.path.join(Util.rootDirectory, "content/assets/sprites/you-win.png"))
        self.rect = self.defaultImage.get_rect()
        self.canvas = canvas
        self.world = world


        self.posX = x
        self.posY = y

        self.rect.x = self.posX
        self.rect.y = self.posY 

        self.opacity = 255   
        self.fadeDirection = -5

    def update(self):
        self.opacity += self.fadeDirection

        if (self.opacity <= 0):
            self.opacity = 0
            self.fadeDirection = 5
        if (self.opacity >= 255):
            self.opacity = 255
            self.fadeDirection = -5

    def attemptDraw(self):
        self.rect.x = self.posX
        self.rect.y = self.posY


        self.image = pygame.transform.rotate(self.defaultImage, 0)
        self.image.fill((255, 255, 255, self.opacity), None, pygame.BLEND_RGBA_MULT)
        
        self.canvas.blit(self.image, (self.rect.x, self.rect.y))