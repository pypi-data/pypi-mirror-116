import math
import copy
from .delaunay import *
from .hull import *

class PolarPoint:
    def __init__(self, r, theta):
        '''
            Creates  a polar point.
            :param int r: The radial distance.
            :param int theta: Polar angle.
            :return: Object of Polar Point
            :rtype: Object
            :raises ValueError: if the theta exceeds abs(360).
            :raises TypeError: if the message_body is not a basestring
        '''
        self.r = r
        if abs(theta) > 360 :
            raise ValueError
        elif theta < 0 :
            self.theta = 360 - theta
        else :
            self.theta = theta
    def toCratesian(self):
        return Point(self.r*math.cos(self.theta),self.r*math.sin(self.theta))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return '('+str(self.x)+' , ' + str(self.y)+')'
    @staticmethod
    def orientation(p, q, r):
        val = (float(q.y - p.y) * float(r.x - q.x)) - (float(q.x - p.x) * float(r.y - q.y))
        if (val > 0):
            return 1
        elif (val < 0):
            return 2
        else:
            return 0
    @staticmethod
    def findQuadrant(p):
        if p.x==0 and p.y==0 :
            return "0"
        if p.x>0 and p.y>0 :
            return "1"
        if p.x<0 and p.y>0 :
            return "2"
        if p.x<0 and p.y<0 :
            return "3"
        if p.x>0 and p.y<0 :
            return "4"
        if p.y<0 and p.x==0 :
            return "-y"
        if p.y>0 and p.x==0 :
            return "+y"
        if p.x>0 and p.y==0 :
            return "+x"
        if p.x<0 and p.y==0 :
            return "-x"
    @classmethod 
    def euclideanDistance(cls, p, q):
        '''To find Euclidean Distance of two Points.'''
        return math.sqrt((p.x-q.x)*(p.x-q.x) + (p.y-q.y)*(p.y-q.y))
    
    @classmethod 
    def manhattanDistance(cls, p, q):
        """ # To find Manhattan Distance of two Points. """
        return abs(p.x-q.x) + abs(p.y-q.y)
    @classmethod 
    def centroid(cls,listOfPoints):
        """ #Cnetroid of a list of Points """
        noOfPoints = len(listOfPoints)
        if noOfPoints==0:
            raise ValueError
        sigmaX = 0
        sigmaY = 0 
        for point in listOfPoints:
            sigmaX += point.x
            sigmaY += point.y
        centroidPoint = Point(sigmaX/noOfPoints, sigmaY/noOfPoints)
        return centroidPoint
    @classmethod
    def convexHull(cls, listOfPoints):
        return CONVEXHULL(listOfPoints)
    # No of lattice points #No of Lattice Points inside a Polygon by Pick's Theorem
    @classmethod
    def pointsOnLine(cls,p, q):
        return math.gcd(q.x - p.x, q.y - p.y) + 1
    @classmethod
    def pointsInsidePolygon(cls, listOfPoints):
        A = int(Point.area(listOfPoints))
        B = 0
        listOfPoints.append(listOfPoints[0]);
        for i in range(0,len(listOfPoints)):
            B += Point.pointsOnLine(listOfPoints[i], listOfPoints[i+1])
        return A + B/2 - 1

# ======================================================================
    # Find the closest pair of points using Divide And Conqure
    @classmethod
    def closestPairOfPoints(cls,listOfPoints):
        n = len(listOfPoints)
        listOfPoints.sort(key = lambda point: point.x)
        Q = copy.deepcopy(listOfPoints)
        Q.sort(key = lambda point: point.y)    
        return Point.closestUtil(listOfPoints, Q, n)
    @staticmethod
    def stripClosest(strip, size, d):
        min_val = d 
        for i in range(size):
            j = i + 1
            while j < size and (strip[j].y - strip[i].y) < min_val:
                min_val = Point.euclideanDistance(strip[i], strip[j])
                j += 1
        return min_val
    @staticmethod
    def closestUtil(P, Q, n):
        mid = n // 2
        midPoint = P[mid]
        dl = Point.closestUtil(P[:mid], Q, mid)
        dr = Point.closestUtil(P[mid:], Q, n - mid) 
        d = min(dl, dr)
        strip = [] 
        for i in range(n): 
            if abs(Q[i].x - midPoint.x) < d: strip.append(Q[i])
        return min(d, Point.stripClosest(strip, len(strip), d))

# ==================================================================
    @classmethod
    def delaunayTriangulation(cls, listOfPoints, listOfList=False):
        points = []
        for Point in listOfPoints:
            points.append([Point.x,Point.y])
        triangles = Delaunator(points).triangles
        if listOfList == True:
            coordinates = []
            for i in range(0, len(triangles), 3):
                coordinates.append([points[triangles[i]], points[triangles[i + 1]], points[triangles[i + 2]]])
                return coordinates
        return triangles

# ===========================TEST============================================
# p1 = Point(1,1)
# print(p1)
# pp1 = PolarPoint(2,30)
# p2 = pp1.toCratesian()
# print(p2)
# p3 = Point(2,2)
# print(Point.orientation(p1,p2,p3))
# print(Point.findQuadrant(p2))
# print(Point.euclideanDistance(p1,p2))
# print(Point.manhattanDistance(p1,p2))
# l = [p1,p2,p3]
# print(Point.centroid(l))
# print(Point.convexHull(l))
# # print(Point.closestPairOfPoints(l))
# print(Point.delaunayTriangulation(l))