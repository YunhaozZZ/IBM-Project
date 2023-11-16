import cv2
import sys
import glob
import numpy as np

sys.path.append('./core/admin/tracker')
sys.path.append('./core/admin/')

from config.config_gen import readConfigFile
from identification.Labels import Colors
from identification.Labels import TrashTypes
from identification.ColoredObjectIdentifier import ColoredObjectIdentifier as coi
from identification.TrashObjectIdentifier import TrashObjectIdentifier as toi
from tracking.CorrectiveTracker import CorrectiveTracker as ct
from tracking.PredictiveTracker import PredictiveTracker as pt

# Get the name of the config file from user input
# configFileName = input('Enter the name of the config file: ')
configFileName = 'default'

# Read the config file
config = readConfigFile(f'./core/admin/config/{configFileName}.ini')

# Static Variables: Customizable Options
# Vertical offset between box and label text
LABEL_DISPLAY_HEIGHT = config.getint('TrashTrack2', 'LABEL_DISPLAY_HEIGHT')
# Path to the video file
VIDEO_PATH = './core/admin/testing/testData/redGreenblueOrangeObj.mp4'

def analyzeFrame(frame, objectIdentifier, tracker):
    # Get the contours
    contourLabelTuples = objectIdentifier.identifyObjects(frame)
    # Draw the contours
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
        x,y,_,_ = trackedObject.getBoundingRectangle()
        cv2.putText(frame, str(trackedObject.getLabel()), (x, y - LABEL_DISPLAY_HEIGHT), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw TrackedObject ID (Debuggging)
        cv2.putText(frame, str(trackedObject.getId()), trackedObject.getCenter(), 
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2)


def showVideoFrames(videoPath):
    # Read the video
    cap = cv2.VideoCapture(videoPath)

    # Get the video resolution
    videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    resolution = (videoWidth, videoHeight)

    # Initialize the object identifier
    objectIdentifier = coi(config, resolution)

    # Initialize the tracker
    tracker = ct(config, resolution)

    # Read the video into a list of identified and tracked frames
    videoFrames = []
    
    # STORE FRAMES
    # Initialize the frame number counter
    i = 0
    while True:
        # Read an image frame
        _, frame = cap.read()

        # If there are no more frames, break
        if frame is None:
            break

        # Analyze the frame
        analyzeFrame(frame, objectIdentifier, tracker)

        # increment the frame number counter
        i += 1

        # draw the frame number in the top left corner
        cv2.putText(frame, str(i), (0, 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Resize the frame for viewing
        while frame.shape[0] > config.getint('TrashTrack2', 'DISPLAY_HEIGHT') or frame.shape[1] > config.getint('TrashTrack2', 'DISPLAY_WIDTH'):
            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Store the frame in the videoFrames list
        videoFrames.append(frame)

    return videoFrames

# Shows the frames of a specified video file in a sequence
def main():

    videoPaths = glob.glob("./core/admin/testing/testData/*.mp4")
    videoPathFrames = [[]] * len(videoPaths)

    # Exit if q is pressed
    # Initialize the run variable
    run = True
    # Initialize the video counter
    i = 0
    while True:

        # SELECT VIDEO, 
        # go to previous video if a is pressed, 
        # go to next video if d (or any other key) is pressed,
        # to select a video, press space
        while True:
            # Show a frame with the video name
            videoName = videoPaths[i].split("\\")[-1].split(".")[0]
            frame = np.full([720,720,3], 1, dtype=np.uint8)
            cv2.putText(frame, videoName, (0, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('frame', frame)
            key = cv2.waitKey(0) & 0xFF
            if key == ord('q'):
                cv2.destroyAllWindows()
                run = False
                break
            elif key == ord(' '):
                cv2.destroyAllWindows()
                break
            elif key == ord('a'):
                i -= 1
                if i < 0:
                    i = len(videoPaths) - 1
            else:
                i += 1
                if i >= len(videoPaths):
                    i = 0
        if not run:
            break

        # Read the video, or get the frames from memory
        if len(videoPathFrames[i]) == 0:
            videoPathFrames[i] = showVideoFrames(videoPaths[i])

        # DISPLAY FRAMES
        # Initialize the frame counter
        j = 0
        while True:
            # Show the frame
            cv2.imshow('frame', videoPathFrames[i][j])
            # Exit if q is pressed
            # If a is pressed, go back one frame
            key = cv2.waitKey(0) & 0xFF
            if key == ord('q'):
                cv2.destroyAllWindows()
                break
            elif key == ord('a'):
                j -= 1
                if j < 0:
                    j = len(videoPathFrames[i]) - 1
            else:
                j += 1
                if j >= len(videoPathFrames[i]):
                    j = 0

if __name__ == '__main__':
    main()