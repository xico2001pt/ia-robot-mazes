import pygame
from graphics_consts import IMAGES_PATH, BLOCK_WIDTH

class Action:
    QUIT = 0
    ENTER = 1
    BACKSPACE = 2
    ESC = 3
    UP = 4
    DOWN = 5
    LEFT = 6
    RIGHT = 7

class PygameGUI:
    input_key_map = {
        pygame.K_RETURN: Action.ENTER,
        pygame.K_BACKSPACE: Action.BACKSPACE,
        pygame.K_ESCAPE: Action.ESC,
        pygame.K_UP: Action.UP,
        pygame.K_w: Action.UP,
        pygame.K_DOWN: Action.DOWN,
        pygame.K_s: Action.DOWN,
        pygame.K_LEFT: Action.LEFT,
        pygame.K_a: Action.LEFT,
        pygame.K_RIGHT: Action.RIGHT,
        pygame.K_d: Action.RIGHT,
        pygame.K_q: Action.QUIT
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = None
        self.images = dict()

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
    
    def draw_image(self, filename, position, width, height):
        image = self.images.get(filename, None)
        if image == None:
            image = pygame.image.load(f'{IMAGES_PATH}{filename}')
            self.images[filename] = image
        image = pygame.transform.scale(image, (width, height))
        self.screen.blit(image, position.to_tuple())

    def draw_text(self, text, position, color, size):
        self.font = pygame.font.SysFont("monospace", size)
        label = self.font.render(text, True, color)
        self.screen.blit(label, position.to_tuple())
    
    def draw_centered_text(self, text, position, color, size):
        self.font = pygame.font.SysFont("monospace", size)
        width, height = self.font.size(text)
        centered_position = (position.x - width/2, position.y - height/2)
        label = self.font.render(text, True, color)
        self.screen.blit(label, centered_position)

    def draw_line(self, start_position, end_position, color, thickness=1):
        pygame.draw.line(
            self.screen,
            color,
            (start_position.x, start_position.y),
            (end_position.x, end_position.y),
            width=thickness
        )

    def draw_rectangle(self, position, width, height, color, thickness=0):
        pygame.draw.rect(
            self.screen, 
            color, 
            pygame.Rect(position.x, position.y, width, height), 
            thickness
        )
    
    def fill_screen(self, color):
        self.screen.fill(color)

    def clear(self):
        self.screen.fill((0, 0, 0))

    def refresh(self):
        pygame.display.update()

    def close(self):
        pass

    def get_surface(self):
        return self.screen

    def blit(self, surface, position=(0,0)):
        surf = surface.get_surface()
        self.screen.blit(surf, position)

class PygameScreenGUI(PygameGUI):
    def __init__(self, width, height):
        super().__init__(width, height)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((width, height))

    def close(self):
        pygame.font.quit()
        pygame.quit()

class PygameSurfaceGUI(PygameGUI):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.screen = pygame.Surface((width, height))