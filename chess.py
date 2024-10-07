import pygame
queen_figure = '♛'

class Queen(pygame.sprite.Sprite):
    def __init__(self, i, j, color, size, board):
        super().__init__()
        self.i = i
        self.j = j
        self.color = color
        self.size = size
        seguisy = pygame.font.SysFont("dejavusans", size)
        self.image = seguisy.render(queen_figure, True, pygame.Color(color))
        self.board = board
        self.set_pos()

    def set_pos(self):
        # Calculate the center position of the square the queen occupies
        square_width = self.board.size  # Width and height of each square
        square_height = self.board.size
        x = self.board.start[0] + self.i * square_width + square_width // 2  # Center of the square in the x direction
        y = self.board.start[1] + (self.board.board_size - 1 - self.j) * square_height + square_height // 2  # Center of the square in the y direction
        self.rect = self.image.get_rect(center=(x, y))  # Place the queen at the center of the square


    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.color == queens[self.board.current_turn].color:
                    event_x, event_y = event.pos
                    event_i = (event_x - self.board.board_rect.left) // (self.board.board_rect.width // self.board.board_size)
                    event_j = self.board.board_size - 1 - (event_y - self.board.board_rect.top) // (self.board.board_rect.height // self.board.board_size)
                    queen_i = self.i
                    queen_j = self.j
                    if event_i >= 0 and event_i < self.board.board_size and event_j >= 0 and event_j < self.board.board_size and (
                        event_i == queen_i or event_j == queen_j or
                        event_i - event_j == queen_i - queen_j or event_i + event_j == queen_i + queen_j):
                        self.i = event_i
                        self.j = event_j
                        self.set_pos()
                        self.board.next_turn = (self.board.current_turn + 1) % num_queens
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

        # Dynamically calculate size based on window size, leave room for text
        window_width, window_height = window.get_size()
        margin = 75  # Space for the text and some padding
        available_height = window_height - margin
        available_width = window_width - 40  # 20 px padding on each side
        self.size = min(available_width // board_size, available_height // board_size)
        self.start = (window_width - self.size * board_size) // 2, margin

        self.board_rect = pygame.Rect(*self.start, self.size * board_size, self.size * board_size)

    def reset_board(self):
        for y in range(self.board_size):
            for x in range(self.board_size):
                color = (192, 192, 164) if (x + y) % 2 == 0 else (96, 64, 32)
                pygame.draw.rect(self.board, color, (self.start[0] + x * self.size, self.start[1] + y * self.size, self.size, self.size))

    def show_legal_moves(self, turn):
        self.reset_board()
        
        # Draw a circle on each valid square the queen can move to
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i == queens[turn].i or j == queens[turn].j or i - j == queens[turn].i - queens[turn].j or i + j == queens[turn].i + queens[turn].j:
                    if not (i == queens[turn].i and j == queens[turn].j):
                        x = self.start[0] + i * self.size + self.size // 2
                        y = self.start[1] + (self.board_size - 1 - j) * self.size + self.size // 2
                        pygame.draw.circle(self.board, (0, 255, 0), (x, y), self.size // 6)  # Green circle in valid moves

        # Draw the grid lines
        for i in range(self.board_size + 1):
            pygame.draw.line(self.board, (0, 0, 0),
                             (self.start[0], self.start[1] + i * self.size),
                             (self.start[0] + self.board_size * self.size, self.start[1] + i * self.size), 4)
            pygame.draw.line(self.board, (0, 0, 0),
                             (self.start[0] + i * self.size, self.start[1]),
                             (self.start[0] + i * self.size, self.start[1] + self.board_size * self.size), 4)


# Function to display turn info
def display_turn_info(window, font, turn):
    turn_text = f"{queens[turn].color.capitalize()}'s Turn"
    text_surface = font.render(turn_text, True, pygame.Color("black"))
    window.blit(text_surface, (window.get_width() // 2 - text_surface.get_width() // 2, 10))

# Pygame setup
num_queens = 6
board_size = 6
pygame.init()
window = pygame.display.set_mode((800, 800))  # Initial window size
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

board = Board(board_size)
queens = [Queen(1, 0, "red", 100, board),
          Queen(board_size - 2, 0, "green", 100, board),
          Queen(1, board_size - 1, "blue", 100, board),
          Queen(board_size - 2, board_size - 1, "yellow", 100, board),
          Queen(0, 2, "purple", 100, board),
          Queen(board_size - 1, board_size - 3, "orange", 100, board)]

group = pygame.sprite.Group()
group.add(queens)

board.show_legal_moves(board.current_turn)

# Initialize font for displaying turn information
font = pygame.font.SysFont("dejavusans", 40)

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

    # Display the turn information
    display_turn_info(window, font, board.current_turn)

    pygame.display.flip()

pygame.quit()
