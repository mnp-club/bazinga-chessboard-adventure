# 8x8 chess board with 4 queens starting at all four corners
# queens take turns choosing a new position to move to (by clicking)
import pygame
queen_figure = '♛'
class Queen(pygame.sprite.Sprite):
    def __init__(self, i, j, color, size, board):
        super().__init__()
        self.i = i
        self.j = j
        self.color = color
        seguisy = pygame.font.SysFont("dejavusans", size)
        self.image = seguisy.render(queen_figure, True, pygame.Color(color))
        self.board = board
        self.set_pos()

    def set_pos(self):
        x = self.board.board_rect.left + self.board.board_rect.width // self.board.board_size * self.i + self.board.board_rect.width // (self.board.board_size * 2)
        y = self.board.board_rect.left + self.board.board_rect.height // self.board.board_size * (self.board.board_size - 1 - self.j) + self.board.board_rect.height // (self.board.board_size * 2)
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
                        self.i = event_i
                        self.j = event_j
                        self.set_pos()
                        self.board.next_turn = (self.board.current_turn + 1) % num_queens
                        # make all squares which are legal moves for the current queen green
                        self.board.show_legal_moves(self.board.next_turn)
                    else:
                        self.board.next_turn = self.board.current_turn
                    

class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = pygame.Surface(window.get_size())
        self.board.fill((255, 255, 255))
        self.current_turn = 0
        self.next_turn = 0
        self.size = (min(window.get_size()) - 20) // board_size
        self.start = (window.get_width() - self.size * board_size) // 2, (window.get_height() - self.size * board_size) // 2
        self.board_rect = pygame.Rect(*self.start, self.size*board_size, self.size*board_size)
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
        # add black grid lines
        for i in range(self.board_size+1):
            pygame.draw.line(self.board, (0, 0, 0), (self.start[0], self.start[1] + i*self.size), (self.start[0] + (self.board_size)*self.size, self.start[1] + i*self.size), 4)
            pygame.draw.line(self.board, (0, 0, 0), (self.start[0] + i*self.size, self.start[1]), (self.start[0] + i*self.size, self.start[1] + self.board_size*self.size), 4)

# pygame setup
num_queens = 6
board_size = 6
pygame.init()
window = pygame.display.set_mode((100*board_size,100*board_size))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

board = Board(board_size)
queens = [Queen(1, 0, "red", 80, board),
          Queen(board_size-2, 0, "green", 80, board),
          Queen(1, board_size-1, "blue", 80, board),
          Queen(board_size-2, board_size-1, "yellow", 80, board),
          Queen(0, 2, "purple", 80, board),
          Queen(board_size-1, board_size-3, "orange", 80, board)]

group = pygame.sprite.Group()
group.add(queens)

board.show_legal_moves(board.current_turn)

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