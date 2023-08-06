from __future__ import division

from functools import reduce
import math
from numbers import Real


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '{0}({1}, {2})'.format(
            self.__class__.__name__,
            self.x,
            self.y
        )

    def __sub__(self, point):
        """Return a Point instance as the displacement of two points."""
        if type(point) is Point:
            return self.substract(point)
        else:
            raise TypeError

    def __add__(self, pt):
        if isinstance(pt, Point):
            return Point(pt.x + self.x, pt.y + self.y)
        else:
            raise TypeError

    def __eq__(self, pt):
        return (self.x == pt.x and self.y == pt.y)

    def to_list(self):
        '''Returns an array of [x,y] of the end points'''
        return [self.x, self.y]

    def substract(self, pt):
        """Return a Point instance as the displacement of two points."""
        if isinstance(pt, Point):
                return Point(self.x- pt.x, self.y - pt.y)
        else:
            raise TypeError

    @classmethod
    def from_list(cls, l):
        """Return a Point instance from a given list"""
        if len(l) == 2:
            x, y = map(float, l)
            return cls(Point(x, y))
        elif len(l) == 2:
            x, y = map(float, l)
            return cls(Point(x, y))
        else:
            raise AttributeError


class Vector(Point):
    """Vector class: Representing a vector in 3D space.
    Can accept formats of:
    Cartesian coordinates in the x, y space.(Regular initialization)
    Spherical coordinates in the r, theta, phi space.(Spherical class method)
    Cylindrical coordinates in the r, theta space.(Cylindrical class method)
    """
    # def __init(self, Point):
    #     if Point is None:
    #         Point = Point
    #     self.Point = Point
    # def __init__(self, x, y):
    #     '''Vectors are created in rectangular coordniates
    #     to create a vector in spherical or cylindrical
    #     see the class methods
    #     '''
    #     super(Vector, self).__init__(x, y)

    def __init__(self, Point):
        '''Vectors are created in rectangular coordniates
        to create a vector in spherical or cylindrical
        see the class methods
        '''
        super(Vector, self).__init__(Point.x,Point.y)
    def __add__(self, vec):
        """Add two vectors together"""
        if(type(vec) == type(self)):
            return Vector(Point(self.x + vec.x, self.y + vec.y))
        elif isinstance(vec, Real):
            return self.add(vec)
        else:
            raise TypeError

    def __sub__(self, vec):
        """Subtract two vectors"""
        if(type(vec) == type(self)):
            return Vector(Point(self.x - vec.x, self.y - vec.y))
        elif isinstance(vec, Real):
            return Vector(Point(self.x - vec, self.y - vec))
        else:
            raise TypeError

    def __mul__(self, anotherVector):
        """Return a Vector instance as the cross product of two vectors"""
        return self.cross(anotherVector)

    def __str__(self):
        res = '(' + str(self.x) + ' , ' + str(self.y) + ')'
        return res

    def __round__(self, n=None):
        if n is not None:
            return Vector(Point(round(self.x, n), round(self.y, n)))
        return Vector(Point(round(self.x), round(self.y)))

    def add(self, number):
        """Return a Vector as the product of the vector and a real number."""
        return self.from_list([x + number for x in self.to_list()])

    def multiply(self, number):
        """Return a Vector as the product of the vector and a real number."""
        return self.from_list([x * number for x in self.to_list()])

    def magnitude(self):
        """Return magnitude of the vector."""
        return math.sqrt(
            reduce(lambda x, y: x + y, [x ** 2 for x in self.to_list()])
        )

    # def sum(self, vector):
    #     """Return a Vector instance as the vector sum of two vectors."""
    #     return self.from_list(
    #         [self.to_list()[i] + vector.to_list()[i] for i in range(2)]
    #     )

    # def subtract(self, vector):
    #     """Return a Vector instance as the vector difference of two vectors."""
    #     return self.__sub__(vector)

    def dot(self, vector, theta=None):
        """Return the dot product of two vectors.
        If theta is given then the dot product is computed as
        v1*v1 = |v1||v2|cos(theta). Argument theta
        is measured in degrees.
        """
        if theta is not None:
            return (self.magnitude() * vector.magnitude() *
                    math.degrees(math.cos(theta)))
        return (reduce(lambda x, y: x + y,
                [x * vector.to_list()[i] for i, x in enumerate(self.to_list())]))

    def cross(self, vector):
        """Return a Vector instance as the cross product of two vectors"""
        return (self.x * vector.y - self.y * vector.x)

    def unit(self):
        """Return a Vector instance of the unit vector"""
        return Vector(Point(
            (self.x / self.magnitude()),
            (self.y / self.magnitude())
        ))

    def angle(self, vector):
        """Return the angle between two vectors in degrees."""
        return math.degrees(
            math.acos(
                self.dot(vector) /
                (self.magnitude() * vector.magnitude())
            )
        )

    def parallel(self, vector):
        """Return True if vectors are parallel to each other."""
        if self.cross(vector) == 0:
            return True
        return False

    def perpendicular(self, vector):
        """Return True if vectors are perpendicular to each other."""
        if self.dot(vector) == 0:
            return True
        return False

    def non_parallel(self, vector):
        """Return True if vectors are non-parallel.
        Non-parallel vectors are vectors which are neither parallel
        nor perpendicular to each other.
        """
        if (self.parallel(vector) is not True and
                self.perpendicular(vector) is not True):
            return True
        return False

    def rotate(self, angle, axis=(0, 0, 1)):
        """Returns the rotated vector. Assumes angle is in radians"""
        if not all(isinstance(a, int) for a in axis):
            raise ValueError
        x, y = self.x, self.y

        # Z axis rotation
        if(axis[2]):
            x = (self.x * math.cos(angle) - self.y * math.sin(angle))
            y = (self.x * math.sin(angle) + self.y * math.cos(angle))

        # Y axis rotation
        if(axis[1]):
            x = self.x * math.cos(angle) 

        # X axis rotation
        if(axis[0]):
            y = self.y * math.cos(angle)

        return Vector(Point(x, y))

    def to_points(self):
        '''Returns an array of [x,y] of the end points'''
        return [self.x, self.y]


# =======================================================

# p = Point(1,1)
# v = Vector(p)
# p1 = Point(1,0)
# v1 = Vector(p1)
# print(v1+v, (v1-v), v1*v)
# print(v1.add(2), v1.magnitude(), v1.multiply(2))
# print(v1.dot(v), v1.cross(v))
# print(v1.unit(), v1.angle(v))
# print(v1.parallel(v), v1.perpendicular(v))
# print(v1.non_parallel(v))
# # print(v1.rotate(math.pi/4,(0,1,0)))
# print(v1.to_points())