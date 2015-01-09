#!/usr/bin/env python

"""
    
"""

import rospy
import re
from actionlib import SimpleActionClient
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from geometry_msgs.msg import *
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
import sys
from phoenix_robot.interact import *
from phoenix_robot.task_setup import *

class ActionTasks:
    def __init__(self, script_path):
        rospy.init_node('task_cordinator')
        rospy.on_shutdown(self.cleanup)
        # Initialize a number of parameters and variables for nav locations
        setup_task_environment(self)
        # Set the default TTS voice to use
        self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.robot = rospy.get_param("~robot", "robbie")
        self.NavPublisher = rospy.Publisher("goto", String)

        

        self.client = SimpleActionClient("move_base", MoveBaseAction)
        self.client.wait_for_server()
        # Create the sound client object
        self.soundhandle = SoundClient()
        
        # Wait a moment to let the client connect to the
        # sound_play server
        rospy.sleep(1)
        
        # Make sure any lingering sound_play processes are stopped.
        self.soundhandle.stopAll()

        # Subscribe to the recognizer output and set the callback function
        rospy.Subscriber('/nltk_interpret', String, self.commands)

# here we do our main text prosessing    
    def commands(self,text):
        task = text.data
        ar = task.split(':')
        if ar[0] == "go":  
            self.move_to(ar[9].replace(" ", ""))
        if ar[0] == "get":  
            pass
        if ar[0] == "pick":  
            self.move_to(ar[9])
        if ar[1] == "what":  
            pass

    def move_to(self, location):
        goal = MoveBaseGoal()
        goal.target_pose.pose = self.room_locations[location]
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
  
        self.client.send_goal(goal)
        self.client.wait_for_result()

        if self.client.get_state() == GoalStatus.SUCCEEDED:
            result = self.client.get_result()
            print "Result: SUCCEEDED " 
        elif self.client.get_state() == GoalStatus.PREEMPTED:
            print "Action pre-empted"
        else:
            print "Action failed"


    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down talk node...")

if __name__=="__main__":
    try:
        ActionTasks(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Talk node terminated.")
