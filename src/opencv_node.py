#!/usr/bin/env python2

from sensor_msgs.msg import CompressedImage

from velocity_publisher import vel_publisher

import cv2
import numpy as np
import rospy

def get_mask(img,color,inRange=[5,50,50]):

	"""
	return the binary mask based on the given color \
	as HSV values.
	"""
	frame = img.copy()
	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	l_color=np.array([i-j for i,j in zip(color,inRange)])
	u_color=np.array([i+j for i,j in zip(color,inRange)])
	mask=cv2.inRange(hsv, l_color, u_color)
	blur_mask=cv2.GaussianBlur(mask, (5,5),0)
	ret,thresh_mask = cv2.threshold(blur_mask,150,255,cv2.THRESH_BINARY)


	return thresh_mask

def get_center(mask_img):
	"""
	return center(x,y) of detected object in \
	binary mask_img.
	"""
	# ~ img, contours, hierarchy = cv2.findContours(mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours, hierarchy = cv2.findContours(mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if len(contours)!=0:
		# cnt = contours[0]
		cnt = max(contours, key = cv2.contourArea)
		(x,y),radius=cv2.minEnclosingCircle(cnt)
	else :
		x,y = 0,0

	return int(x),int(y)




def callback(msg):
	# np_arr = np.array(msg.data,dtype = np.uint8)
	np_arr = np.fromstring(msg.data, dtype=np.uint8)
	frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

	h,w = frame.shape[0:2]

	result = get_mask(frame,color=[60,150,150],inRange=[10,100,100])
	x,y = get_center(result)

	if x == 0:
		x=w/2

	k = .1
	vel = 0
	omega = -k*(w/2 - x)

	vel_publisher(vel,omega)

	# ~ radius=10
	# ~ img_circle=cv2.circle(frame.copy(),(x,y), radius, (0,0,0), 4)
	# ~ cv2.putText(img_circle,'({},{})'.format(w/2-x,y),(25,100), font, 0.5,(0,0,0),2,cv2.LINE_AA)

	# ~ cv2.imshow('frame',result)
	# ~ cv2.waitKey(2)

def main():
	rospy.init_node("opencv_node",anonymous=True)
	subscriber = rospy.Subscriber("/image",CompressedImage,callback)
	rospy.spin()

font = cv2.FONT_HERSHEY_SIMPLEX

if __name__=="__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass

#cv2.destroyAllWindows()

