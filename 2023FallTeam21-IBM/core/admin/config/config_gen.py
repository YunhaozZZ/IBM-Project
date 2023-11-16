import configparser
import cv2

# Helper method to read a config file and return a ConfigParser object
def readConfigFile(path):
    config = configparser.ConfigParser(converters={'list': lambda x: [int(i.strip()) for i in x.split(',')]})
    config.read(path)
    return config

def main():
    config = configparser.ConfigParser()

    # Add sections to the config file
    config.add_section('TrashTrack2')
    config.add_section('ColoredObjectIdentifier')
    config.add_section('ContourMerger')
    config.add_section('CorrectiveTracker')

    # Add options to the TrashTrack2 section
    config.set('TrashTrack2', 'LABEL_DISPLAY_HEIGHT', '10')
    config.set('TrashTrack2', 'DISPLAY_WIDTH', '1280')
    config.set('TrashTrack2', 'DISPLAY_HEIGHT', '720')
    config.set('TrashTrack2', 'FLIP_CAMERA', 'False')

    # Add options to the ColoredObjectIdentifier section
    config.set('ColoredObjectIdentifier', 'CVT_COLOR_CODE', f"{cv2.COLOR_BGR2HSV}")
    config.set('ColoredObjectIdentifier', 'ERODE_ITERATIONS', '1')
    config.set('ColoredObjectIdentifier', 'DILATE_ITERATIONS', '2')
    config.set('ColoredObjectIdentifier', 'MINIMUM_CONTOUR_AREA', '400')
    config.set('ColoredObjectIdentifier', 'SWALLOW_INNER_CONTOURS', 'False')
    config.set('ColoredObjectIdentifier', 'SWALLOW_SAME_COLOR_INNER_CONTOURS', 'True')
    config.set('ColoredObjectIdentifier', 'RED_LOWER1', '170, 100, 100')
    config.set('ColoredObjectIdentifier', 'RED_UPPER1', '180, 255, 255')
    config.set('ColoredObjectIdentifier', 'RED_LOWER2', '0, 100, 100')
    config.set('ColoredObjectIdentifier', 'RED_UPPER2', '5, 255, 255')
    config.set('ColoredObjectIdentifier', 'GREEN_LOWER', '45, 75, 50')
    config.set('ColoredObjectIdentifier', 'GREEN_UPPER', '90, 255, 255')
    config.set('ColoredObjectIdentifier', 'BLUE_LOWER', '100, 100, 75')
    config.set('ColoredObjectIdentifier', 'BLUE_UPPER', '129, 255, 255')
    config.set('ColoredObjectIdentifier', 'YELLOW_LOWER', '20, 75, 100')
    config.set('ColoredObjectIdentifier', 'YELLOW_UPPER', '40, 255, 255')
    config.set('ColoredObjectIdentifier', 'PURPLE_LOWER', '130, 75, 50')
    config.set('ColoredObjectIdentifier', 'PURPLE_UPPER', '160, 255, 255')
    config.set('ColoredObjectIdentifier', 'ORANGE_LOWER', '6, 100, 125')
    config.set('ColoredObjectIdentifier', 'ORANGE_UPPER', '19, 255, 255')

    # Add options to the ContourMerger section
    config.set('ContourMerger', 'DEFAULT_THRESHOLD_DISTANCE', '50.0')
    config.set('ContourMerger', 'SWALLOW_AREA_RATIO_THRESHOLD', '.5')

    # Add options to the CorrectiveTracker section
    config.set('CorrectiveTracker', 'DEFAULT_TRACKER_THRESHOLD', '150.0')

    # Get a name for the config file from the user
    configFileName = input('Enter the name of the config file: ')

    # Write the config file to disk
    with open(f'./core/admin/config/{configFileName}.ini', 'w') as f:
        config.write(f)

if __name__ == '__main__':
    main()