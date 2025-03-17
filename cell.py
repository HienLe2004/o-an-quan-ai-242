from setting import *
import random
from arrow_cell import *
import math

class Cell:
    hovered_color = (200, 0, 0)
    selected_color = (100, 0, 0)
    quan_image = pygame.image.load('images/quan.png')
    dan_image = pygame.image.load('images/dan.png')
    def __init__(self, game, number, position=(0, 0), size=(50, 50),value=5,bigValue=0):
        self.size = size
        self.game = game
        self.screen = game.screen
        self.number = number
        self.position = position
        self.cell_surf = pygame.Surface(self.size)
        self.cell_rect = self.cell_surf.get_frect(center=self.position)
        self.is_hovered = False
        self.is_selected = False
        self.arrow_cells = []
        if (number >= 1 and number <= 5):
            self.arrow_cells = [Arrow_Cell(game,True,(position[0]+size[0]*0.4,position[1]+size[1]*0.8),(size[0]*0.3,size[1]*0.3)),
                                Arrow_Cell(game,False,(position[0]-size[0]*0.4,position[1]+size[1]*0.8),(size[0]*0.3,size[1]*0.3))]        
        elif (number >= 7):
            self.arrow_cells = [Arrow_Cell(game,True,(position[0]+size[0]*0.4,position[1]-size[1]*0.8),(size[0]*0.3,size[1]*0.3)),
                                Arrow_Cell(game,False,(position[0]-size[0]*0.4,position[1]-size[1]*0.8),(size[0]*0.3,size[1]*0.3))]
        self.bigAngle = []
        self.angles = []
        self.positions = []
        positions = []
        #39 slots = 1 + 8 + 12 + 18
        if (number != 0 and number != 6):
            positions = [position]
            radius = 0.2
            n = 8
            positions += [(position[0]+size[0]*radius*math.cos(a*2*math.pi/n),position[1]+size[1]*radius*math.sin(a*2*math.pi/n))
                        for a in range(n)]
            radius = 0.3
            n = 12
            positions += [(position[0]+size[0]*radius*math.cos(a*2*math.pi/n),position[1]+size[1]*radius*math.sin(a*2*math.pi/n))
                        for a in range(n)]
            radius = 0.45
            n = 18
            positions += [(position[0]+size[0]*radius*math.cos(a*2*math.pi/n),position[1]+size[1]*radius*math.sin(a*2*math.pi/n))
                        for a in range(n)]
        #32 slot = 1 + 5 + 13 + 13
        elif (number == 0):
            positions = [(position[0]+size[0]*0.25,position[1])]
            radius = 0.4
            n = 5
            positions += [(positions[0][0]+size[0]*radius*math.cos(a*math.pi/(n-1)+math.pi/2),positions[0][1]+size[1]*radius*math.sin(a*math.pi/(n-1)+math.pi/2))
                        for a in range(n)]
            radius = 0.6
            n = 13
            positions += [(positions[0][0]+size[0]*radius*math.cos(a*math.pi/(n-1)+math.pi/2),positions[0][1]+size[1]*radius*math.sin(a*math.pi/(n-1)+math.pi/2))
                        for a in range(n)]
            radius = 0.8
            n = 13
            positions += [(positions[0][0]+size[0]*radius*math.cos(a*math.pi/(n-1)+math.pi/2),positions[0][1]+size[1]*radius*math.sin(a*math.pi/(n-1)+math.pi/2))
                        for a in range(n)]
        else:
            positions = [(position[0]-size[0]*0.25,position[1])]
            radius = 0.4
            n = 5
            positions += [(positions[0][0]+size[0]*radius*math.cos(a*math.pi/(n-1)-math.pi/2),positions[0][1]+size[1]*radius*math.sin(a*math.pi/(n-1)-math.pi/2))
                        for a in range(n)]
            radius = 0.6
            n = 13
            positions += [(positions[0][0]+size[0]*radius*math.cos(a*math.pi/(n-1)-math.pi/2),positions[0][1]+size[1]*radius*math.sin(a*math.pi/(n-1)-math.pi/2))
                        for a in range(n)]
            radius = 0.8
            n = 13
            positions += [(positions[0][0]+size[0]*radius*math.cos(a*math.pi/(n-1)-math.pi/2),positions[0][1]+size[1]*radius*math.sin(a*math.pi/(n-1)-math.pi/2))
                        for a in range(n)]
            
        while len(positions) > 0:
            randomIndex = random.randint(0, len(positions) - 1)
            randomValue = positions.pop(0)
            self.positions.append(randomValue)
        if (bigValue != 0):
            self.bigAngle = [random.randint(-20,20) for _ in range(bigValue)]
        if (value != 0):
            self.angles = [random.randint(-20,20) for _ in range(value)]
    def select_cell(self):
        self.is_selected = True
    def deselect_cell(self):
        self.is_selected = False
    def update_dan(self, number):
        if len(self.angles) == number:
            return
        if len(self.angles) > number:
            # print("Lay dan")
            while (len(self.angles) > number):
                self.angles.pop()
        else:
            # print("Them dan")
            while (len(self.angles) < number):
                self.angles.append(random.randint(-20,20))
    def update_quan(self, number):
        if len(self.bigAngle) == number:
            return
        if len(self.bigAngle) > number:
            # print("Lay quan")
            self.bigAngle.pop()
        else:
            # print("Them quan")
            self.bigAngle.append(random.randint(-20,20))
    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_just_released()
        self.is_hovered = self.cell_rect.collidepoint(mouse_pos)
        if self.is_hovered:
            if mouse_buttons[0]:
                self.game.change_cell(self.number)

    def draw(self):
        if self.is_hovered:
            pygame.draw.circle(surface=self.screen, color=self.hovered_color, center=self.position, radius=self.size[0] * 0.3)
        if self.is_selected:
            pygame.draw.circle(surface=self.screen, color=self.selected_color, center=self.position, radius=self.size[0] * 0.3)
            for a in self.arrow_cells:
                a.draw()
        if (self.number != 0 and self.number != 6):
            for i in range(len(self.angles)-1,-1,-1):
                rotated_image = pygame.transform.rotozoom(self.dan_image, self.angles[i], 0.1)
                dan_rect = rotated_image.get_frect(center=self.positions[i%len(self.positions)])
                self.screen.blit(rotated_image, dan_rect)
        else:
            for i in range(len(self.angles)-1,-1,-1):
                rotated_image = pygame.transform.rotozoom(self.dan_image, self.angles[i], 0.1)
                dan_rect = rotated_image.get_frect(center=self.positions[i%(len(self.positions)-1)+1])
                self.screen.blit(rotated_image, dan_rect)
        if (len(self.bigAngle)>0):
            rotated_image = pygame.transform.rotozoom(self.quan_image, self.bigAngle[0], 0.1)
            quan_rect = rotated_image.get_frect(center=self.positions[0])
            self.screen.blit(rotated_image, quan_rect)

    def update(self):
        if (self.number == 0 or self.number == 6):
            return
        if (self.game.player1Turn and self.number > 5):
            return
        if (not self.game.player1Turn and self.number < 6):
            return
        self.input()
        if (self.is_selected):
            for a in self.arrow_cells:
                a.update()