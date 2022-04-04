import time
from model import Position

class GameLoop:
    def __init__(self, fps, gui):
        self.fps = fps
        self.gui = gui
        self.running = False
    
    def run(self):
        if self.running:    return
        
        self.running = True
        seconds_per_frame = 1 / self.fps 
        last_instant = time.time()
        x = 0
        while self.running:
            current_instant = time.time()
            elapsed_time = current_instant - last_instant

            print("Frame")
            self.gui.clear()
            self.gui.draw_rectangle(Position(10+x, 10), 50, 50, (0, 255, 0))
            x += 1
            self.gui.refresh()


            last_instant = current_instant
            time.sleep(max(0, seconds_per_frame + current_instant - time.time()))
        self.gui.close()


    def stop(self):
        pass