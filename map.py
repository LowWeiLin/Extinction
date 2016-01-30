import Base

class Map:
    size = (100, 100)
    foodNum = 30


    grid = None
    minionList = []
    foodList = []

    def initialize(self):
        self.initializeEmptyMap()

    def initializeEmptyMap(self):
        self.grid = [[None] * self.size[0]] * self.size[1]

    def populateFoodRandomly(self):
        pass

    def addRandomFood(self):
        pass

    def addMinion(self):
        pass

    def getMinionsTeam(self, team):
        pass

    def getMinionsExclTeam(self, team):
        pass
        
'''
m =  Map()
m.initialize()
print m.grid
'''