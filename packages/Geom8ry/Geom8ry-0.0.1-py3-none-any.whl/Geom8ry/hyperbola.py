from __future__ import division

from functools import reduce
import math
from numbers import Real


class Hyperbola(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        if (math.sqrt(1+(a*a)/(b*b)) < 1):
            raise AttributeError

    @classmethod
    def conjugate(cls, hyperbola):
        """Return a Conjugate of the hyperbola"""
        return Hyperbola()
            # raise AttributeError
