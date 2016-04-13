import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
import time


def callback(data):
	global distance
	global posx_init
	global posx	
	rospy.loginfo(str(distance))
	posx = data.pose.pose.position.x
	if posx_init == 0:	
		posx_init = posx

def rotar(angulo, vel_angular, data, rate):
	data.angular = vel_angular
	time.sleep(angulo/vel_angular)
	data.angular = 0	
	rospy.spin()
		
def ir(distancia, vel, data):
	posx_init = posx		
def talker():

	pub = rospy.Publisher('/turtlebot/cmd_vel', Twist)
	sub = rospy.Subscriber('turtlebot/odom',Odometry, callback)
	rospy.init_node('talker2', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	
	# script
	velx = 0.2
	totravel = 3	
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
	
	# frenar
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

