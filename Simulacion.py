import rospy
from SMSBot.robot_simulacion import RobotMaze
#from mapa import Mapa

def main():
	tortuga = RobotMaze('e')
	#m = Mapa("c.txt")
	#pasos = m.solveMap()
	pasos = ['e', 'e', 'e', 'n', 'w', 'w', 'w', 'n', 'n', 'e', 'e']
	for p in pasos:
		tortuga.move(p)

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
