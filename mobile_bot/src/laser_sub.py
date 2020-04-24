#! /usr/bin/env python

import rospy 
from sensor_msgs.msg import LaserScan

def callback(msg):
    print msg.ranges

rospy.init_node('laser_sub')
sub = rospy.Subscriber('kobuki/laser/scan', LaserScan, callback)
direction=LaserScan()

rospy.spin()

publi = rospy.Publisher('/interim', 

while(rospy.ok):
    if(direction.ranges<540)
    

