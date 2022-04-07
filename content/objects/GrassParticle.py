import pygame, math, os, random

import content.modules.Util as Util

class GrassParticle(pygame.sprite.Sprite):
    def __init__(self, canvas, world, x, y):
        super().__init__()

        self.defaultImage = pygame.image.load(os.path.join(Util.rootDirectory, "content/assets/sprites/ball-grass-particle.png"))
        self.rect = self.defaultImage.get_rect()
        self.canvas = canvas
        self.world = world

        self.velocity = 0

        self.posX = x
        self.posY = y

        self.rect.x = self.posX
        self.rect.y = self.posY

        self.rotation = 0
        self.imageRotation = random.randint(0, 360)
        
        self.zIndex = -1

        self.opacity = 255
        self.deathTick = 0
        
    def update(self):
        self.velocity = max(self.velocity - 0.2, 0)

        self.posX += math.cos(math.radians(self.rotation)) * self.velocity
        self.posY += math.sin(math.radians(self.rotation)) * self.velocity

        self.rotation = self.rotation % 360

        if (self.velocity == 0):
            self.deathTick += random.randint(1, 3)
            if (self.deathTick >= 100):
                self.opacity -= random.randint(1, 3)
                if (self.opacity <= 0):
                    self.kill()

    def kill(self):
        for i, obj in enumerate(self.world.objectClasses):
            if (obj == self):
                del self.world.objectClasses[i]
                break

    def launchParticle(self, angle, power):
        self.velocity = power
        self.rotation = angle
    
    def attemptDraw(self):
        self.rect.x = self.posX
        self.rect.y = self.posY

        self.imageRotation += 1 * self.velocity
        if (self.imageRotation > 360):
            self.imageRotation = 0

        self.image = pygame.transform.rotate(self.defaultImage, self.imageRotation)
        self.image = pygame.transform.scale(self.image, (int(self.rect.size[0]), int(self.rect.size[1])))
        self.image.fill((255, 255, 255, self.opacity), None, pygame.BLEND_RGBA_MULT)

        pygame.transform.rotate(self.image, self.rotation)
        self.canvas.blit(self.image, (self.rect.x, self.rect.y))