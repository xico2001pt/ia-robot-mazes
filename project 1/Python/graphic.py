import pygame

class GUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.init()
        pygame.font.init()

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    #def draw_image()

    #def draw_text()
    #def draw rectangle()
    def draw_rectangle(self, position, width, height, color, thickness=0):
        pygame.draw.rect(
            self.screen, 
            color, 
            pygame.Rect(position.x, position.y, width, height), 
            thickness
        )

    def clear(self):
        pygame.event.pump() # TODO: ONLY FOR TESTING PURPOSES
        self.screen.fill((0, 0, 0))

    def refresh(self):
        pygame.display.update()

    def close(self):
        pygame.quit()