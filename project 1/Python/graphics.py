from multiprocessing import Event
from tkinter import EventType
import pygame

class Action:
    QUIT = 0
    ENTER = 1
    ESC = 2
    MOUSE_DOWN = 3
    UP = 4
    DOWN = 5
    LEFT = 6
    RIGHT = 7

class PygameGUI:
    input_key_map = {
        pygame.K_RETURN: Action.ENTER,
        pygame.K_ESCAPE: Action.ESC,
        pygame.K_UP: Action.UP,
        pygame.K_DOWN: Action.DOWN,
        pygame.K_LEFT: Action.LEFT,
        pygame.K_RIGHT: Action.RIGHT
        # TODO: ADD WASD?
    }

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
    
    def get_actions(self):
        actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append(Action.QUIT)
            elif event.type == pygame.KEYDOWN:
                action = PygameGUI.input_key_map.get(event.key, None)
                if action != None:
                    actions.append(action)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                actions.append(Action.MOUSE_DOWN)
        return actions
    
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
        self.screen.fill((0, 0, 0))

    def refresh(self):
        pygame.display.update()

    def close(self):
        pygame.quit()