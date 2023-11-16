import cv2
import sys
import glob

sys.path.append('./core/admin/tracker')
sys.path.append('./core/admin/')

from tracking.PredictiveTracker import PredictiveTracker as pt
from tracking.CorrectiveTracker import CorrectiveTracker as ct
from identification.TrashObjectIdentifier import TrashObjectIdentifier as toi
from identification.ColoredObjectIdentifier import ColoredObjectIdentifier as coi
from identification.Labels import TrashTypes
from identification.Labels import Colors
from config.config_gen import readConfigFile

# Get the name of the config file from user input
# configFileName = input('Enter the name of the config file: ')
configFileName = 'default'

# Read the config file
config = readConfigFile(f'./core/admin/config/{configFileName}.ini')

# Static Variables: Customizable Options
# Vertical offset between box and label text
LABEL_DISPLAY_HEIGHT = config.getint('TrashTrack2', 'LABEL_DISPLAY_HEIGHT')

def showIdentifiedImage(imagePath):
    # Read an image frame
    frame = cv2.imread(imagePath)

    # Get the image resolution
    imageHeight, imageWidth, _ = frame.shape
    resolution = (imageWidth, imageHeight)

    # Create the object identifier
    objectIdentifier = coi(config, resolution)

    # Create the tracker
    tracker = ct(config, resolution)

    # Get and draw the contours
    contourLabelTuples = objectIdentifier.identifyObjects(frame)
    for contour, label in contourLabelTuples:
        cv2.drawContours(frame, [contour], -1, Colors.labelColor(label), 2)

    # Update the tracker
    tracker.update(contourLabelTuples)

    # Draw the contours
    trackedObjects = tracker.getTrackedObjects()
    for id in trackedObjects:
        trackedObject = trackedObjects[id]
        # Draw the bounding rectangle
        cv2.rectangle(frame, trackedObject.getBoundingRectangle(),
                      Colors.labelColor(trackedObject.getLabel()), 2)

        # Draw the label
        x, y, _, _ = trackedObject.getBoundingRectangle()
        cv2.putText(frame, str(trackedObject.getLabel()), (x, y - LABEL_DISPLAY_HEIGHT),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Get the text between the last slash and the period in the file path of the image
    imageName = imagePath.split("\\")[-1].split(".")[0]

    # Halve the size of the image until it fits on the screen
    while frame.shape[0] > config.getint('TrashTrack2', 'DISPLAY_HEIGHT') or frame.shape[1] > config.getint('TrashTrack2', 'DISPLAY_WIDTH'):
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Draw the name of the image in the top left corner
    cv2.putText(frame, imageName, (0, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('frame', frame)


# Shows the images in the testData folder in sequence
def main():
    imagePaths = glob.glob("./core/admin/testing/testData/*.jpg")

    # Exit if q is pressed,
    # go to previous image if a is pressed,
    # go to next image if d (or any other key) is pressed
    i = 0
    while True:
        showIdentifiedImage(imagePaths[i])
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
        elif key == ord('a'):
            i -= 1
            if i < 0:
                i = len(imagePaths) - 1
        else:
            i += 1
            if i >= len(imagePaths):
                i = 0


if __name__ == '__main__':
    main()
