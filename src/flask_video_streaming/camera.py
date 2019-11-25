from time import time, sleep
import os
import cv2



class Camera(object):
	def __init__(self):
		self.frames = [open("./static/img/asphalt/" + f + '.jpg', 'rb').read() for f in [str(i) for i in range(1,1200)]]
		# self.cap = cv2.VideoCapture(0)
		# self.image = open("./static/img/cam.jpg","rb").read()
		def frame():
			i=0
			while 1:
				yield i
				i+=1
				if i>2000:i=0
				sleep(1/30)
		self.frameNumber = frame()

	def get_frame(self):


		

		# ret, frame = self.cap.read()

		# if(self.cap.isOpened()):
			# cv2.imwrite("./static/img/cam.jpg",frame)
		# return self.frames[int(time()*60) % len(self.frames)]
		i=next(self.frameNumber)
		return self.frames[i % len(self.frames)]
		# return self.image

	# def __del__(self):
	# 	self.cap.release()

