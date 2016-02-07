

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
            index = m.closest(foodList)
            if index != -1:
                food = foodList[index]
                m.moveTo(food.pos)
                m.pick(food.pos)

