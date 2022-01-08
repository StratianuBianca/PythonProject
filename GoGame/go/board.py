import copy
import random
from scipy import ndimage
import numpy as np
import pygame
from go.group import Group, Point
from go.constants import WHITE, RED, BLUE, BLACK, ROWS, SQUARE_SIZE, WIDTH, HEIGHT


def calculate_opponent(color):
    """Calculate opponent for given data.
        :param color: color of board
                """
    if color == 1:
        return 2
    elif color == 2:
        return 1


def compareMatrix(a, b):
    """Calculates whether two matrices are equal.

        :param a: first matrix
        :param b: second matrix
        :return: boolean
        """
    find = False
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i][j] != b[i][j]:
                find = True
    return find


def get_clicked_column(x):
    """Calculates the clicked column

        :param x: x clicked
        :return: column
        """
    for i in range(1, ROWS + 1):
        if x < i * WIDTH / (ROWS + 2) + SQUARE_SIZE / 2:
            return i - 1
    return ROWS


def get_clicked_row(y):
    """Calculates the clicked row

            :param y: y clicked
            :return: row
            """
    for i in range(1, ROWS + 1):
        if y < i * HEIGHT / (ROWS + 2) + SQUARE_SIZE / 2:
            return i - 1
    return ROWS


class Board:
    def __init__(self):
        """Init class Board
                """
        self.board = [[WHITE, 0, WHITE, 0, WHITE],
                      [RED, 0, RED, 0, WHITE],
                      []]
        self.selected_piece = None
        self.game_board = [[-1, -1, -1, -1, -1, -1],
                           [-1, -1, -1, -1, -1, -1],
                           [-1, -1, -1, -1, -1, -1],
                           [-1, -1, -1, -1, -1, -1],
                           [-1, -1, -1, -1, -1, -1],
                           [-1, -1, -1, -1, -1, -1]
                           ]
        self.players = [1, 2]
        self.turn = ''
        self.pass_op1 = False
        self.pass_op2 = False
        self.capture_op1 = 0
        self.capture_op2 = 0
        self.previously = []
        self.groups = []
        self.ai_activate = False
        self.empty_group = []
        self.blackScore = 0
        self.whiteScore = 0
        self.previously_move_pass = False
        """
        :param board: list
        :param selected_piece: optional
        :param game_board: matrix, initially matrix
        :param players: list, list of players
        :param turn: str, turn of board
        :param pass_op1: bool, check if player 1 presses pass
        :param pass_op2: bool, check if player 2 pressed pass
        :param capture_op1: int, capture score for player 1
        :param capture_op2: int, capture score for player 2
        :param previously: list, previously matrix for ko rule
        :param groups: list, list of groups
        :param ai_activate: bool, check if player choose AI
        :param empty_group: list, list of empty groups
        :param blackScore: int, score for player1
        :param whiteScore: int, score for player2
        :param previously_move_pass: bool, check if previously move was pass
        """

    def verify_if_exits(self, row, column, add_row,
                        add_column):
        """Add the game piece to the group that the next piece belongs to

                :param row: int, x
                :param column: int, y
                :param add_row: int, new x
                :param add_column: int, new y
                """
        if self.game_board[row][column] == self.game_board[add_row][add_column]:
            self.unit_two_groups(row, column, add_row, add_column)

    def add_to_group(self, row, column):
        """Add the point in a group
            :param row: int, x point
            :param column: int, y point
         """
        point = Point(row, column)
        group = Group(point, self.game_board[row][column], 4)
        self.groups.append(group)
        if row != 0:
            self.verify_if_exits(row - 1, column, row, column)
        if row != len(self.game_board) - 1:
            self.verify_if_exits(row + 1, column, row, column)
        if column != 0:
            self.verify_if_exits(row, column - 1, row, column)
        if column != len(self.game_board) - 1:
            self.verify_if_exits(row, column + 1, row, column)

    def verify_if_unites_two_groups(self, row, column):
        """Check if we can join two groups
            :param row: int, x point
            :param column: int, y point
        """
        if row != 0 and self.game_board[row - 1][column] == self.game_board[row][column]:
            if column != len(self.game_board) - 1 and self.game_board[row][column] == self.game_board[row][column + 1]:
                self.unit_two_groups(row - 1, column, row, column + 1)
                self.verify_if_exits(row - 1, column, row, column)
            if row != len(self.game_board) - 1 and self.game_board[row][column] == self.game_board[row + 1][column]:
                self.unit_two_groups(row - 1, column, row + 1, column)
                self.verify_if_exits(row - 1, column, row, column)
            if column != 0 and self.game_board[row][column] == self.game_board[row][column - 1]:
                self.unit_two_groups(row - 1, column, row, column - 1)
                self.verify_if_exits(row - 1, column, row, column)
        if column != len(self.game_board) - 1 and self.game_board[row][column + 1] == self.game_board[row][column]:
            if row != len(self.game_board) - 1 and self.game_board[row][column] == self.game_board[row + 1][column]:
                self.unit_two_groups(row, column + 1, row + 1, column)
                self.verify_if_exits(row, column + 1, row, column)
            if column != 0 and self.game_board[row][column] == self.game_board[row][column - 1]:
                self.unit_two_groups(row, column + 1, row, column - 1)
                self.verify_if_exits(row, column + 1, row, column)
        if row != len(self.game_board) - 1 and self.game_board[row + 1][column] == self.game_board[row][column]:
            if column != 0 and self.game_board[row][column] == self.game_board[row][column - 1]:
                self.unit_two_groups(row + 1, column, row, column - 1)
                self.verify_if_exits(row + 1, column, row, column)

    def unit_two_groups(self, row_group1, column_group1, row_group2, column_group2):
        """Join two groups of the same color
           :param row_group1: int, x point for group 1
           :param column_group1: int, y point for group 1
           :param row_group2: int, x point for group 2
           :param column_group2: int, y point for group 2
         """
        group2 = -1
        index = -1
        for j in self.groups:
            for k in j.points:
                if k.getX() == row_group1 and k.getY() == column_group1:
                    find = False
                    for a in self.groups:
                        group2 = a.points
                        find = False
                        for m in a.points:
                            if m.getX() == row_group2 and m.getY() == column_group2:
                                # group2 = l.points
                                find = True
                                index = self.groups.index(a)
                    if find:
                        for point in group2:
                            j.addPoint(point.getX(), point.getY())
        if index != -1:
            self.groups.pop(index)

    def calculate_group_liberty(self):
        """Check the degree of freedom of a group
            """
        for group in self.groups:
            liberty = 0
            for point in group.points:
                liberty += self.calculate_point_liberty(point.getX(), point.getY())
            group.number_of_liberties = liberty

    def calculate_point_liberty(self, row, column):
        """Check the degree of freedom of a point

            :param row: int, row of point
            :param column: int, column of point
            :return: int, point liberty
            """
        liberty = 0
        if row != 0:
            if self.game_board[row - 1][column] == -1:
                liberty += 1
        if column != 0:
            if self.game_board[row][column - 1] == -1:
                liberty += 1
        if row != len(self.game_board) - 1:
            if self.game_board[row + 1][column] == -1:
                liberty += 1
        if column != len(self.game_board) - 1:
            if self.game_board[row][column + 1] == -1:
                liberty += 1
        return liberty

    def capture_group(self, color):
        """if a group no longer has any degree of freedom it means that it has been captured by the opponent
           :param color: int, color of group
                    """
        list_of_groups = set()
        for group in self.groups:
            if group.number_of_liberties == 0:
                for point in group.points:
                    if self.game_board[point.getX()][point.getY()] != color:
                        list_of_groups.add(group)
                        self.game_board[point.getX()][point.getY()] = -1
        for i in list_of_groups:
            self.groups.pop(self.groups.index(i))

    def capture_group_color(self, color_board):
        """For the ko rule, the first group captured is the one of a different color

            :param color_board: int, color of the board
            :return: int
            """
        list_of_groups = []
        color = []
        for group in self.groups:
            if group.number_of_liberties == 0:
                list_of_groups.append(group)
        if len(list_of_groups) <= 0:
            return -3
        if len(list_of_groups) > 1:
            for group in list_of_groups:
                point = group.points[0]
                color.append(self.game_board[point.getX()][point.getY()])
            find = False
            for i in color:
                if i != color_board:
                    find = True
            if find is False:
                return color_board
            else:
                return -3
        for point in list_of_groups[0].points:
            if self.game_board[point.getX()][point.getY()] == color_board:
                return color_board
        return -3

    def is_in_group(self, row, column):
        """See if a point exists in a group.
            :param row: int, row of point
            :param column: int, column of point
            :return: bool
            """
        for group in self.empty_group:
            for point in group.points:
                if point.getX() == row and point.getY() == column:
                    return True
        return False

    def draw_squares(self, win):
        """Draw the table.
            :param win: pygame.display
            """
        for row in range(0, ROWS + 1):
            for col in range(0, ROWS + 1):
                if self.game_board[row][col] == -1:
                    pygame.draw.circle(win, BLACK,
                                       (col * SQUARE_SIZE + SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE),
                                       40)
        for row in range(0, ROWS):
            for col in range(0, ROWS):
                pygame.draw.rect(win, RED, (
                    row * SQUARE_SIZE + SQUARE_SIZE, col * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
        for row in range(0, ROWS + 1):
            for col in range(0, ROWS + 1):
                if self.game_board[row][col] == 1:
                    pygame.draw.circle(win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE),
                                       40)
                else:
                    if self.game_board[row][col] == 2:
                        pygame.draw.circle(win, WHITE,
                                           (col * SQUARE_SIZE + SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE),
                                           40)

    def generate_AI(self):
        """AI who randomly chooses the positions, and if he chose the wrong 4 times, then he passes.
            :return: (row, column)
            """
        self.turn = 2
        row = random.randint(0, len(self.game_board) - 1)
        column = random.randint(0, len(self.game_board) - 1)
        if self.is_ok_move(column, row):
            return row, column
        for i in range(0, 4):
            row = random.randint(0, len(self.game_board) - 1)
            column = random.randint(0, len(self.game_board) - 1)
            if self.is_ok_move(column, row):
                return row, column
        return -1, -1

    def draw_circle(self, column, row):
        """Check all the rules and then draw the board
            :param column: int, column point
            :param row: int, row point
            """
        if self.turn == 1:
            self.game_board[row][column] = 1
        else:
            self.game_board[row][column] = 2
        self.verify_if_unites_two_groups(row, column)
        self.add_to_group(row, column)
        self.calculate_group_liberty()
        self.capture_group(self.game_board[row][column])

    def return_index_group(self, row, column):
        """Calculate the index from the list of a certain group.

            :param row: int, row of point
            :param column: int,  column of point
            :return: int, index
            """
        for i in self.groups:
            for j in i.points:
                if j.getX == row and j.getY == column:
                    return self.groups.index(i)
        return -1

    def calculate_score(self):
        """The score is equal to the number of pieces of each player plus the areas that are captured by the players.
            """
        area_matrix = copy.deepcopy(self.game_board)
        for i in range(0, len(self.game_board)):
            for j in range(0, len(self.game_board)):
                if self.game_board[i][j] != -1:
                    area_matrix[i][j] = 0
                else:
                    area_matrix[i][j] = 1
        empty_labels, num_empty_areas = ndimage.measurements.label(np.array(area_matrix))
        for numberArea in range(1, num_empty_areas + 1):
            black = 0
            white = 0
            number_of_neighbours = 0
            for i in range(0, len(self.game_board)):
                for j in range(0, len(self.game_board)):
                    if empty_labels[i][j] == numberArea:
                        number_of_neighbours += 1
                        neighbours = self.calculate_neighbors(i, j)
                        for neighbour in neighbours:
                            if neighbour == 1:
                                black += 1
                            elif neighbour == 2:
                                white += 1
            if white == 0 and black > 0:
                self.blackScore += number_of_neighbours
            if black == 0 and white > 0:
                self.whiteScore += number_of_neighbours
        for i in range(0, len(self.game_board)):
            for j in range(0, len(self.game_board)):
                if self.game_board[i][j] == 1:
                    self.blackScore += 1
                elif self.game_board[i][j] == 2:
                    self.whiteScore += 1

    def calculate_neighbors(self, row, column):
        """The neighbors are: up, down, left and right

            :param row: int, the row of point
            :param column: int, the column of point
            :return: list , list of neighbors
            """
        neighbors = []
        if row != 0:
            neighbors.append(self.game_board[row - 1][column])
        if row != len(self.game_board) - 1:
            neighbors.append(self.game_board[row + 1][column])
        if column != 0:
            neighbors.append(self.game_board[row][column - 1])
        if column != len(self.game_board) - 1:
            neighbors.append(self.game_board[row][column + 1])
        return neighbors

    def is_ok_move(self, column, row):
        """We have two rules "ko" and "suicide".
            For ko we are not allowed to repeat the same positions, to have the same board several times.
            For suicide we are not allowed for the player to lose his own stones.

            :param column: int, column of point
            :param row: int, row of point
            :return: bool
            """
        if self.game_board[row][column] != -1:
            return False
        else:
            before_move = copy.deepcopy(self.game_board)
            self.game_board[row][column] = self.turn
            self.verify_if_unites_two_groups(row, column)
            self.add_to_group(row, column)
            self.calculate_group_liberty()
            color = self.capture_group_color(self.game_board[row][column])
            if color == self.game_board[row][column]:
                self.game_board = copy.deepcopy(before_move)
                return False
            for i in self.previously:
                if not compareMatrix(i, self.game_board):
                    self.game_board = copy.deepcopy(before_move)
                    return False
            self.previously.append(self.game_board)
            self.game_board = copy.deepcopy(before_move)
            return True
