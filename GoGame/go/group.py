import pygame
from go.constants import WHITE, RED, BLUE, BLACK, ROWS, SQUARE_SIZE, WIDTH, HEIGHT


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class Group(object):
    def __init__(self, point, color, number_of_liberties):
        self.points = []
        self.color = color
        self.number_of_liberties = number_of_liberties
        self.points.append(point)

    def addPoint(self, row, column):
        point = Point(row, column)
        self.points.append(point)

    def getPoints(self):
        return self.points
