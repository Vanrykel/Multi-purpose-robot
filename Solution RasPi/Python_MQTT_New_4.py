
from imutils import contours
#from imutils import perspective
#from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import numpy as np
import cv2
import math
import imutils
import matplotlib, cv2
import matplotlib.pyplot as plt
import sys
from ftplib import FTP
import os
import urllib
cv2.__version__
'3.3.0'

broker_url = "192.168.1.174"
broker_port = 1883

#vision
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

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)

def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")

def on_message(client, userdata, message):
   #print("Message Recieved: "+message.payload.decode())
   test=json.loads(message.payload.decode())
   print(test["input"])
   data_input = test["input"].lower()
   print(data_input)
   if test["input"].lower() == "take picture":
       video_capture = cv2.VideoCapture(0)
	# Check success
	#if not video_capture.isOpened():
 	 #  raise Exception("Could not open video device")
	# Read picture. ret === True on success
       ret, frame = video_capture.read()
	# Close device
       video_capture.release()

	#from matplotlib import pyplot as plt
       frameRGB = frame[:,:,::-1] # BGR => RGB
	#plt.imshow(frameRGB)
       cv2.imwrite('scanfoto.jpg', frameRGB)
       print("test foto gemaakt")

   if data_input == "scan":
        # load our input image, convert it to grayscale, and blur it slightly
       image = cv2.imread("scanfoto.jpg")
       #image = frameRGB
       gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
       gray = cv2.GaussianBlur(gray, (7, 7), 0)

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

       #to get nparray in JSONfile
       class NumpyEncoder(json.JSONEncoder):
           def default(self, obj):
               if isinstance(obj, np.ndarray):
                   return obj.tolist()
               return json.JSONEncoder.default(self, obj)

       #clear json file
       #open('jason.txt', 'w').close()


       # loop over the contours individually
       for (i, c) in enumerate(cnts):
         # if the contour is not sufficiently large, ignore it
         #if cv2.contourArea(c) < 100:
         #	continue

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

         print("test 2")
   if data_input == "scan difference":
       # Set code here
       print("test 3")
   if data_input == "outline":
       frame = cv2.imread("scanfoto.jpg")
       hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
       #lower_blue = np.array([13,150,38])
       #lower_blue =np.array([10,20,38]) tussenstuk
       lower_blue = np.array([10,240,38])#(normaal deze uncomment)
       #lower_blue = np.array([10,40,38])#(normaal deze uncomment)


       upper_blue = np.array([100,255,255])#normaal deze

       mask =cv2.inRange(hsv, lower_blue, upper_blue)
       res =cv2.bitwise_and(frame, frame,mask=mask)
       plt.imshow(res)
       cv2.imwrite('foto-kleur.png', res)

       foto_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       foto_preprocessed = cv2.GaussianBlur(foto_gray, (5, 5), 0)
       _, foto_binary = cv2.threshold(foto_preprocessed, 130, 255, cv2.THRESH_BINARY)

       # invert image to get foto
       foto_binary = cv2.bitwise_not(mask)
       plt.imshow(cv2.cvtColor(foto_binary, cv2.COLOR_GRAY2RGB))
       cv2.imwrite('foto-binary.png', mask)

       rest =cv2.bitwise_and(foto_binary, foto_binary,mask=mask)

       #noise remove
       morph_kernel = np.ones((2,2),np.uint8)
       coins_morph = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, morph_kernel)

       plt.imshow(cv2.cvtColor(coins_morph, cv2.COLOR_GRAY2RGB))
       cv2.imwrite('foto-zwawit.png', coins_morph)

       # Converting the image to grayscale.
       #gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

       # Using the Canny filter to get contours
       edges = cv2.Canny(coins_morph, 20, 30)
       # Using the Canny filter with different parameters
       edges_high_thresh = cv2.Canny(coins_morph, 60, 120)
       # Stacking the images to print them together
       # For comparison
       images = np.hstack((coins_morph, edges, edges_high_thresh))
       # Display the resulting frame
       plt.imshow(edges)
       plt.imshow(edges_high_thresh)
       #cv2.imshow('frame', edges)
       cv2.imwrite('outlineGcode.png', edges_high_thresh)
       plt.imshow(edges)
       witzwart= np.invert(edges)
       plt.imshow(witzwart)
       cv2.imwrite('outlineGcodeconvert.png', edges_high_thresh)

       print("test 3 outline gemaakt")
   if data_input == "create g-code":
         #domain name or server ip:
       ftp = FTP('ftp.pxl-ea-ict.be')
       ftp.login(user='username', passwd = 'password')               # user anonymous, passwd anonymous@
       #ftp.cwd('/outlineGcode.gcode')
       def grabFile():

         filename = 'outlineGcode.gcode'

         localfile = open(filename, 'wb')
         ftp.retrbinary('RETR ' + filename, localfile.write, 2048)

         ftp.quit()
         localfile.close()
       grabFile()
       #session = FTP('ftp.pxl-ea-ict.be','11600404@pxl-ea-ict.be','p1qeLfqpZpoK')
       #file = open('outlineGcode.gcode','rb')                  # file to send
       #session.storbinary('STOR outlineGcode.gcode', file)     # send the file
       #file.close()                                    # close file and FTP
       #session.quit()
       print("test 7 gcode overgedragen")
   if data_input == "object detect":
       image = cv2.imread("scanfoto.jpg")
       #image = frameRGB
       gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
       gray = cv2.GaussianBlur(gray, (7, 7), 0)

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

       #to get nparray in JSONfile
       class NumpyEncoder(json.JSONEncoder):
           def default(self, obj):
               if isinstance(obj, np.ndarray):
                   return obj.tolist()
               return json.JSONEncoder.default(self, obj)

       #clear json file
       open('jason.txt', 'w').close()
       json_1 ="{[\"objects\""
       with open('jason.txt', 'a') as f:
             json.dumps(json_1, f)
       print("{[\"objects\":[", file=open("jason.txt", "a"))

       # Set code here
       # Set code here
       for (i, c) in enumerate(cnts):
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
         with open('jason.txt', 'a') as f:
             json.dumps(json_dump, f)
         print(json_dump)
         print(json_dump, file=open("jason.txt", "a"))
       with open('jason.txt', 'a') as f:
           json.dumps("]}", f)
       print("]}", file=open("jason.txt", "a"))
       session = FTP('username','password')
       file = open('jason.txt','rb')                  # file to send
       session.storbinary('STOR jason.txt', file)     # send the file
       file.close()                                    # close file and FTP
       session.quit()
       print("test 5 objectdetect")
   if data_input == "find angle and centre point":
      image = cv2.imread("scanfoto.jpg")
      #image = frameRGB
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray, (7, 7), 0)

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

      #to get nparray in JSONfile
      class NumpyEncoder(json.JSONEncoder):
          def default(self, obj):
              if isinstance(obj, np.ndarray):
                  return obj.tolist()
              return json.JSONEncoder.default(self, obj)

      #clear json file
      open('jason.txt', 'w').close()
      # Set code here
      for (i, c) in enumerate(cnts):
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
        json_dump = json.dumps({"objectNumber":"{}".format(i + 1),'angle':mydegrees,'centrepoint':midpunt,}, cls=NumpyEncoder)
        print(json_dump, file=open("jason.txt", "a"))
      print(json_dump)
      print("test 4 print middel and corners")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

#client.subscribe("TestingTopic", qos=1)
client.subscribe("hermes/intent/GeneraalAlfa:Vision", qos=1)

#client.publish(topic="TestingTopic", payload="TestingPayload", qos=1, retain=False)
client.publish(topic="Test/Text_To_Speech", payload='{"text": "This is the Python test"}', qos=1, retain=False)
client.publish(topic="hermes/intent/GeneraalAlfa:Vision", payload='{"input": "This is the Python test"}', qos=1, retain=False)

client.loop_forever()
