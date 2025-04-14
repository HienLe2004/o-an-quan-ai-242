from setting import *
import random
import math

class Point_Cell:
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
        self.bigAngles = []
        self.angles = []
        self.positions = []
        #36 slots
        positions = [(position[0]-size[0]*0.2,position[1]),(position[0]+size[0]*0.2,position[1])]
        radius = 0.5
        n = 16
        positions += [(position[0]+size[0]*radius*math.cos(a*2*math.pi/n),position[1]+size[1]*radius*math.sin(a*2*math.pi/n))
                    for a in range(n)]
        radius = 0.7
        n = 24
        positions += [(position[0]+size[0]*radius*math.cos(a*2*math.pi/n),position[1]+size[1]*radius*math.sin(a*2*math.pi/n))
                    for a in range(n)]
        while len(positions) > 0:
            # randomIndex = random.randint(0, len(positions) - 1)
            randomValue = positions.pop(0)
            self.positions.append(randomValue)
        if (bigValue != 0):
            self.bigAngles = [random.randint(-20,20) for _ in range(bigValue)]
        if (value != 0):
            self.angles = [random.randint(-20,20) for _ in range(value)]
    def update_dan(self, number):
        if number < 0:
            number = 0
        if len(self.angles) == number:
            return
        #Lay dan
        while (len(self.angles) > number):
            self.angles.pop()
        #Them dan
        while (len(self.angles) < number):
            self.angles.append(random.randint(-20,20))
    def update_quan(self, number):
        if len(self.bigAngles) == number:
            return
        #Lay quan
        while len(self.bigAngles) > number:
            self.bigAngles.pop()
        #Them quan
        while len(self.bigAngles) < number:
            self.bigAngles.append(random.randint(-20,20))

    def draw(self):
        if self.is_hovered:
            pygame.draw.circle(surface=self.screen, color=self.hovered_color, center=self.position, radius=self.size[0] * 0.3)
        if self.is_selected:
            pygame.draw.circle(surface=self.screen, color=self.selected_color, center=self.position, radius=self.size[0] * 0.3)
            for a in self.arrow_cells:
                a.draw()
        for i in range(len(self.angles)):
            rotated_image = pygame.transform.rotozoom(self.dan_image, self.angles[i], 0.1)
            dan_rect = rotated_image.get_frect(center=self.positions[(i+2)%len(self.positions)])
            self.screen.blit(rotated_image, dan_rect)
        for i in range(len(self.bigAngles)):
            rotated_image = pygame.transform.rotozoom(self.quan_image, self.bigAngles[0], 0.1)
            quan_rect = rotated_image.get_frect(center=self.positions[i])
            self.screen.blit(rotated_image, quan_rect)