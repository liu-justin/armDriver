import numpy as np
import CoordinateSystem as cs
import math
import time

class Point(object):
    def __init__(self, name, x, y, z=0, state="nready"):
        self.name = name
        self._homogeneous = np.array([x,y,z,1])
        self._regular = self._homogeneous[:-1]
        self.x = x
        self.y = y
        self.z = z
        self.links = []
        self.waitingLinks = []
        self._state = state

    def __getitem__(self, position):
        return self._homogeneous[position]

    def magnitude(self):
        return math.sqrt( self.x**2 + self.y**2 + self.z**2 )

    def distanceTo(self, otherPoint):
        distance = self.regular - otherPoint.regular
        return np.sqrt(np.einsum('i,i', distance, distance))
        # return math.sqrt((otherPoint.x - self.x)**2 +(otherPoint.y - self.y)**2 +(otherPoint.z - self.z)**2)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def intersectionPoint(self):
        linkA = self.waitingLinks[0]
        linkB = self.waitingLinks[1]
        pointA = linkA.points[self]
        pointB = linkB.points[self]
        print(f"point {self.name} calculating intersection point between two links {linkA.name}, {linkB.name} - points are {pointA.name}:{pointA},{pointB.name}:{pointB}")
        x1 = 0.5*(pointA.x + pointB.x)
        y1 = 0.5*(pointA.y + pointB.y)

        R = pointA.distanceTo(pointB)

        c2 = (linkA.length**2 - linkB.length**2)/(2*R**2)
        x2 = c2*(pointB.x - pointA.x)
        y2 = c2*(pointB.y - pointA.y)

        c3_1 = 2*(linkA.length**2+linkB.length**2)/R**2
        c3_2 = (linkA.length**2-linkB.length**2)**2/R**4
        c3 = 0.5*math.sqrt(c3_1 - c3_2 - 1)
        x3 = c3*(pointB.y - pointA.y)
        y3 = c3*(pointA.x - pointB.x)

        self.waitingLinks = []

        return (x1+x2+x3, y1+y2+y3)

    @property
    def homogeneous(self):
        return self._homogeneous
    @homogeneous.setter
    def homogeneous(self, incomingArray):
        self._homogeneous = incomingArray
        self._regular = self._homogeneous[:-1]
        self.x = self._homogeneous[0]
        self.y = self._homogeneous[1]
        self.z = self._homogeneous[2]
        self.state = "ready"
        for link in self.links: link.update(self)
            
    @property
    def regular(self):
        return self._regular
    @regular.setter
    def regular(self, incomingArray):
        
        self._regular = incomingArray
        self._homogeneous = np.append(self.regular, 1 )
        self.x = self._regular[0]
        self.y = self._regular[1]
        self.z = self._regular[2]
        print(f"in point {self.name} regular.setter, just set regular to {self.regular}")

        self.state = "ready"

        for link in self.links: link.lookAtRelations()
        for link in self.links: link.update(self)

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, incomingState):
        self._state = incomingState
        print(f"in point {self.name} state.setter, just set state to {self.state}")

        for link in self.links: link.findState()

# -----------------------------------------------------------------------------------------------------------------

def addRelation(relation, linkA, linkB):
    linkA.relations[relation].append(linkB)
    linkB.relations[relation].append(linkA)

def magnitude(v):
    return np.sqrt(v.dot(v))

def findCommonPoint(linkA, linkB):
    list1 = linkA.points.values()
    list2 = linkB.points.values()
    return set(list1).intersection(list2).pop()

def collinearTransformation(linkA, linkB):
    # this means both links are not able to move, so don't transform it
    if stateImportance[linkA.state] <= 1 and stateImportance[linkB.state] <= 1:
        return

    # establishing harbor and ship, which link moves to which
    if stateImportance[linkA.state] < stateImportance[linkB.state]:
        harbor = linkA
        ship = linkB
    else:
        harbor = linkB
        ship = linkA

    pivot = findCommonPoint(harbor, ship)
    # startang = time.perf_counter()
    harborAngle = math.atan2(harbor.vectorFrom(pivot)[1],harbor.vectorFrom(pivot)[0])
    # if harborAngle < 0: harborAngle = 2*np.pi - harborAngle
    shipAngle = math.atan2(ship.vectorFrom(pivot)[1],ship.vectorFrom(pivot)[0])
    # if shipAngle < 0: shipAngle = 2*np.pi - shipAngle
    if abs(shipAngle - harborAngle) > np.pi/2:
        harborAngle = math.atan2(harbor.vectorTo(pivot)[1],harbor.vectorTo(pivot)[0])
    angle = harborAngle - shipAngle
    # angtime = time.perf_counter() - startang

    # law of cosines doesn't show negative or positive, it just shows the abs angle value
    # angle = math.acos(np.dot(harbor.vectorFrom(pivot), ship.vectorFrom(pivot))/(magnitude(harbor.vectorFrom(pivot))*magnitude(ship.vectorFrom(pivot))))
    # if abs(angle) > np.pi/2: angle2 = np.pi - angle
    # elif abs(angle) > np.pi: angle2 = angle - np.pi #- angle
    
    r = getXYRotationMatrix(angle)

    ship.points[pivot].regular = pivot.regular + np.dot(r, ship.vectorFrom(pivot)) # need to add property for vector

relToFunc = {"collinear": collinearTransformation, "perpendicular": "perpendicularTransformation", "parallel": "parallelTransformation"}
stateImportance = {"fixed": 0, "ready": 1, "nready": 2, "waiting": 2}

# -----------------------------------------------------------------------------------------------------------------

class Link(object):
    def __init__(self, name, length, pointA, pointB):
        self.name = name
        self.length = length
        self.points = {}
        self.points[pointA] = pointB
        self.points[pointB] = pointA

        self.relations = {key:[] for key in relToFunc.keys()}

        pointA.links.append(self)
        pointB.links.append(self)

        self.state = "nready"
    
    def vectorFrom(self, point):
        return self.points[point].regular - point.regular

    def vectorTo(self, point):
        return point.regular - self.points[point].regular

    def findState(self):
        highestPointState = "fixed"
        for point in self.points.values():
            if (stateImportance[point.state] > stateImportance[highestPointState]):
                highestPointState = point.state
        self.state = highestPointState
        print(f"in link {self.name}, findState;  just set self.state to {self.state}")


    def update(self, point):
        # find the location of the other point, based on distances
        print(f"link {self.name} updating, currently checking point {self.points[point].name} state")

        if self.points[point].state == "nready":
            print("- state was nready, so setting to waiting")
            self.points[point].state = "waiting"
            self.points[point].waitingLinks.append(self)

        # if another link put the point into waiting, that means it can be found thru intersection
        elif self.points[point].state == "waiting":
            print("- state was waiting, so doing an intersection")
            self.points[point].waitingLinks.append(self)
            tup = self.points[point].intersectionPoint()
            
            self.points[point].regular = np.array([tup[0], tup[1], 0])

        # if the other point is fixed, search thru the other links from that point
        elif self.points[point].state == "fixed":
            print("- state was fixed, so checking all the other links assoicated with this point")
            for link in self.points[point].links:
                if link != self: link.update(self.points[point])

    def lookAtRelations(self):
        print(f"in link {self.name}, lookatRelations")
        for relation, links in self.relations.items():
            for link in links:
                relToFunc[relation](self, link)

    def changeAngle(self, incomingAngle, baseLink):
        pivot = findCommonPoint(self, baseLink)
        print(f"in link {self.name}, changeAngle; just found pivot point {pivot.name}")
        r = getXYRotationMatrix(incomingAngle)
        notnormalized = np.dot(r, baseLink.vectorFrom(pivot)) # this isnt right
        self.points[pivot].regular = pivot.regular + notnormalized*magnitude(self.vectorFrom(pivot))/magnitude(baseLink.vectorFrom(pivot))

def getXYRotationMatrix(angle):

    a = np.array([[ np.cos(angle), -np.sin(angle),              0],
                  [ np.sin(angle),  np.cos(angle),              0],
                  [             0,              0,              1]])

    return a

# class Circle(Point):
#     def __init__(self, r, x, y, z=0):
#         Point.__init__(self, x, y, z=0)
#         self.radius = r

#     # returns one of the intersection points between two circles
#     def intersectionPoint(self, other):
#         x1 = 0.5*(self.x + other.x)
#         y1 = 0.5*(self.y + other.y)

#         R = self.distanceTo(other)

#         c2 = (self.radius**2 - other.radius**2)/(2*R**2)
#         x2 = c2*(other.x - self.x)
#         y2 = c2*(other.y - self.y)

#         c3_1 = 2*(self.radius**2+other.radius**2)/R**2
#         c3_2 = (self.radius**2-other.radius**2)**2/R**4
#         c3 = 0.5*math.sqrt(c3_1 - c3_2 - 1)
#         x3 = c3*(other.y - self.y)
#         y3 = c3*(self.x - other.x)

#         return Point(x1+x2-x3, y1+y2-y3)

def getAngleBetween(a, pivot, b):
    return np.arccos(np.dot( a.homogeneous[:-1] - pivot.homogeneous[:-1], b.homogeneous[:-1] - pivot.homogeneous[:-1]) / (a.magnitude() * b.magnitude()) )
