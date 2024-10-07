# 8x8 chess board with 4 queens starting at all four corners
# queens take turns choosing a new position to move to (by clicking)
import pygame
import pandas as pd
import numpy as np
queen_figure = '♛'

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        # x = rect.left
        x = rect[0] + (rect[2] - image.get_width()) // 2
        surface.blit(image, (x, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

class Queen(pygame.sprite.Sprite):
    def __init__(self, i, j, color, size, board):
        super().__init__()
        self.i = i
        self.j = j
        self.align = "left"
        self.color = color
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
                    if event_i >= 0 and event_i < self.board.board_size and event_j >= 0 and event_j < self.board.board_size and (event_i == queen_i or event_j == queen_j or event_i-event_j == queen_i-queen_j or event_i+event_j == queen_i+queen_j):
                        # check if there is a queen at the new position in the left alignment
                        found_left = False
                        found_right = False
                        for queen in queens:
                            if queen.i == event_i and queen.j == event_j:
                                if queen.align == "left":
                                    found_left = True
                                if queen.align == "right":
                                    found_right = True
                        if found_left and found_right:
                            self.board.next_turn = self.board.current_turn
                        else:
                            if found_left:
                                self.align = "right"
                            if found_right:
                                self.align = "left"
                            self.i = event_i
                            self.j = event_j
                            self.set_pos()
                            self.board.next_turn = (self.board.current_turn + 1) % num_queens
                            # make all squares which are legal moves for the current queen green
                            self.board.show_legal_moves(self.board.next_turn)
                            self.board.question_visible = False
                            self.board.show_question()
                    else:
                        self.board.next_turn = self.board.current_turn
                    

class Board:
    def __init__(self, board_size, questions):
        self.board_size = board_size
        self.board = pygame.Surface(window.get_size())
        self.board.fill((255, 255, 255))
        self.current_turn = 0
        self.next_turn = 0
        self.size = (min(window.get_size()) - 20) // board_size
        self.window_size = window.get_size()
        # self.start = (window.get_width() - self.size * board_size) // 2, (window.get_height() - self.size * board_size) // 2
        self.start = (window.get_height() - self.size * board_size) // 2, (window.get_height() - self.size * board_size) // 2
        self.board_rect = pygame.Rect(*self.start, self.size*board_size, self.size*board_size)
        # create a board_size x board_size array of questions
        # questions is a pandas array, get the first board_size x board_size questions and reshape them into a board_size x board_size array
        self.questions = questions.iloc[:board_size*board_size]
        self.question_visible = False

    def reset_board(self):
        # ts, w, h, c1, c2 = 50, *window.get_size(), (128, 128, 128), (64, 64, 64)
        for y in range(self.board_size):
            for x in range(self.board_size):
                color = (192, 192, 164) if (x+y) % 2 == 0 else (96, 64, 32)
                pygame.draw.rect(self.board, color, (self.start[0]+ x*self.size, self.start[1] + y*self.size, self.size, self.size))
                
    def show_legal_moves(self, turn):
        self.reset_board()
        # make all squares which are legal moves for the current queen green
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i == queens[turn].i or j == queens[turn].j or i-j == queens[turn].i-queens[turn].j or i+j == queens[turn].i+queens[turn].j:
                    # delete the old rect and draw a new one
                    pygame.draw.rect(self.board, (50, 100, 50), (self.start[0]+ i*self.size, self.start[1] + (self.board_size-1-j)*self.size, self.size, self.size))
                # add question text (topic, difficulty) inside square
                row = self.questions.iloc[i*self.board_size+j]
                seguisy = pygame.font.SysFont("dejavusans", 28, bold=True)
                topic_text = seguisy.render(row['Topic'], True, pygame.Color('black'))
                difficulty_text = seguisy.render(row['Difficulty'], True, pygame.Color('black'))
                # horizontally center the text inside the square
                x = self.start[0] + i*self.size + self.size // 2 - topic_text.get_width() // 2
                y = self.start[1] + (self.board_size-1-j)*self.size + 30
                self.board.blit(topic_text, (x, y))
                x = self.start[0] + i*self.size + self.size // 2 - difficulty_text.get_width() // 2
                y = self.start[1] + (self.board_size-1-j)*self.size + 70
                self.board.blit(difficulty_text, (x, y))
        # add black grid lines
        for i in range(self.board_size+1):
            pygame.draw.line(self.board, (0, 0, 0), (self.start[0], self.start[1] + i*self.size), (self.start[0] + (self.board_size)*self.size, self.start[1] + i*self.size), 4)
            pygame.draw.line(self.board, (0, 0, 0), (self.start[0] + i*self.size, self.start[1]), (self.start[0] + i*self.size, self.start[1] + self.board_size*self.size), 4)
    def show_question(self):
        # reset the right side of the screen
        pygame.draw.rect(self.board, (255, 255, 255), (self.start[0] + self.board_size*self.size, self.start[1], self.window_size[0] - self.start[0] - self.board_size*self.size, self.board_size*self.size))
        # add question details (and name of current player) on right side of screen (outside of board)
        seguisy = pygame.font.SysFont("dejavusans", 112, bold=True)
        # center the text horizontally (use self.window_size) and add black border
        text = "Team " + queens[self.next_turn].color
        x = self.start[0] + self.board_size*self.size + (self.window_size[0] - self.start[0] - self.board_size*self.size) // 2 - seguisy.render(text, True, pygame.Color(queens[self.next_turn].color)).get_width() // 2
        y = self.start[1] + 30
        text = seguisy.render(text, True, pygame.Color(queens[self.next_turn].color))
        self.board.blit(text, (x, y))
        # add question details
        seguisy = pygame.font.SysFont("dejavusans", 48, bold=True)
        # center the text horizontally (use self.window_size) and add black border
        row = self.questions.iloc[queens[self.next_turn].i*self.board_size+queens[self.next_turn].j]
        text = row['Topic'] + " (" + row['Difficulty'] + ")"
        x = self.start[0] + self.board_size*self.size + (self.window_size[0] - self.start[0] - self.board_size*self.size) // 2 - seguisy.render(text, True, pygame.Color('black')).get_width() // 2
        y = self.start[1] + 200
        text = seguisy.render(text, True, pygame.Color('black'))
        self.board.blit(text, (x, y))
        if self.question_visible:
            # add question text
            seguisy = pygame.font.SysFont("dejavusans", 48, bold=True)
            # use drawText to wrap the text
            text = row['Question']
            drawText(self.board, text, pygame.Color('black'), (self.start[0] + self.board_size*self.size + 20, self.start[1] + 300, self.window_size[0] - self.start[0] - self.board_size*self.size - 40, self.board_size*self.size - 300), seguisy, aa=True, bkg=None)
        # # add the show question button - move to a different class
        # seguisy = pygame.font.SysFont("dejavusans", 48)
        # text = "Show Question"
        # x = self.start[0] + self.board_size*self.size + (self.window_size[0] - self.start[0] - self.board_size*self.size) // 2 - seguisy.render(text, True, pygame.Color('black')).get_width() // 2
        # y = self.start[1] + self.board_size*self.size - 100
        # text = seguisy.render(text, True, pygame.Color('black'))
        # self.board.blit(text, (x, y))
        # # add a button to show the question
        # pygame.draw.rect(self.board, (0, 0, 0), (x-20, y-10, text.get_width()+40, text.get_height()+20), 4)

# button with border which displays "Show Question"
class ShowQuestionButton(pygame.sprite.Sprite):
    def __init__(self, board, text):
        super().__init__()
        self.board = board
        seguisy = pygame.font.SysFont("dejavusans", 48)
        self.image = seguisy.render(text, True, pygame.Color('black'))
        self.rect = self.image.get_rect(center = (board.start[0] + board.board_size*board.size + (board.window_size[0] - board.start[0] - board.board_size*board.size) // 2, board.start[1] + board.board_size*board.size - 50))
        # pygame.draw.rect(board.board, (0, 0, 0), (self.rect.left-20, self.rect.top-10, self.image.get_width()+40, self.image.get_height()+20), 400)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.board.question_visible = not self.board.question_visible
                    self.board.show_question()



# load questions
questions = pd.read_csv('questions.csv')
# pygame setup
num_queens = 6
board_size = 6
# queen_size = 80
queen_size = 120
pygame.init()
# window = pygame.display.set_mode((100*board_size,100*board_size))
window = pygame.display.set_mode((2560,1440))
# set full screen
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

board = Board(board_size,questions)
queens = [Queen(1, 0, "red", queen_size, board),
          Queen(board_size-2, 0, "green", queen_size, board),
          Queen(1, board_size-1, "blue", queen_size, board),
          Queen(board_size-2, board_size-1, "yellow", queen_size, board),
          Queen(0, 2, "purple", queen_size, board),
          Queen(board_size-1, board_size-3, "orange", queen_size, board)]
group = pygame.sprite.Group()
group.add(queens)
group.add(ShowQuestionButton(board, "Show Question"))

board.show_legal_moves(board.current_turn)
board.show_question()

run = True
while run:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
    group.update(event_list)
    board.current_turn = board.next_turn

    window.blit(board.board, (0, 0))
    group.draw(window)
    pygame.display.flip()

pygame.quit()