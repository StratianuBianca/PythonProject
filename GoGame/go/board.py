import copy
import random
from scipy import ndimage
import numpy as np
import pygame
from go.group import Group, Point
from go.constants import WHITE, RED, BLUE, BLACK, ROWS, SQUARE_SIZE, WIDTH, HEIGHT


def calculate_opponent(color):
    if color == 1:
        return 2
    elif color == 2:
        return 1


def compareMatrix(a, b):  # vedem daca doua matrici sunt egale
    find = False
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i][j] != b[i][j]:
                find = True
    return find


def get_clicked_column(x):
    for i in range(1, ROWS + 1):
        if x < i * WIDTH / (ROWS + 2) + SQUARE_SIZE / 2:
            return i - 1
    return ROWS


def get_clicked_row(y):
    for i in range(1, ROWS + 1):
        if y < i * HEIGHT / (ROWS + 2) + SQUARE_SIZE / 2:
            return i - 1
    return ROWS


class Board:
    def __init__(self):
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

    def verify_if_exits(self, row, column, add_row,
                        add_column):  # adaugam piesa la grupul din care face parte piesa de langa
        if self.game_board[row][column] == self.game_board[add_row][add_column]:
            self.unit_two_groups(row, column, add_row, add_column)

    def add_to_group(self, row, column):   # adaugam punctul intr-un grup
        point = Point(row, column)
        group = Group(point, self.game_board[row][column], 4)  # cream un grup nou
        self.groups.append(group)
        if row != 0:
            self.verify_if_exits(row - 1, column, row, column)  # verificam daca exista intr-un grup piesa de langa
        if row != len(self.game_board) - 1:
            self.verify_if_exits(row + 1, column, row, column)
        if column != 0:
            self.verify_if_exits(row, column - 1, row, column)
        if column != len(self.game_board) - 1:
            self.verify_if_exits(row, column + 1, row, column)

    def verify_if_unites_two_groups(self, row, column):  # verificam daca putem sa unim doua grupuri
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
        # unim doua grupuri de aceeasi culoare
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

    def calculate_group_liberty(self):  # verificam care este gradul de libertate al unui grup
        for group in self.groups:
            liberty = 0
            for point in group.points:
                liberty += self.calculate_point_liberty(point.getX(), point.getY())
            group.number_of_liberties = liberty

    def calculate_point_liberty(self, row, column):  # verificam care este gradul de libertate al unui punct
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
        # daca un grup nu mai are nici un grad de libertate inseamna ca a fost capturat de oponent
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
        # pentru regula ko, primul grup capturat este cel de culoare diferita
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

    def is_in_group(self, row, column):  # vedem daca un punct exista intr-un grup
        for group in self.empty_group:
            for point in group.points:
                if point.getX() == row and point.getY() == column:
                    return True
        return False

    def draw_squares(self, win):  # desenam tabla
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
        # AI care alege random pozitiile, iar daca a ales de 4 ori gresit, atunci da pass
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
        if self.turn == 1:
            self.game_board[row][column] = 1
        else:
            self.game_board[row][column] = 2
        self.verify_if_unites_two_groups(row, column)
        self.add_to_group(row, column)
        self.calculate_group_liberty()
        self.capture_group(self.game_board[row][column])

    def return_index_group(self, row, column):  # calculam indexul din lista al unui anumit grup
        for i in self.groups:
            for j in i.points:
                if j.getX == row and j.getY == column:
                    return self.groups.index(i)
        return -1

    def calculate_score(self):
        # scorul este egal cu numarul de piese ale fiecarui jucator plus zonele care sunt capturate de jucatori
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

    def calculate_neighbors(self, row, column):  # vecinii sunt: sus, jos, stanga si dreapta
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
        """
        avem doua reguli "ko" si "suicide"
        pentru ko nu avem voie sa repetam aceeleasi pozitii, sa avem aceeasi tabla de mai multe ori
        pentru suicide nu avem voie ca jucatorul sa isi piarta propriile pietre
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
