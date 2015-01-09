cmake_minimum_required(VERSION 2.8.3)
project(phoenix_robot)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

catkin_python_setup()

add_service_files(FILES
   
   Parse.srv
   #AskInfo.srv
   #InternetService.srv

 )

include_directories(
  ${catkin_INCLUDE_DIRS}
)
generate_messages(DEPENDENCIES std_msgs)
catkin_package(CATKIN_DEPENDS roscpp rospy std_msgs message_runtime)

