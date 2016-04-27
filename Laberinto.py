import rospy
from SMSBot.robot import Robot
from busqueda.mapa import Mapa

def main():
	tortuga = Robot('e')
	mapa = Mapa("mapa.txt")
	
	while (tortuga.kinect.getDepthImage().shape == (1,1,3)):
		rospy.loginfo("cargando kinect")	
	tortuga.sound.say("kinect ready")

	#tortuga.correctAlignment()
	#tortuga.correctDistance(0.5)	
	
	#tortuga.moveStraight(2, 0.3)
	tortuga.sound.playBuiltSound(3)
	#pasos = ['e','n','w','n','e']
	pasos= mapa.solveMap()
	for p in pasos:
		tortuga.moveMaze(p)
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
