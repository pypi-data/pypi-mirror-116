# import math
# from fractions import *
# from  exceptions  import * 
# from  point import *
# from  line  import * 
# from  ellipse  import * 
# from  polygon  import * 
# from  hyperbola  import * 
# from  triangle  import * 
# from  rectangle  import * 
# from  graph  import * 
# from  delaunay  import * 


class Segment:
    def __init__(self, p, q):
        self.p = p
        self.q = q
    @classmethod
    def findIntersection(cls, segment):
        return None