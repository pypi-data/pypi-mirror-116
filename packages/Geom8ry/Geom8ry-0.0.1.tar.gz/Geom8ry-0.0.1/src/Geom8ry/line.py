import math
from .point import Point
from fractions import *

# y=mx+c
class SlopeIntercept:
    def __init__(self, m, c):
        self.m = m
        self.c = c
# y-y1/x-x1 = (y2-y1)/(x2-x1)
class TwoPoint:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
# x/a + y/b = 1
class TwoIntercept:
    def __init__(self, a, b):
        self.a = a
        self.b = b
class SlopePoint():
    def __init__(self, m ,Point):
        self.m = m
        self.Point = Point
        

# ax + by = c
# Standard Lines
class Line:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def __str__(self):
        return '('+str(self.a) +'*X + ' + str(self.b) +'*Y = '+ str(self.c)+')'
    class Transform:
        def __init__(self):
            pass
        @classmethod
        def SlopeInterceptToStandard(cls, slopeLine):
            res = Line(-slopeLine.m,1,slopeLine.c)
            return res
        @classmethod
        def TwoPointToStandard(cls , pointLine):
            res = Line(None,None,None)
            slope = Fraction(pointLine.y2-pointLine.y1,pointLine.x2-pointLine.x1)
            if slope.denominator==0:
                res = Line(1,0,pointLine.x1)
                return res
            else:
                res = Line(slope,-1,slope*pointLine.x1-pointLine.y1)
                return res
        @classmethod
        def TwoInterceptToStandard(cls , interceptLine):
            res = Line(interceptLine.b,interceptLine.a,interceptLine.a*interceptLine.b)
            return res
    @classmethod
    def distanceBetweenLines(cls, stdLine1, stdLine2):
        numerator = abs(stdLine1.c-stdLine2.c)
        denominator = math.sqrt(stdLine1.a**2 + stdLine1.b**2)
        if numerator==0:
            return 0
        return numerator/denominator
    @classmethod
    def isIntersecting(cls, stdLine1, stdLine2):
        if cls.distanceBetweenLines(stdLine1,stdLine2)==0:
            return 1
        else:
            return 0
    def rotate(self, aboutPoint, thetaClockwise):
        """ (Acosθ+Bsinθ)(x−x0)+(Bcosθ−Asinθ)(y−y0)+Ax0+By0+C=0.
        Ax+By+C=0
         """
        A = self.a*math.cos(thetaClockwise) + self.b*math.sin(thetaClockwise)
        B = self.b*math.cos(thetaClockwise) - self.a*math.sin(thetaClockwise)
        C = -(self.a*math.cos(thetaClockwise) + self.b*math.sin(thetaClockwise))*aboutPoint.x
        -(self.b*math.cos(thetaClockwise) - self.a*math.sin(thetaClockwise))*aboutPoint.y
        +self.a*aboutPoint.x + self.b*aboutPoint.y - self.c
        return Line(A,B,C)

    # determinant = a1 b2 - a2 b1
    # if (determinant == 0)
    # {
    #     // Lines are parallel
    # }
    # else
    # {
    #     x = (c1b2 - c2b1)/determinant
    #     y = (a1c2 - a2c1)/determinant
    # }

    @classmethod
    def findIntersection(cls, stdLine1,stdLine2):
        a1 = stdLine1.a
        b2 = stdLine2.b
        a2 = stdLine2.a
        b1 = stdLine1.b
        c1 = stdLine1.c
        c2 = stdLine2.c
        determinant = a1 * b2 - a2 * b1
        if determinant == 0 :
            return -1
        else:
            x = (c1*b2 - c2*b1)/determinant
            y = (a1*c2 - a2*c1)/determinant
            res = Point(x,y)
            return res

#===========================================
# p = Point(1,0)
# p1 = Point(0,1)
# l1 = SlopeIntercept(-1,1)
# # l2 = TwoPoint(p,p2)
# l3 = TwoIntercept(2,2)
# # l4 = SlopePoint(-1,p)
# print(Line.Transform.SlopeInterceptToStandard(l1))
# print(Line.Transform.TwoInterceptToStandard(l3))
# # print(Line.Transform.slopeToStandard(l1))

# print(Line.distanceBetweenLines(Line.Transform.SlopeInterceptToStandard(l1),Line.Transform.TwoInterceptToStandard(l3)))
# print(Line.isIntersecting(Line.Transform.SlopeInterceptToStandard(l1),Line.Transform.TwoInterceptToStandard(l3)))
# # print(Line.Transform.TwoInterceptToStandard(l3).rotate(Point(0,0),math.pi/2))