class Point(object):
    """Point class
        """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        """Return x for a given Point
               """
        return self.x

    def getY(self):
        """Return y for a given Point
                    """
        return self.y


class Group(object):
    def __init__(self, point, color, number_of_liberties):
        self.points = []
        self.color = color
        self.number_of_liberties = number_of_liberties
        self.points.append(point)

    def addPoint(self, row, column):
        """Add point to list of points
            :param row: int, x
            :param column: int,  y
                    """
        point = Point(row, column)
        self.points.append(point)

    def getPoints(self):
        """Return list of points
                        """
        return self.points
