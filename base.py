import Map
import Minion
import Food

class Base:

    # Map
    _map = None

    def initialize(self):
        pass

    # Returns list of minions from own team
    def findOwnMinions(self):
        pass

    # Returns list of minions from enemy teams
    def findEnemyMinions(self):
        pass

    # Returns list of food
    def findFood(self):
        pass

