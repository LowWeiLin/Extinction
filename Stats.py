
class Stats:

    _hp = 10
    _maxHp = 10
    _dmg = 1
    _actionRange = 5
    _attackRange = 5

    _energy = 10
    _energyReplenishment = 1

    _food = 0
    _reproduceFoodCost = 5

    _foodTurnCost = 0.05

    def _takeDmg(self, damage, minion, attacker):
        self._hp -= damage
        if self._hp <= 0:
            minion._die(attacker)

    def _consumeFood(self, minion):
        if self._food > self._foodTurnCost:
            self._food -= self._foodTurnCost
            if self._hp < self._maxHp:
                self._hp += self._foodTurnCost
        else:
            self._takeDmg(self._foodTurnCost, minion, minion)


