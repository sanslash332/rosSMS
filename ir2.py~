import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
import time

def callback(data):
	global distance
	global posx	
	posx = data.pose.pose.position.x
	rospy.loginfo(str(distance))

def rotar(angulo, vel, pub, rate):
	ang = 0
	data = Twist()
	data.linear.x = 0
	data.angular.z = 1.1*vel
	while(ang>2*angulo):
		ang = ang + 0.1*vel
		pub.publish(data)
		rate.sleep()
	data.angular.z = 0	
	pub.publish(data)
	return
def ir(toTravel, vel, pub, rate):
	global distance	
	global posx
	distance = 0	
	data = Twist()
	posx_init = posx
	data.linear.x = vel*3.0/2.63
	#data.linear.x = vel	
	while(distance<toTravel):
		distance = distance + 0.1*vel
		pub.publish(data)
		rate.sleep()
	data.linear.x = 0
	pub.publish(data)
	return
def irVenir(toTravel, vel, pub, rate):	
	ir(toTravel, vel, pub, rate)
	for i in range (10):
		rate.sleep()	
	vela = math.pi/2
	rotar(math.pi, vela, pub, rate)
	for i in range (10):
		rate.sleep()
	ir(toTravel, vel, pub, rate)
	return
def square(lado, vel, pub, rate):
	vela = -math.pi/2
	ang = -math.pi/2	
	for i in range(12):
		ir(lado, vel, pub, rate)
		for i in range (10):
			rate.sleep()			
		rotar(ang, vela, pub, rate)
		for i in range (10):
			rate.sleep()
	return
def DCC(pub, rate):
	#ir(1, 0.3, pub, rate)
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
	#esquina D
	angulo = 0
	data = Twist()
	data.linear.x = 0
	data.angular.z = -velang
	while(angulo<math.pi):
		angulo = angulo + 0.1*velang
		pub.publish(data)
		rate.sleep()
	#curva D
	distancia = 0	
	angulo = 0
	data = Twist()
	data.linear.x = 0.46
	data.angular.z =  -1.6
	while(angulo<1.5*math.pi):
		angulo = angulo + 0.1*velang
		pub.publish(data)
		rate.sleep()	
	
		
def talker():
	pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist)
	sub = rospy.Subscriber('/odom',Odometry, callback)
	rospy.init_node('talker2', anonymous=True)	
	rate = rospy.Rate(10) # 10hz
	velx = 0.3
	vela = math.pi/2
	ang = math.pi*2
	lado = 1
	toTravel = 3
	#ir(toTravel, velx, pub, rate)
	#rotar(ang, vela, pub, rate)
	#irVenir(toTravel, velx, pub, rate)
	square(lado, velx, pub, rate)
	#DCC(pub, rate)
if __name__ == '__main__':
	distance = 0
	try:
		talker()
	except rospy.ROSInterruptException:
		pass

