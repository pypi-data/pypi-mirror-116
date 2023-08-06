import math
from fractions import *
from .point import Point
class RegularPolygon :
    def __init__(self, noOfEdges, lengthOfEdges):
        self.E = noOfEdges
        self.L = lengthOfEdges
    def area(self):
        if self.E < 3:
            raise ValueError()
            return
        else :
            numerator = self.E*self.L
            denominator = 2*math.tan(math.pi/self.E)
            return numerator/denominator
    def perimeter(self):
        if self.E < 3:
            raise ValueError()
            return
        else:
            return self.E*self.L
    def cicumradius(self):
        if self.E < 3:
            raise ValueError()
            return
        else:
            numerator = self.L
            denominator = 2*math.sin(math.pi/self.E)
            return numerator/denominator
    def inradius(self):
        if self.E < 3:
            raise ValueError()
            return
        else:
            numerator = self.L
            denominator = 2*math.tan(math.pi/self.E)
            return numerator/denominator
    def internalangles(self):
        if self.E < 3:
            raise ValueError()
            return
        else:
            return 180*(self.E-2)/self.E
# ================================================

# rp = RegularPolygon(4,2)
# print(rp.area(), rp.perimeter(), rp.cicumradius(), rp.inradius(), rp.internalangles())