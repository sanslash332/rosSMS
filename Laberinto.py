import rospy
from SMSBot.robot import Robot
from busqueda.mapa import Mapa

def main():
	mapa = Mapa("mapa.txt")
	
	tortuga = Robot(mapa.getStartDirection())
	while (tortuga.kinect.getDepthImage().shape == (1,1,3)):
		rospy.loginfo("cargando kinect")	
	tortuga.sound.say("kinect ready")

	tortuga.sound.playBuiltSound(3)
	pasos= mapa.solveMap()

	#rospy.loginfo(mapa.getStartDirection())
	for p in pasos:
		tortuga.moveMaze(p)		
		#rospy.loginfo(p)
	tortuga.sound.say("I got to the goal!")
	tortuga.sound.playSound('/home/user/sounds/1up.wav')
	
	"""while(1):
		tortuga.kinect.showDistances()
		tortuga.movement.rate.sleep()"""

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
