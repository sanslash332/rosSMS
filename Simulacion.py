import rospy
from SMSBot.robot_simulacion import RobotMaze
from busqueda.mapa import Mapa

def main():
	tortuga = RobotMaze('n')
	m = Mapa("c.txt")
	pasos = m.solveMap()
	#pasos.pop()
	for p in pasos:
		rospy.loginfo(p)
		tortuga.move(p)

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
