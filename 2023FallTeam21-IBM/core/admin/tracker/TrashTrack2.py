import cv2
import sys

sys.path.append('./core/admin/')

from config.config_gen import readConfigFile
from identification.Labels import Colors
from identification.Labels import TrashTypes
from identification.ColoredObjectIdentifier import ColoredObjectIdentifier as coi
from identification.TrashObjectIdentifier import TrashObjectIdentifier as toi
from tracking.CorrectiveTracker import CorrectiveTracker as ct
from tracking.PredictiveTracker import PredictiveTracker as pt

# Get the name of the config file from user input
configFileName = input('Enter the name of the config file: ')

# Read the config file
config = readConfigFile(f'./core/admin/config/{configFileName}.ini')

# Static Variables: Customizable Options
# Vertical offset between box and label text
LABEL_DISPLAY_HEIGHT = config.getint('TrashTrack2', 'LABEL_DISPLAY_HEIGHT')
# Capture resolution
DISPLAY_WIDTH = config.getint('TrashTrack2', 'DISPLAY_WIDTH')
DISPLAY_HEIGHT = config.getint('TrashTrack2', 'DISPLAY_HEIGHT')

def showFrame(frame, objectIdentifier, tracker):
    # Get the contours
    contourLabelTuples = objectIdentifier.identifyObjects(frame)

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
        x,y,_,_ = trackedObject.getBoundingRectangle()
        cv2.putText(frame, str(trackedObject.getLabel()), (x, y - LABEL_DISPLAY_HEIGHT), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw TrackedObject ID 
        cv2.putText(frame, str(trackedObject.getId()), trackedObject.getCenter(), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('frame', frame)


def main():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, DISPLAY_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DISPLAY_HEIGHT)

    # Get the resolution of the camera
    resolutionWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    resolutionHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    resolution = (resolutionWidth, resolutionHeight)

    # Initialize the object identifier
    objectIdentifier = coi(config, resolution)

    # Initialize the tracker
    tracker = ct(config, resolution)

    while True:
        # Read an image frame
        _, frame = cap.read()
        if config.getboolean('TrashTrack2', 'FLIP_CAMERA'):
            frame = cv2.flip(frame, 1)

        # Analyze and show the frame
        showFrame(frame, objectIdentifier, tracker)

        # Exit if q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()