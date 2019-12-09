#!/usr/bin/env python2


import rospy

from serial import Serial
from geometry_msgs.msg import Twist
s = Serial("/dev/ttyUSB0",115200,timeout=0.1)


pre_time = 0
pre_v = 0
pre_w = 0
a_max = 1.5
alpha_max = 1.2



def runBot(msg):
	global pre_time, pre_v, pre_w, a_max, alpha_max
	curr_time = rospy.Time().now().to_sec()
	delta_t = curr_time - pre_time
	pre_time = curr_time
	
	v=msg.linear.x
	w=msg.angular.z
	
	#delta_v = (v-pre_v) if (v-pre_v)!=0 else 1
	#delta_w = (w-pre_w) if (w-pre_w)!=0 else 1
	
	dir_v = (v-pre_v)/abs(v-pre_v) if (v-pre_v)!=0 else 0
	dir_w = (w-pre_w)/abs(w-pre_w) if (w-pre_w)!=0 else 0
	
	calc_v = pre_v + dir_v*a_max*delta_t
	calc_w = pre_w + dir_w*alpha_max*delta_t
	
	v = pre_v = calc_v if v!=0 else 0
	w = pre_w = calc_w if w!=0 else 0
	
	
	l,r=.14,.06 #bot's track-width and wheel radius.
	vB = (1/r)*(v + (w*l/2))
	vA = (1/r)*(v - (w*l/2))
	global s
	# call = s.readline()
	# print (call)
	# if b"ok" in call:
	vA=max(-255,min(255,vA*200/33))
	vB=max(-255,min(255,vB*200/33))
	
	x=bytearray("{},{};".format(vA,vB))
	print(x)
	s.write(x)


def subscriber():
	rospy.init_node("Arduino_communication",anonymous=True)
	rospy.Subscriber("cmd_vel", Twist, runBot)
	rospy.spin()

if __name__=="__main__":
	try:
		s = Serial("/dev/ttyUSB0",115200,timeout=0.1)
		subscriber()
	except rospy.ROSInterruptException:
		pass
