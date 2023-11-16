import cv2

# Abstract class for object identification
class ObjectIdentifier():

    # Static Variables: Customizable Options
    # Contour Retrieval Mode
    FIND_CONTOURS_MODE = cv2.RETR_TREE # cv2.RETR_EXTERNAL
    # Contour Approximation Method
    FIND_CONTOURS_METHOD = cv2.CHAIN_APPROX_SIMPLE

    # Clean noise from the image, returns the cleaned image
    # @param image: The image to clean
    # @param erodeIter: The number of iterations for erosion
    # @param dilateIter: The number of iterations for dilation
    # @return: The cleaned image
    def cleanNoise(self, image, erodeIter, dilateIter):
        return cv2.dilate(cv2.erode(image, None, iterations=erodeIter), None, iterations=dilateIter)

    # Define contours in the image, returns a list of contours
    # @param image: The image to define contours in
    # @return: A list of contours
    def defineContours(self, image):
        return cv2.findContours(image, self.FIND_CONTOURS_MODE, self.FIND_CONTOURS_METHOD)[-2]
    
    # Assign a label to a contour, returns a tuple (contour, label)
    # @param contour: The contour to assign a label to
    # @param label: The label to assign to the contour
    # @return: A tuple (contour, label)
    def assignLabel(self, contour, label):
        return (contour, label)
    
    # Assign labels to contours, returns a list of tuples (contour, label)
    # @param contours: The contours to assign labels to
    # @param label: The label to assign to the contours
    # @return: A list of tuples (contour, label)
    def assignLabels(self, contours, label):
        return [self.assignLabel(contour, label) for contour in contours]

    # Abstract method for object identification, returns a list of tuples (contour, label)
    def identifyObjects(self, image):
        pass

    
    
    