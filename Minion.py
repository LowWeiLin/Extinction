import Base
import Stats
import Food
from Quadtree import *

INF = 1000000000

class Minion:

    _base = None

    team = -1
    pos = None
    prevPos = None
    stats = None

    def __init__(self, base, team, pos, stats):
        self._base = base
        self.team = team
        self.pos = pos
        self.prevPos = pos
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
                    if self._base._map.inMapRange((x,y)) is False:
                        continue
                    dist = self._base.dist(targetPos, (x,y))
                    if dist < minDist:
                        minDist = dist
                        newPos = (x, y)
            if newPos != (-1, -1):
                self._base._map.moveMinion(self, newPos)

    def _takeDmg(self, dmg, attacker):
        self.stats._takeDmg(dmg, self, attacker)

    def _die(self, attacker):
        #print "Died! ", self.team
        self._base._removeMinion(self)

    def attack(self, pos):
        # Check range
        if self.inAttackRange(pos) is False:
            return None

        # Find minion
        obj = self._base._map.getAtPos(pos)
        if obj is None:
            return None
        # Minion
        if isinstance(obj, Minion):
            obj._takeDmg(self.stats._dmg, self)
            
    def pick(self, pos):
        # Check range
        if self.inActionRange(pos) is False:
            return None

        # Find item
        obj = self._base._map.getAtPos(pos)
        if obj is None:
            return None
        # Food
        if isinstance(obj, Food.Food):
            self._base._map.removeFood(obj)
            self.stats._food += 1
    
    def inActionRange(self, pos):
        return self._base.dist(self.pos, pos) <= self.stats._actionRange

    def inAttackRange(self, pos):
        return self._base.dist(self.pos, pos) <= self.stats._attackRange

    def reproduce(self, pos):
        # Check if max minion limit is hit
        if self.team in self._base._map.minionTeamList:
            if len(self._base._map.minionTeamList[self.team]) >= self._base.getPlayer(self.team)._maxMinions:           
                return None

        # Check range
        if self.inActionRange(pos) is False:
            return None
        # Find obj
        obj = self._base._map.getAtPos(pos)
        if obj is None:
            return None
        # Minion from same team
        if isinstance(obj, Minion) and obj.team == self.team and obj != self:
            # Self must have enough food
            if self.stats._food >= self.stats._reproduceFoodCost:
                # Target must have enough food
                if obj.stats._food >= obj.stats._reproduceFoodCost:
                    # Reproduce #1
                    obj.stats._food -= obj.stats._reproduceFoodCost
                    obj._base._addMinionAroundGauss(obj.pos, obj.team)
                    # Reproduce #2
                    self.stats._food -= self.stats._reproduceFoodCost
                    self._base._addMinionAroundGauss(self.pos, self.team)


    # Returns closest item in given objList
    def closest(self, objList):
        minDist = INF
        index = -1
        for i in range(len(objList)):
            dist = self._base.dist(self.pos, objList[i].pos)
            if dist < minDist:
                minDist = dist
                index = i

        if index == -1:
            return None

        return objList[index]

        # sortedList = self.sortedByDistance(objList)
        # if len(sortedList) == 0:
        #     return None

        # return sortedList[0]

    def closestFood(self):
        closestFood = self._base._map.foodQuadtree.queryNearest(Point(self.pos))
        if closestFood is not None:
            closestFood = closestFood[0].obj
        return closestFood

    def closestFriendly(self, k=1):
        if self._base._map.minionTeamQuadtree[self.team] is None:
            return None

        points = self._base._map.minionTeamQuadtree[self.team].queryKNearest(Point(self.pos), k)
        closestFriendlyList = []
        for point in points:
            closestFriendlyList.append(point.obj)

        return closestFriendlyList

    def closestEnemy(self, k=1):
        if self._base._map.minionTeamQuadtree[self.team] is None:
            return None

        enemies = []
        for t, minionTeamList in self._base._map.minionTeamQuadtree.items():
            if t != self.team:
                points = self._base._map.minionTeamQuadtree[t].queryKNearest(Point(self.pos), k)
                enemyList = []
                for point in points:
                    enemyList.append(point.obj)
                enemies.extend(enemyList)

        return self.sortedByDistance(enemies)[:k]

    # Returns sorted list based on how close ibj is
    def sortedByDistance(self, objList):
        sortedObjList = objList[:]

        for i in range(len(sortedObjList)):
            for j in range(i, len(sortedObjList)):
                if i == j:
                    continue
                disti = self._base.dist(self.pos, sortedObjList[i].pos)
                distj = self._base.dist(self.pos, sortedObjList[j].pos)
                if disti > distj:
                    temp = sortedObjList[i]
                    sortedObjList[i] = sortedObjList[j]
                    sortedObjList[j] = temp

        return sortedObjList