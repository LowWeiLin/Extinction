import pygame
from pygame.locals import *

import Game
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 800, 600
        self._ticks = 0

        self._game = Game.Game()
        self._game.initialize()

        self._maxFps = 2

 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self._game.gameIteration()

    def on_render(self):
        # Clear screen to white
        self._display_surf.fill((255,255,255))

        # Draw food
        for food in self._game._base._map.foodList:
            color = (0, 0, 0)
            pos = tuple([20*x for x in food.pos])
            pygame.draw.circle(self._display_surf, color, pos, 10, 0)

        # Draw minions
        for minion in self._game._base._map.minionList:
            color = (255, 0, 0)
            pos = tuple([20*x for x in minion.pos])
            pygame.draw.circle(self._display_surf, color, pos, 10, 0)

        # Draw FPS
        myfont = pygame.font.SysFont("monospace", 15)
        fpsLabel = myfont.render("FPS:" + str(round(1000./self._msElapsed, 3)), 1, (0,0,0))
        self._display_surf.blit(fpsLabel, (0, 0))

        # Switch buffer
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        self._clock = pygame.time.Clock()
        while( self._running ):
            # Restrict frame rate
            self._msElapsed = self._clock.tick(self._maxFps)
            # Handle events
            for event in pygame.event.get():
                self.on_event(event)
            # Update
            self.on_loop()
            # Render
            self.on_render()
            # Increment ticks
            self._ticks += 1

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()