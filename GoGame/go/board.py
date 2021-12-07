import random
import select

import numpy as np
import pygame
from go.group import Group, Point
from go.constants import WHITE, RED, BLUE, BLACK, ROWS, SQUARE_SIZE, WIDTH, HEIGHT


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

    def calculate_opponent(self, color):
        if color == 1:
            return 2
        elif color == 2:
            return 1

    def verify_if_exits(self, row, column, add_row,
                        add_column):  # adaugam piesa la grupul din care face parte piesa de langa
        if self.game_board[row][column] == self.game_board[add_row][add_column]:
            self.unit_two_groups(row, column, add_row, add_column)

    def add_to_group(self, row, column):
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

    def verify_if_unites_two_groups(self, row, column):  # unim 2 grupuri
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
        group2 = -1
        index = -1
        for j in self.groups:
            for k in j.points:
                if k.getX() == row_group1 and k.getY() == column_group1:
                    find = False
                    for l in self.groups:
                        group2 = l.points
                        find = False
                        for m in l.points:
                            if m.getX() == row_group2 and m.getY() == column_group2:
                                #group2 = l.points
                                find = True
                                index = self.groups.index(l)
                    if find:
                        for point in group2:
                            j.addPoint(point.getX(), point.getY())
        if index != -1:
            self.groups.pop(index)

    def calculate_group_liberty(self):
        for group in self.groups:
            liberty = 0
            for point in group.points:
                liberty += self.calculate_point_liberty(point.getX(), point.getY())
            group.number_of_liberties = liberty

    def calculate_point_liberty(self, row, column):
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

    def capture_group(self):
        list_of_groups = []
        for group in self.groups:
            if group.number_of_liberties == 0:
                list_of_groups.append(group)
                for point in group.points:
                    self.game_board[point.getX()][point.getY()] = -1
        for i in list_of_groups:
            self.groups.pop(self.groups.index(i))

    def draw_squares(self, win):
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
                # pygame.display.flip()
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
                    # pygame.display.flip()

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

    def generateAI(self):
        self.turn = 2
        row = random.randint(0, len(self.game_board)-1)
        column = random.randint(0, len(self.game_board)-1)
        if self.is_ok_move(column, row):
            return row, column
        for i in range(0, 4):
            row = random.randint(0, len(self.game_board) - 1)
            column = random.randint(0, len(self.game_board) - 1)
            if self.is_ok_move(column, row):
                return row, column
        return -1, -1

    def draw_circle(self, column, row, win):
        if self.turn == 1:
            self.game_board[row][column] = 1
        else:
            self.game_board[row][column] = 2
        #self.capture()
        self.verify_if_unites_two_groups(row, column)
        self.add_to_group(row, column)
        self.calculate_group_liberty()
        self.capture_group()
        print("Aici incepe")
        for j in self.groups:
            # print(self.groups.index(j))
            print("Liberty ", j.number_of_liberties, len(j.points))
            for k in j.points:
                print(k.getX())
                print(k.getY())

    # pygame.draw.circle(win, BLUE, (column * SQUARE_SIZE + SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE), 40)
    # pygame.display.flip()
    def compare_matix(self, a, b):
        find = False
        for i in range(len(a)):
            for j in range(len(b)):
                if a[i][j] != b[i][j]:
                    find = True
        return find

    def is_ok_move(self, column, row):
        if self.game_board[row][column] != -1:
            return False
        else:
            before_move = self.game_board
            self.game_board[row][column] = self.turn
            self.verify_if_unites_two_groups(row, column)
            self.add_to_group(row, column)
            self.calculate_group_liberty()
            self.capture_group()
            for i in self.previously:
                if self.compare_matix(i, self.game_board):
                    self.game_board = before_move
                    return False
            self.game_board = before_move
            self.previously.append(self.game_board)
            return True

        #if self.game_board[row][column] ==:
         #   return True
        #return False
