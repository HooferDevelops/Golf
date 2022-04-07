import pygame

from content.modules.WorldParser import WorldParser
import content.modules.Util as Util
from content.modules.Audio import Audio
from content.objects.Background import Background

clock = pygame.time.Clock()

class Golf:
    def __init__(self):
        self.backgroundMusic = Audio()
        self.backgroundMusic.loadSound("content/assets/sounds/music/track-1.mp3")
        self.backgroundMusic.loopPlaySound()

        self.screen = pygame.display.set_mode((Util.windowSize, Util.windowSize))

        self.canvas = pygame.Surface((16*8, 16*8))
        self.background = Background(self.canvas, 16*8, 16*8)

        self.world = WorldParser(self.canvas)
        self.world.loadWorld("content/assets/worlds/2.json")

        pygame.display.set_caption("Golf")

    def drawUpdate(self):
        self.background.attemptDraw()

        self.world.objectClasses.sort(key=lambda x: hasattr(x, "zIndex") and x.zIndex or 0)

        for obj in self.world.objectClasses:
            if (hasattr(obj, "attemptDraw")):
                obj.attemptDraw()
            
        self.screen.blit(pygame.transform.scale(self.canvas, self.screen.get_rect().size), (0, 0))
        pygame.display.update()

        clock.tick(60)

    def eventsCheck(self):
        for event in pygame.event.get():
            for obj in self.world.objectClasses:
                if (hasattr(obj, "event")):
                    obj.event(event)
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def physicsCheck(self):
        for obj in self.world.objectClasses:
            if (hasattr(obj, "update")):
                obj.update()

    def gameLoop(self):
        while True:
            self.physicsCheck()
            self.drawUpdate()
            self.eventsCheck()