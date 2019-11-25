#!/usr/bin/env python2

import rospy
import time


rospy.init_node("test",anonymous=True)
for i in range(20):
	print(i,"<",i+1)
	time.sleep(.5)

rospy.spin()
