import Base
import Stats
import Food

class Minion:

    team = -1
    pos = None
    stats = None

    def _initialize(self):
        self.stats = Stats()
        
    def move(self, x, y):
        pass

    def attack(self, x, y):
        pass

    def pick(self, x, y):
        pass

    def reproduce(self, x, y):
        pass


