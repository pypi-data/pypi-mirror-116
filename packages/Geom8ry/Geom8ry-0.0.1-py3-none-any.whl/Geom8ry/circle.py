from __future__ import division

from functools import reduce
import math
from numbers import Real
from .point import Point
from .line import Line

class Circle:
    def __init__(self, r):
        self.r = r
    def area(self) :
        return (math.pi*self.r*self.r)
    def findLatticePoints(self):
        r = self.r
        if (r <= 0):
            return 0  
        result = 4 
        for x in range(1, r):
            ySquare = r*r - x*x 
            y = int(math.sqrt(ySquare)) 
            if (y*y == ySquare):
                result += 4 
        return result 
    def isInside(self,point):
        x = point.x
        y = point.y
        r = self.r
        if x*x+y*y-r*r > 0 :
            return False
        if x*x+y*y-r*r == 0 :
            return False
        if x*x+y*y-r*r < 0 :
            return True
    def isOn(self,point):
        x = point.x
        y = point.y
        r = self.r
        if x*x+y*y-r*r == 0 :
            return True
        else :
            return False
    def getTangent(self,point):
        x = point.x
        y = point.y
        r = self.r
        if self.isOn(point):
            return Line(x,y,r*r)

# ==================================TEST=================================

# c = Circle(2)
# print(c.area(), c.findLatticePoints())
# p = Point(0,0)
# # print(p)
# p1 = Point(2,0)
# print(c.isInside(p))
# print(c.isOn(p1))
# print(c.getTangent(p1))