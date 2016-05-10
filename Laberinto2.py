import rospy
from SMSBot.robot import Robot
from busqueda.mapa import Mapa

def main():
	mapa = Mapa("mapa.txt")
	
	tortuga = Robot('n')#mapa.getStartDirection())
	while (tortuga.kinect.getDepthImage().shape == (1,1,3)):
		rospy.loginfo("cargando kinect")	
	tortuga.sound.say("kinect ready")

	tortuga.sound.say("con che tu ma dre")
	#pasos= mapa.solveMap()
	#tortuga.advanceOneCell()
	'''while(1):
		if tortuga.kinect.obstacleOnLeft(0.55):
			rospy.loginfo("YES")
		else:
			rospy.loginfo("NO")'''
	'''for j in range(1,5):
		tortuga.sound.say("Lap " + str(j))		
		for i in range(1,5):			
			tortuga.turnRight()
			tortuga.advanceOneCell()		
		tortuga.turnLeft()
		for i in range(1,5):
			tortuga.turnLeft()
			tortuga.advanceOneCell()'''
	
	pasos = ['n','w','s','n','e','s']

	#tortuga.sound.playSound('/home/user/sounds/1up.wav')
	#rospy.loginfo(mapa.getStartDirection())
	while 1:	
		for p in pasos:
			tortuga.moveMaze(p)		
			#rospy.loginfo(p)
			tortuga.sound.say("I got to the goal!")
	
	#tortuga.sound.playSound('/home/user/sounds/1up.wav')
	
	"""while(1):
		tortuga.kinect.showDistances()
		tortuga.movement.rate.sleep()"""

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
