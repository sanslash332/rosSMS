import rospy
from SMSBot.robot import Robot
from busqueda.mapa import Mapa

def main():
	tortuga = Robot('s')
	while (tortuga.kinect.getDepthImage().shape == (1,1,3)):
		rospy.loginfo("cargando kinect")	
	tortuga.sound.say("kinect ready")

	#tortuga.correctAlignment()
	#tortuga.correctDistance(0.5)	
	
	tortuga.moveStraight(2, 0.3)
	#pasos = ['w','n','n','e','s','e','e']
	#for p in pasos:
	#	tortuga.moveMaze(p)

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
