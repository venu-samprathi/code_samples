#! /usr/bin/env python

import rospy 
from nav_msgs.msg import Odometry

rospy.init_node('topic_publisher')
pub = rospy.Publisher('/odom', Odometry, queue_size=1)
rate = rospy.Rate(2)
move = Odometry()
move.twist=[0.5,0,0]
print Age.date

while not rospy.is_shutdown():
  pub.publish(move)
  rate.sleep()      
