import cv2
import numpy as np
import math

class ContourMerger():
    # Standard resolution average (pixels) (for width of 1280 and height of 720)
    STANDARD_RESOLUTION_AVERAGE = 1000.0

    # Constructor, initializes the Contour Merger
    # @param config: The configuration object that stores the settings the project is running on
    def __init__(self, config, resolution):
        # Get the options from the config file
        self.DEFAULT_THRESHOLD_DISTANCE = config.getfloat('ContourMerger', 'DEFAULT_THRESHOLD_DISTANCE')
        self.SWALLOW_AREA_RATIO_THRESHOLD = config.getfloat('ContourMerger', 'SWALLOW_AREA_RATIO_THRESHOLD')

        # Convert the resolution into pixel thresholds
        #       (DEFAULT_THRESHOLD_DISTANCE) 
        resolutionWidth = resolution[0]
        resolutionHeight = resolution[1]
        resolutionAverage = (resolutionWidth + resolutionHeight) / 2
        self.DEFAULT_THRESHOLD_DISTANCE = self.DEFAULT_THRESHOLD_DISTANCE * resolutionAverage / self.STANDARD_RESOLUTION_AVERAGE
        # Call the parent constructor
        super().__init__()


    # Calculate the distance between two contours
    # Determines the direction of the distance,
    # and calculates the distance between the 
    # corners of the bounding rectangles that 
    # should be closest to each other.
    # @param contour1: The first contour
    # @param contour2: The second contour
    def calculateContourDistance(self, contour1, contour2):
        # Get the bounding rectangles
        x1, y1, w1, h1 = cv2.boundingRect(contour1)
        x2, y2, w2, h2 = cv2.boundingRect(contour2)
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
            # bottom right corner of contour1 to top left corner of contour2
            distA = math.hypot(x1 + w1 - x2, y1 + h1 - y2)
            # bottom left corner of contour1 to top left corner of contour2
            distB = math.hypot(x1 - x2, y1 + h1 - y2)
            # top right corner of contour1 to top left corner of contour2
            distC = math.hypot(x1 + w1 - x2, y1 - y2)
            # middle of bottom side of contour1 to top left corner of contour2
            distD = math.hypot(x1 + w1/2 - x2, y1 + h1 - y2)
            # middle of right side of contour1 to top left corner of contour2
            distE = math.hypot(x1 + w1 - x2, y1 + h1/2 - y2)
            # return the minimum distance
            return min(distA, distB, distC, distD, distE)
        elif up and right:
            # bottom left corner of contour1 to top right corner of contour2
            distA = math.hypot(x1 - x2 - w2, y1 + h1 - y2)
            # top left corner of contour1 to top right corner of contour2
            distB = math.hypot(x1 - x2 - w2, y1 - y2)
            # bottom right corner of contour1 to top right corner of contour2
            distC = math.hypot(x1 + w1 - x2 - w2, y1 + h1 - y2)
            # middle of left side of contour1 to top right corner of contour2
            distD = math.hypot(x1 - x2 - w2, y1 + h1/2 - y2)
            # middle of bottom side of contour1 to top right corner of contour2
            distE = math.hypot(x1 + w1/2 - x2 - w2, y1 + h1 - y2)
            # return the minimum distance
            return min(distA, distB, distC, distD, distE)
        elif down and left:
            # top right corner of contour1 to bottom left corner of contour2
            distA = math.hypot(x1 + w1 - x2, y1 - y2 - h2)
            # bottom right corner of contour1 to bottom left corner of contour2
            distB = math.hypot(x1 + w1 - x2, y1 + h1 - y2 - h2)
            # top left corner of contour1 to bottom left corner of contour2
            distC = math.hypot(x1 - x2, y1 - y2 - h2)
            # middle of right side of contour1 to bottom left corner of contour2
            distD = math.hypot(x1 + w1 - x2, y1 + h1/2 - y2 - h2)
            # middle of top side of contour1 to bottom left corner of contour2
            distE = math.hypot(x1 + w1/2 - x2, y1 - y2 - h2)
            # return the minimum distance
            return min(distA, distB, distC, distD, distE)
        elif down and right:
            # top left corner of contour1 to bottom right corner of contour2
            distA = math.hypot(x1 - x2 - w2, y1 - y2 - h2)
            # top right corner of contour1 to bottom right corner of contour2
            distB = math.hypot(x1 + w1 - x2 - w2, y1 - y2 - h2)
            # bottom left corner of contour1 to bottom right corner of contour2
            distC = math.hypot(x1 - x2 - w2, y1 + h1 - y2 - h2)
            # middle of top side of contour1 to bottom right corner of contour2
            distD = math.hypot(x1 + w1/2 - x2 - w2, y1 - y2 - h2)
            # middle of left side of contour1 to bottom right corner of contour2
            distE = math.hypot(x1 - x2 - w2, y1 + h1/2 - y2 - h2)
            # return the minimum distance
            return min(distA, distB, distC, distD, distE)
        elif up:
            # middle of bottom side of contour1 to top side of contour2
            return math.hypot(x1 + w1/2 - x2, y1 + h1 - y2)
        elif down:
            # middle of top side of contour1 to bottom side of contour2
            return math.hypot(x1 + w1/2 - x2, y1 - y2 - h2)
        elif left:
            # middle of right side of contour1 to left side of contour2
            return math.hypot(x1 + w1 - x2, y1 + h1/2 - y2)
        elif right:
            # middle of left side of contour1 to right side of contour2
            return math.hypot(x1 - x2 - w2, y1 + h1/2 - y2)
        else:
            return 0
    
    # Merge two contours, returns the merged contour
    # @param contour1: The first contour
    # @param contour2: The second contour
    # @return: The merged contour
    def mergeContours(self, contour1, contour2):
        return np.concatenate((contour1, contour2), axis=0)

    # Cluster contours, returns a list of contours
    # Clusters contours by merging the two closest contours repeatedly
    # until the distance between the two closest contours is greater than
    # the threshold distance.
    # @param contours: The contours to cluster
    # NOTE: contours should be of the same object type
    # @return: A list of contours
    def clusterContours(self, contours):
        current_contours = contours
        while len(current_contours) > 1:
            min_distance = None
            min_coordinate = None

            # Find the two closest contours
            for x in range(len(current_contours)-1):
                for y in range(x+1, len(current_contours)):
                    # distance = calculate_contour_distance(current_contours[x], current_contours[y])
                    distance = self.calculateContourDistance(current_contours[x], current_contours[y])
                    if min_distance is None:
                        min_distance = distance
                        min_coordinate = (x, y)
                    elif distance < min_distance:
                        min_distance = distance
                        min_coordinate = (x, y)

            # Merge the two closest contours if the distance is less than the threshold distance
            if min_distance < self.DEFAULT_THRESHOLD_DISTANCE:
                index1, index2 = min_coordinate
                # print("Merging contours at indices {} and {}".format(index1, index2))
                # print("Contour1: {}".format(current_contours[index1]))
                # print("Contour2: {}".format(current_contours[index2]))
                current_contours[index1] = self.mergeContours(current_contours[index1], current_contours[index2])
                del current_contours[index2]
            else: 
                break

        return current_contours
    
    # Swallow inner contours, returns a list of contours
    # Determines if one contour is inside another contour,
    # and marks the inner contour for removal. This process
    # is repeated until no more inner contours are found.
    # @param contours: The contours to swallow
    # @return: A list of contours
    def swallowContours(self, contourLabelTuples):
        # get contours and labels
        current_contours = [contour for contour, _ in contourLabelTuples]
        current_labels = [label for _, label in contourLabelTuples]
        # indeces to delete
        delete_indeces = []

        # find inner contours
        # for each contour, check to see if it has any inner contours
        for a in range(len(current_contours)):
            for b in range(len(current_contours)):
                # If a and b are the same, or b has already been marked for deletion, skip
                if a==b or b in delete_indeces:
                    continue
                # Get bounding rectangles
                ax, ay, aw, ah = cv2.boundingRect(current_contours[a])
                bx, by, bw, bh = cv2.boundingRect(current_contours[b])
                # If all corners of b are inside a, have a swallow b
                if (ax < bx and ay < by and ax + aw > bx + bw and ay + ah > by + bh):
                    delete_indeces.append(b)
                # If a is larger than b, and b is at least SWALLOW_AREA_RATIO_THRESHOLD contained in a, have a swallow b
                elif(aw * ah > bw * bh):
                    x_distance = min(ax + aw, bx + bw) - max(ax, bx)
                    y_distance = min(ay + ah, by + bh) - max(ay, by)
                    if (not (x_distance > 0 and y_distance > 0)):
                        continue
                    coveredAreaofB = x_distance * y_distance
                    totalAreaofB = bw * bh
                    if (coveredAreaofB / totalAreaofB > self.SWALLOW_AREA_RATIO_THRESHOLD):
                        delete_indeces.append(b)
        
        # sort delte_indeces in reverse order to avoid index errors
        delete_indeces.sort(reverse=True)
        # delete inner contours
        for index in delete_indeces:
            del current_contours[index]
            del current_labels[index]

        # return list of tuples
        current_contourLabelTuples = [(contour, label) for contour, label in zip(current_contours, current_labels)]
        return current_contourLabelTuples