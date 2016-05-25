#!/bin/bash'
# -*- ENCODING: UTF-8 -*-

nohup roscore &

nohup roslaunch turtlebot_bringup minimal.launch &
nohupt nohup roslaunch openni_launch openni.launch &
nohup roslaunch sound_play soundplay_node.launch &
exit
