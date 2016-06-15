import rospy
import numpy
import math
from SMSBot.robot import Robot
from SMSBot.navigation import *

def main():
	tortuga = Robot('n')
	r = rospy.Rate(10)

	simulated = 0	
	
	while (tortuga.kinect.getDepthImage().shape == (1,1,3)) and (not simulated):
		rospy.loginfo("cargando kinect")
	
	tortuga.sound.say("kinect ready")
	
	mapKnown = 1
	startKnown = 0

	navigator = Navigator(tortuga, 'mapaLab6.txt',mapKnown,startKnown,simulated)
	#navigator.goToGoal()
	navigator.searchMaze()
	
	print 'llegue a la puerta'
	tortuga.sound.say('open sesame')
	
	while tortuga.kinect.wallInFront():
		r.sleep()
	print 'se abrio la puerta'
	for i in range(0,50):
		r.sleep()	
	
	tortuga.sound.say("door open")	

	navigator.moveAndUpdate(navigator.orient)
	print 'Posicion actual (row, col, orientacion): '  + str(navigator.row) + ", " + str(navigator.col) + ", " + str(navigator.orient)

	navigator.goToGoal(arrows = True)
	tortuga.sound.playSound('/home/user/sounds/1up.wav')

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass



