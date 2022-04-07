import pygame, math, os, random

import content.modules.Util as Util

class BrickWall(pygame.sprite.Sprite):
    def __init__(self, canvas, world, x, y):
        super().__init__()

        self.image = pygame.image.load(os.path.join(Util.rootDirectory, "content/assets/sprites/brick.png"))
        self.rect = self.image.get_rect()
        self.canvas = canvas
        self.world = world

        self.posX = x
        self.posY = y

        self.rect.x = self.posX
        self.rect.y = self.posY

    def attemptDraw(self):
        self.rect.x = self.posX
        self.rect.y = self.posY

        self.canvas.blit(self.image, (self.rect.x, self.rect.y))