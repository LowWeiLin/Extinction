import Map
import Minion
import Food
import Stats

import math

class Base:

    # Map
    _map = None
    _turn = 0
    _teamTurn = -1

    _players = []
    _playerNextTeam = 0

    def __init__(self):
        self._map = Map.Map()
        self._turn = 0

    # Returns player from team
    def getPlayer(self, team):
        for p in self._players:
            if p.team == team:
                return p

    # Returns list of minions from own team
    def findOwnMinions(self):
        return self._map.getMinionsInTeam(self._teamTurn)

    # Returns list of minions from enemy teams
    def findEnemyMinions(self):
        return self._map.getMinionsNotInTeam(self._teamTurn)

    # Returns list of food
    def findFood(self):
        return self._map.getFood()

    def getStartingStats(self):
        # TODO randomize this?
        return Stats.Stats()

    def _addMinion(self, minion):
        self._map.addMinion(minion)

    def _removeMinion(self, minion):
        self._map.removeMinion(minion)

    def _addMinionRand(self, team):
        randPos = self._map.getRandomUnoccupiedPos()
        if randPos != None:
            stats = self.getStartingStats()
            minion = Minion.Minion(self, team, randPos, stats)
            # Spawn
            self._addMinion(minion)
            return minion
        return None

    def _addMinionAroundGauss(self, randPos, team):
        randPos = self._map.getRandomGaussUnoccipiedPos(randPos)
        if randPos != None:
            stats = self.getStartingStats()
            minion = Minion.Minion(self, team, randPos, stats)
            # Spawn
            self._addMinion(minion)
            return minion
        return None

    def dist(self, pos0, pos1):
        return math.sqrt((pos0[0] - pos1[0])**2 + (pos0[1] - pos1[1])**2)
