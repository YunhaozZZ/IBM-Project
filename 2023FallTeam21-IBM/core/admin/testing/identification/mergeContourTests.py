import unittest
import cv2
import numpy as np
import sys

sys.path.append('./core/admin')
sys.path.append('./core/admin/tracker')
sys.path.append('./core/admin/testing')

from config.config_gen import readConfigFile
from identification.ColoredObjectIdentifier import ColoredObjectIdentifier as coi
from identification.ContourMerger import ContourMerger as cm
from tracking.CorrectiveTracker import CorrectiveTracker as ct

class contourMergerTest(unittest.TestCase):

    # Test if two contours will be merged if they are moving towards each other.
    def testTwoYellowItemMerge(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/oneYellowObjectMerged.mp4")

        # Get the video resolution
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # Get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # initialize the list of tracked objects
        trackedObjectsLength = []

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()
            trackedObjectsLength.append(len(trackedObjects))

        # these two lines below are debugging statements ment to help us see how many objects are detected at once
        # print ("Occurance of number 2: " + str(trackedObjectsLength.count(2)))
        # print ("Occurance of number 1: " + str(trackedObjectsLength.count(1)))

        assert sorted(trackedObjectsLength,
                      reverse=True) == trackedObjectsLength, "The two contours umerged"
        # the contours should be merged between 55% and 65% of the time, and not merged also between 35% and 45% of the time
        assert (trackedObjectsLength.count(2) < (
            len(trackedObjectsLength) * 0.45)) and (trackedObjectsLength.count(2) > (
            len(trackedObjectsLength) * 0.35)), f"The two contours were not merged {trackedObjectsLength.count(2)*100}% of the frames, not between 35% and 45%"

    def testSwallowContourBlue(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # Initialize the camera
        bluePenAndBook = "./core/admin/testing/testData/swallowContourBlue.jpg"

        # Get the image resolution
        frame = cv2.imread(bluePenAndBook)
        resolution = (frame.shape[1], frame.shape[0])

        # Initialize the object identifier
        objId = coi(config, resolution)

        identifyObjects = objId.identifyObjects(frame)
        assert identifyObjects[0][1] == "blue", "the tracked object is not blue"

        assert len(
            identifyObjects) == 1, "there are not only 1 contour in the image"

    # test swallow contour red
    def testSwallowContourRed(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # Initialize the camera
        redPenAndBook = "./core/admin/testing/testData/swallowContourRed2.jpg"
        frame = cv2.imread(redPenAndBook)

        # Get the image resolution
        resolution = (frame.shape[1], frame.shape[0])

        objId = coi(config, resolution)
        identifyObjects = objId.identifyObjects(frame)
        assert identifyObjects[0][1] == "red", "the tracked object is not blue"

        assert len(
            identifyObjects) == 1, "there are not only 1 contour in the image"

    # Test for two orange markers will be merged if they are moving towards each other.
    def testTwoOrangeMarkerMerge(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/twoOrangeMarkerMerge.mp4")

        # Get the video resolution
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # initialize the list of tracked objects
        trackedObjectsLength = []

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()
            trackedObjectsLength.append(len(trackedObjects))

            # If there are an incorrect number of objects in the video, then the test fails.
            assert len(trackedObjects) in (
                1, 2), f"There are {len(trackedObjects)} objects in the video when there should be 1 or 2"

        # these two lines below are debugging statements ment to help us see how many objects are detected at once
        # print ("Occurance of number 2: " + str(trackedObjectsLength.count(2)))
        # print ("Occurance of number 1: " + str(trackedObjectsLength.count(1)))

        assert sorted(trackedObjectsLength,
                      reverse=True) == trackedObjectsLength, "The two contours umerged"
        # the contours should be merged between 50% and 60% of the time, and not merged also between 40% and 50% of the time
        assert (trackedObjectsLength.count(2) < (
            len(trackedObjectsLength) * 0.50)) and (trackedObjectsLength.count(2) > (
            len(trackedObjectsLength) * 0.40)), f"The two contours were not merged {trackedObjectsLength.count(2)*100}% of the frames, not between 40% and 50%"

    # test all the frames of two green skittles in the video to see if the two objects are merging.
    def testTwoGreenSkittlesMerge(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        cap = cv2.VideoCapture("./core/admin/testing/testData/greenMerge.mp4")

        # Get the video resolution
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # initialize the list of tracked objects
        trackedObjectsLength = []

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            trackedObjectsLength.append(len(trackedObjects))

            # If there are an incorrect number of objects in the video, then the test fails.
            assert len(trackedObjects) in (
                1, 2), f"There are {len(trackedObjects)} objects in the video when there should be 1 or 2"

        # print ("Occurance of number 2: " + str(trackedObjectsLength.count(2)))
        # print ("Occurance of number 1: " + str(trackedObjectsLength.count(1)))

        assert sorted(trackedObjectsLength,
                      reverse=True) == trackedObjectsLength, "The two contours umerged"
        # the contours should be merged between 45% and 55% of the time, and not merged also between 45% and 55% of the time
        assert (trackedObjectsLength.count(2) < (
            len(trackedObjectsLength) * 0.55)) and (trackedObjectsLength.count(2) > (
            len(trackedObjectsLength) * 0.45)), f"The two contours were not merged {trackedObjectsLength.count(2)*100}% of the frames, not between 45% and 55%"

    # test all the frames of the two red skittles in the video to see if the two objects are merging.
    def testTwoRedSkittlesMerge(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        cap = cv2.VideoCapture("./core/admin/testing/testData/redMerge.mp4")

        # Get the video resolution
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # initialize the list of tracked objects
        trackedObjectsLength = []

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            trackedObjectsLength.append(len(trackedObjects))

            # If there are an incorrect number of objects in the video, then the test fails.
            assert len(trackedObjects) in (
                1, 2), f"There are {len(trackedObjects)} objects in the video when there should be 1 or 2"

        # print ("Occurance of number 2: " + str(trackedObjectsLength.count(2)))
        # print ("Occurance of number 1: " + str(trackedObjectsLength.count(1)))

        assert sorted(trackedObjectsLength,
                      reverse=True) == trackedObjectsLength, "The two contours umerged"
        # the contours should be merged between 50% and 60% of the time, and not merged also between 40% and 50% of the time
        assert (trackedObjectsLength.count(2) < (
            len(trackedObjectsLength) * 0.50)) and (trackedObjectsLength.count(2) > (
            len(trackedObjectsLength) * 0.40)), f"The two contours were not merged {trackedObjectsLength.count(2)*100}% of the frames, not between 40% and 50%"


    # Test to see if two objects of different colors will merge when close together (they shouldn't)
    def testYellowOrangeMarkerMerge(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/yellowOrangeMarkerMerge.mp4")

        # Get the video resolution
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # initialize the list of tracked objects
        trackedObjectsLength = []

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            trackedObjectsLength.append(len(trackedObjects))

            # If there are fewer than 2 objects any point in the video, then the test fails.
            # We test using greater than or equal to 2 specifically because the issue of a single object being
            # detected as two objects is an issue that should cause a colored object identifier test to fail.
            assert len(
                trackedObjects) >= 2, "failed to detect one of the objects in the video."

    # Test to see if two objects of different colors will merge when close together (they shouldn't)
    def testTwoRedOrangeSkittlesMerge(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/twoRedOrangeItems.mp4")

        # Get the video resolution
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Initialize the tracker
        tracker = ct(config, resolution)

        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # initialize the list of tracked objects
        trackedObjectsLength = []

        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            trackedObjectsLength.append(len(trackedObjects))

            # If there are fewer than 2 objects any point in the video, then the test fails.
            # We test using greater than or equal to 2 specifically because the issue of a single object being
            # detected as two objects is an issue that should cause a colored object identifier test to fail.
            assert len(
                trackedObjects) >= 2, "failed to detect one of the objects in the video."

    # Test to see if two objects of different colors will merge when close together (they shouldn't)
    def testTwoYellowGreenSkittlesMerge(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        # Initialize the camera
        cap = cv2.VideoCapture(
            "./core/admin/testing/testData/twoYellowGreenMerge.mp4")

        # Get the video resolution
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)
        
        # Initialize the tracker
        tracker = ct(config, resolution)
        
        # get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # initialize the list of tracked objects
        trackedObjectsLength = []
        
        for _ in range(num_frames):
            # Read the frame
            _, frame = cap.read()

            # Get the contours
            contourLabelTuples = objectIdentifier.identifyObjects(frame)

            tracker.update(contourLabelTuples)
            trackedObjects = tracker.getTrackedObjects()

            trackedObjectsLength.append(len(trackedObjects))

            # If there are fewer than 2 objects any point in the video, then the test fails.
            # We test using greater than or equal to 2 specifically because the issue of a single object being
            # detected as two objects is an issue that should cause a colored object identifier test to fail.
            assert len(
                trackedObjects) >= 2, "failed to detect one of the objects in the video."


if __name__ == "__main__":
    unittest.main()  # run all tests
