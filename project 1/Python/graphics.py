from multiprocessing import Event
from tkinter import EventType
import pygame

class Action:
    QUIT = 0
    ENTER = 1
    ESC = 2
    UP = 3
    DOWN = 4
    LEFT = 5
    RIGHT = 6

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
        pygame.init()
        pygame.font.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("monospace", 15)

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
        return actions
    
    #def draw_image()

    def draw_text(self, text, position, color):
        label = self.font.render(text, True, color)
        self.screen.blit(label, position.to_tuple())

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
        pygame.font.quit()
        pygame.quit()