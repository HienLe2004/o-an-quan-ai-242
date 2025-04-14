from setting import *
import asyncio
class Arrow_Cell:
    arrow_image = pygame.image.load('images/arrow.png')
    hovered_color = (50, 30, 0)
    def __init__(self, game, is_right, position=(0, 0), size=(50,50)):
        self.game = game
        self.screen = game.screen
        self.position = position
        self.is_right = is_right
        self.size = size
        self.cell_surf = pygame.Surface(self.size)
        self.cell_rect = self.cell_surf.get_frect(center=self.position)
        self.is_hovered = False
        self.is_selected = False
    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_just_released()
        self.is_hovered = self.cell_rect.collidepoint(mouse_pos)
        if self.is_hovered:
            if mouse_buttons[0]:
                self.game.play(self.is_right)

    def select_cell(self):
        self.is_selected = True
    def deselect_cell(self):
        self.is_selected = False
    def draw(self):
        if self.is_hovered or self.is_selected:
            edges = []
            if self.is_right:
                edges = [(self.position[0]-self.size[0]*0.6,self.position[1]-self.size[1]*0.25),
                         (self.position[0]-self.size[0]*0.6,self.position[1]+self.size[1]*0.25),
                         (self.position[0]-self.size[0]*0.05,self.position[1]+self.size[1]*0.25),
                         (self.position[0]-self.size[0]*0.05,self.position[1]+self.size[1]*0.6),
                         (self.position[0]+self.size[0]*0.7,self.position[1]),
                         (self.position[0]-self.size[0]*0.05,self.position[1]-self.size[1]*0.6),
                         (self.position[0]-self.size[0]*0.05,self.position[1]-self.size[1]*0.25)]
            else:
                edges = [(self.position[0]+self.size[0]*0.6,self.position[1]-self.size[1]*0.25),
                         (self.position[0]+self.size[0]*0.6,self.position[1]+self.size[1]*0.25),
                         (self.position[0]+self.size[0]*0.05,self.position[1]+self.size[1]*0.25),
                         (self.position[0]+self.size[0]*0.05,self.position[1]+self.size[1]*0.6),
                         (self.position[0]-self.size[0]*0.7,self.position[1]),
                         (self.position[0]+self.size[0]*0.05,self.position[1]-self.size[1]*0.6),
                         (self.position[0]+self.size[0]*0.05,self.position[1]-self.size[1]*0.25)]
            pygame.draw.polygon(surface=self.screen, color=self.hovered_color, points=edges)
            # pygame.draw.circle(surface=self.screen, color=self.hovered_color, center=self.position, radius=self.size[0])
        rotated_image = pygame.transform.rotozoom(self.arrow_image, 0, 0.1)
        if not self.is_right:
            rotated_image = pygame.transform.rotozoom(self.arrow_image, 180, 0.1)
        dan_rect = rotated_image.get_frect(center=self.position)
        self.screen.blit(rotated_image, dan_rect)

    def update(self):
        self.input()