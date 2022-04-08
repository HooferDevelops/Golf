import pygame, math, os, random

import content.modules.Util as Util
from content.objects.GrassParticle import GrassParticle
from content.modules.Audio import Audio

class GolfBall(pygame.sprite.Sprite):
    def __init__(self, canvas, world, x, y):
        super().__init__()

        self.swingSounds = Audio()
        self.swingSounds.loadSound("content/assets/sounds/ball/swing-1.ogg")
        self.swingSounds.loadSound("content/assets/sounds/ball/swing-2.ogg")
        
        self.hitSounds = Audio()
        self.hitSounds.loadSound("content/assets/sounds/wall/impact-1.ogg")
        self.hitSounds.loadSound("content/assets/sounds/wall/impact-2.ogg")
        self.hitSounds.loadSound("content/assets/sounds/wall/impact-3.ogg")

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
        self.targetHole = None
        self.opacity = 255

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
        if (self.targetHole):
            self.opacity -= 5
            if (random.randint(1,3) == 3):
                holeAngle = math.degrees(math.atan2(self.targetHole.rect.y+4+random.randint(-3,3)-self.rect.y, self.targetHole.rect.x+4+random.randint(-3,3)-self.rect.x)) % 360
                self.rotation = holeAngle #+ random.randint(-22,22)

        if (self.targetHole and self.opacity <= 0):
            for i, obj in enumerate(self.world.objectClasses):
                if (obj == self):
                    del self.world.objectClasses[i]
                    return
        
        self.velocity = max(self.velocity - 0.03, 0)
        
        newPotX = self.posX + math.cos(math.radians(self.rotation)) * self.velocity
        newPotY = self.posY + math.sin(math.radians(self.rotation)) * self.velocity

        # make the ball bounce off the walls
        if newPotX < 0:
            newPotX = 0
            self.rotation = 180 + self.rotation
        elif newPotX > 16*8 - (self.rect.size[0]):
            newPotX = 16*8 - (self.rect.size[0])
            self.rotation = 180 + self.rotation
        elif newPotY < 0:
            newPotY = 0
            self.rotation = 360 - self.rotation
        elif newPotY > 16*8 - (self.rect.size[1]):
            newPotY = 16*8 - (self.rect.size[1])
            self.rotation = 360 - self.rotation

        self.posX = newPotX
        self.posY = newPotY

        # make the ball bounce off the bricks
        for obj in self.world.objectClasses:
            if (type(obj).__name__ == "BrickWall" or type(obj).__name__ == "GolfBall" and obj != self):
                collisionObjects = []
                # check if the ball is colliding with the brick
                if (obj.rect.colliderect(self.rect) and self.velocity > 0):
                    collisionObjects.append(obj)
                
                collisionObjects.sort(key=lambda x: pygame.math.Vector2(self.rect.x, self.rect.y).distance_to((x.rect.x, x.rect.y)))

                if (len(collisionObjects) > 0):
                    obj = collisionObjects[0]
                    
                    hitAngle = math.degrees(math.atan2(self.rect.y-obj.rect.y, self.rect.x-obj.rect.x)) % 360
                    
                    if (self.rect.x - obj.rect.x < 0 and hitAngle > 111 and hitAngle < 225):
                        # ball is to the left of the brick
                        self.rotation = 180 + self.rotation
                        newPotX = obj.rect.x - self.rect.size[0]
                    elif (obj.rect.x - self.rect.x < 0 and hitAngle < 45 or hitAngle > 335):
                        # ball is to the right of the brick
                        self.rotation = 180 + self.rotation
                        newPotX = obj.rect.x + obj.rect.size[0]
                    elif (obj.rect.y - self.rect.y < 0 and hitAngle < 111 and hitAngle >= 45):
                        # ball is below the brick
                        self.rotation = 360 - self.rotation
                        newPotY = obj.rect.y + obj.rect.size[1]
                    elif (self.rect.y - obj.rect.y < 0 and hitAngle > 225 and hitAngle < 335):
                        # ball is above the brick
                        self.rotation = 360 - self.rotation
                        newPotY = obj.rect.y - self.rect.size[1]
                                        
                    break

        self.rotation = self.rotation % 360

        self.posX = newPotX
        self.posY = newPotY

        if (self.velocity > 0):
            particle = GrassParticle(self.canvas, self.world, self.posX + (random.randint(-1,1) * 4), self.posY + (random.randint(-1,1) * 4))
            particle.velocity = self.velocity
            particle.rotation = (self.rotation + 180) % 360
            self.world.objectClasses.append(particle)

    def launchBall(self):
        self.holding = False
        bX, bY = (self.rect.x + (self.rect.size[0]/2), self.rect.y + (self.rect.size[1]/2))
        mX, mY = pygame.mouse.get_pos()
        mX /= (Util.windowSize / self.canvas.get_rect().size[0])
        mY /= (Util.windowSize / self.canvas.get_rect().size[1])
        
        lineLength = math.hypot(bX-mX, bY-mY)

        angle = math.atan2(bY-mY, bX-mX)

        self.velocity += lineLength/10
        self.velocity = min(self.velocity, 7)
        self.rotation = math.degrees(angle)

        self.swingSounds.playSound()
    
    def attemptDraw(self):
        self.rect.x = self.posX
        self.rect.y = self.posY

        if (self.velocity > 0 and random.randint(1,4) == 1):
            self.imageRotation += 90
        if (self.imageRotation > 360):
            self.imageRotation = 0

        self.image = pygame.transform.rotate(self.defaultImage, self.imageRotation)
        self.image.fill((255, 255, 255, self.opacity), None, pygame.BLEND_RGBA_MULT)
        
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