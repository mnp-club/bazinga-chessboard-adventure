# 8x8 chess board with 4 queens starting at all four corners
# queens take turns choosing a new position to move to (by clicking)
import pygame
import pandas as pd
import matplotlib.pyplot as plt
queen_figure = '♛'
plt.rcParams['text.usetex'] = True
# change this to change the resolution
# dim = (2560,1440)
dim = (1920,1080)

class Queen(pygame.sprite.Sprite):
    def __init__(self, i, j, color, size, board, name):
        super().__init__()
        self.last_i = i
        self.i = i
        self.last_j = j
        self.j = j
        self.align = "left"
        self.color = color
        self.name = name
        seguisy = pygame.font.SysFont("dejavusans", size)
        self.image = seguisy.render(queen_figure, True, pygame.Color(color))
        self.board = board
        self.set_pos()

    def set_pos(self):
        x = self.board.board_rect.left + self.board.board_rect.width // self.board.board_size * self.i + self.board.board_rect.width // (self.board.board_size * 2) * [0.5,1.5][self.align == "right"]
        y = self.board.board_rect.left + self.board.board_rect.height // self.board.board_size * (self.board.board_size - 1 - self.j) + self.board.board_rect.height // (self.board.board_size * 2) * 1.5
        self.rect = self.image.get_rect(center = (x, y))

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.color == queens[self.board.current_turn].color:
                    # move to the point clicked
                    event_x, event_y = event.pos
                    event_i = (event_x - self.board.board_rect.left) // (self.board.board_rect.width // self.board.board_size)
                    event_j = self.board.board_size - 1 - (event_y - self.board.board_rect.top) // (self.board.board_rect.height // self.board.board_size)
                    queen_i = self.i
                    queen_j = self.j
                    if event_i >= 0 and event_i < self.board.board_size and event_j >= 0 and event_j < self.board.board_size and (event_i == queen_i or event_j == queen_j or event_i-event_j == queen_i-queen_j or event_i+event_j == queen_i+queen_j) and not self.board.move_chosen and not (event_i == queen_i and event_j == queen_j):
                        # check if there is a queen at the new position in the left alignment
                        found_left = False
                        found_right = False
                        for queen in queens:
                            if queen.i == event_i and queen.j == event_j:
                                if queen.align == "left":
                                    found_left = True
                                if queen.align == "right":
                                    found_right = True
                        if not (found_left and found_right):
                            if found_left:
                                self.align = "right"
                            if found_right:
                                self.align = "left"
                            self.last_i = self.i
                            self.last_j = self.j
                            self.i = event_i
                            self.j = event_j
                            self.board.move_chosen = True
                            self.set_pos()
                            # make all squares which are legal moves for the current queen green
                            self.board.show_legal_moves(self.board.current_turn)
                        
                    

class Board:
    def __init__(self, board_size, questions):
        self.board_size = board_size
        self.board = pygame.Surface(window.get_size())
        self.board.fill((255, 255, 255))
        self.current_turn = 0
        self.size = (min(window.get_size()) - 20) // board_size
        self.window_size = window.get_size()
        self.start = (window.get_height() - self.size * board_size) // 2, (window.get_height() - self.size * board_size) // 2
        self.board_rect = pygame.Rect(*self.start, self.size*board_size, self.size*board_size)
        self.questions = questions
        self.move_chosen = False
        self.board_state = 0 # 0: board visible, 1: question visible, 2: answer visible

    def reset_board(self):
        for y in range(self.board_size):
            for x in range(self.board_size):
                color = (192, 192, 164) if (x+y) % 2 == 0 else (96, 64, 32)
                pygame.draw.rect(self.board, color, (self.start[0]+ x*self.size, self.start[1] + y*self.size, self.size, self.size))
                
    def show_legal_moves(self, turn):
        self.reset_board()
        # make all squares which are legal moves for the current queen green
        pygame.draw.rect(self.board, (136, 134, 72), (self.start[0]+ queens[turn].i*self.size, self.start[1] + (self.board_size-1-queens[turn].j)*self.size, self.size, self.size))
        # calculate all squares with two queens
        queen_pos_list = [(queen.i, queen.j) for queen in queens]
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i == queens[turn].i or j == queens[turn].j or i-j == queens[turn].i-queens[turn].j or i+j == queens[turn].i+queens[turn].j) and not self.move_chosen and not (i == queens[turn].i and j == queens[turn].j) and queen_pos_list.count((i, j)) < 2:
                        # delete the old rect and draw a new one
                        pygame.draw.rect(self.board, (50, 100, 50), (self.start[0]+ i*self.size, self.start[1] + (self.board_size-1-j)*self.size, self.size, self.size))
                # add question text (topic, difficulty) inside square
                row = self.questions.iloc[questions_jumbled[i*self.board_size+j]]
                
                seguisy = pygame.font.SysFont("dejavusans", int(28*scale), bold = True)
                board_id_text = seguisy.render(str(i*self.board_size+j), True, pygame.Color('black'))
                if not self.questions.iloc[questions_jumbled[i*self.board_size+j]]['Solved']:
                    topic_text = seguisy.render(row['Topic'], True, pygame.Color('black'))
                    difficulty_text = seguisy.render(row['Difficulty'], True, pygame.Color('black'))
                else:
                    topic_text = seguisy.render("Solved", True, pygame.Color('black'))
                    difficulty_text = seguisy.render("", True, pygame.Color('black'))
                # horizontally center the text inside the square
                x = self.start[0] + i*self.size + self.size // 2 - board_id_text.get_width() // 2
                y = self.start[1] + (self.board_size-1-j)*self.size + 10
                self.board.blit(board_id_text, (x, y))
                x = self.start[0] + i*self.size + self.size // 2 - topic_text.get_width() // 2
                y = self.start[1] + (self.board_size-1-j)*self.size + 45
                self.board.blit(topic_text, (x, y))
                x = self.start[0] + i*self.size + self.size // 2 - difficulty_text.get_width() // 2
                y = self.start[1] + (self.board_size-1-j)*self.size + 80
                self.board.blit(difficulty_text, (x, y))
        # add black grid lines
        for i in range(self.board_size+1):
            pygame.draw.line(self.board, (0, 0, 0), (self.start[0], self.start[1] + i*self.size), (self.start[0] + (self.board_size)*self.size, self.start[1] + i*self.size), 4)
            pygame.draw.line(self.board, (0, 0, 0), (self.start[0] + i*self.size, self.start[1]), (self.start[0] + i*self.size, self.start[1] + self.board_size*self.size), 4)
        # add question details (and name of current player) on right side of screen (outside of board)
        seguisy = pygame.font.SysFont("dejavusans", int(80*scale), bold=True)
        # center the text horizontally (use self.window_size) and add black border
        color = queens[self.current_turn].color
        text = "Team " + queens[self.current_turn].name
        x = self.start[0] + self.board_size*self.size + (self.window_size[0] - self.start[0] - self.board_size*self.size) // 2 - seguisy.render(text, True, pygame.Color(color)).get_width() // 2
        y = self.start[1] + 30*scale
        # whitewash the area before writing the text
        pygame.draw.rect(self.board, (255, 255, 255), (x-60*scale, y-10*scale, seguisy.render(text, True, pygame.Color(color)).get_width()+120*scale, seguisy.render(text, True, pygame.Color(color)).get_height()+20*scale))
        text = seguisy.render(text, True, pygame.Color(color))
        self.board.blit(text, (x, y))

    def show_question(self):
        if self.board_state != 1:
            image = pygame.image.load(f"questions_{dim[1]}p/" + str(questions_jumbled[queens[self.current_turn].i*self.board_size+queens[self.current_turn].j]) + ".png")
            # scale image to down if its bigger than board size
            if image.get_width() > self.size*self.board_size:
                image = pygame.transform.scale(image, (self.size*self.board_size, int(image.get_height() * self.size*self.board_size / image.get_width())))
            if image.get_height() > self.size*self.board_size:
                image = pygame.transform.scale(image, (int(image.get_width() * self.size*self.board_size / image.get_height()), self.size*self.board_size))
            # scale image to board without changing aspect ratio
            # image = pygame.transform.scale(image, (self.size*self.board_size, self.size*self.board_size))
            self.board.fill((255, 255, 255), (self.start[0], self.start[1], self.size*self.board_size, self.size*self.board_size))
            # center image on board
            self.board.blit(image, (self.start[0] + (self.size*self.board_size - image.get_width()) // 2, self.start[1] + (self.size*self.board_size - image.get_height()) // 2))
            # make the queens invisible
            for queen in queens:
                queen.image = pygame.Surface((0, 0))
            self.board_state = 1
        else:
            self.reset_board()
            self.show_legal_moves(self.current_turn)
            # make the queens visible again
            seguisy = pygame.font.SysFont("dejavusans", queen_size)
            for queen in queens:
                queen.image = seguisy.render(queen_figure, True, pygame.Color(queen.color))
            self.board_state = 0
    
    def show_answer(self):
        if self.board_state != 2:
            self.questions.loc[questions_jumbled[queens[self.current_turn].i*self.board_size+queens[self.current_turn].j], "Solved"] = True
            image = pygame.image.load(f"answers_{dim[1]}p/" + str(questions_jumbled[queens[self.current_turn].i*self.board_size+queens[self.current_turn].j]) + ".png")
            # scale image  to down if its bigger than board size
            if image.get_width() > self.size*self.board_size:
                image = pygame.transform.scale(image, (self.size*self.board_size, int(image.get_height() * self.size*self.board_size / image.get_width())))
            if image.get_height() > self.size*self.board_size:
                image = pygame.transform.scale(image, (int(image.get_width() * self.size*self.board_size / image.get_height()), self.size*self.board_size))
            # image is transparent, so a white background is added
            # image = pygame.transform.scale(image, (self.size*self.board_size, self.size*self.board_size))
            self.board.fill((255, 255, 255), (self.start[0], self.start[1], self.size*self.board_size, self.size*self.board_size))
            # center image on board
            self.board.blit(image, (self.start[0] + (self.size*self.board_size - image.get_width()) // 2, self.start[1] + (self.size*self.board_size - image.get_height()) // 2))
            # make the queens invisible
            for queen in queens:
                queen.image = pygame.Surface((0, 0))
            self.board_state = 2
        else:
            self.reset_board()
            self.show_legal_moves(self.current_turn)
            # make the queens visible again
            seguisy = pygame.font.SysFont("dejavusans", queen_size)
            for queen in queens:
                queen.image = seguisy.render(queen_figure, True, pygame.Color(queen.color))
            self.board_state = 0


# button with border which displays "Show Question"
class ShowQuestionButton(pygame.sprite.Sprite):
    def __init__(self, board, text):
        super().__init__()
        self.board = board
        seguisy = pygame.font.SysFont("dejavusans", int(72*scale))
        self.image = seguisy.render(text, True, pygame.Color('black'))
        self.rect = self.image.get_rect(center = (board.start[0] + board.board_size*board.size + (board.window_size[0] - board.start[0] - board.board_size*board.size) // 2, board.start[1] + board.board_size*board.size*0.25))
        pygame.draw.rect(board.board, (0, 0, 0), (self.rect.left-20, self.rect.top-10, self.image.get_width()+40, self.image.get_height()+20), 4)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and self.board.move_chosen:
                    self.board.show_question()

class ShowAnswerButton(pygame.sprite.Sprite):
    def __init__(self, board, text):
        super().__init__()
        self.board = board
        seguisy = pygame.font.SysFont("dejavusans", int(72*scale))
        self.image = seguisy.render(text, True, pygame.Color('black'))
        self.rect = self.image.get_rect(center = (board.start[0] + board.board_size*board.size + (board.window_size[0] - board.start[0] - board.board_size*board.size) // 2, board.start[1] + board.board_size*board.size*0.45))
        pygame.draw.rect(board.board, (0, 0, 0), (self.rect.left-20, self.rect.top-10, self.image.get_width()+40, self.image.get_height()+20), 4)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and self.board.move_chosen:
                    self.board.show_answer()

class NextButton(pygame.sprite.Sprite):
    def __init__(self, board, text):
        super().__init__()
        self.board = board
        seguisy = pygame.font.SysFont("dejavusans", int(72*scale))
        self.image = seguisy.render(text, True, pygame.Color('black'))
        self.rect = self.image.get_rect(center = (board.start[0] + board.board_size*board.size + (board.window_size[0] - board.start[0] - board.board_size*board.size) // 2, board.start[1] + board.board_size*board.size*0.65))
        pygame.draw.rect(board.board, (0, 0, 0), (self.rect.left-20, self.rect.top-10, self.image.get_width()+40, self.image.get_height()+20), 4)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and self.board.move_chosen and self.board.board_state == 0:
                    self.board.move_chosen = False
                    self.board.current_turn = (self.board.current_turn + 1) % num_queens
                    self.board.show_legal_moves(self.board.current_turn)

class UndoButton(pygame.sprite.Sprite):
    def __init__(self, board, text):
        super().__init__()
        self.board = board
        seguisy = pygame.font.SysFont("dejavusans", int(72*scale))
        self.image = seguisy.render(text, True, pygame.Color('black'))
        self.rect = self.image.get_rect(center = (board.start[0] + board.board_size*board.size + (board.window_size[0] - board.start[0] - board.board_size*board.size) // 2, board.start[1] + board.board_size*board.size*0.85))
        pygame.draw.rect(board.board, (0, 0, 0), (self.rect.left-20, self.rect.top-10, self.image.get_width()+40, self.image.get_height()+20), 4)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and self.board.move_chosen and self.board.board_state == 0:
                    self.board.move_chosen = False
                    queens[self.board.current_turn].i = queens[self.board.current_turn].last_i
                    queens[self.board.current_turn].j = queens[self.board.current_turn].last_j
                    queens[self.board.current_turn].set_pos()
                    self.board.show_legal_moves(self.board.current_turn)

# add a dict for jumbling the questions
questions_jumbled = [23, 10, 8, 2, 16, 20, 21, 9, 1, 18, 5, 22, 17, 14, 24, 19, 13, 7, 0, 12, 3, 4, 6, 15, 11]
# load questions, escape with \
questions = pd.read_csv("questions.csv", escapechar = "\\")
questions["Solved"] = False
scale = dim[1]/1440
# pygame setup
num_queens = 6
board_size = 5
queen_size = int(120*scale)
pygame.init()
# window = pygame.display.set_mode(dim)
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

board = Board(board_size,questions)
queens = [Queen(1, 0, "red", queen_size, board, "Sophia"),
          Queen(board_size-2, 0, "green", queen_size, board, "Ada"),
          Queen(1, board_size-1, "blue", queen_size, board, "Emmy"),
          Queen(board_size-2, board_size-1, "gold", queen_size, board, "Julia"),
          Queen(0, 2, "purple", queen_size, board, "Dorothy"),
          Queen(board_size-1, board_size-3, "orange", queen_size, board, "Hypatia")]
group = pygame.sprite.Group()
group.add(queens)
group.add(ShowQuestionButton(board, "Show Question"))
group.add(ShowAnswerButton(board, "Show Answer"))
group.add(NextButton(board, "Next Question"))
group.add(UndoButton(board, "Undo Move"))

board.show_legal_moves(board.current_turn)

run = True
while run:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
    group.update(event_list)

    window.blit(board.board, (0, 0))
    group.draw(window)
    pygame.display.flip()

pygame.quit()
