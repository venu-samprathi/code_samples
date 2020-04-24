#! /usr/bin/env python
import rospy
import actionlib
from geometry_msgs.msg import Twist
from actionlib.msg import TestAction, TestFeedback, TestResult, TestGoal

class TestClass(object):
    _feedback = TestFeedback()
    _result   = TestResult()
    
    def __init__(self):
        self._as = actionlib.SimpleActionServer("ardrone_as", TestAction, self.goal_callback, False)
        self._as.start()
#        self.goal = TestGoal()
#        print self
#        print self.goal
        print "move object intialized"
        self.move1 = Twist()
        self.move2 = Twist()
        self.move3 = Twist()
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    def straight(self,goal):
        self.move1.linear.x = goal.goal
        self.move1.linear.y = 0.0
        self.move1.linear.z = 0.0
        self.move1.angular.x =0.0
        self.move1.angular.y =0.0
        self.move1.angular.z =0.0
#        self.t = (goal.goal)/(self.move1.linear.x)
#        print ("goal.goal = %i" % self.goal.goal)
#        print ("self.t = %f " % self.t)
#        print (goal)
        
#        self.pub.publish(self.move3)
#        rospy.sleep(2)
        self.pub.publish(self.move1)
        print "moving straight"
        rospy.sleep(goal.goal/self.move1.linear.x)
        self.pub.publish(self.move3)
        rospy.sleep(2)
    
    def turn(self):
        self.move2.linear.x =0.0
        self.move2.linear.y =0.0
        self.move2.linear.z =0.0
        self.move2.angular.x =0.0
        self.move2.angular.y =0.0
        self.move2.angular.z =0.7854
            
#        self.pub.publish(self.move3)
#        rospy.sleep(1)
        self.pub.publish(self.move2)
        print "turning"
        rospy.sleep(2)
        self.pub.publish(self.move3)
        rospy.sleep(1)
    
    def stop(self):
        self.move3.linear.x =0.0
        self.move3.linear.y =0.0
        self.move3.linear.z =0.0
        self.move3.angular.x =0.0
        self.move3.angular.y =0.0
        self.move3.angular.z =0.0
#        while not rospy.is_shutdown():
        print "stopping"
        self.pub.publish(self.move3)
        rospy.sleep(1)
    
    def goal_callback(self, goal):
        # this callback is called when the action server is called.
        # and returns the sequence to the node that called the action server
        
        # helper variables
        r = rospy.Rate(1)
        success = True
        
        self._feedback.feedback = 0
        
        # publish info to the console for the user

        for i in xrange(0, 4):
        
          # check that preempt (cancelation) has not been requested by the action client
          if self._as.is_preempt_requested():
            rospy.loginfo('The goal has been cancelled/preempted')
            # the following line, sets the client in preempted state (goal cancelled)
            self._as.set_preempted()
            success = False

            break
          self.straight(goal)
          self.stop()
          self.turn()
          self.stop()
          i = i+1
          self._feedback.feedback = self._feedback.feedback + 1
          self._as.publish_feedback(self._feedback)
          rospy.loginfo('"ardrone_as": Finished Executing square of size %i with current side number %i' % ( goal.goal, self._feedback.feedback))
          # the sequence is computed at 1 Hz frequency
          r.sleep()
        
          # at this point, either the goal has been achieved (success==true)
          # or the client preempted the goal (success==false)
          # If success, then we publish the final result
          # If not success, we do not publish anything in the result
        if success:
            self._result.result = int(rospy.get_time())
            rospy.loginfo('Succeeded executing the in time %i ' % (self._result.result))
            self._as.set_succeeded(self._result)
          
if __name__ == '__main__':
    rospy.init_node('ardrone')
    TestClass()
    rospy.spin()