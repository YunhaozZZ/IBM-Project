import cv2
from tracking.Tracker import Tracker
from tracking.TrackedObject import TrackedObject

# Concrete class for corrective Object Tracking
class CorrectiveTracker(Tracker):
    
    # Standard resolution average (pixels) (for width of 1280 and height of 720)
    STANDARD_RESOLUTION_AVERAGE = 1000.0

    # Constructor, initializes the Corrective Tracker
    # @param config: The configuration object that stores the settings the project is running on
    def __init__(self, config, resolution):
        # Get the options from the config file
        self.DEFAULT_TRACKER_THRESHOLD = config.getfloat('CorrectiveTracker', 'DEFAULT_TRACKER_THRESHOLD')

        # Convert the resolution into pixel thresholds
        #       (DEFAULT_TRACKER_THRESHOLD) 
        resolutionWidth = resolution[0]
        resolutionHeight = resolution[1]
        resolutionAverage = (resolutionWidth + resolutionHeight) / 2
        self.DEFAULT_TRACKER_THRESHOLD = self.DEFAULT_TRACKER_THRESHOLD * resolutionAverage / self.STANDARD_RESOLUTION_AVERAGE
        # Call the parent constructor
        super().__init__()
    
    # Concrete method for updating the tracker, returns a list of tuples (contour, label)
    # For each contour to update, the method finds the closest tracked object and
    # updates the tracked object with the contour's bounding rectangle.
    # NOTE: update will only assign a contour to a tracked object if the contour's label
    #       matches the tracked object's label.
    # @param contoursToUpdate: The contours to update the tracker with
    # @return: A list of tuples (contour, label)
    def update(self, contoursToUpdate):
        # Initialize the updated tracked objects dictionary
        updatedTrackedObjects = dict[int, TrackedObject]([])
        updatedTrackedObjects = self.trackedObjects.copy()
        # Initialize the updated IDs list
        updatedIds = []

        # For each contour to update, find the closest tracked object
        for updateContour, label in contoursToUpdate:
            # Initialize the minimum distance and ID
            minDist = self.DEFAULT_TRACKER_THRESHOLD
            minDistId = -1
            # Get the bounding rectangle of the contour
            rect = cv2.boundingRect(updateContour)
            # Find out if that object was detected already
            for id in self.trackedObjects:
                # Get the tracked object
                existingObject = self.trackedObjects[id]
                # Check if the label is the same
                if existingObject.getLabel() != label:
                    # If not, skip
                    continue
                # Calculate distance between edges of contours
                dist = self.calculateObjectDistance(rect, existingObject)
                # If the distance is less than the minimum distance, update the minimum distance and ID
                if dist < minDist:
                    minDist = dist
                    minDistId = id
            # If a satisfactory object is found, update the tracked object
            if minDistId != -1:
                updatedTrackedObjects[minDistId].updatePosition(rect)
                updatedIds.append(minDistId)
            else:
                # New object is detected: we assign a new ID to that object
                newObject = TrackedObject(self.idCount, rect, label)
                updatedTrackedObjects[self.idCount] = newObject
                updatedIds.append(self.idCount)
                self.idCount += 1

        # Clean the dictionary by box points to remove IDS not used anymore
        for id in self.trackedObjects:
            if id not in updatedIds:
                updatedTrackedObjects.pop(id)

        # Update dictionary with IDs not used removed
        self.trackedObjects = updatedTrackedObjects.copy()
        return
    
