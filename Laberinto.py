import rospy
from SMSBot.robot import Robot
from busqueda.mapa import Mapa

def main():
	tortuga = Robot('e')
	m = Mapa("c.txt")
	pasos = m.solveMap()
	pasos = ['n','o','n','n']
	for p in pasos:
		tortuga.moveMaze(p)

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
