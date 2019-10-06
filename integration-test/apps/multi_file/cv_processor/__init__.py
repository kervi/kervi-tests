from kervi.streams import stream_observer
from kervi.streams import stream_images, stream_observer
from kervi.vision.region import region_observer, Region, Regions
from imutils.video import VideoStream

import datetime
import imutils
import time
import cv2 
import numpy as np

firstFrame = None
firstPicture = True
lastRegion = None

@stream_observer(stream_id="cam1.my_observer")
def my_cv_observer(this_observer, stream_event, stream_data):
    pass
    #print("oni", stream_event)
    
