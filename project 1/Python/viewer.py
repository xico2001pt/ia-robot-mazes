from model import Position

class Viewer:
    def __init__(self, model):
        self.model = model
    
    def get_model(self): # TODO: IS IT NECESSARY?
        return self.model
    
    def draw(self, gui):
        raise NotImplementedError()

class MainMenuViewer(Viewer):
    def draw(self, gui):
        gui.draw_rectangle(Position(10, 10+self.model.x), 50, 50, (0, 255, 0))
        gui.draw_text("Goodbye World!", Position(10+self.model.x, 10), (255, 0, 0))