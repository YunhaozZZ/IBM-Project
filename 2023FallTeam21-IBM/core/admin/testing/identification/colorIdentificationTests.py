# Start a test file for color identification
#Path: core/admin/tracker/testing/colorIdentificationTest.py
import unittest
import cv2
import sys

sys.path.append('./core/admin/')
sys.path.append('./core/admin/tracker/')

from config.config_gen import readConfigFile
from identification.ColoredObjectIdentifier import ColoredObjectIdentifier as coi

# This needs to a test file for the color identification module, which is a concrete class of the abstract class ObjectIdentifier.
# This test file should test object identifcation, object identification by color, making a mask using still images from our testData folder.
class colorIdentificationTest(unittest.TestCase):
    

    # Test a red object and see if the Color Object Identifier labels this object as red and identifies a single object
    def testOneRedObjectLightBackground(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        oneRedObjectLightBackground = "./core/admin/testing/testData/oneRedObjectLightBackground.jpg"
        
        # Read the frame
        frame = cv2.imread(oneRedObjectLightBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)
        
        # Check if the label is red
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'red', "Red object not identified as red"


    def testOneOrangeObjectLightBackground(self):
        config = readConfigFile(f'./core/admin/config/default.ini')
        
        oneOrangeObjectLightBackground = "./core/admin/testing/testData/oneOrangeObjectLightBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneOrangeObjectLightBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is orange
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'orange', "Orange object not identified as orange"


    # est a yellow object and see if the Color Object Identifier labels this object as yellow and identifies a single object
    def testOneYellowObjectLightBackground(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        oneYellowObjectLightBackground = "./core/admin/testing/testData/oneYellowObjectLightBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneYellowObjectLightBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is yellow
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'yellow', "Yellow Wax not identified as yellow"


    # Test a green object and see if the Color Object Identifier labels this object as green and identifies a single object
    def testOneGreenObjectLightBackground(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        oneGreenObjectLightBackground = "./core/admin/testing/testData/oneGreenObjectLightBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneGreenObjectLightBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is green
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'green', "Green object not identified as green"

    
    # Test a blue object and see if the Color Object Identifier labels this object as blue and identifies a single object
    def testOneBlueObjectLightBackground(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        oneBlueObjectLightBackground = "./core/admin/testing/testData/oneBlueObjectLightBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneBlueObjectLightBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is blue
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'blue', "Blue object not identified as blue"

    
    # Test a purple object and see if the Color Object Identifier labels this object as purple and identifies a single object
    def testOnePurpleObjectLightBackground(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        onePurpleObjectLightBackground = "./core/admin/testing/testData/onePurpleObjectLightBackground.jpg"

        # Read the frame
        frame = cv2.imread(onePurpleObjectLightBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is purple
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'purple', "Purple object not identified as purple"


    def testAllObjectsLightBackground(self):
        config = readConfigFile(f'./core/admin/config/default.ini')

        allObjectsLightBackground = "./core/admin/testing/testData/allObjectsLightBackground.jpg"

        # Read the frame
        frame = cv2.imread(allObjectsLightBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if each object was labeled correctly
        assert len(identifiedObjects) == 6, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        
        red, orange, yellow, green, blue, purple = False, False, False, False, False, False
        for object in identifiedObjects:
            if object[1] == 'red':
                red = True
            elif object[1] == 'orange':
                orange = True
            elif object[1] == 'yellow':
                yellow = True
            elif object[1] == 'green':
                green = True
            elif object[1] == 'blue':
                blue = True
            elif object[1] == 'purple':
                purple = True

        assert red, "Red object not identified"
        assert orange, "Orange object not identified"
        assert yellow, "Yellow object not identified"
        assert green, "Green object not identified"
        assert blue, "Blue object not identified"
        assert purple, "Purple object not identified"


    def testOneRedObjectDarkBackground(self):
        config = readConfigFile(f'./core/admin/config/defaultDark.ini')

        oneRedObjectDarkBackground = "./core/admin/testing/testData/oneRedObjectDarkBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneRedObjectDarkBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is red
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'red', "Red object not identified as red"


    def testOneOrangeObjectDarkBackground(self):
        config = readConfigFile(f'./core/admin/config/defaultDark.ini')

        oneOrangeObjectDarkBackground = "./core/admin/testing/testData/oneOrangeObjectDarkBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneOrangeObjectDarkBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is orange
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'orange', "Orange object not identified as orange"


    def testOneYellowObjectDarkBackground(self):
        config = readConfigFile(f'./core/admin/config/defaultDark.ini')

        oneYellowObjectDarkBackground = "./core/admin/testing/testData/oneYellowObjectDarkBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneYellowObjectDarkBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is yellow
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'yellow', "Yellow object not identified as yellow"


    def testOneGreenObjectDarkBackground(self):
        config = readConfigFile(f'./core/admin/config/defaultDark.ini')

        oneGreenObjectDarkBackground = "./core/admin/testing/testData/oneGreenObjectDarkBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneGreenObjectDarkBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is green
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'green', "Green object not identified as green"


    def testOneBlueObjectDarkBackground(self):
        config = readConfigFile(f'./core/admin/config/defaultDark.ini')

        oneBlueObjectDarkBackground = "./core/admin/testing/testData/oneBlueObjectDarkBackground.jpg"

        # Read the frame
        frame = cv2.imread(oneBlueObjectDarkBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is blue
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'blue', "Blue object not identified as blue"

    
    def testOnePurpleObjectDarkBackground(self):
        config = readConfigFile(f'./core/admin/config/defaultDark.ini')

        onePurpleObjectDarkBackground = "./core/admin/testing/testData/onePurpleObjectDarkBackground.jpg"

        # Read the frame
        frame = cv2.imread(onePurpleObjectDarkBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if the label is purple
        assert len(identifiedObjects) == 1, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        assert identifiedObjects[0][1] == 'purple', "Purple object not identified as purple"


    def testAllObjectsDarkBackground(self):
        config = readConfigFile(f'./core/admin/config/defaultDark.ini')

        allObjectsDarkBackground = "./core/admin/testing/testData/allObjectsDarkBackground.jpg"

        # Read the frame
        frame = cv2.imread(allObjectsDarkBackground)

        # Get the image resolution
        height, width, _ = frame.shape
        resolution = (width, height)

        # Initialize the object identifier
        objectIdentifier = coi(config, resolution)

        # Get the contours
        identifiedObjects = objectIdentifier.identifyObjects(frame)

        # Check if each object was labeled correctly
        assert len(identifiedObjects) == 6, f"Incorrect amount of objects identified: {len(identifiedObjects)}"
        
        red, orange, yellow, green, blue, purple = False, False, False, False, False, False
        for object in identifiedObjects:
            if object[1] == 'red':
                red = True
            elif object[1] == 'orange':
                orange = True
            elif object[1] == 'yellow':
                yellow = True
            elif object[1] == 'green':
                green = True
            elif object[1] == 'blue':
                blue = True
            elif object[1] == 'purple':
                purple = True

        assert red, "Red object not identified"
        assert orange, "Orange object not identified"
        assert yellow, "Yellow object not identified"
        assert green, "Green object not identified"
        assert blue, "Blue object not identified"
        assert purple, "Purple object not identified"


if __name__ == "__main__":
    unittest.main() # run all tests
