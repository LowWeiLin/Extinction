import Map
import Minion
import Food

class Base:

    # Map
    _map = None
    _turn = 0
    _teamTurn = -1

    def __init__(self):
        self._map = Map.Map()
        self._turn = 0


    # Returns list of minions from own team
    def findOwnMinions(self):
        return self._map.getMinionsInTeam(self._teamTurn)

    # Returns list of minions from enemy teams
    def findEnemyMinions(self):
        return self._map.getMinionsNotInTeam(self._teamTurn)

    # Returns list of food
    def findFood(self):
        return self._map.getFood()

    def _addMinion(self, minion):
        self._map.addMinion(minion)

