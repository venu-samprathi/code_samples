#! /usr/bin/env python
import rospy
import time
import actionlib
from actionlib.msg import TestAction, TestGoal, TestResult, TestFeedback
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty


fb = TestFeedback()

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received
def feedback_callback(feedback):
    global fb
    print('[Feedback] current side %d received' % fb.feedback)
    rospy.spin()

takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)

# initializes the action client node
rospy.init_node('drone_action_client')
print "node initialized"

# create the connection to the action server
client = actionlib.SimpleActionClient('ardrone_as', TestAction)
# waits until the action server is up and running
client.wait_for_server()
print "server available"

blank = Empty()
#rate = rospy.Rate(1)
takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
takeoff_pub.publish(blank)
#rate.sleep()
print "taking off"

# creates a goal to send to the action server
goalobj = TestGoal()
goalobj.goal = 5
# sends the goal to the action server, specifying which feedback function
# to call when feedback received
client.send_goal(goalobj, feedback_cb=feedback_callback)
print " goal sent"

status = client.get_state()
print('[Result] State: %d'%(client.get_state()))
#rate.sleep()

while status < 2:
    rospy.sleep(1)
    status = client.get_state()
    rospy.loginfo("state_result: "+str(status))

#    rate = rospy.Rate(0.5)

#time.sleep(goal.nseconds)
#client.cancel_goal()
if status >=2:
    status = client.get_state()
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
