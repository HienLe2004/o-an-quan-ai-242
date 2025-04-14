from setting import *
import pygame_gui
from cell import *
from point_cell import *
import Ai
import asyncio
class Game:
    QUAN_COEFFICIENT:int = 5
    DAN_LIMIT:int = 0
    def __init__(self):
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Ô ăn quan')
        self.clock = pygame.time.Clock()
        self.dan_count:list = [0,5,5,5,5,5,0,5,5,5,5,5]
        self.quan_count:list = [1,1]
        self.point_count:list = [[0,0],[0,0]]
        self.player1_turn:bool = False
        self.player1_ai:int = -1
        self.player2_ai:int = -1
        self.win_player:int = 0
        self.selected_cell = -1
        self.ai_is_playing: bool = False
        self.cells = [Cell(self, 0, (95,320), (70,70), self.dan_count[0], self.quan_count[0])]
        self.cells = self.cells + [Cell(self, i+1, (170+75*i,357.5), (70,70), self.dan_count[i+1]) for i in range(5)]
        self.cells = self.cells + [Cell(self, 6, (545,320), (70,70), self.dan_count[6], self.quan_count[1])]
        self.cells = self.cells + [Cell(self, i+7, (170+75*(4-i),282.5), (70,70), self.dan_count[i+7]) for i in range(5)]
        self.point_cells = [Point_Cell(self, 1, (120, 520), (70,70), 0, 0),
                            Point_Cell(self, 2, (520, 120), (70,70), 0, 0)]

        self.background_image = pygame.image.load('images/oanquan.jpeg')
        self.background_rect = self.background_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.manager.get_theme().load_theme('themes/game_theme.json')
        reset_btn_surf = pygame.Surface((100,50))
        reset_btn_rect = reset_btn_surf.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT)).move(-10,-10)
        self.reset_button = pygame_gui.elements.UIButton(relative_rect=reset_btn_rect, text="Reset", 
                                                       manager=self.manager,
                                                       object_id="#reset_btn")
        p1_options_surf = pygame.Surface((150,50))
        p1_options_rect = p1_options_surf.get_rect(center=(320, 520))
        self.p1_options = pygame_gui.elements.UIDropDownMenu(options_list=['Human','AI-0','AI-4','AI-5','AI-6'], 
                                                                starting_option='Human',
                                                                relative_rect=p1_options_rect,
                                                                manager=self.manager,
                                                                object_id="#p1_options")
        
        p2_options_surf = pygame.Surface((150,50))
        p2_options_rect = p2_options_surf.get_rect(center=(320, 120))
        self.p2_options = pygame_gui.elements.UIDropDownMenu(options_list=['Human','AI-0','AI-4','AI-5','AI-6'], 
                                                                starting_option='Human',
                                                                relative_rect=p2_options_rect,
                                                                manager=self.manager,
                                                                object_id="#p2_options")
    def change_cell(self, number):
        if self.cells[number].is_selected:
            #deselect
            self.cells[number].deselect_cell()
            self.selected_cell=-1
        else:
            #select
            self.cells[number].select_cell()
            if self.selected_cell != -1:
                self.cells[self.selected_cell].deselect_cell()
            self.selected_cell = number

    def play(self, is_right):
        is_clockwise = True
        if self.selected_cell <= 6 and is_right:
            is_clockwise = False
        elif self.selected_cell > 6 and not is_right:
            is_clockwise = False
        self.move(self.dan_count, self.selected_cell, is_clockwise)
        self.cells[self.selected_cell].deselect_cell()
        if (is_right):
            self.cells[self.selected_cell].arrow_cells[1].deselect_cell()
        else:
            self.cells[self.selected_cell].arrow_cells[0].deselect_cell()
        self.selected_cell = -1
        self.player1_turn = not self.player1_turn
        self.check_ending()
        self.check_all_empty_cells()
        for i in range(12):
            self.cells[i].update_dan(self.dan_count[i])
            if i == 0 or i == 6:
                self.cells[i].update_quan(self.quan_count[i%5])
        for i in range(2):
            self.point_cells[i].update_dan(self.point_count[i][0])
            self.point_cells[i].update_quan(self.point_count[i][1])
        

    def check_all_empty_cells(self):
        if self.win_player == 0:
            if self.player1_turn:
                all_cells_is_empty = True
                for i in range(1,6):
                    if self.dan_count[i] != 0:
                        all_cells_is_empty = False
                        break
                if all_cells_is_empty:
                    self.point_count[0][0] -= 5
                    for i in range(1,6):
                        self.dan_count[i] = 1
            else:
                all_cells_is_empty = True
                for i in range(7,12):
                    if self.dan_count[i] != 0:
                        all_cells_is_empty = False
                        break
                if all_cells_is_empty:
                    self.point_count[1][0] -= 5
                    for i in range(7,12):
                        self.dan_count[i] = 1


    def check_ending(self):
        if self.quan_count[0] == 0 and self.quan_count[1] == 0:
            for i in range(6):
                self.point_count[0][0] += self.dan_count[i]
                self.dan_count[i] = 0
                self.point_count[1][0] += self.dan_count[i+6]
                self.dan_count[i+6] = 0
            player1_point = self.point_count[0][0] + self.point_count[0][1] * self.QUAN_COEFFICIENT
            player2_point = self.point_count[1][0] + self.point_count[1][1] * self.QUAN_COEFFICIENT
            if (player1_point > player2_point):
                self.win_player = 1
            elif (player1_point < player2_point):
                self.win_player = 2
            else:
                self.win_player = 3

    def move(self, dan_count, index, is_clockwise):
        print(f"index: {index}, is_clockwise: {is_clockwise}")
        if index < 0 or index > 11 or index == 0 or index == 6:
            return
        if dan_count[index] == 0:
            return 
        pieces_on_hand = dan_count[index]
        dan_count[index] = 0
        step = 1
        if is_clockwise:
            step = -1
        current_index = index

        while pieces_on_hand != 0:
            current_index = clamp(current_index + step)
            dan_count[current_index] += 1
            pieces_on_hand -= 1

        current_index = clamp(current_index + step)
        #Not empty and not O_QUAN -> new Move
        if (dan_count[current_index] != 0 and current_index != 0 and current_index != 6):
            self.move(dan_count, current_index, is_clockwise)
            return
        #Empty and next square is not empty -> get Points
        while (dan_count[current_index] == 0 and dan_count[clamp(current_index + step)] != 0):
            #Quan_cells must have at least 5 dan to get Points
            if (clamp(current_index + step) in [0,6] 
                and (self.quan_count[clamp(current_index + step)%5] != 0 and dan_count[clamp(current_index + step)] < Game.DAN_LIMIT)):
                pass
            else:
                points = [dan_count[clamp(current_index + step)],0]
                if (clamp(current_index + step) in [0,6]):
                    points[1] += self.quan_count[(clamp(current_index + step)%5)]
                    self.quan_count[(clamp(current_index + step)%5)] = 0
                if self.player1_turn:
                    self.point_count[0][0] += points[0]
                    self.point_count[0][1] += points[1]
                else:
                    self.point_count[1][0] += points[0]
                    self.point_count[1][1] += points[1]
                print(f"Get {dan_count[clamp(current_index + step)]} quan at index {clamp(current_index + step)}")
                dan_count[clamp(current_index + step)] = 0
            current_index = clamp(current_index + 2 * step)

    async def ai_play(self, is_right):
        await asyncio.sleep(1)
        self.play(is_right)
        self.ai_is_playing = False

    async def handle_AI(self):
        if self.ai_is_playing:
            return
        self.ai_is_playing = True
        if self.player1_turn:
            print("AI player 1 turn")
            if (self.player1_ai == 0):
                position,direction = Ai.player_random_move(board=self.dan_count)
                self.selected_cell = position
                self.cells[self.selected_cell].select_cell()
                if (direction == 1):
                    self.cells[self.selected_cell].arrow_cells[1].select_cell()
                else:
                    self.cells[self.selected_cell].arrow_cells[0].select_cell()
                asyncio.create_task(self.ai_play(direction > 0))
            else:
                new_board, new_quan_count, new_point, position, direction = Ai.player(board=self.dan_count, 
                                   quan_count=self.quan_count, 
                                   point_count=[self.point_count[0][1]+Game.QUAN_COEFFICIENT+self.point_count[0][0],
                                                self.point_count[1][1]+Game.QUAN_COEFFICIENT+self.point_count[1][0]], 
                                   depth=self.player1_ai)
                self.selected_cell = position
                self.cells[self.selected_cell].select_cell()
                if (direction == 1):
                    self.cells[self.selected_cell].arrow_cells[1].select_cell()
                else:
                    self.cells[self.selected_cell].arrow_cells[0].select_cell()
                asyncio.create_task(self.ai_play(direction > 0))
        else:
            print("AI player 2 turn")
            if (self.player2_ai == 0):
                #Make random move
                position,direction = Ai.opponent_random_move(board=self.dan_count)
                self.selected_cell = position
                self.cells[self.selected_cell].select_cell()
                if (direction == 1):
                    self.cells[self.selected_cell].arrow_cells[1].select_cell()
                else:
                    self.cells[self.selected_cell].arrow_cells[0].select_cell()
                asyncio.create_task(self.ai_play(direction > 0))
            else:
                new_board, new_quan_count, new_point, position, direction = Ai.opponent(board=self.dan_count, 
                                   quan_count=self.quan_count, 
                                   point_count=[self.point_count[0][1]+Game.QUAN_COEFFICIENT+self.point_count[0][0],
                                                self.point_count[1][1]+Game.QUAN_COEFFICIENT+self.point_count[1][0]], 
                                   depth=self.player2_ai)
                self.selected_cell = position
                self.cells[self.selected_cell].select_cell()
                if (direction == -1):
                    self.cells[self.selected_cell].arrow_cells[1].select_cell()
                else:
                    self.cells[self.selected_cell].arrow_cells[0].select_cell()
                asyncio.create_task(self.ai_play(direction < 0))

    def reset(self):
        self.dan_count:list = [0,5,5,5,5,5,0,5,5,5,5,5]
        self.quan_count:list = [1,1]
        self.point_count:list = [[0,0],[0,0]]
        self.player1_turn:bool = True
        self.win_player:int = 0
        self.selected_cell = -1
        for i in range(12):
            self.cells[i].update_dan(self.dan_count[i])
            if i == 0 or i == 6:
                self.cells[i].update_quan(self.quan_count[i%5])
        for i in range(2):
            self.point_cells[i].update_dan(self.point_count[i][0])
            self.point_cells[i].update_quan(self.point_count[i][1])

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.reset_button:
                    self.reset()
                    print("~Reset game")
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.p1_options:
                    if event.text == 'Human':
                        self.player1_ai = -1
                    else:
                        self.player1_ai = int(event.text[-1])
                    print("~Selected P1 option:", self.player1_ai)
                elif event.ui_element == self.p2_options:
                    if event.text == 'Human':
                        self.player2_ai = -1
                    else:
                        self.player2_ai = int(event.text[-1])
                    print("~Selected P2 option:", self.player2_ai)

    def draw(self):
        self.screen.blit(self.background_image, self.background_rect)
        for cell in self.cells:
            cell.draw()
        if self.player1_turn:
            pygame.draw.circle(surface=self.screen, color=(200,200,0), center=(120,520), radius=60, width=5)
        else:
            pygame.draw.circle(surface=self.screen, color=(200,200,0), center=(520,120), radius=60, width=5)
        for cell in self.point_cells:
            cell.draw()
        font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 32)
        text_1 = font.render("Player1", True, (0,0,0))
        text_rect_1 = text_1.get_frect(midtop=(120, 520)).move(0,60)
        self.screen.blit(text_1, text_rect_1)
        text_1_point = font.render(str(self.point_count[0][0]+self.point_count[0][1]*self.QUAN_COEFFICIENT), True, (0,0,0))
        text_rect_1_point = text_1_point.get_frect(midright=(120, 520)).move(-70,0)
        self.screen.blit(text_1_point, text_rect_1_point)
        text_2 = font.render("Player2", True, (0,0,0))
        text_rect_2 = text_2.get_frect(midbottom=(520,120)).move(0,-60)
        self.screen.blit(text_2, text_rect_2)
        text_2_point = font.render(str(self.point_count[1][0]+self.point_count[1][1]*self.QUAN_COEFFICIENT), True, (0,0,0))
        text_rect_2_point = text_2_point.get_frect(midleft=(520, 120)).move(70,0)
        self.screen.blit(text_2_point, text_rect_2_point)

        if self.win_player == 1:
            text_1_result= font.render("WIN", True, (255,255,0))
            text_rect_1_result = text_1_result.get_frect(midbottom=(120, 520)).move(0,-80)
            self.screen.blit(text_1_result, text_rect_1_result)
        elif self.win_player == 2:
            text_2_result= font.render("WIN", True, (255,255,0))
            text_rect_2_result = text_2_result.get_frect(midtop=(520, 120)).move(0,80)
            self.screen.blit(text_2_result, text_rect_2_result)
        elif self.win_player == 3:
            text_1_result= font.render("TIE", True, (50,50,50))
            text_rect_1_result = text_1_result.get_frect(midbottom=(120, 520)).move(0,-80)
            self.screen.blit(text_1_result, text_rect_1_result)
            text_2_result= font.render("TIE", True, (50,50,50))
            text_rect_2_result = text_2_result.get_frect(midtop=(520, 120)).move(0,80)
            self.screen.blit(text_2_result, text_rect_2_result)


    def update(self):
        for cell in self.cells:
            cell.update()
        self.input()
    
    async def late_update(self):
        if self.win_player != 0:
            return
        if ((self.player1_ai != -1 and self.player1_turn) or (self.player2_ai != -1 and not self.player1_turn)):
            await self.handle_AI()

    async def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.update()
            self.draw()
            self.manager.update(dt)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
            await self.late_update()
            await asyncio.sleep(0)
        pygame.quit()

def clamp(value):
    while value < 0:
        value += 12
    while value > 11:
        value -= 12
    return value