#! /usr/bin/env python
import rospy
import time
import actionlib
from droner.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

nImage = 1

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received
def feedback_callback(feedback):
    global nImage
    print('[Feedback] image n.%d received'%nImage)
    nImage += 1

# initializes the action client node
takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)

rospy.init_node('drone_action_client')
print "node initialized"

# create the connection to the action server
client = actionlib.SimpleActionClient('/ardrone_action_server', ArdroneAction)
# waits until the action server is up and running
client.wait_for_server()
print "server available"

blank = Empty()
#rate = rospy.Rate(1)
takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
takeoff_pub.publish(blank)
#rate.sleep()

# creates a goal to send to the action server
goal = ArdroneGoal()
goal.nseconds = 10 # indicates, take pictures along 10 seconds

# sends the goal to the action server, specifying which feedback function
# to call when feedback received
client.send_goal(goal, feedback_cb=feedback_callback)
print " goal sent"

status = client.get_state()
print('[Result] State: %d'%(client.get_state()))
#rate.sleep()

while status < 2:
    var= Twist()
    status = client.get_state()
    var.linear.x = 0.5
    var.linear.y = 0.0
    var.linear.z = 0.0

    var.angular.x = 0.0
    var.angular.y = 0.0
    var.angular.z = 0.5

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
#    rate = rospy.Rate(0.5)
    pub.publish(var)

#time.sleep(goal.nseconds)
#client.cancel_goal()
land_pub.publish(blank)
print "landing"

# Uncomment these lines to test goal preemption:
#time.sleep(3.0)
#client.cancel_goal()  # would cancel the goal 3 seconds after starting

# wait until the result is obtained
# you can do other stuff here instead of waiting
# and check for status from time to time 

# check the client API link below for more info

#client.wait_for_result()
