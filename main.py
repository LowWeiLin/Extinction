import Map
import Minion
import Food
import Base
import Player
import Stats

class Game:

    _base = None

    _players = []
    _playerNextTeam = 0

    def __init__(self):
        self._base = Base.Base()

    def initialize(self):
        # Add initial players here
        testPlayer = Player.Player(-1, "")
        self.addPlayer(testPlayer)

    def addPlayer(self, player):
        # Add to player list
        player.team = self._playerNextTeam
        self._players.append(player)

        # Give player starting minions

        # Find random position near a position?
        self.spawnStartingMinion(player.team)
        self.spawnStartingMinion(player.team)

    def getStartingStats(self):
        # TODO randomize this?
        return Stats.Stats()

    def spawnStartingMinion(self, team):

        randPos = self._base._map.getRandomUnoccupiedPos()
        if randPos != None:
            stats = self.getStartingStats()
            minion = Minion.Minion(team, randPos, stats)
            # Spawn
            self._base._addMinion(minion)

            randPos = self._base._map.getRandomGaussUnoccipiedPos(randPos)
            if randPos != None:
                stats = self.getStartingStats()
                minion = Minion.Minion(team, randPos, stats)
                # Spawn
                self._base._addMinion(minion)


    def gameLoop(self):

        while self.gameHasEnded() == False:

            # Game does its thing
            self._base._teamTurn = -1
            self.gameTurn(self._base)

            # Run scripts of all players in turn
            for p in self._players:
                print "Team", p.team, "-", p.name
                self._base._teamTurn = p.team
                p.runScript(self._base)

            # Increment game turn count
            self._base._turn += 1

            # Output game state to display?
            self._base._map.printMap()

            break

    def gameTurn(self, base):
        pass

    def gameHasEnded(self):
        return False


def main():
    game = Game()
    game.initialize()
    game.gameLoop()


if __name__ == "__main__":
    main()