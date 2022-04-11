import pygame, json, os

from content.objects.BrickWall import BrickWall
from content.objects.GolfBall import GolfBall
from content.objects.GolfHole import GolfHole
from content.objects.Pointer import Pointer
from content.objects.Win import Win

class WorldParser():
    def __init__(self, canvas):
        self.rawData = []
        self.objectClasses = []
        self.tileMap = {
            0: None,
            1: BrickWall,
            2: GolfBall,
            3: GolfHole,
            4: Pointer,
            5: Win
        }

        self.canvas = canvas
        
        self.worldId = 0

    def loadWorld(self, fileName):
        self.objectClasses = []
        self.rawData = []

        with open(fileName, "r") as file:
            data = json.load(file)
            self.rawData = data.get("data")
            self.worldId = data.get("worldId")
            
        self.parseRawData()
        return self.rawData
    
    def checkForWorld(self, fileName):
        if (os.path.isfile(fileName)):
            return True
        else:
            return False
    
    def parseRawData(self):
        for y in range(0, len(self.rawData)):
            for x in range(0, len(self.rawData[y])):
                tile = self.rawData[y][x]
                tileClass = self.tileMap[tile]

                if (tileClass):
                    instiatedTile = tileClass(self.canvas, self, x*16, y*16)
                    self.objectClasses.append(instiatedTile)