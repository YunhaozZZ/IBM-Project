# Tracked Object Class
class TrackedObject():
    # Constuctor for the TrackedObject class
    # @param id: The ID of the tracked object
    # @param boundingRectangle: The bounding rectangle of the tracked object
    # @param label: The label of the tracked object
    # Fields:
    #   id: The ID of the tracked object
    #   boundingRectangle: The bounding rectangle of the tracked object
    #   boundingRectangleColor: The color of the bounding rectangle of the tracked object
    #                    (Color is determined by the label of the tracked object)
    #   center: The center of the bounding rectangle of the tracked object
    #   label: The label of the tracked object
    #   trail: The trail of the tracked object
    def __init__(self, id, boundingRectangle, label):
        self.id = id
        self.boundingRectangle = boundingRectangle
        x, y, w, h = boundingRectangle
        self.boundingRectangleColor = None
        self.center = (int(x + w/2), int(y + h/2))
        self.label = label
        self.trail = []
        self.trail.append(self.center)

    # Set the bounding rectangle color
    # @param boundingRectangleColor: The color of the bounding rectangle of the tracked object
    def setBoundingRectangleColor(self, boundingRectangleColor):
        self.boundingRectangleColor = boundingRectangleColor

    # Update the position of the tracked object
    # Updates the bounding rectangle, center, and trail of the tracked object
    # @param boundingRectangle: The bounding rectangle of the tracked object
    def updatePosition(self, boundingRectangle):
        x, y, w, h = boundingRectangle
        self.boundingRectangle = boundingRectangle
        self.center = (int(x + w/2), int(y + h/2))
        self.trail.append(self.center)

    # Get the center of the tracked object
    # @return: The center of the tracked object
    def getCenter(self):
        return self.center

    # Get the ID of the tracked object
    # @return: The ID of the tracked object
    def getId(self):
        return self.id

    # Get the trail of the tracked object
    # @return: The trail of the tracked object
    def getTrail(self):
        return self.trail

    # Get the bounding rectangle of the tracked object
    # @return: The bounding rectangle of the tracked object
    def getBoundingRectangle(self):
        return self.boundingRectangle
    
    # Get the bounding rectangle color of the tracked object
    # @return: The bounding rectangle color of the tracked object
    def getBoundingRectangleColor(self):
        return self.boundingRectangleColor

    # Get the label of the tracked object
    # @return: The label of the tracked object
    def getLabel(self):
        return self.label
