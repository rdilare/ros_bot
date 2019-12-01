#! /usr/bin/env python2

from sensor_msgs.msg import CompressedImage

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
	mask1=cv2.inRange(hsv, l_color, u_color)
	result=cv2.bitwise_and(img,img,mask=mask1)

	return mask1

def get_center(mask_img):
	"""
	return center(x,y) of detected object in \
	binary mask_img.
	"""
	img, contours, hierarchy = cv2.findContours(mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if len(contours)!=0:
		cnt = contours[0]
		(x,y),radius=cv2.minEnclosingCircle(cnt)
	else :
		x,y = 0,0

	return int(x),int(y)


font = cv2.FONT_HERSHEY_SIMPLEX


def callback(msg):
	# np_arr = np.array(msg.data,dtype = np.uint8)
	np_arr = np.fromstring(msg.data, dtype=np.uint8)
	frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


	result = get_mask(frame,color=[100,150,150],inRange=[30,100,100])
	x,y = get_center(result)

	radius=10
	img_circle=cv2.circle(frame.copy(),(x,y), radius, (0,0,0), 4)


	cv2.putText(img_circle,'({},{})'.format(300-x,y),(25,100), font, 0.5,(0,0,0),2,cv2.LINE_AA)

	cv2.imshow('frame',img_circle)
	cv2.waitKey(2)

def main():
	rospy.init_node("opencv_velocity_publisher",anonymous=True)
	subscriber = rospy.Subscriber("/image",CompressedImage,callback)
	rospy.spin()


if __name__=="__main__":
	main()

cv2.destroyAllWindows()
