#!/usr/bin/env python
'''
'''

import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

# A class to track global variables
class BlackBoard():
    def __init__(self):
        # A list to store rooms and tasks
        self.task_list = list()
        
        # The robot's current position on the map
        self.robot_position = 1234


