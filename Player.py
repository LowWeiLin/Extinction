

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
        
        food = base.findFood()
        for m in base.findOwnMinions():
            m.moveTo(food[0].pos)

