#!/usr/bin/env python2


import rospy

from serial import Serial
from geometry_msgs.msg import Twist
s = Serial("/dev/ttyUSB0",115200,timeout=0.1)

def runBot(msg):
	v=msg.linear.x
	w=msg.angular.z
	l,r=.8,.3 #bot's track-width and wheel radius.
	vA = (1/r)*(v + (w*l/2))
	vB = (1/r)*(v - (w*l/2))
	global s
	# call = s.readline()
	# print (call)
	# if b"ok" in call:
	vA=vA*200/33
	vB=vB*200/33
	x=bytearray("{},{};".format(vA,vB))
	print(x)
	s.write(x)


def subscriber():
	rospy.init_node("Arduino_communication",anonymous=True)
	rospy.Subscriber("cmd_vel", Twist, runBot)
	rospy.spin()

if __name__=="__main__":
	try:
		subscriber()
	except rospy.ROSInterruptException:
20      pass
