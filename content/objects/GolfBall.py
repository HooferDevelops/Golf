import pygame, math, os, random

import content.modules.Util as Util
from content.objects.GrassParticle import GrassParticle

class GolfBall(pygame.sprite.Sprite):
    def __init__(self, canvas, world, x, y):
        super().__init__()

        self.defaultImage = pygame.image.load(os.path.join(Util.rootDirectory, "content/assets/sprites/ball-3.png"))
        self.rect = self.defaultImage.get_rect()
        self.canvas = canvas
        self.world = world

        self.velocity = 0

        self.posX = x
        self.posY = y+8

        self.rect.x = self.posX
        self.rect.y = self.posY

        self.rotation = 0
        self.imageRotation = 0

        self.holding = False

    def event(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            # check if the mouse is over the ball
            mX, mY = pygame.mouse.get_pos()

            mX /= (Util.windowSize / self.canvas.get_rect().size[0])
            mY /= (Util.windowSize / self.canvas.get_rect().size[1])

            if self.rect.collidepoint((mX, mY)):
                self.holding = True
        if (event.type == pygame.MOUSEBUTTONUP):
            if (self.holding):
                self.launchBall()
        
    def update(self):
        self.velocity = max(self.velocity - 0.1, 0)

        self.posX += math.cos(math.radians(self.rotation)) * self.velocity
        self.posY += math.sin(math.radians(self.rotation)) * self.velocity

        # make the ball bounce off the walls
        if self.posX < 0:
            self.posX = 0
            self.rotation = 180 + self.rotation
        elif self.posX > 16*8 - (self.rect.size[0]):
            self.posX = 16*8 - (self.rect.size[0])
            self.rotation = 180 + self.rotation
        elif self.posY < 0:
            self.posY = 0
            self.rotation = 360 - self.rotation
        elif self.posY > 16*8 - (self.rect.size[1]):
            self.posY = 16*8 - (self.rect.size[1])
            self.rotation = 360 - self.rotation

        # make the ball bounce off the bricks
        for obj in self.world.objectClasses:
            if (type(obj).__name__ == "BrickWall" or type(obj).__name__ == "GolfBall" and obj != self):
                # check if the ball is colliding with the brick
                if (obj.rect.colliderect(self.rect)):
                    # inverse the ball's rotation
                    self.rotation = self.rotation + 180

        self.rotation = self.rotation % 360

        if (self.velocity > 0 and random.randint(1,2) == 1):
            particle = GrassParticle(self.canvas, self.world, self.posX + (random.randint(-1,1) * 4), self.posY + (random.randint(-1,1) * 4))
            particle.velocity = self.velocity
            particle.rotation = (self.rotation + 180) % 360
            self.world.objectClasses.append(particle)

    def launchBall(self):
        self.holding = False
        bX, bY = (self.posX, self.posY)
        mX, mY = pygame.mouse.get_pos()
        mX /= (Util.windowSize / self.canvas.get_rect().size[0])
        mY /= (Util.windowSize / self.canvas.get_rect().size[1])
        
        lineLength = math.hypot(bX-mX, bY-mY)

      
        angle = math.atan2(bY-mY, bX-mX)

        self.velocity += lineLength/10
        self.rotation = math.degrees(angle)
    
    def attemptDraw(self):
        self.rect.x = self.posX
        self.rect.y = self.posY

        if (self.velocity > 0 and random.randint(1,4) == 1):
            self.imageRotation += 90
        if (self.imageRotation > 360):
            self.imageRotation = 0

        self.image = pygame.transform.rotate(self.defaultImage, self.imageRotation)

        pygame.transform.rotate(self.image, self.rotation)
        self.canvas.blit(self.image, (self.rect.x, self.rect.y))

        if (self.holding):
            mX, mY = pygame.mouse.get_pos()

            mX /= (Util.windowSize / self.canvas.get_rect().size[0])
            mY /= (Util.windowSize / self.canvas.get_rect().size[1])

            bX, bY = (self.rect.x + (self.rect.size[0]/2), self.rect.y + (self.rect.size[1]/2))

            lineLength = math.hypot(bX-mX, bY-mY)

            lineLength = min((lineLength+5)/32, 1)
            Util.createLine(self.canvas, Util.lerp3Color((0,255,0, 0), (255,255,0, 255/2), (255,0,0, 255), lineLength), (bX, bY), (mX, mY), 0.5, 32)