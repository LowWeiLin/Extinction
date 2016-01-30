import Base

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
        # TODO make this random
        # TODO make a version that is random within a range.
        pos = (0,0)
        if self.isOccupied(pos):
           return None
        else:
            return pos

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