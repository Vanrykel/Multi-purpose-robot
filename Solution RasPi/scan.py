
# coding: utf-8

# In[34]:


# import the necessary packages
#from __future__ import print_function
#from imutils import perspective
#from imutils import contours
import numpy as np
#import argparse
#import imutils
import cv2

video_capture = cv2.VideoCapture(0)
# Check success
if not video_capture.isOpened():
    raise Exception("Could not open video device")
# Read picture. ret === True on success
ret, frame = video_capture.read()
# Close device
video_capture.release()

from matplotlib import pyplot as plt
frameRGB = frame[:,:,::-1] # BGR => RGB
plt.imshow(frameRGB)
cv2.imwrite('scanfoto.jpg', frameRGB)

