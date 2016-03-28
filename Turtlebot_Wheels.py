import rospy
import math
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist


class Turtlebot_Wheels:
    def __init__(self):
    	self.odom_sub = rospy.Subscriber('/odom',Odometry,self.position_recv)
    	self.nav_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist)
    	self.rate = rospy.Rate(10)
		self.posx
		self.posy
		self.ang
		self.Kpx = 0.1
		self.Kpa = 0.2
        
	def position_recv(self, data):
		pos = data.pose.pose.position
		quat = data.pose.pose.orientation
		self.posx = pos.x
		self.posy = pos.y
		self.ang = tf.transformations.euler_from_quaternion(quat)[2] # Transforma de quaterniones a angulos. El ángulo en yaw es el que interesa

	def move_straight(self, distance, vel): # Mueve el robot una distancia en linea recta a una velocidad, leyendo de odom la pos
		data = Twist()
		posx_init = self.posx #Guarda la posición actual como incial
		posy_init = self.posy
		dist = 0
		data.linear.x = vel
		while(dist < distance):
			x = self.posx - posx_init
			y = self.posy - posy_init	
			dist = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) # Como la orientación cambia, para avanzar en linea recta que vaya calculando 
			self.nav_pub.publish(data) 						  # la distancia en línea recta entre los puntos de origen y actual
			rate.sleep()
		data = Twist()		
		self.nav_pub.publish(data)
		
	def move_rotate(self, angle, vel): #La misma idea pero con ángulo
		data = Twist()
		ang_init = self.ang
		ang = 0
		data.angular.z = vel
		while(ang < angle):
			self.nav_pub.publish(data)
			ang = self.ang - ang_init
			rate.sleep()
		data = Twist()		
		self.nav_pub.publish(data)

	def move_straight2(self, distance): #Los dos siguientes métodos usan un control proporcional, es para empezar con algo
		data = Twist()
		posx_init = self.posx
		posy_init = self.posy
		dist = 0
		while(dist < distance):
			x = self.posx - posx_init
			y = self.posy - posy_init
			dist = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
			velx = self.kp * dist
			if(vel > 0.5)
				vel = 0.5
			data.linear.x = vel
			self.nav_pub.publish(data)
			rate.sleep()
		data = Twist()		
		self.nav_pub.publish(data)

	def move_rotate2(self, angle):
		data = Twist()
		ang_init = self.ang
		ang = 0
		while(ang < angle):
			self.nav_pub.publish(data)
			ang = self.ang - ang_init
			vel = self.Kpa*ang
			rate.sleep()
		data = Twist()		
		self.nav_pub.publish(data)

