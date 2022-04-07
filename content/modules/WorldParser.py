import pygame, json

from content.objects.BrickWall import BrickWall
from content.objects.GolfBall import GolfBall
from content.objects.GolfHole import GolfHole

class WorldParser():
    def __init__(self, canvas):
        self.rawData = []
        self.objectClasses = []
        self.tileMap = {
            0: None,
            1: BrickWall,
            2: GolfBall,
            3: GolfHole
        }

        self.canvas = canvas
        
        self.worldId = 0

    def loadWorld(self, fileName):
        with open(fileName, "r") as file:
            data = json.load(file)
            self.rawData = data.get("data")
            self.worldId = data.get("worldId")
            
        self.parseRawData()
        return self.rawData
    
    def parseRawData(self):
        for y in range(0, len(self.rawData)):
            for x in range(0, len(self.rawData[y])):
                tile = self.rawData[y][x]
                tileClass = self.tileMap[tile]

                if (tileClass):
                    instiatedTile = tileClass(self.canvas, self, x*16, y*16)
                    self.objectClasses.append(instiatedTile)