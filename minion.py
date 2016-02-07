import Base
import Stats
import Food

INF = 1000000000

class Minion:

    _base = None

    team = -1
    pos = None
    stats = None

    def __init__(self, base, team, pos, stats):
        self._base = base
        self.team = team
        self.pos = pos
        self.stats = stats
        
    def moveTo(self, targetPos):
        if self._base._teamTurn == self.team and self.pos != targetPos:
            newPos = (-1, -1)
            minDist = INF
            for xOff in range(-1, 2):
                for yOff in range(-1, 2):
                    if xOff == 0 and yOff == 0:
                        continue
                    x = self.pos[0] + xOff
                    y = self.pos[1] + yOff
                    if self._base._map.inMapRange((x,y)) == False:
                        continue
                    dist = self._base.dist(targetPos, (x,y))
                    if dist < minDist:
                        minDist = dist
                        newPos = (x, y)
            if newPos != (-1, -1):
                self._base._map.moveMinion(self, newPos)

    def attack(self, pos):
        pass

    def pick(self, pos):
        # Check range
        if self.inActionRange(pos) == False:
            return None

        # Find item
        obj = self._base._map.getAtPos(pos)
        if obj == None:
            return None
        # Food
        if isinstance(obj, Food.Food):
            self._base._map.removeFood(obj)
            self.stats._food += 1
    
    def inActionRange(self, pos):
        return self._base.dist(self.pos, pos) <= self.stats._actionRange

    def reproduce(self, x, y):
        pass

    # Returns index of closest item in given objList
    def closest(self, objList):
        minDist = INF
        index = -1
        for i in range(len(objList)):
            dist = self._base.dist(self.pos, objList[i].pos)
            if dist < minDist:
                minDist = dist
                index = i
        return index

