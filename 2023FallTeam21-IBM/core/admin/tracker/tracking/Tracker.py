import math
from tracking.TrackedObject import TrackedObject

# Abstract class for tracking objects
class Tracker():

    def __init__(self):
        # Store the box points of the objects
        self.trackedObjects = dict[int, TrackedObject]([])
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.idCount = 0

    def calculateObjectDistance(self, rect, obj: TrackedObject): 
        # Get the bounding rectangles
        x1, y1, w1, h1 = rect
        x2, y2, w2, h2 = obj.getBoundingRectangle()
        # Get the centers of the bounding rectangles
        center1 = (x1 + w1/2, y1 + h1/2)
        center2 = (x2 + w2/2, y2 + h2/2)
        # Initialize the direction variables
        up, right, down, left = False, False, False, False
        # Determine the direction of the distance
        if center1[1] < center2[1]:
            up = True
        if center1[1] > center2[1]:
            down = True
        if center1[0] < center2[0]:
            left = True
        if center1[0] > center2[0]:
            right = True
        # Calculate the distance between the corners of the bounding rectangles
        if up and left:
            # top left corner of contour1 to top left corner of contour2
            distA = math.hypot(x1 - x2, y1 - y2)
            # bottom left corner of contour1 to top left corner of contour2
            distB = math.hypot(x1 - x2, y1 + h1 - y2)
            # top right corner of contour1 to top left corner of contour2
            distC = math.hypot(x1 + w1 - x2, y1 - y2)
            # middle of left side of contour1 to top left corner of contour2
            distD = math.hypot(x1 - x2, y1 + h1/2 - y2)
            # middle of top side of contour1 to top left corner of contour2
            distE = math.hypot(x1 + w1/2 - x2, y1 - y2)
            # return the minimum distance
            return min(distA, distB, distC, distD, distE)
        elif up and right:
            # top right corner of contour1 to top right corner of contour2
            distA = math.hypot(x1 + w1 - x2 - w2, y1 - y2)
            # top left corner of contour1 to top right corner of contour2
            distB = math.hypot(x1 - x2 - w2, y1 - y2)
            # bottom right corner of contour1 to top right corner of contour2
            distC = math.hypot(x1 + w1 - x2 - w2, y1 + h1 - y2)
            # middle of top side of contour1 to top right corner of contour2
            distD = math.hypot(x1 + w1/2 - x2 - w2, y1 - y2)
            # middle of right side of contour1 to top right corner of contour2
            distE = math.hypot(x1 + w1 - x2 - w2, y1 + h1/2 - y2)
            # return the minimum distance
            return min(distA, distB, distC, distD, distE)
        elif down and left:
            # bottom left corner of contour1 to bottom left corner of contour2
            distA = math.hypot(x1 - x2, y1 + h1 - y2 - h2)
            # bottom right corner of contour1 to bottom left corner of contour2
            distB = math.hypot(x1 + w1 - x2, y1 + h1 - y2 - h2)
            # top left corner of contour1 to bottom left corner of contour2
            distC = math.hypot(x1 - x2, y1 - y2 - h2)
            # middle of bottom side of contour1 to bottom left corner of contour2
            distD = math.hypot(x1 + w1/2 - x2, y1 + h1 - y2 - h2)
            # middle of left side of contour1 to bottom left corner of contour2
            distE = math.hypot(x1 - x2, y1 + h1/2 - y2 - h2)
            # return the minimum distance
            return min(distA, distB, distC, distD, distE)
        elif down and right:
            # bottom right corner of contour1 to bottom right corner of contour2
            distA = math.hypot(x1 + w1 - x2 - w2, y1 + h1 - y2 - h2)
            # top right corner of contour1 to bottom right corner of contour2
            distB = math.hypot(x1 + w1 - x2 - w2, y1 - y2 - h2)
            # bottom left corner of contour1 to bottom right corner of contour2
            distC = math.hypot(x1 - x2 - w2, y1 + h1 - y2 - h2)
            # middle of right side of contour1 to bottom right corner of contour2
            distD = math.hypot(x1 + w1 - x2 - w2, y1 + h1/2 - y2 - h2)
            # middle of bottom side of contour1 to bottom right corner of contour2
            distE = math.hypot(x1 + w1/2 - x2 - w2, y1 + h1 - y2 - h2)
            # return the minimum distance
            return min(distA, distB, distC, distD, distE)
        elif up:
            # middle of top side of contour1 to top side of contour2
            return math.hypot(x1 + w1/2 - x2 - w2/2, y1 - y2)
        elif down:
            # middle of bottom side of contour1 to bottom side of contour2
            return math.hypot(x1 + w1/2 - x2 - w2/2, y1 + h1 - y2 - h2)
        elif left:
            # middle of left side of contour1 to left side of contour2
            return math.hypot(x1 - x2, y1 + h1/2 - y2 - h2/2)
        elif right:
            # middle of right side of contour1 to right side of contour2
            return math.hypot(x1 + w1 - x2 - w2, y1 + h1/2 - y2 - h2/2)
        else:
            return 0
    
    # Abstract method for updating the tracker
    def update(self, contoursToUpdate):
        pass

    # Returns the tracked objects
    # @return: The list of tracked objects
    def getTrackedObjects(self):
        return self.trackedObjects
    
