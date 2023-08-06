import math
from fractions import *
from .point import Point


class Polygon :
    def __init__(self, lop=None):
        if lop is None:
         lop = []
        self.lop = lop
    def __repr__(self):
        rep = ''
        for i in range(len(self.lop)):
            rep += str('(')+(str((self.lop[i]).x)  + str(',') + str(self.lop[i].y))+') '
        return rep 
    def area(self):
        """ #Area bounded by list of Points """
        polygonArea = 0.0
        noOfPoints = len(self.lop)
        j = noOfPoints - 1
        for i in range(0,noOfPoints) :
            polygonArea += (self.lop[i].x + self.lop[j].x) * (self.lop[j].y - self.lop[i].y)
            j = i
        return abs(polygonArea / 2.0)
    def perimeter(self):
        perimeter = 0
        for i in range(0, len(self.lop)-1):
            perimeter += Point.euclideanDistance(self.lop[i],self.lop[i+1])
        perimeter += Point.euclideanDistance(self.lop[-1],self.lop[0])
        return perimeter
# ======================================================
# p1 = Point(2,0)
# p2 = Point(2,2)
# p3 = Point(0,2)
# p4 = Point(0,0)

# l= [p1,p2,p3,p4]
# p = Polygon(l)

# print(p)
# print(p.area())
# print(p.perimeter())