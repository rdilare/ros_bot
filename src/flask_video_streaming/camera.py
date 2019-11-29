from __future__ import division
from time import time, sleep


import os
import cv2
import imageio
import numpy as np


dirname = os.path.dirname(os.path.realpath(__file__))

class Camera(object):
	def __init__(self):
		self.frames = [open(os.path.join(dirname,"static/img/asphalt/" + str(i) + '.jpg'), 'rb').read() for i in range(1,50)]
		self.framesinArray = [imageio.imread(os.path.join(dirname,"static/img/asphalt/" + str(i) + '.jpg')) for i in range(1,50)]
		# self.cap = cv2.VideoCapture(0)
		# self.image = open("./static/img/cam.jpg","rb").read()
		def frame():
			i=0
			while 1:
				yield i
				i+=1
				if i>2000:i=0
				sleep(1/10)
		self.frameNumber = frame()

	def get_frame(self):


		

		# ret, frame = self.cap.read()

		# if(self.cap.isOpened()):
			# cv2.imwrite("./static/img/cam.jpg",frame)
		i=next(self.frameNumber)
		frame = self.frames[i % len(self.frames)]
		arrayFrame = self.framesinArray[i % len(self.framesinArray)]
		# arrayFrame.dtype = np.uint8
		return frame, arrayFrame
		# return self.frames[int(time()) % len(self.frames)]
		# return self.image

	# def __del__(self):
	# 	self.cap.release()

