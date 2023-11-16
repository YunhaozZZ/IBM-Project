import unittest
import cv2
import numpy as np
import sys

sys.path.append('./core/admin/')
sys.path.append('./core/admin/tracker')

from config.config_gen import readConfigFile
from identification.ColoredObjectIdentifier import ColoredObjectIdentifier as coi
from identification.TrashObjectIdentifier import TrashObjectIdentifier as toi
from tracking.CorrectiveTracker import CorrectiveTracker as ct
from tracking.PredictiveTracker import PredictiveTracker as pt

class CorrectiveTrackerTests(unittest.TestCase):

    def testNoItemsTracked(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/NoItemsTracked.mp4")

        # Get the video resolution
        videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (videoWidth, videoHeight)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            assert len(
                trackedObjects) == 0, "an item was tracked when there were no items to track"

    def testBlueObjTracked(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # set global id and color
        objID = 0
        objectColor = "blue"

        # Initialize the camera
        cap = cv2.VideoCapture("./core/admin/testing/testData/blueObj.mp4")

        # Get the video resolution
        videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (videoWidth, videoHeight)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            # make sure there is only one object tracked
            assert len(
                trackedObjects) == 1, "more or less than one item was tracked"

            # make sure the id and color are the same as in the first frame
            assert trackedObjects[0].getId(
            ) == objID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[0].getLabel(
            ) == objectColor, "the color of the tracked object is not the same as the first frame"

    def testBlueOrangeObjTracked(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # set global id and color (will be initalized in the first frame)
        firstObjID = 0
        firstObjColor = "blue"

        secondObjID = 1
        secondObjColor = "orange"

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/blueOrangeObj.mp4")

        # Get the video resolution
        videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (videoWidth, videoHeight)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            # make sure there is only two objects tracked
            assert len(
                trackedObjects) == 2, "more or less than one item was tracked"

            # make sure the ids and colors are the same as in the first frame
            assert trackedObjects[0].getId(
            ) == firstObjID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[0].getLabel(
            ) == firstObjColor, "the color of the tracked object is not the same as the first frame"

            assert trackedObjects[1].getId(
            ) == secondObjID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[1].getLabel(
            ) == secondObjColor, "the color of the tracked object is not the same as the first frame"

    def testRedGreenBlueOrangeObjTracked(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # set global id and color
        firstObjID = 0
        firstObjColor = "red"

        secondObjID = 1
        secondObjColor = "green"

        thirdObjID = 2
        thirdObjColor = "blue"

        fourthObjID = 3
        fourthObjColor = "orange"

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/redGreenblueOrangeObj.mp4")

        # Get the video resolution
        videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (videoWidth, videoHeight)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            # make sure there are exactly four objects tracked
            assert len(
                trackedObjects) == 4, "more or less than one item was tracked"

            # make sure the id is the same as the first frame
            assert trackedObjects[0].getId(
            ) == firstObjID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[0].getLabel(
            ) == firstObjColor, "the color of the tracked object is not the same as the first frame"

            assert trackedObjects[1].getId(
            ) == secondObjID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[1].getLabel(
            ) == secondObjColor, "the color of the tracked object is not the same as the first frame"

            assert trackedObjects[2].getId(
            ) == thirdObjID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[2].getLabel(
            ) == thirdObjColor, "the color of the tracked object is not the same as the first frame"

            assert trackedObjects[3].getId(
            ) == fourthObjID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[3].getLabel(
            ) == fourthObjColor, "the color of the tracked object is not the same as the first frame"

    def testRedObjTracked(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # set global id and color
        globalID = 0
        globalColor = "red"

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/redSkittleTracking.mp4")

        # Get the video resolution
        videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (videoWidth, videoHeight)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            # make sure there is only one object tracked
            assert len(
                trackedObjects) == 1, "more or less than one item was tracked"

            # make sure the id and color are the same as in the first frame
            assert trackedObjects[0].getLabel(
            ) == globalColor, "the color of the tracked object must be red"

            assert trackedObjects[0].getId(
            ) == globalID, "the id of the tracked object is not the same as the first frame"

    def testGreenObjTracked(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # set global id and color
        objID = 0
        objColor = "green"

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/greenSkittleTracking.mp4")

        # Get the video resolution
        videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (videoWidth, videoHeight)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            # make sure there is only one object tracked
            assert len(
                trackedObjects) == 1, "more or less than one item was tracked"

            # make sure the id is the same as the first frame
            assert trackedObjects[0].getId(
            ) == objID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[0].getLabel(
            ) == objColor, "the color of the tracked object is not the same as the first frame"

    def testYellowObjTracked(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # set global id and color
        globalID = 0
        globalColor = "yellow"

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/yellowSkittleTracking.mp4")

        # Get the video resolution
        videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (videoWidth, videoHeight)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            # make sure there is only one object tracked
            assert len(
                trackedObjects) == 1, "more or less than one item was tracked"

            # make sure the id is the same as the first frame
            assert trackedObjects[0].getId(
            ) == globalID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[0].getLabel(
            ) == globalColor, "the color of the tracked object is not the same as the first frame"

    def testOrangeObjTracked(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # set global id and color
        globalID = 0
        globalColor = "orange"

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/orangeSkittleTracking.mp4")

        # Get the video resolution
        videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (videoWidth, videoHeight)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            # make sure there is only one object tracked
            assert len(
                trackedObjects) == 1, "more or less than one item was tracked"

            # make sure the id and color are the same as in the first frame
            assert trackedObjects[0].getId(
            ) == globalID, "the id of the tracked object is not the same as the first frame"
            assert trackedObjects[0].getLabel(
            ) == globalColor, "the color of the tracked object is not the same as the first frame"


if __name__ == "__main__":
    unittest.main()  # run all tests
