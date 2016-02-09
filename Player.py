

class Player:
    team = -1
    name = "Player"
    scriptFile = None
    script = None

    def __init__(self, t, scriptFile):
        self.team = t
        self.scriptFile = scriptFile

        # Read script
        #self.script = 

    def runScript(self, base):
        # TODO evaluate script provided

        # TODO write simple test script
        
        foodList = base.findFood()
        for m in base.findOwnMinions():
            # Go to and pick closest food
            closestFoodIndex = m.closest(foodList)
            if closestFoodIndex != -1:
                food = foodList[closestFoodIndex]
                m.moveTo(food.pos)
                m.pick(food.pos)

            # Reproduce
            ownMinionsExceptSelf = base.findOwnMinions()
            ownMinionsExceptSelf.remove(m)
            closestTeamMinionIndex = m.closest(ownMinionsExceptSelf)
            if closestTeamMinionIndex != -1:
                friendly = ownMinionsExceptSelf[closestTeamMinionIndex]
                m.reproduce(friendly.pos)

