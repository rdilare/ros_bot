import rospy
from sensor_msgs.msg import CompressedImage
import numpy as np
import cv2

def img_publisher(img):
	publisher = rospy.Publisher("image",CompressedImage, queue_size=10)
	img_msg = CompressedImage()
	img_msg.header.stamp = rospy.Time().now()
	img_msg.format = 'jpeg'
	# img_msg.data = np.array(img,dtype = np.uint8).tostring()
	img_msg.data = np.array(cv2.imencode('.jpg', img)[1]).tostring()

	publisher.publish(img_msg)
