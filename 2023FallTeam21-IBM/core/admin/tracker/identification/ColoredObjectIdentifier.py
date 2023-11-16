import cv2
import numpy as np

from identification.ObjectIdentifier import ObjectIdentifier
from identification.ContourMerger import ContourMerger
from identification.Labels import Colors

# Concrete class for object identification by the 6 colors: red, green, blue, yellow, purple, orange
class ColoredObjectIdentifier(ObjectIdentifier):
    
    # Standard resolution average (pixels) (for width of 1280 and height of 720)
    STANDARD_RESOLUTION_AREA = 1280.0 * 720.0

    # Initializes the Colored Object Identifier and its options
    # @param config: The configuration object that stores the settings the project is running on
    def __init__(self, config, resolution):
        # Get the options from the config file
        self.CVT_COLOR_CODE = config.getint('ColoredObjectIdentifier', 'CVT_COLOR_CODE')
        self.ERODE_ITERATIONS = config.getint('ColoredObjectIdentifier', 'ERODE_ITERATIONS')
        self.DILATE_ITERATIONS = config.getint('ColoredObjectIdentifier', 'DILATE_ITERATIONS')
        self.MINIMUM_CONTOUR_AREA = config.getint('ColoredObjectIdentifier', 'MINIMUM_CONTOUR_AREA')
        self.SWALLOW_INNER_CONTOURS = config.getboolean('ColoredObjectIdentifier', 'SWALLOW_INNER_CONTOURS')
        self.SWALLOW_SAME_COLOR_INNER_CONTOURS = config.getboolean('ColoredObjectIdentifier', 'SWALLOW_SAME_COLOR_INNER_CONTOURS')
        self.RED_LOWER1 = np.array(config.getlist('ColoredObjectIdentifier', 'RED_LOWER1'))
        self.RED_UPPER1 = np.array(config.getlist('ColoredObjectIdentifier', 'RED_UPPER1'))
        self.RED_LOWER2 = np.array(config.getlist('ColoredObjectIdentifier', 'RED_LOWER2'))
        self.RED_UPPER2 = np.array(config.getlist('ColoredObjectIdentifier', 'RED_UPPER2'))
        self.GREEN_LOWER = np.array(config.getlist('ColoredObjectIdentifier', 'GREEN_LOWER'))
        self.GREEN_UPPER = np.array(config.getlist('ColoredObjectIdentifier', 'GREEN_UPPER'))
        self.BLUE_LOWER = np.array(config.getlist('ColoredObjectIdentifier', 'BLUE_LOWER'))
        self.BLUE_UPPER = np.array(config.getlist('ColoredObjectIdentifier', 'BLUE_UPPER'))
        self.YELLOW_LOWER = np.array(config.getlist('ColoredObjectIdentifier', 'YELLOW_LOWER'))
        self.YELLOW_UPPER = np.array(config.getlist('ColoredObjectIdentifier', 'YELLOW_UPPER'))
        self.PURPLE_LOWER = np.array(config.getlist('ColoredObjectIdentifier', 'PURPLE_LOWER'))
        self.PURPLE_UPPER = np.array(config.getlist('ColoredObjectIdentifier', 'PURPLE_UPPER'))
        self.ORANGE_LOWER = np.array(config.getlist('ColoredObjectIdentifier', 'ORANGE_LOWER'))
        self.ORANGE_UPPER = np.array(config.getlist('ColoredObjectIdentifier', 'ORANGE_UPPER'))

        # Convert the resolution into pixel thresholds
        resolutionWidth = resolution[0]
        resolutionHeight = resolution[1]
        resolutionArea = resolutionWidth * resolutionHeight
        self.MINIMUM_CONTOUR_AREA = self.MINIMUM_CONTOUR_AREA * resolutionArea / self.STANDARD_RESOLUTION_AREA
        # Initialize the contour merger
        self.contourMerger = ContourMerger(config, resolution)
        # Call the parent constructor
        super().__init__()

    # Make a mask for the color, returns the mask
    # @param hsvFrame: The HSV frame to make a mask for
    # @param lower: The lower bound of the color
    # @param upper: The upper bound of the color
    # @return: The mask
    def makeMask(self, hsvFrame, lower, upper):
        mask = cv2.inRange(hsvFrame, lower, upper)
        mask = self.cleanNoise(mask, self.ERODE_ITERATIONS, self.DILATE_ITERATIONS)
        return mask

    # Identify objects by color, returns a list of tuples (contour, label)
    # Gets the contours for the specific color mask, merges the contours,
    # swallows inner contours, and assigns labels to the contours.
    # @param mask: The mask to identify objects in
    # @param color: The color to identify objects by
    # @return: A list of tuples (contour, label)
    def identifyObjectsByColor(self, mask, color):
        # Find contours in the mask
        contours = self.defineContours(mask)
        # Merge contours
        contours = [contour for contour in contours if cv2.contourArea(contour) > self.MINIMUM_CONTOUR_AREA]
        contours = self.contourMerger.clusterContours(contours)
        # Assign labels
        tuples = self.assignLabels(contours, color)
        if self.SWALLOW_SAME_COLOR_INNER_CONTOURS:
            tuples = self.contourMerger.swallowContours(tuples)
        return tuples

    # Concrete definition for object identification, returns a list of tuples (contour, label)
    # Creates mask for every color, identifies objects by color, and returns the compiled list of tuples
    # @param image: The image to identify objects in
    # @return: A list of tuples (contour, label)
    def identifyObjects(self, image):
        # Convert the image to HSV
        hsvFrame = cv2.cvtColor(image, self.CVT_COLOR_CODE)
        # Initialize the list of masks
        masks = []
        # Threshold the HSV image to get only red colors
        redMask1 = self.makeMask(hsvFrame, self.RED_LOWER1, self.RED_UPPER1)
        redMask2 = self.makeMask(hsvFrame, self.RED_LOWER2, self.RED_UPPER2)
        redMask = cv2.bitwise_or(redMask1, redMask2)
        masks.append(redMask)
        # Threshold the HSV image to get only green colors
        greenMask = self.makeMask(hsvFrame, self.GREEN_LOWER, self.GREEN_UPPER)
        masks.append(greenMask)
        # Threshold the HSV image to get only blue colors
        blueMask = self.makeMask(hsvFrame, self.BLUE_LOWER, self.BLUE_UPPER)
        masks.append(blueMask)
        # Threshold the HSV image to get only yellow colors
        yellowMask = self.makeMask(hsvFrame, self.YELLOW_LOWER, self.YELLOW_UPPER)
        masks.append(yellowMask)
        # Threshold the HSV image to get only purple colors
        purpleMask = self.makeMask(hsvFrame, self.PURPLE_LOWER, self.PURPLE_UPPER)
        masks.append(purpleMask)
        # Threshold the HSV image to get only orange colors
        orangeMask = self.makeMask(hsvFrame, self.ORANGE_LOWER, self.ORANGE_UPPER)
        masks.append(orangeMask)
        # Compile the list of tuples
        colorTuples = []
        for i in range(len(masks)):
            colorTuples += self.identifyObjectsByColor(masks[i], Colors.labels[i])
        # If SWALLOW_INNER_CONTOURS is true, swallow all inner contours
        if self.SWALLOW_INNER_CONTOURS:
            colorTuples = self.contourMerger.swallowContours(colorTuples)
        return colorTuples


    