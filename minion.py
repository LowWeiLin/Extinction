import Base
import Stats
import Food

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
            minDist = 1000000000
            for xOff in range(-1, 1):
                for yOff in range(-1, 1):
                    if xOff == 0 and yOff == 0:
                        continue
                    x = self.pos[0] + xOff
                    y = self.pos[1] + yOff
                    if self._base._map.inMapRange((x,y)) == False:
                        continue
                    dist = x*x + y*y
                    if dist < minDist:
                        minDist = dist
                        newPos = (x, y)
            if newPos != (-1, -1):
                self._base._map.moveMinion(self, newPos)

    def attack(self, x, y):
        pass

    def pick(self, x, y):
        pass

    def reproduce(self, x, y):
        pass


