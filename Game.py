import Map
import Minion
import Food
import Base
import Player
import Stats

import time

class Game:

    _base = None

    _players = []
    _playerNextTeam = 0

    def __init__(self):
        self._base = Base.Base()

    def initialize(self):
        # Add initial players here
        testPlayer0 = Player.Player(0, "P0")
        self.addPlayer(testPlayer0)

        testPlayer1 = Player.Player(1, "P1")
        self.addPlayer(testPlayer1)

        # Place food
        self._base._map.populateFoodRandomly()

    def addPlayer(self, player):
        # Add to player list
        player.team = self._playerNextTeam
        self._players.append(player)

        # Give player starting minions
        self.spawnStartingMinion(player.team)

        self._playerNextTeam += 1

    def spawnStartingMinion(self, team):
        # First minion
        m = self._base._addMinionRand(team)
        # Second
        if m != None:
            self._base._addMinionAroundGauss(m.pos, team)

    def gameLoop(self):

        while self.gameHasEnded() == False:
            self.gameIteration()

        print "Turns:", self._base._turn

    def gameIteration(self):
        # Game does its thing
        self._base._teamTurn = -1
        self.gameTurn(self._base)

        # Run scripts of all players in turn
        for p in self._players:
            #print "Team", p.team, "-", p.name
            self._base._teamTurn = p.team
            p.runScript(self._base)

        # Increment game turn count
        self._base._turn += 1

        # Output game state to display?
        #self._base._map.printMap()
        #time.sleep(0.1)


    def gameTurn(self, base):
        base._map.populateFoodRandomly()
        #pass

    def gameHasEnded(self):
        #return self._base._turn > 10
        return len(self._base._map.foodList) == 0 and self._base._turn > 1


def main():
    game = Game()
    game.initialize()
    game.gameLoop()


if __name__ == "__main__":
    main()