import time
from model import Position

class GameLoop:
    def __init__(self, fps, gui, initial_state):
        self.fps = fps
        self.gui = gui
        self.running = False
        self.state = initial_state
    
    def run(self):
        if self.running:    return
        
        self.running = True
        seconds_per_frame = 1 / self.fps 
        last_instant = time.time()
        while self.running:
            current_instant = time.time()
            elapsed_time = current_instant - last_instant

            self.state.step(self, self.gui, elapsed_time)

            last_instant = current_instant
            time.sleep(max(0, seconds_per_frame + current_instant - time.time()))
        self.gui.close() # TODO: Maybe this should not be here


    def stop(self):
        self.running = False