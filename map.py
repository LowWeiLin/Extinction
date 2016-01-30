import Base
import random as random

class Map:
    size = (10, 10)
    foodNum = 30


    grid = None
    minionList = []
    foodList = []

    def __init__(self):
        self.initializeEmptyMap()

    def initializeEmptyMap(self):
        self.grid = []
        for rows in range(self.size[1]):
            self.grid.append([None] * self.size[0])

    def printMap(self):
        for row in self.grid:
            print row

    def getRandomUnoccupiedPos(self):
        for i in range(100):
            pos = (int(random.random()%self.size[0]), int(random.random()%self.size[1]))
            if self.isOccupied(pos) == False:
               return pos
        return None

    def clamp(self, x, mn, mx):
        return max(mn, min(x, mx))

    def getRandomGaussUnoccipiedPos(self, m, sigma=5):
        for i in range(100):
            random.gauss(m[0], sigma)
            pos = (self.clamp(int(random.gauss(m[0], sigma)), 0, self.size[0]-1),
                   self.clamp(int(random.gauss(m[1], sigma)), 0, self.size[1]-1))
            if self.isOccupied(pos) == False:
               return pos
        return None

    def populateFoodRandomly(self):
        pass

    def addRandomFood(self):
        pass

    def addMinion(self, minion):
        # Check if cell is occupied
        if self.isOccupied(minion.pos) == False:
            self.minionList.append(minion)
            pos = minion.pos
            self.grid[pos[0]][pos[1]] = minion

    def removeMinion(self, minion):
        self.minionList.remove(minion)
        pos = minion.pos
        self.grid[pos.x][pos.y] = None

    def moveMinion(self, minion, newPos):
        if isOccupied(newPos) == False:
            pos = minion.pos
            self.grid[pos.x][pos.y] = None
            minion.pos = newPos
            self.grid[newPos.x][newPos.y] = minion

    def getMinionsInTeam(self, team):
        pass

    def getMinionsNotInTeam(self, team):
        pass
        
    def getAtPos(self, pos):
        return self.grid[pos[0]][pos[1]]

    def isOccupied(self, pos):
        return self.getAtPos(pos) != None

'''
m =  Map()
m.initialize()
print m.grid
'''