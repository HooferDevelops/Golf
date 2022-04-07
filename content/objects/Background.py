import pygame, math, os

import content.modules.Util as Util

class Background(pygame.surface.Surface):
    def __init__(self, canvas, x, y):
        super().__init__((x, y))

        self.fill((0, 0, 0))
        self.image = pygame.image.load(os.path.join(Util.rootDirectory, "content/assets/sprites/grass.png"))
        self.canvas = canvas

        xRepeat = int(math.ceil(x/16))
        yRepeat = int(math.ceil(y/16))
        for x in range(0, xRepeat):
            for y in range(0, yRepeat):
                self.blit(self.image, (x*16, y*16))
    
    def attemptDraw(self):
        self.canvas.blit(self, (0, 0))