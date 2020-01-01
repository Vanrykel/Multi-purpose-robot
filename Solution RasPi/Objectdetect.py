
# coding: utf-8

# In[1]:


# import the necessary packages
from __future__ import print_function
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import json
import math


# In[2]:


def order_points_old(pts):
    # initialize a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect



# In[3]:


# load our input image, convert it to grayscale, and blur it slightly
image = cv2.imread("scanfoto.jpg")
#image = frameRGB
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)


# In[4]:



# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# sort the contours from left-to-right and initialize the bounding box
# point colors
(cnts, _) = contours.sort_contours(cnts)
colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))


# In[5]:


#to get nparray in JSONfile
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


# In[6]:


#clear json file
open('jason.txt', 'w').close()


# In[7]:


# loop over the contours individually
for (i, c) in enumerate(cnts):
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) < 100:
		continue

	# compute the rotated bounding box of the contour, then
	# draw the contours
	box1 = cv2.minAreaRect(c)
	box1 = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box1)
	box1 = np.array(box1, dtype="int")
	cv2.drawContours(image, [box1], -1, (0, 255, 0), 2)

	# show the original coordinates
	json_dump = json.dumps({"objectNumber":"{}".format(i + 1),'arrayCorners':box1,}, cls=NumpyEncoder)
	print(json_dump)

	print("Object #{}:".format(i + 1))
	print(box1)
    
    
	# order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left
	# order, then draw the outline of the rotated bounding
	# box
	rect = order_points_old(box1)
    #rect = perspective.order_points(box)

	# check to see if the new method should be used for
	# ordering the coordinates
#	if args["new"] > 0:
#rect = perspective.order_points(box)

	# show the re-ordered coordinates
	#print(rect.astype("int"))


# In[8]:


# loop over the contours individually
for (i, c) in enumerate(cnts):
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) < 100:
		continue

	# compute the rotated bounding box of the contour, then
	# draw the contours
	box = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	
	#bepalen middelpunt
	x1=box[0][0]
	x2=box[2][0]
	y1=box[0][1]
	y2=box[2][1]
	midpunt=( (x1 +x2)/2 ,(y1 + y2)/2 )  
	#make line from coordinates  
	myradians = math.atan2((box[0][1])-(box[1][1]), (box[0][0])-(box[1][0]))
	mydegrees = math.degrees(myradians)
	#if (angle < 0) { angle += 2 * M_PI; }

	# order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left
	# order, then draw the outline of the rotated bounding
	# box
	rect =order_points_old(box)   
	json_dump = json.dumps({"objectNumber":"{}".format(i + 1),'arrayCorners':box,'angle':mydegrees,'centrepoint':midpunt,}, cls=NumpyEncoder)
	print(json_dump, file=open("jason.txt", "a"))
	#f= open("jason.txt","w+")
	#for j in range(i):
	#f.write(json_dump)
	#f.write("\n")                
	#f.close()
	print(json_dump)


# In[ ]:


# loop over the original points and draw them
for ((x, y), color) in zip(rect, colors):
	cv2.circle(image, (int(x), int(y)), 5, color, -1)

# draw the object num at the top-left corner
cv2.putText(image, "Object #{}".format(i + 1),
	(int(rect[0][0] - 15), int(rect[0][1] - 15)),
	cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    
 #show the image(uncomment to see the image)
cv2.imshow("Image", image)
cv2.waitKey(0)


# In[ ]:


#image = cv2.imread('download.jpg')
#y=0
#x=0
#h=100
#w=200
#crop = image[y:y+h, x:x+w]
#cv2.imshow('Image', crop)
#cv2.waitKey(0) 

