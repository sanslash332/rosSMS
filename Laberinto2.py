import rospy
from SMSBot.robot import Robot
from busqueda.mapa import Mapa

def main():
	mapa = Mapa("mapa.txt")
	tortuga = Robot('n')

	while (tortuga.kinect.getDepthImage().shape == (1,1,3)):
		rospy.loginfo("cargando kinect")	
	tortuga.sound.say("kinect ready")

	mapa.detectMyCeld(tortuga)

	pasos= mapa.solveMap()
		
	for p in pasos:
		tortuga.moveMaze(p)		
		#rospy.loginfo(p)
		tortuga.sound.say("I got to the goal!")
	
	tortuga.sound.playSound('/home/user/sounds/1up.wav')

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
