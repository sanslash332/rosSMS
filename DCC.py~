import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math

def callback(data):
	global distance
	global posx	
	posx = data.pose.pose.position.x
	rospy.loginfo(str(distance))

def talker():
	pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist)
	sub = rospy.Subscriber('/odom',Odometry, callback)
	rospy.init_node('talker2', anonymous=True)	
	rate = rospy.Rate(10) # 10hz
	# recta D
	distance = 0
	vel = 0.3
	velang = 1.5
	data = Twist()
	data.linear.x = vel*3.0/2.63
	while(distance<1):
		distance = distance + 0.1*vel
		pub.publish(data)
		rate.sleep()
	for i in range (10):
		rate.sleep()	
	
	#esquina D
	angulo = 0
	data = Twist()
	data.linear.x = 0
	data.angular.z = -velang
	while(angulo<math.pi):
		angulo = angulo + 0.1*velang
		pub.publish(data)
		rate.sleep()
	for i in range (10):
		rate.sleep()	

	#curva D	
	angulo = 0
	data = Twist()
	data.angular.z =  -1.46
	data.linear.x = 0.1
	while(angulo<2*math.pi):
		if(data.linear.x < 0.4):
			data.linear.x += 0.1
		angulo = angulo + 0.1*velang
		pub.publish(data)
		rate.sleep()
	for i in range (10):
		rate.sleep()	

	#avanza a punto de C
	data = Twist()
	pub.publish(data)
	data.linear.x = -vel*3.0/2.63
	distance = 0	
	while(distance<1.5):
		if(distance >= 1.3):
			data.linear.x += 0.1
		distance = distance + 0.1*vel
		pub.publish(data)
		rate.sleep()
	for i in range (10):
		rate.sleep()	

	#C
	angulo = 0
	data = Twist()
	pub.publish(data)
	data.angular.z =  -1.46
	data.linear.x = 0.1
	while(angulo<1.9*math.pi):
		if(data.linear.x < 0.4):
			data.linear.x += 0.1
		angulo = angulo + 0.1*velang
		pub.publish(data)
		rate.sleep()
	for i in range (10):
		rate.sleep()	

	#avanza a punto de segunda C
	data = Twist()
	pub.publish(data)
	data.linear.x = +vel*3.0/2.63
	distance = 0	
	while(distance<1):
		if(distance >= 0.8):
			data.linear.x -= 0.1
		distance = distance + 0.1*vel
		pub.publish(data)
		rate.sleep()
	for i in range (10):
		rate.sleep()

	#segunda C
	angulo = 0
	data = Twist()
	pub.publish(data)
	data.angular.z =  +1.465
	data.linear.x = -0.1
	while(angulo<1.9*math.pi):
		if(data.linear.x > -0.4):
			data.linear.x -= 0.1
		angulo = angulo + 0.1*velang
		pub.publish(data)
		rate.sleep()
if __name__ == '__main__':
	distance = 0
	try:
		talker()
	except rospy.ROSInterruptException:
		pass

