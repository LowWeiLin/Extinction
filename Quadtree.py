#
#   Quadtree for 2D points
#
#   Supports:
#       insert
#       update
#       remove
#       query range
#       query nearest neighbour
#       query k nearest neighbour
#

import random
import math

# Arbitrary constant to indicate how many elements can be stored in each quadtree node
QT_NODE_CAPACITY = 10


class Point:
    XY = (0,0)
    obj = None

    def __init__(self, XY, obj=None):
        self.XY = XY
        self.obj = obj

    def __repr__(self):
        return '{P:'+str(self.XY)+' V:'+str(self.obj)+'}'

# Axis-aligned bounding box
class AABB:
    center = Point((0,0))
    halfDimension = 1

    def __init__(self, center, halfDimension):
        self.center = center
        self.halfDimension = halfDimension

        self.x1 = self.center.XY[0] - self.halfDimension
        self.x2 = self.center.XY[0] + self.halfDimension
        self.y1 = self.center.XY[1] - self.halfDimension
        self.y2 = self.center.XY[1] + self.halfDimension

    def containsPoint(self, point):
        if self.center.XY[0] - point.XY[0] > self.halfDimension:
            return False
        if point.XY[0] - self.center.XY[0] >= self.halfDimension:
            return False
        if self.center.XY[1] - point.XY[1] > self.halfDimension:
            return False
        if point.XY[1] - self.center.XY[1] >= self.halfDimension:
            return False
        return True

    def intersectsAABB(self, other):
        if self.center.XY[0] - self.halfDimension >= other.center.XY[0] + other.halfDimension:
            return False
        if other.center.XY[0] - other.halfDimension >= self.center.XY[0] + self.halfDimension:
            return False
        if self.center.XY[1] - self.halfDimension >= other.center.XY[1] + other.halfDimension:
            return False
        if other.center.XY[1] - other.halfDimension >= self.center.XY[1] + self.halfDimension:
            return False
        return True

class Quadtree:

    def __init__(self, boundary, depth=0):
        self.boundary = boundary
        self.points = []
        self.children = None
        self.parent = None
        self.numPoints = 0
        self.depth = depth
        #print self.depth

    def __subdivide(self):
        newHD = self.boundary.halfDimension/2.0
        centerXY = self.boundary.center.XY
        nw = Quadtree(AABB(Point((centerXY[0] - newHD, centerXY[1] - newHD)), newHD), self.depth+1)
        ne = Quadtree(AABB(Point((centerXY[0] + newHD, centerXY[1] - newHD)), newHD), self.depth+1)
        sw = Quadtree(AABB(Point((centerXY[0] - newHD, centerXY[1] + newHD)), newHD), self.depth+1)
        se = Quadtree(AABB(Point((centerXY[0] + newHD, centerXY[1] + newHD)), newHD), self.depth+1)
        self.children = [nw, ne, sw, se]

        points = self.points[:]
        for point in points:
            self.remove(point)
            self.insert(point)


    def insert(self, p):
        # Ignore objects that do not belong in this quad tree
        if self.boundary.containsPoint(p) is False:
          return False # object cannot be added

        # If there is space in this quad tree, add the object here
        if len(self.points) < QT_NODE_CAPACITY and self.children is None:
            self.points.append(p)
            self.numPoints += 1
            return True

        # Otherwise, subdivide and then add the point to whichever node will accept it
        if self.children is None:
            self.__subdivide()

        if self.children[0].insert(p):
            self.numPoints += 1
            return True
        if self.children[1].insert(p):
            self.numPoints += 1
            return True
        if self.children[2].insert(p):
            self.numPoints += 1
            return True
        if self.children[3].insert(p):
            self.numPoints += 1
            return True

        # Otherwise, the point cannot be inserted for some unknown reason (this should never happen)
        print "Quadtree error! Failed to insert point!"
        return False;

    # Called after update to point XY
    def update(self, p):
        pass

    # Remove one point in quadtree where point position is equals to position of p and has value of p
    def remove(self, p):
        # Ignore points that do not belong in this quad tree
        if self.boundary.containsPoint(p) is False:
          return False

        # Try to find the point in this node
        for point in self.points:
            if point.XY == p.XY and point.obj == p.obj:
                self.points.remove(point)
                self.numPoints -= 1
                return True

        # Remove from children
        if self.children is None:
            return False

        if self.children[0].remove(p):
            self.numPoints -= 1
            return True
        if self.children[1].remove(p):
            self.numPoints -= 1
            return True
        if self.children[2].remove(p):
            self.numPoints -= 1
            return True
        if self.children[3].remove(p):
            self.numPoints -= 1
            return True

        # The point was not found and cannot be removed
        print "Cannot remove!"
        return False;

    # Find all points that appear within a range
    def queryRange(self, searchRange):
        # Prepare an array of results
        pointsInRange = [];

        # Automatically abort if the range does not intersect this quad
        if self.boundary.intersectsAABB(searchRange) is False:
          return pointsInRange; # empty list

        # Check objects at this quad level
        for p in range(0,len(self.points)):
            if searchRange.containsPoint(self.points[p]):
                pointsInRange.append(self.points[p])

        # Terminate here, if there are no children
        if self.children is None:
          return pointsInRange

        # Otherwise, add the points from the children
        pointsInRange.extend(self.children[0].queryRange(searchRange));
        pointsInRange.extend(self.children[1].queryRange(searchRange));
        pointsInRange.extend(self.children[2].queryRange(searchRange));
        pointsInRange.extend(self.children[3].queryRange(searchRange));

        return pointsInRange;

    def queryNearest(self, p, radius=float('inf')):
        return self.queryKNearest(p, 1, radius)

    def queryKNearest(self, p, k, radius=10):
        #return self.queryKNearestBinary(p, k)
        result = self.__queryKNearest(p, k, radius, [])
        points = []
        for r in result:
            points.append(r[0])
        return points

    def __queryKNearest(self, p, k, radius, bestPointDistTuple=[]):
        if self.numPoints == 0:
            return bestPointDistTuple

        x = p.XY[0]
        y = p.XY[1]
        
        # Exclude node if point is farther away than best distance in either axis
        x1 = self.boundary.x1
        x2 = self.boundary.x2
        y1 = self.boundary.y1
        y2 = self.boundary.y2
        
        if x < x1 - radius or x > x2 + radius or y < y1 - radius or y > y2 + radius:
            return bestPointDistTuple

        if len(bestPointDistTuple) == k:
            # Find the largest distance of the closest points, which is the minimum required to be considered as the nearest point(s)
            maxBestDist = bestPointDistTuple[k-1][1]
            if x < x1 - maxBestDist or x > x2 + maxBestDist or y < y1 - maxBestDist or y > y2 + maxBestDist:
                return bestPointDistTuple
        else:
            maxBestDist = float('inf')

        # Test points, potentially updating best
        for point in self.points:
            dist = math.sqrt(self.distSquared(point, p))
            if dist < maxBestDist:
                # Insert into bestPointDistTuple
                # Find position to insert into
                insertPosition = len(bestPointDistTuple)
                pointDistTuple = (point, dist)
                #print pointDistTuple
                for i in range(len(bestPointDistTuple)-1, -1, -1):
                    if dist >= bestPointDistTuple[i][1]:
                        break
                    insertPosition -= 1
                bestPointDistTuple.insert(insertPosition, pointDistTuple)

                # Trim list to be of length at most k
                if len(bestPointDistTuple) > k:
                    bestPointDistTuple = bestPointDistTuple[:k]
                # Update maxBestDist
                if len(bestPointDistTuple) == k:
                    maxBestDist = bestPointDistTuple[k-1][1]


        # Look for potentially better points in children
        # Check if point is on the right or left, top or bottom
        # and then recurse on most likely children first, so we quickly find a 
        # nearby point and then exclude many larger rectangles later
        if self.children is not None:
            rl = 1 if (2*x > x1 + x2) else 0
            bt = 1 if (2*y > y1 + y2) else 0
                
            bestPointDistTuple = self.children[bt*2+rl].__queryKNearest(p, k, radius, bestPointDistTuple)
            bestPointDistTuple = self.children[bt*2+(1-rl)].__queryKNearest(p, k, radius, bestPointDistTuple)
            bestPointDistTuple = self.children[(1-bt)*2+rl].__queryKNearest(p, k, radius, bestPointDistTuple)
            bestPointDistTuple = self.children[(1-bt)*2+(1-rl)].__queryKNearest(p, k, radius, bestPointDistTuple)

        return bestPointDistTuple

    def queryNearestBinary(self, p):
        return self.queryKNearestBinary(p, 1)

    def queryKNearestBinary(self, p, k):

        center = p.XY
        minHD = 0.000001
        maxHD = self.boundary.halfDimension * 2
        searchHD = self.boundary.halfDimension
        searchedMinHD = minHD
        searchedMaxHD = maxHD

        itr = 0
        maxItr = 1000
        epsilon = 0.000001

        points = []
        while True :
            if searchHD > maxHD or searchHD < minHD or abs(searchedMinHD - searchedMaxHD) < epsilon:
                break
            itr+=1
            if itr > maxItr:
                print searchHD, len(points), searchedMinHD, searchedMaxHD

            points = self.queryRange(AABB(p, searchHD))
            if len(points) == k:
                break
            elif len(points) < k:
                searchedMinHD = searchHD
                searchHD = (searchedMinHD + searchedMaxHD)/2.0
            else:
                searchedMaxHD = searchHD
                searchHD = (searchedMinHD + searchedMaxHD)/2.0

        if len(points) == 0:
            return None

        if len(points) == k:
            return points

        bestPoint = points[0]
        minRadius2 = self.distSquared(points[0], p)
        for i in range(1, len(points)):
            rad2 = self.distSquared(points[i], p)
            if rad2 < minRadius2:
                bestPoint = points[i]
                minRadius2 = rad2

        return [bestPoint]

    def distSquared(self, p1, p2):
        return (p1.XY[0] - p2.XY[0])**2 + (p1.XY[1] - p2.XY[1])**2

# a = AABB(Point((5,5)), 5)
# print a.containsPoint(Point((5,5)))
# print a.containsPoint(Point((0,0)))
# print a.containsPoint(Point((0,10)))
# print a.containsPoint(Point((10,0)))
# print a.containsPoint(Point((10,10)))
# b = AABB(Point((5,5)), 5)
# print a.intersectAABB(b)
# b = AABB(Point((5,5)), 10)
# print a.intersectAABB(b)
# b = AABB(Point((-5,-5)), 5)
# print a.intersectAABB(b)
# b = AABB(Point((-5,-5)), 6)
# print a.intersectAABB(b)
# b = AABB(Point((-5,5)), 5)
# print a.intersectAABB(b)
# b = AABB(Point((10,-5)), 5)
# print a.intersectAABB(b)
# b = AABB(Point((10,10)), 5)
# print a.intersectAABB(b)
# b = AABB(Point((15,15)), 5)
# print a.intersectAABB(b)
# b = AABB(Point((14,14)), 5)
# print a.intersectAABB(b)


# qt = Quadtree(AABB(Point((50, 50)), 50))
# qt.insert(Point((5,5)))
# print qt.queryRange(AABB(Point((50, 50)), 50))
# print qt.queryRange(AABB(Point((50, 50)), 5))
# qt.insert(Point((5,6)))
# qt.insert(Point((5,6)))
# qt.insert(Point((5,7)))
# qt.insert(Point((5,8)))
# qt.insert(Point((5,9)))
# print qt.queryRange(AABB(Point((50, 50)), 50))
# print qt.queryRange(AABB(Point((50, 50)), 5))
# print qt.queryRange(AABB(Point((5, 50)), 43))

# print "b",qt.queryNearestBinary(Point((5,10)))
# print "b",qt.queryNearestBinary(Point((5,8.5)))

# print "*",qt.queryNearest(Point((5,10)))
# print "*",qt.queryNearest(Point((5,8.5)))


# Insertion test
# 10000         - 0.3
# 100000        - 3.2
# 250000        - 9.2
# 500000        - 19.8
# 750000        - 30.0
# 1000000       - 40.1
# qt = Quadtree(AABB(Point((50, 50)), 50))
# for i in range(0, 100000):
#     res = qt.insert(Point((random.uniform(0.0, 100.0), random.uniform(0.0, 100.0))))
#     if res == False:
#         print "failed to insert"

# print "Inserted points"

# # 1     - 0.6
# # 10    - 2.6
# # 100   - 26.6, 2.6, 0.1
# for i in range(0, 10):
#     res = qt.queryNearestBinary(Point((random.uniform(0.0, 100.0), random.uniform(0.0, 100.0))))
#     #print len(res)

# for i in range(0, 1):
#     res = qt.queryKNearestBinary(Point((50,50)), 1)
#     print len(res)
#     print res
#     print qt.distSquared(res[0], Point((50,50)))

#     res = qt.queryKNearest(Point((50,50)), 1)
#     print len(res)
#     print res
#     print qt.distSquared(res[0], Point((50,50)))

# qt = Quadtree(AABB(Point((50, 50)), 50))
# qt.insert(Point((5,5)))
# print qt.queryRange(AABB(Point((50, 50)), 50))
# print qt.queryRange(AABB(Point((50, 50)), 5))
# qt.insert(Point((5,6)))
# qt.insert(Point((5,6)))
# qt.insert(Point((5,7)))
# qt.insert(Point((5,8)))
# qt.insert(Point((5,9)))
# print qt.queryKNearest(Point((5,10)), 5)
# qt.remove(Point((5,9)))
# print qt.queryKNearest(Point((5,10)), 2)



