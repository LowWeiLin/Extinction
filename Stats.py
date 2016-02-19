
class Stats:

    _hp = 10
    _maxHp = 10
    _dmg = 1
    _actionRange = 3
    _attackRange = 6

    _energy = 10
    _energyReplenishment = 1

    _food = 0
    _reproduceFoodCost = 5

    def _takeDmg(self, damage, minion, attacker):
        self._hp -= damage
        if self._hp <= 0:
            minion._die(attacker)

