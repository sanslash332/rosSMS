#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist



def callback(data):
	global distance
	global posx_init
	global posx	
	rospy.loginfo(str(distance))
	posx = data.pose.pose.position.x
	if posx_init == 0:	
		posx_init = posx

def talker():

	pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist)
	sub = rospy.Subscriber('/odom',Odometry, callback)
	rospy.init_node('talker2', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	
	# script
	velx = 0.1
	totravel = 1	
	global posx
	global posx_init 
	global distance	
	data = Twist()	
	while(distance<totravel):        

		data.linear.x = velx
		pub.publish(data)   
		# lazo cerrado		
		# distance = posx - posx_init   
		# lazo abierto
		distance = distance + 0.1*velx 
		rate.sleep()
	
	# frenartalk
	data.linear.x = 0
	pub.publish(data)        
	rate.sleep()
	rospy.spin()
	

if __name__ == '__main__':
    
	posx_init = 0
	posx = 0
	distance = 0
	try:
		talker()
	except rospy.ROSInterruptException:
		pass

