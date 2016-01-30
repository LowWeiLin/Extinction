import Base
import Stats
import Food

class Minion:

    team = -1
    pos = None
    stats = None

    def __init__(self, team, pos, stats):
        self.team = team
        self.pos = pos
        self.stats = stats
        
    def moveTo(self, x, y):
        pass

    def attack(self, x, y):
        pass

    def pick(self, x, y):
        pass

    def reproduce(self, x, y):
        pass


