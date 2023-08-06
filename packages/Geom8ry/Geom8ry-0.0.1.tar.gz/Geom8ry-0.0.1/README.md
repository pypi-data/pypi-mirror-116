# Geom8ry - Python Geom8ry Package

## Development Stage : 2 - Pre-Alpha 
## Warning : Unstable
Version: 0.0.1

Geom8ry is a python package for performing computational
geometry. Geom8ry can handle various 2D - geometrical constructs like Points, Lines, Line Segments,  Polygons, Circles,  Fourier Transforms, Matrices, Graphs, Triangulations, and  Polynomials, etc.

It's also a personal exercise in learning how to provide a high
quality python package:

- support of powerful tools like Delaunay Triangulations, FFTs, Inverse FFTs, Convex Hulls, and Fast Polynomial Multiplications
- appropriate use of exceptions and exception handling
- designing of useful base classes and methods
- high-quality documentation
- efficient implementation of algorithms and data structures



### Point
    
```python
p1 = Point(1,1)
print(p1)
pp1 = PolarPoint(2,30)
p2 = pp1.toCratesian()
print(p2)
p3 = Point(2,2)
print(Point.orientation(p1,p2,p3))
print(Point.findQuadrant(p2))
print(Point.euclideanDistance(p1,p2))
print(Point.manhattanDistance(p1,p2))
l = [p1,p2,p3]
print(Point.centroid(l))
print(Point.convexHull(l)) # Graham Scan
# print(Point.closestPairOfPoints(l))
print(Point.delaunayTriangulation(l))
=============================
(1 , 1)
(0.3085028997751681 , -1.9760632481857237)        
2
4
3.0553429753173558
3.6675603484105554
(1.102834299925056 , 0.3413122506047588)
[1, 2, 0]
[0, 2, 1]
```



### Line
```python
p = Point(1,0)
p1 = Point(0,1)
l1 = SlopeIntercept(-1,1)
# l2 = TwoPoint(p,p2)
l3 = TwoIntercept(2,2)
# l4 = SlopePoint(-1,p)
print(Line.Transform.SlopeInterceptToStandard(l1))
print(Line.Transform.TwoInterceptToStandard(l3))
# print(Line.Transform.slopeToStandard(l1))

print(Line.distanceBetweenLines(Line.Transform.SlopeInterceptToStandard(l1),Line.Transform.TwoInterceptToStandard(l3)))
print(Line.isIntersecting(Line.Transform.SlopeInterceptToStandard(l1),Line.Transform.TwoInterceptToStandard(l3)))
# print(Line.Transform.TwoInterceptToStandard(l3).rotate(Point(0,0),math.pi/2))
===================================
(1*X + 1*Y = 1)
(2*X + 2*Y = 4)
2.1213203435596424
0
```
### Matrix
```python
m = [[1,2,3],[4,5,6],[7,8,9]]

mt = Matrix(m)
print(mt)
print(mt.transpose())
print(mt.trace)
print(mt.size)

mt2 =  mt.transpose()
mt3 = Matrix.gen(3,3,9)
print(mt3)
print(mt2 + mt,mt2 - mt, mt2 * mt)
==================================
|   1.00   2.00   3.00 |
|   4.00   5.00   6.00 |
|   7.00   8.00   9.00 |


|   1.00   4.00   7.00 |
|   2.00   5.00   8.00 |
|   3.00   6.00   9.00 |

45
(3, 3)

|   9.00   9.00   9.00 |
|   9.00   9.00   9.00 |
|   9.00   9.00   9.00 |


|   2.00   6.00  10.00 |
|   6.00  10.00  14.00 |
|  10.00  14.00  18.00 |

|   0.00   2.00   4.00 |
|  -2.00   0.00   2.00 |
|  -4.00  -2.00   0.00 |

|  66.00  78.00  90.00 |
|  78.00  93.00 108.00 |
|  90.00 108.00 126.00 |
```
### Vector
```python
p = Point(1,1)
v = Vector(p)
p1 = Point(1,0)
v1 = Vector(p1)
print(v1+v, (v1-v), v1*v)
print(v1.add(2), v1.magnitude(), v1.multiply(2))
print(v1.dot(v), v1.cross(v))
print(v1.unit(), v1.angle(v))
print(v1.parallel(v), v1.perpendicular(v))
print(v1.non_parallel(v))
# print(v1.rotate(math.pi/4,(0,1,0)))
print(v1.to_points())
========================
(2 , 1) (0 , -1) 1
(3.0 , 2.0) 1.0 (2.0 , 0.0)
1 1
(1.0 , 0.0) 45.00000000000001
False False
True
[1, 0]
```


### Circle
```python
c = Circle(2)
print(c.area(), c.findLatticePoints())
p = Point(0,0)
# print(p)
p1 = Point(2,0)
print(c.isInside(p))
print(c.isOn(p1))
print(c.getTangent(p1))
=======================
12.566370614359172 4
True
True
(2*X + 0*Y = 4)
```

### DFT
```python
l = [1,2,3,4]
print(dft(l))
=============
[(10+0j), (-2-2j), (-2+0j), (-1.9999999999999998+2j)]
```

### Inverse DFT
```python
l = [1,2,3,4]
print(idft(l))
# ==============
[(2.5+0j), (-0.5+0.5j), (-0.5+0j), (-0.49999999999999994-0.5j)]
```

### Polynomial
```python
l = [1,2,3,4]
p = Polynomial(l)
l2 = [11,22,33,44]
p2 = Polynomial(l2)
print(p)
print(p2)
print(p+p2)
print(p-p2)
print(p*p2) ## BY FFT
=====================
1x^0 + 2x^1 + 3x^2 + 4x^3
11x^0 + 22x^1 + 33x^2 + 44x^3
12x^0 + 24x^1 + 36x^2 + 48x^3
-10x^0 + -20x^1 + -30x^2 + -40x^3
11x^0 + 44x^1 + 110x^2 + 220x^3 + 275x^4 + 264x^5 + 176x^6
```

### Regular Polygon
```python
rp = RegularPolygon(4,2)
print(rp.area(), rp.perimeter(), rp.cicumradius())
print(rp.inradius(), rp.internalangles())
============================================
4.000000000000001 8 1.414213562373095 
1.0000000000000002 90.0
```

### Polygon
```python
p1 = Point(2,0)
p2 = Point(2,2)
p3 = Point(0,2)
p4 = Point(0,0)

l= [p1,p2,p3,p4]
p = Polygon(l)

print(p)
print(p.area())
print(p.perimeter())
====================
(2,0) (2,2) (0,2) (0,0)
4.0
8.0
```