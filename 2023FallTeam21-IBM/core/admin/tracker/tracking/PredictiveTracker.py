import math
import numpy as np
import cv2
import sys
from tracking.Tracker import Tracker
from tracking.TrackedObject import TrackedObject

class PredictiveTracker(Tracker):
    def update(self, contoursToUpdate):
        # Not Implemented
        return