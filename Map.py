import Base
import Food
import Minion
import random as random


class Map:
    size = (150, 150)
    foodNum = 60


    grid = None
    minionList = []
    foodList = []

    minionTeamList = {}

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
        if self.inMapRange(pos) == False:
            return None
        return self.grid[pos[0]][pos[1]]

    def isOccupied(self, pos):
        return self.getAtPos(pos) != None

    def inMapRange(self, pos):
        return pos[0] >= 0 and pos[0] < self.size[0] and pos[1] >= 0 and pos[1] < self.size[1]

    '''
    Food
    '''

    def populateFoodRandomly(self):
        for i in range(self.foodNum):
            if len(self.foodList) >= self.foodNum:
                break
            self.addRandomFood()

    def addRandomFood(self):
        pos = self.getRandomGaussUnoccipiedPos((75,75), 20)
        #pos = self.getRandomUnoccupiedPos()
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
        self.grid[pos[0]][pos[1]] = None
        # Repopulate food randomly
        #self.populateFoodRandomly()

    def getFood(self):
        return self.foodList

    '''
    Minion
    '''

    def addMinion(self, minion):
        # Check if cell is occupied
        if self.isOccupied(minion.pos) == False:
            self.minionList.append(minion)
            pos = minion.pos
            self.grid[pos[0]][pos[1]] = minion

            if not minion.team in self.minionTeamList:
                self.minionTeamList[minion.team] = []
            self.minionTeamList[minion.team].append(minion)
            
    def removeMinion(self, minion):
        self.minionList.remove(minion)
        pos = minion.pos
        self.grid[pos[0]][pos[1]] = None

        if minion.team in self.minionTeamList:
            self.minionTeamList[minion.team].remove(minion)

    def moveMinion(self, minion, newPos):
        if self.isOccupied(newPos) == False:
            pos = minion.pos
            self.grid[pos[0]][pos[1]] = None
            minion.pos = newPos
            self.grid[newPos[0]][newPos[1]] = minion

    def getMinionsInTeam(self, team):
        minions = []
        # for m in self.minionList:
        #     if m.team == team:
        #         minions.append(m)
        if self.minionTeamList[team] != None:
            for m in self.minionTeamList[team]:
                minions.append(m)
        return minions

    def getMinionsNotInTeam(self, team):
        minions = []
        # for m in self.minionList:
        #     if m.team != team:
        #         minions.append(m)

        for t, minionTeamList in self.minionTeamList.items():
            if t != team:
                for m in minionTeamList:
                    minions.append(m)

        return minions
        
'''
m =  Map()
m.initialize()
print m.grid
'''