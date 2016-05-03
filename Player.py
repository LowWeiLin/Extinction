import Base
from Quadtree import *

class Player:
    team = -1
    name = "Player"
    scriptFile = None
    script = None


    _kills = 0
    _deaths = 0
    
    _maxMinions = 1000

    def __init__(self, t, scriptFile):
        self.team = t
        self.scriptFile = scriptFile

        # Read script
        #self.script = 

    def runScript(self, base):
        if self.team == 1:
            self.runScript1(base)
        else:
            self.runScript2(base)

    def runScript2(self, base):
        
        friendly = base.findOwnMinions()
        for m in friendly:

            # Move direction
            movDir = (0,0)
            
            # Go to and pick closest food
            closestFood = m.closestFood()

            targetVector = (0, 0)
            if closestFood is not None:
                targetVector = closestFood.pos
                targetVector = base.minus(targetVector, m.pos)

            targetVector = base.unit(targetVector)
            targetVector = base.mul(targetVector, 5)
            movDir = base.add(movDir, targetVector)

            # Move
            m.moveTo(base.add(m.pos, movDir))


            # Pick
            if closestFood is not None:
                m.pick(closestFood.pos)

            # Reproduce
            closestTeamMinion = m.closestFriendly(2)
            if closestTeamMinion is not None and len(closestTeamMinion) > 1:
                closestTeamMinion = closestTeamMinion[1]
                m.reproduce(closestTeamMinion.pos)

            # Attack
            closestEnemyMinion = m.closestEnemy(1)
            if closestEnemyMinion is not None and len(closestEnemyMinion) > 0:
                closestEnemyMinion = closestEnemyMinion[0]
                m.attack(closestEnemyMinion.pos)

    def runScript1(self, base):
        
        friendly = base.findOwnMinions()
        for m in friendly:

            # Move direction
            movDir = (0,0)

            # Flocking motion
            # 1) Separation
            # 2) Alignment
            # 3) Cohesion

            sortedFriendly = m.closestFriendly(8)

            if len(sortedFriendly) > 1:
                # 1) Seperation
                closestFriendly = sortedFriendly[1]
                if base.dist(m.pos, closestFriendly.pos) < 3:
                    separationVector = m.pos
                    separationVector = base.minus(separationVector, closestFriendly.pos)
                    separationVector = base.unit(separationVector)

                    separationVector = base.mul(separationVector, 5)
                    movDir = base.add(movDir, separationVector)
                
                # 2) Alignment
                closest7 = sortedFriendly[1:7]        
                alignmentVectorSum = (0, 0)
                for f in closest7:
                    alignmentVector = base.minus(f.pos, f.prevPos)
                    alignmentVectorSum = base.add(alignmentVectorSum, alignmentVector)

                alignmentVectorSum = base.unit(alignmentVectorSum)
                alignmentVectorSum = base.mul(alignmentVectorSum, 5)
                movDir = base.add(movDir, alignmentVectorSum)


                # 3) Cohesion
                cohesionVectorSum = (0, 0)
                for f in closest7:
                    cohesionVector = f.pos
                    cohesionVector = base.minus(cohesionVector, m.pos)
                    cohesionVectorSum = base.add(cohesionVectorSum, cohesionVector)

                cohesionVectorSum = base.unit(cohesionVectorSum)
                cohesionVectorSum = base.mul(cohesionVectorSum, 5)
                movDir = base.add(movDir, cohesionVectorSum)

            
            # Go to and pick closest food
            closestFood = m.closestFood()

            # DEBUG
            # if closestFood1 != closestFood:
            #     print "-", closestFood1.pos, base.dist(closestFood1.pos, m.pos)
            #     print "+", closestFood.pos, base.dist(closestFood.pos, m.pos)
            #     print "*", m.pos

            targetVector = (0, 0)
            if closestFood is not None:
                targetVector = closestFood.pos
                targetVector = base.minus(targetVector, m.pos)

            targetVector = base.unit(targetVector)
            targetVector = base.mul(targetVector, 5)
            movDir = base.add(movDir, targetVector)

            # Move
            m.moveTo(base.add(m.pos, movDir))


            # Pick
            if closestFood is not None:
                m.pick(closestFood.pos)

            # Reproduce
            closestTeamMinion = m.closestFriendly(2)
            if closestTeamMinion is not None and len(closestTeamMinion) > 1:
                closestTeamMinion = closestTeamMinion[1]
                m.reproduce(closestTeamMinion.pos)

            # Attack
            closestEnemyMinion = m.closestEnemy(1)
            if closestEnemyMinion is not None and len(closestEnemyMinion) > 0:
                closestEnemyMinion = closestEnemyMinion[0]
                m.attack(closestEnemyMinion.pos)


