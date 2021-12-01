import pygame
from go.constants import WHITE, RED, BLUE, BLACK, ROWS, SQUARE_SIZE, WIDTH, HEIGHT


class Board:
    def __init__(self):
        self.board = [[WHITE, 0, WHITE, 0, WHITE],
                      [RED, 0, RED, 0, WHITE],
                      []]
        self.selected_piece = None
        self.game_board = [['x', 'x', 'x', 'x', 'x', 'x'],
                           ['x', 'x', 'x', 'x', 'x', 'x'],
                           ['x', 'x', 'x', 'x', 'x', 'x'],
                           ['x', 'x', 'x', 'x', 'x', 'x'],
                           ['x', 'x', 'x', 'x', 'x', 'x'],
                           ['x', 'x', 'x', 'x', 'x', 'x']
                           ]
        self.players = ['op1', 'op2']
        self.turn = ''
        self.pass_op1 = False
        self.pass_op2 = False

    def capture(self, row, col):
        opponent = self.game_board[row][col]

    def draw_squares(self, win):
        for row in range(0, ROWS):
            for col in range(0, ROWS):
                pygame.draw.rect(win, RED, (
                    row * SQUARE_SIZE + SQUARE_SIZE, col * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
                # pygame.display.flip()
        for row in range(0, ROWS + 1):
            for col in range(0, ROWS + 1):
                if self.game_board[row][col] == 'A':
                    pygame.draw.circle(win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE),
                                       40)
                else:
                    if self.game_board[row][col] == 'B':
                        pygame.draw.circle(win, WHITE,
                                           (col * SQUARE_SIZE + SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE),
                                           40)
                    # pygame.display.flip()

        x_pos = 30
        y_pos = 30
        width = 50
        height = 50
        # for i in range(6):
        # for j in range(6):
        # pygame.draw.rect(win, RED, (x_pos*i, y_pos*j, width, height), 2)

        # pygame.draw.line(win, RED, [i * WIDTH / 8, 30], [i * WIDTH / 8, HEIGHT], 5)
        # pygame.draw.line(win, WHITE, [40, i * HEIGHT / 8], [WIDTH, i * HEIGHT / 8], 5)

    def get_clicked_column(self, x):
        for i in range(1, ROWS + 1):
            if x < i * WIDTH / (ROWS + 2) + SQUARE_SIZE / 2:
                print(i - 1)
                return i - 1
        return ROWS

    def get_clicked_row(self, y):
        for i in range(1, ROWS + 1):
            if y < i * HEIGHT / (ROWS + 2) + SQUARE_SIZE / 2:
                print(i - 1)
                return i - 1
        return ROWS

    def draw_circle(self, column, row, win):
        if self.turn == 'op1':
            self.game_board[row][column] = 'A'
        else:
            self.game_board[row][column] = 'B'
        # pygame.draw.circle(win, BLUE, (column * SQUARE_SIZE + SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE), 40)
        # pygame.display.flip()

    def is_ok_move(self, column, row):
        if self.game_board[row][column] == 'x':
            return True
        return False
