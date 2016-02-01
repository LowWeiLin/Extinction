import Base
import Food
import Minion
import random as random


class Map:
    size = (20, 20)
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
        asciiGrid = []
        for row in self.grid:
            asciiRow = []
            for cell in row:
                if cell == None:
                    asciiRow.append('-')
                elif isinstance(cell, Food.Food):
                    asciiRow.append('F')
                elif isinstance(cell, Minion.Minion):
                    asciiRow.append(str(cell.team))
            asciiGrid.append(asciiRow)

        for row in asciiGrid:
            print ''.join(row)


    def clamp(self, x, mn, mx):
        return max(mn, min(x, mx))

    def getRandomUnoccupiedPos(self):
        for i in range(100):
            pos = (random.randint(0,self.size[0]-1), random.randint(0,self.size[1]-1))
            if self.isOccupied(pos) == False:
               return pos
        return None

    def getRandomGaussUnoccipiedPos(self, m, sigma=5):
        for i in range(100):
            random.gauss(m[0], sigma)
            pos = (self.clamp(int(random.gauss(m[0], sigma)), 0, self.size[0]-1),
                   self.clamp(int(random.gauss(m[1], sigma)), 0, self.size[1]-1))
            if self.isOccupied(pos) == False:
               return pos
        return None

    def getAtPos(self, pos):
        return self.grid[pos[0]][pos[1]]

    def isOccupied(self, pos):
        return self.getAtPos(pos) != None


    '''
    Food
    '''

    def populateFoodRandomly(self):
        for i in range(self.foodNum):
            if len(self.foodList) >= self.foodNum:
                break
            self.addRandomFood()

    def addRandomFood(self):
        pos = self.getRandomUnoccupiedPos()
        if pos != None:
            food = Food.Food(pos, 1)
            self.addFood(food)

    def addFood(self, food):
        # Check if cell is occupied
        if self.isOccupied(food.pos) == False:
            self.foodList.append(food)
            pos = food.pos
            self.grid[pos[0]][pos[1]] = food

    def removeFood(self, food):
        self.foodList.remove(food)
        pos = food.pos
        self.grid[pos.x][pos.y] = None
        # Repopulate food randomly
        self.populateFoodRandomly()

    '''
    Minion
    '''

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
        
'''
m =  Map()
m.initialize()
print m.grid
'''