import Base
import Food
import Minion
import random as random

from Quadtree import *


class Map:
    size = (150, 150)
    foodNum = 60


    grid = None
    minionList = []
    foodList = []

    foodQuadtree = None

    minionTeamQuadtree = {}
    minionTeamList = {}

    quadtreeBoundary = AABB(Point((150/2, 150/2)), 150/2)

    def __init__(self):
        self.initializeEmptyMap()
        self.foodQuadtree = Quadtree(self.quadtreeBoundary)

    def initializeEmptyMap(self):
        self.grid = []
        for rows in range(self.size[1]):
            self.grid.append([None] * self.size[0])

    def printMap(self):
        asciiGrid = []
        for row in self.grid:
            asciiRow = []
            for cell in row:
                if cell is None:
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
            if self.isOccupied(pos) is False:
                return pos
        return None

    def getRandomGaussUnoccipiedPos(self, m, sigma=5):
        for i in range(100):
            random.gauss(m[0], sigma)
            pos = (self.clamp(int(random.gauss(m[0], sigma)), 0, self.size[0]-1),
                   self.clamp(int(random.gauss(m[1], sigma)), 0, self.size[1]-1))
            if self.isOccupied(pos) is False:
                return pos
        return None

    def getAtPos(self, pos):
        if self.inMapRange(pos) is False:
            return None
        return self.grid[pos[0]][pos[1]]

    def isOccupied(self, pos):
        return self.getAtPos(pos) is not None

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
        if pos is not None:
            food = Food.Food(pos, 1)
            self.addFood(food)

    def addFood(self, food):
        # Check if cell is occupied
        if self.isOccupied(food.pos) is False:
            self.foodList.append(food)
            self.foodQuadtree.insert(Point(food.pos, food))
            pos = food.pos
            self.grid[pos[0]][pos[1]] = food

    def removeFood(self, food):
        self.foodList.remove(food)
        self.foodQuadtree.remove(Point(food.pos, food))
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
        if self.isOccupied(minion.pos) is False:
            self.minionList.append(minion)
            pos = minion.pos
            self.grid[pos[0]][pos[1]] = minion

            if not minion.team in self.minionTeamList:
                self.minionTeamList[minion.team] = []
                self.minionTeamQuadtree[minion.team] = Quadtree(self.quadtreeBoundary)
                
            self.minionTeamList[minion.team].append(minion)
            self.minionTeamQuadtree[minion.team].insert(Point(minion.pos,minion))

            
    def removeMinion(self, minion):
        self.minionList.remove(minion)
        pos = minion.pos
        self.grid[pos[0]][pos[1]] = None

        if minion.team in self.minionTeamList:
            self.minionTeamList[minion.team].remove(minion)

        self.minionTeamQuadtree[minion.team].remove(Point(minion.pos,minion))

    def moveMinion(self, minion, newPos):
        if self.isOccupied(newPos) is False:
            # Remove from quadtree
            self.minionTeamQuadtree[minion.team].remove(Point(minion.pos,minion))

            pos = minion.pos
            self.grid[pos[0]][pos[1]] = None
            minion.prevPos = minion.pos
            minion.pos = newPos
            self.grid[newPos[0]][newPos[1]] = minion

            # Re-insert into quadtree
            self.minionTeamQuadtree[minion.team].insert(Point(minion.pos,minion))

    def getMinionsInTeam(self, team):
        minions = []
        if self.minionTeamList[team] is not None:
            return self.minionTeamList[team][:]
        return minions

    def getMinionsNotInTeam(self, team):
        minions = []
        # for m in self.minionList:
        #     if m.team != team:
        #         minions.append(m)

        for t, minionTeamList in self.minionTeamList.items():
            if t != team:
                minions.extend(minionTeamList[:])

        return minions
        
'''
m =  Map()
m.initialize()
print m.grid
'''