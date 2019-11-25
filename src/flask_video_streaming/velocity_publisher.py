import rospy
from geometry_msgs.msg import Twist, Vector3


def vel_publisher(vel,omega):
	publisher = rospy.Publisher("cmd_vel",Twist, queue_size=10)
	twist_msg = Twist(Vector3(vel, 0.0, 0.0), Vector3(0.0, 0.0, omega))
	publisher.publish(twist_msg)
