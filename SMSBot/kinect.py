#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
import math
from sensor_msgs.msg import Image

import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError


class KinectManager(object):
    """ clase que maneja todo lo referente a la cámara, el kinect e imágenes"""
    def __init__(self):
               #rospy.init_node('TurtleBot_Kinect', anonymous=True)
        self.__depth_img = rospy.Subscriber('/camera/depth/image',Image ,self.depth_handler)
        self.__rgb_img= rospy.Subscriber('/camera/rgb/image_color',Image,self.rgb_handler)
        self.bridge = CvBridge()
        self.current_cv_depth_image = numpy.zeros((1,1,3))
        self.current_cv_rgb_image = numpy.zeros((1,1,3))
	#self.faceClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    def depth_handler(self, data):
            try:
                D = numpy.asarray(self.bridge.imgmsg_to_cv(data,"32FC1"))[:,:540]
                D = numpy.ma.masked_array(D, numpy.isnan(D))
                self.current_cv_depth_image = D
                #rospy.loginfo("imagen depth recibida " + str(self.current_cv_depth_image.shape))
                #cv2.imshow("image_depth",D )
                #cv2.waitKey(10)
            except CvBridgeError, e:
                print e

    def rgb_handler(self, data):
        try:
            self.current_cv_rgb_image = numpy.asarray(self.bridge.imgmsg_to_cv(data,"bgr8"))[:,:540]
            #rospy.loginfo("imagen rgb recibida " + str(self.current_cv_rgb_image.shape))
            
            #cv2.imshow("image_rgb",self.current_cv_rgb_image )
            #cv2.waitKey(10)
            
        except CvBridgeError, e:
            print e
    
    def obstacleInFront(self, threshold):
        D = self.current_cv_depth_image
        banda = D[:, 300:370]
        dists = banda.mean(0);
        if(numpy.any(dists<threshold)):
            rospy.loginfo("STOP!!")            
	    return 1
        return 0
    
    def obstacleOnRight(self, threshold):
	D = self.current_cv_depth_image
        banda = D[230:250, 500:540]
        dists = banda.mean(0);
        if(numpy.any(dists<threshold)):
            return 1
        return 0    

    def obstacleOnLeft(self, threshold):
	D = self.current_cv_depth_image
        banda = D[230:250, 130:170]
        dists = banda.mean(0);
        if(numpy.any(dists<threshold)):
            return 1
        return 0  

    def wallInFront(self):
	if(self.getDistance(320, 240)<1):
	    return 1
	elif (not self.getDistance(240,320).any()):
	    rospy.loginfo("muro al peo")
	    return 1
	return 0

    def showDistances(self):
	D = self.current_cv_depth_image
        bandar = D[230:250, 440:540]
	bandal = D[230:250, 130:230]
	bandaf = D[:, 300:370]
        dr = bandar.mean(0);
	dl = bandal.mean(0);
	df = bandaf.mean(0);
	rospy.loginfo("dr = " + str(numpy.any(dr < 0.7)))
	rospy.loginfo("dl = " + str(numpy.any(dl < 0.7)))
	rospy.loginfo("df = " + str(numpy.any(df < 0.5)))
    '''
    def hayPared(self,distancia_pared):        
        D = self.current_cv_depth_image
        """Aca yo veria si es que en un sector mas o menos grande, por ejemplo R[100:400, 150:350], es del mismo color    """
        banda = D[250:420, :]
        dist = banda.mean(0);
        #rospy.loginfo(str(dist))
        rospy.loginfo(str(numpy.mean(dist)))
        if(numpy.mean(dist) < distancia_pared):
            return 1            
        return 0
    '''

    def getSideAlignment(self):
        D = self.current_cv_depth_image
        """Ve dos de los lados y entrega la diferencia"""
        banda = D[230:250, :];
        a1 = numpy.mean(banda[:,100:120])
        a2 = numpy.mean(banda[:,520:540])
        return a2-a1
    
    def getAlignment(self):
	D = self.current_cv_depth_image
        """Ve dos puntos de una pared y entrega la diferencia"""
        banda = D[230:250, :];
        a1 = numpy.mean(banda[:,250:300])
        a2 = numpy.mean(banda[:,370:420])
        #rospy.loginfo(str(numpy.mean(a2-a1)))
        return a2-a1
    
    def showDepthImage(self):
        cv2.imshow("image_depth",self.current_cv_depth_image)    
        cv2.waitKey(10)

    def showRgbImage(self):
        cv2.imshow("image_rgb",self.current_cv_rgb_image)    
        cv2.waitKey(10)

    def getRgbImage(self):
        return self.current_cv_rgb_image
        
    def getDepthImage(self):
        return self.current_cv_depth_image

    def getDistance(self, x, y):
        D = self.current_cv_depth_image
        #rospy.loginfo(str(self.current_cv_rgb_image.shape))
        #cv2.imshow("Depth", D)
        #cv2.waitKey(10)
        try:
            return np.mean(D[y-5:y+5,x-5:x+5])
        except:
            return 0

    def detectarObjeto(self):
    
        img = self.current_cv_rgb_image
        img = np.uint8(img)
        
        
        # convert the image to HSV
        hsv_img = cv2.cvtColor(img,  cv2.COLOR_BGR2HSV)
        
        # apply thresholds
        #threshold_img1 = cv2.inRange(hsv_img, (165, 155, 110), (250, 200, 150))  # red
        #threshold_img1a = cv2.inRange(hsv_img, (0, 155, 110), (10, 200, 150))  # red again
        threshold_img1 = cv2.inRange(hsv_img, (160, 100, 100), (179, 255, 255))  # otro red
        
        # determine the moments of the two objects
        threshold_img1 = numpy.asarray(threshold_img1)
        M = cv2.moments(threshold_img1, 0)
        area1 = M['m00']

        # there can be noise in the video so ignore objects with small areas
        if (area1 > 20000):
            # x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
            x1 = int(M['m10']/M['m00'])
            y1 = int(M['m01']/M['m00'])

            # draw circle
            cv2.circle(img, (x1, y1), 2, (0, 255, 0), 20)
            return (x1, y1)
        #cv2.imshow("Object", threshold_img1)
        #cv2.imshow("Target", img)
        #cv2.waitKey(10)
        return (320, 240)
    
    def detectarCara(self):
		
	cascPath = "haarcascade_frontalface_default.xml"
	#path = "barack.jpg"
	faceCascade = cv2.CascadeClassifier(cascPath)	
	img = self.current_cv_rgb_image
	#img = cv2.imread(path)	
	cv2.imshow("img", img)
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors = 5)
	#print "Found {0} faces!".format(len(faces))	
	for (x,y,w,h) in faces:
		rospy.loginfo("Cara detectada")
		cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
	cv2.imshow("img", img)
	if len(faces) > 0:
		return 1
	return 0	
	#cv2.waitKey(10)

   
    def detectarPuerta(self, show = False):	
	img = self.current_cv_rgb_image

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5,5), 0)
	edged = cv2.Canny(gray, 75, 200)
	
	# find contours in the image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	detected = 0
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02*peri, True)
		
		if len(approx) == 4:
			papel = approx
			detected = 1
			break
	if detected:
		x,y,w,h = cv2.boundingRect(papel)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		M1 = cv2.moments(papel);
		area1 = M1['m00']
		if area1 < 10000:
			return 0
		thresh_img = cv2.inRange(gray, 0, 80)[y:y+h, x:x+w]
		"""thresh_img = thresh_img[20:h-20,20:w-20]
		se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
		#thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, se1)oscor
		thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, se1)"""
		M2 = cv2.moments(thresh_img, 0)
		area2 = M2['m00']/100
		if show:
			cv2.imshow("Lala", thresh_img)	
			cv2.waitKey(10)
		areaRatio = area2/area1
		#print "area ratio = " + str(areaRatio)
		if areaRatio > 2.3:
			return 1		
	return 0
	
    def detectarFormas(self, show = False):
	img = self.current_cv_rgb_image

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5,5), 0)
	edged = cv2.Canny(gray, 75, 200)
	
	# find contours in the image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	detected = 0
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02*peri, True)
		
		if len(approx) == 4:
			papel = approx
			detected = 1
			break
	if detected:
		x,y,w,h = cv2.boundingRect(papel)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		M1 = cv2.moments(papel);
		area1 = M1['m00']
		if area1 < 10000:
			return "Nada"
		thresh_img = cv2.inRange(gray, 0, 50)[y:y+h, x:x+w]
		thresh_img = thresh_img[20:h-20,20:w-20]
		se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
		#thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, se1)
		thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, se1)
		M2 = cv2.moments(thresh_img, 0)
		area2 = M2['m00']/100
		if show:
			cv2.imshow("Lala", thresh_img)	
			cv2.waitKey(10)
		areaRatio = area2/area1
		print "area ratio = " + str(areaRatio)
		if areaRatio > 2.3:
			return "Puerta"
		elif areaRatio < 0.5 and areaRatio > 0.3:
			return "Llave"
		elif areaRatio < 0.2 and areaRatio > 0.09:			
			xc = int(M2['m10']/M2['m00'])
			yc = int(M2['m01']/M2['m00'])

			if xc < thresh_img.shape[1]*0.5:
				return "No doblar izquierda"
			return "No doblar derecha"
		elif areaRatio < 0.05 and areaRatio > 0.01:			
			xc = int(M2['m10']/M2['m00'])
			yc = int(M2['m01']/M2['m00'])

			if xc < thresh_img.shape[1]*0.5:
				return "Doblar izquierda"
			return "Doblar derecha"
			
	return "Nada"



    def detectarFlecha(self, show = False):
	img = self.current_cv_rgb_image

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5,5), 0)
	edged = cv2.Canny(gray, 75, 200)
	
	# find contours in the image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	detected = 0
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02*peri, True)
		
		if len(approx) == 4:
			papel = approx
			detected = 1
			break
	if detected:
		x,y,w,h = cv2.boundingRect(papel)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		M1 = cv2.moments(papel);
		area1 = M1['m00']
		if area1 < 10000:
			return 0
		thresh_img = cv2.inRange(gray, 0, 50)[y:y+h, x:x+w]
		thresh_img = thresh_img[20:h-20,20:w-20]
		se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
		#thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, se1)
		thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, se1)
		M2 = cv2.moments(thresh_img, 0)
		area2 = M2['m00']/100
		if show:
			cv2.imshow("Lala", thresh_img)	
			cv2.waitKey(10)
		areaRatio = area2/area1
		if show: print "area ratio = " + str(areaRatio)
		if areaRatio < 0.2 and areaRatio > 0.09:			
			xc = int(M2['m10']/M2['m00'])
			yc = int(M2['m01']/M2['m00'])

			if xc < thresh_img.shape[1]*0.5:
				return 3 # no doblar izquierda
			return 4 # no doblar derecha
		elif areaRatio < 0.05 and areaRatio > 0.01:			
			xc = int(M2['m10']/M2['m00'])
			yc = int(M2['m01']/M2['m00'])

			if xc < thresh_img.shape[1]*0.5:
				return 1 # doblar izquierda
			return 2 # doblar derecha
			
	return 0


    def detectarLlave2(self, show = False):
	img = self.current_cv_rgb_image

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5,5), 0)
	edged = cv2.Canny(gray, 75, 200)
	
	# find contours in the image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	detected = 0
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02*peri, True)
		
		if len(approx) == 4:
			papel = approx
			detected = 1
			break
	#print detected
	if detected:
		x,y,w,h = cv2.boundingRect(papel)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		M1 = cv2.moments(papel);
		area1 = M1['m00']
		if area1 < 10000:
			return 0
		thresh_img = cv2.inRange(gray, 0, 80)[y:y+h, x:x+w]
		thresh_img = thresh_img[20:h-20,20:w-20]
		se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
		#thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, se1)
		thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, se1)
		M2 = cv2.moments(thresh_img, 0)
		area2 = M2['m00']/100
		if show:
			cv2.imshow("Lala", thresh_img)	
			cv2.waitKey(10)
		areaRatio = area2/area1
		print "area ratio = " + str(areaRatio)
		if show: print "area ratio = " + str(areaRatio)
		if areaRatio < 0.6 and areaRatio > 0.2:
			return 1			
	return 0
	

#    #def detectarLlave2(self, show = False):
#	img = self.current_cv_rgb_image
#	img = img[10:440,60:500,:]
#	hsv_img = cv2.cvtColor(img,  cv2.COLOR_BGR2HSV)
#	mask = cv2.inRange(hsv_img, (0,0,0), (255,100,50))  
#	se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
#	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se1)
#	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se1)
#	# area        
#	mask = np.asarray(mask)
#	B = np.argwhere(mask)
#	if B.shape[0] == 0 or B.shape[1] == 0:
#		return 0
#	(ystart, xstart), (ystop, xstop) = B.min(0), B.max(0) + 1 
#	llave = mask[ystart:ystop, xstart:xstop]
#	#print str(xmin) + ':' + str(xmax) + ',' + str(ymin) + ':' + str(ymax)
 #       M = cv2.moments(llave, 0)
  #      area1 = M['m00']
#	if show:	
#		cv2.imshow("img", llave)
#		cv2.waitKey(10)
#	if (area1 > 700000):	
#		x1 = int(M['m10']/M['m00'])
#		y1 = int(M['m01']/M['m00'])
#		#print str(area1) + '-' + str(x1) + '/' + str(y1)
#		if x1 > llave.shape[1]*0.4 and x1 < llave.shape[1]*0.6 and y1 < llave.shape[0]*0.4:	    
#			print 'Llave detectada'			
#			return 1
#	return 0



