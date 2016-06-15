#!/usr/bin/python
# coding: utf-8

# In[1]:

import rospy
import numpy as np
from random import randint
from SMSBot.robot import Robot


# In[2]:


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.wallN = -1
        self.wallW = -1
        self.wallS = -1
        self.wallE = -1

    def defineWall(self,direction,wall):
        if direction == 'n':
            self.wallN = wall
        elif direction == 'w':
            self.wallW = wall
        elif direction == 's':
            self.wallS = wall
        elif direction == 'e':
            self.wallE = wall
        else:
            print 'Invalid direction'
    
    def getWalls(self,direction):
        if direction == 'n':
            return [self.wallN, self.wallW, self.wallS, self.wallE]
        elif direction == 'w':
            return [self.wallW, self.wallS, self.wallE, self.wallN]
        elif direction == 's':
            return [self.wallS, self.wallE, self.wallN, self.wallW]
        elif direction == 'e':
            return [self.wallE, self.wallN, self.wallW, self.wallS]
        else:
            print 'Invalid direction'
    
    def mapData(self):
        return '{0} {1} {2} {3} {4} {5}\n'.format(self.row, self.col, 
                                               self.wallN, self.wallW, 
                                               self.wallS, self.wallE)



class SearchNode:
    def __init__(self, row, col, depth):
        self.row = row
        self.col = col
        self.nodeList = []
        self.depth = depth
	self.goalConnected = 0

    def buildNodes(self, startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
        if(startNode == None):
            startNode = self
        
	if startNode.goalConnected == 1:
	    return
        ## esto puede optimizarse actualizando los depths
        
	if self.buildNodeNorth(startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
	    return
	if self.buildNodeWest(startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
	    return
	if self.buildNodeSouth(startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
	    return
	if self.buildNodeEast(startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
	    return              
   
        for node in self.nodeList:
            node.buildNodes(startNode, cellMap, n_rows, n_cols, row_goal, col_goal)
    
    def buildNodeNorth(self, startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
        # NORTH NODE
        if ((self.row+1<n_rows) and (self.wallInDirection(cellMap,'n') != 1)):
            #[targetCell, targetCellParentList] = startNode.getCell(self.row+1, self.col, None)
	    if not startNode.hasCell(self.row+1, self.col):#targetCell == None:#not startNode.hasCell(self.row+1, self.col):
                node = SearchNode(self.row+1, self.col, self.depth+1)
                self.nodeList.append(node)
		if node.row == row_goal and node.col == col_goal:
		    startNode.goalConnected = 1
		    return 1
            #elif not targetCell == None and targetCell.depth > self.depth+1:
                #print 'REMOVED: fila: ' + str(targetCell.row) + " - columna: " + str(targetCell.col) + ' - depth: ' + str(targetCell.depth)
                #for node in targetCellParentList:
                #    print "node row: " + str(node.row) + " - node col: " + str(node.col)
            #    targetCellParentList.remove(targetCell)
            #    node = SearchNode(self.row+1, self.col, self.depth+1)
            #    self.nodeList.append(node)
	return 0

    def buildNodeWest(self, startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
	# WEST NODE
        if (self.col-1>-1) and (self.wallInDirection(cellMap,'w') != 1):
            #[targetCell, targetCellParentList] = startNode.getCell(self.row, self.col -1, None)
            if not startNode.hasCell(self.row, self.col -1):#targetCell == None:
                node = SearchNode(self.row, self.col-1, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)
		if node.row == row_goal and node.col == col_goal:
		    startNode.goalConnected = 1
		    return 1
            #elif not targetCell == None and targetCell.depth > self.depth+1:
                #print 'REMOVED: fila: ' + str(targetCell.row) + " - columna: " + str(targetCell.col) + ' - depth: ' + str(targetCell.depth)
            #    targetCellParentList.remove(targetCell)
            #    node = SearchNode(self.row, self.col-1, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
            #    self.nodeList.append(node) 
	return 0
        
    def buildNodeSouth(self, startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
	# SOUTH NODE
        if (self.row-1>-1) and (self.wallInDirection(cellMap,'s') != 1):
            #[targetCell, targetCellParentList] = startNode.getCell(self.row-1, self.col, None)
            if not startNode.hasCell(self.row-1, self.col):#targetCell == None:
                node = SearchNode(self.row-1, self.col, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)
		if node.row == row_goal and node.col == col_goal:
		    startNode.goalConnected = 1
		    return 1
            #elif not targetCell == None and targetCell.depth > self.depth+1:
                #print 'REMOVED: fila: ' + str(targetCell.row) + " - columna: " + str(targetCell.col) + ' - depth: ' + str(targetCell.depth)
            #    targetCellParentList.remove(targetCell)
            #    node = SearchNode(self.row-1, self.col, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
            #    self.nodeList.append(node)
	return 0

    def buildNodeEast(self, startNode, cellMap, n_rows, n_cols, row_goal, col_goal):
        # EAST NODE
        if (self.col+1<n_cols) and (self.wallInDirection(cellMap,'e') != 1):
            #[targetCell, targetCellParentList] = startNode.getCell(self.row, self.col+1, None)
            if not startNode.hasCell(self.row, self.col +1):#targetCell == None:
                node = SearchNode(self.row, self.col+1, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)
		if node.row == row_goal and node.col == col_goal:
		    startNode.goalConnected = 1
		    return 1
            #elif not targetCell == None and targetCell.depth > self.depth+1:
                #print 'REMOVED: fila: ' + str(targetCell.row) + " - columna: " + str(targetCell.col) + ' - depth: ' + str(targetCell.depth)
            #    targetCellParentList.remove(targetCell)
            #    node = SearchNode(self.row, self.col+1, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
            #    self.nodeList.append(node)
	return 0

    def hasCell(self, row, col):
        if self.row == row and self.col == col:
            #print str(row) + "/" + str(col) + " Has cell: " + str(1)
            return 1
        elif len(self.nodeList) == 0:
            #print str(row) + "/" + str(col) + " Has cell: " + str(0)
            return 0
        else:
            #childrenHaveCell = 0
            for node in self.nodeList:
                #if(node.depth < )
                if(node.hasCell(row,col)):
                    return 1
                #return node.hasCell(row,col)
            return 0
        
    def getCell(self, row, col, parentList):
        if self.row == row and self.col == col:
            return [self, parentList]
        elif len(self.nodeList) == 0:
            return [None, None]
        else:
            for node in self.nodeList:
                if node.getCell(row,col,self.nodeList)[0] != None:
                    return [node.getCell(row,col,self.nodeList)[0], node.getCell(row,col,self.nodeList)[1]]
            return [None, None]
    
    def wallInDirection(self, cellMap, direction):
        mapLines = cellMap.split('\n')
        for i in range(1,len(mapLines)-1):
            mapLine = mapLines[i]
            lineData = mapLine.split(' ')
            if int(lineData[0]) == self.row and int(lineData[1]) == self.col:
                if direction == 'n':
                    return int(lineData[2])
                elif direction == 'w':
                    return int(lineData[3])
                elif direction == 's':
                    return int(lineData[4])
                elif direction == 'e':
                    return int(lineData[5])
                else:
                    print 'wall check ERROR'
    
    def moveToGoal(self, row_goal, col_goal, moveList):
        if self.row == row_goal and self.col == col_goal:
            return 1
        elif len(self.nodeList) == 0:
            moveList.pop()
            return 0
        else:
            for node in self.nodeList:
                if node.row > self.row:
                    moveList.append('n')
                    if node.moveToGoal(row_goal, col_goal, moveList):
                        return 1
                elif node.col < self.col:
                    moveList.append('w')
                    if node.moveToGoal(row_goal, col_goal, moveList):
                        return 1
                elif node.row < self.row:
                    moveList.append('s')
                    if node.moveToGoal(row_goal, col_goal, moveList):
                        return 1
                elif node.col > self.col:
                    moveList.append('e')
                    if node.moveToGoal(row_goal, col_goal, moveList):
                        return 1
            #print 'row: ' + str(self.row) + ' - col: ' + str(self.col)
            #print 'row: ' + str(self.nodeList[0].row) + ' - col: ' + str(self.nodeList[0].col)
            moveList.pop()
            return 0



class Navigator:
    
    def __init__(self, robot, fileName, mapKnown, startKnown, simulated):
	self.robot = robot        
	self.mapKnown = mapKnown
        self.startKnown = startKnown
	self.simulated = simulated
        self.mapFile = self.readMap(fileName)
        #[row0, col0, orient0] = startPositionMap(mapFile)
        [self.row_goal, self.col_goal] = self.goalPositionMap(self.mapFile)
        [self.n_rows, self.n_cols] = self.mapDimensions(self.mapFile)
        
        # puede eliminarse
        print 'Fila objetivo: ' + str(self.row_goal)
        print 'Columna objetivo: ' + str(self.col_goal)
        print 'Numero de filas: ' + str(self.n_rows)
        print 'Numero de columnas: ' + str(self.n_cols)
        
        self.row = 0 
        self.col = 0 
        self.orient = 'X'
	self.robot.orientacionActual = self.orient

        startCell = None
        if self.startKnown:
            [row0, col0, orient0] = self.startPositionMap(self.mapFile)
            startCell = Cell(row0, col0) 
            self.row = row0 
            self.col = col0 
            self.orient = orient0
	    self.robot.orientacionActual = self.orient
            print 'Fila inicial: ' + str(row0)
            print 'Columna inicial: ' + str(col0)
            print 'Orientacion inicial: ' + str(orient0)

        self.cellList = []
        if mapKnown:
            self.cellList = self.getCellsMap(self.mapFile)
        else:
            self.cellList = [startCell]

        self.currentMap = self.buildCurrentMap(self.cellList, self.n_rows, self.n_cols)
        
        if(not self.startKnown):
            self.locateStart()
    
    def searchMaze(self):
	print 'BUSCANDO'	
	manFound = 0
	keyFound = 0
	doorFound = 0
	doorCoords = []
	#visitedCells = [[0]*self.n_cols]*self.n_rows
	visitedCells = np.zeros((self.n_rows, self.n_cols), dtype=np.int)
	while not manFound or not keyFound or not doorFound:
		results = self.searchCell()
		manFound = manFound or results[0] 
		keyFound = keyFound or results[1]
		doorFound = doorFound or results[2] 
		if results[2] == 1:
			doorCoords = [self.row, self.col]
		print 'Man found? ' + str(manFound)
		visitedCells[self.row,self.col] = 1 

		if (manFound and keyFound and doorFound):
		    break
		[nextRow, nextCol] = self.nextSearchCell(self.currentMap, visitedCells, self.row, self.col, self.n_rows, self.n_cols)
		#print 'next: ' + str(nextRow) + '/' + str(nextCol)
		moveList = self.routeToGoal(self.currentMap, self.row, self.col, nextRow, nextCol, self.n_rows, self.n_cols)
		# moverse hacia siguiente 		
		for move in moveList:
			if move == 'n':
				self.row = self.row + 1
				self.orient = 'n'
				self.robot.moveMaze(self.orient)
			elif move == 'w':
				self.col = self.col - 1
				self.orient = 'w'
				self.robot.moveMaze(self.orient)
			elif move == 's':
				self.row = self.row - 1
				self.orient = 's'
				self.robot.moveMaze(self.orient)
			elif move == 'e':
				self.col = self.col + 1
				self.orient = 'e'
				self.robot.moveMaze(self.orient)
			else:
				print 'invalid move ERROR'
				break
			#print 'Se movio hacia ' + str(moveList[0])
	moveList = self.routeToGoal(self.currentMap, self.row, self.col, doorCoords[0], doorCoords[1], self.n_rows, self.n_cols)
	self.robot.sound.say('Going to door')	
	# moverse hacia puerta 		
	for move in moveList:
		if move == 'n':
			self.row = self.row + 1
			self.orient = 'n'
			self.robot.moveMaze(self.orient)
		elif move == 'w':
			self.col = self.col - 1
			self.orient = 'w'
			self.robot.moveMaze(self.orient)
		elif move == 's':
			self.row = self.row - 1
			self.orient = 's'
			self.robot.moveMaze(self.orient)
		elif move == 'e':
			self.col = self.col + 1
			self.orient = 'e'
			self.robot.moveMaze(self.orient)
		else:
			print 'invalid move ERROR'
			break
		#print 'Se movio hacia ' + str(moveList[0])	
	puerta = self.robot.kinect.detectarPuerta()
	while puerta == 0:
		self.robot.turnLeft()	
		self.updateOrientLeft()	
		puerta = self.robot.kinect.detectarPuerta()
	self.robot.correctAlignment()	
	
		

    def goToGoal(self,arrows = False):
        goalReached = 0
        while(not goalReached):
            # revisar si se llego a la meta
            if self.row == self.row_goal and self.col == self.col_goal:
                goalReached = 1
                break    
            # buscar ruta hacia meta 
            moveList = self.routeToGoal(self.currentMap, self.row, self.col, self.row_goal, self.col_goal, self.n_rows, self.n_cols)
	    self.moveUntilWall(moveList)
            # revisar si se llego a la meta (despues de moverse)
            if self.row == self.row_goal and self.col == self.col_goal:
                goalReached = 1
                break 
            pathBlocked = self.wallInFront()
            if pathBlocked: #and (not self.mapKnown):       
                # imprimir posicion actual
                #print ''
                #print 'ROW: ' + str(self.row) + ' - COL: ' + str(self.col) + ' - ORIENT: ' + str(self.orient)
                # imprimir mapa actual
                #print ''
                #print 'MAPA ACTUAL'
                self.currentMap = self.buildCurrentMap(self.cellList, self.n_rows, self.n_cols) 
                #print self.currentMap
                # revisar muro en frente
                #print ''
                wall = self.wallInFront()
		# decidir segun flecha
		if arrows and wall: 
			arrow = self.robot.kinect.detectarFlecha()
			wallOrient = 'X'
			wallOrient2 = 'X'
			if arrow == 1: # doblar izquierda
				print 'hay flecha para izquierda'
				wallOrient = self.orientAtRight()
				wallOrient2 = self.orientAtBack()
			elif arrow == 2: # doblar derecha
				print 'hay flecha para derecha'
				wallOrient = self.orientAtLeft()
				wallOrient2 = self.orientAtBack()
			elif arrow == 3: # no doblar izquierda
				print 'hay flecha para no izquierda'
				wallOrient = self.orientAtLeft()
			elif arrow == 4: # no doblar derecha
				print 'hay flecha para no derecha'
				wallOrient = self.orientAtRight()
			cellFound = 0
			print 'se coloco muro en: ' + str(wallOrient)			
			if arrow != 0:
				for cell in self.cellList:
				    if self.row == cell.row and self.col == cell.col:
					cellFound = 1
					cell.defineWall(wallOrient,1)
					if wallOrient2 != 'X': cell.defineWall(wallOrient2,1)
				if not cellFound:
				    newCell = Cell(self.row,self.col)
				    self.cellList.append(newCell)
				    newCell.defineWall(self.orient,1)
				    if wallOrient2 != 'X': cell.defineWall(wallOrient2,1)
                # actualizar muro en celda actual
                cellFound = 0
                for cell in self.cellList:
                    if self.row == cell.row and self.col == cell.col:
                        cellFound = 1
                        cell.defineWall(self.orient,wall)
                if not cellFound:
                    newCell = Cell(self.row,self.col)
                    self.cellList.append(newCell)
                    newCell.defineWall(self.orient,wall)
                self.currentMap = self.buildCurrentMap(self.cellList, self.n_rows, self.n_cols)
                #pathBlocked = wall
                # buscar ruta hacia meta 
                #moveList = self.routeToGoal(self.currentMap, self.row, self.col, self.row_goal, self.col_goal, self.n_rows, self.n_cols)
                # revisar si hay ruta posible
		#self.moveUntilWall(self)


        # imprimir mapa final
        if goalReached:
            print ''
            print 'MAPA FINAL'
            self.currentMap = self.buildCurrentMap(self.cellList, self.n_rows, self.n_cols) 
            print self.currentMap        
    
    def moveUntilWall(self, moveList):
	if len(moveList) == 0:
            print 'cannot reach goal ERROR'
            return
        else:
	    while len(moveList) > 0:
	        self.orient = moveList[0]                
	        self.robot.moveMaze(self.orient,move=0)
	        if self.wallInFront():
		    return
                # moverse hacia meta 
                if moveList[0] == 'n':
                    self.row = self.row + 1
                    self.orient = 'n'
		    self.robot.moveMaze(self.orient)
                elif moveList[0] == 'w':
                    self.col = self.col - 1
                    self.orient = 'w'
		    self.robot.moveMaze(self.orient)
                elif moveList[0] == 's':
                    self.row = self.row - 1
                    self.orient = 's'
		    self.robot.moveMaze(self.orient)
                elif moveList[0] == 'e':
                    self.col = self.col + 1
		    self.orient = 'e'
		    self.robot.moveMaze(self.orient)
                else:
                    print 'invalid move ERROR'
                    break
                print 'Se movio hacia ' + str(moveList[0])
		moveList.pop(0)

    def locateStart(self):
        possibleStart = []
        for r in range(0,self.n_rows):
            for c in range(0,self.n_cols):
                for ori in ['n','w','s','e']:
                    possibleStart.append([r,c,ori])
        x_off = 0
        y_off = 0
        spin_off = 0
        while len(possibleStart)>1:       
            print " "
            print "Quedan " + str(len(possibleStart)) + " posibilidades." 
	    self.robot.sound.say(str(len(possibleStart)) + ' possibilities left')
            # scan current cell
            walls = self.scanCell()
            # select possibilities to remove from list
            updatedList = []
            for poss in possibleStart:
                possible = 0
                for cell in self.cellList:
                    # add offset to current cell from initial cell
                    row_off = 0
                    col_off = 0
                    scan_dir = poss[2]
                    if poss[2] == 'n':
                        shift = ['n','w','s','e']
                        scan_dir = shift[spin_off]
                        row_off = y_off
                        col_off = x_off
                    elif poss[2] == 'w': 
                        shift = ['w','s','e','n']
                        scan_dir = shift[spin_off]
                        col_off = -y_off
                        row_off = x_off
                    elif poss[2] == 's':
                        shift = ['s','e','n','w']
                        scan_dir = shift[spin_off]
                        row_off = -y_off
                        col_off = -x_off
                    elif poss[2] == 'e': 
                        shift = ['e','n','w','s']
                        scan_dir = shift[spin_off]
                        col_off = y_off
                        row_off = -x_off
                    else:
                        print 'POSSIBLITY INTERPRET ERROR'
                    if cell.row == poss[0]+row_off and cell.col == poss[1]+col_off: #incorporar x_off y y_off aqui
                        cellWalls = cell.getWalls(scan_dir)
                        if cellWalls == walls:
                            possible = 1
                if possible:
                    updatedList.append(poss)

            possibleStart = updatedList
            if len(possibleStart) > 1:
                blocked = self.wallInFront()
                spinDir = randint(0,1)
                while blocked:
                    if spinDir == 0: 
                        spin_off = spin_off + 1
                        if self.simulated: print 'Se giro una vez a la izquierda'
			else: self.robot.turnLeft()
                    else:
                        spin_off = spin_off - 1
                        if self.simulated: print 'Se giro una vez a la derecha'
			else: self.robot.turnRight()
                    if spin_off > 3: spin_off = 0
                    if spin_off < 0: spin_off = 3
                    blocked = self.wallInFront()

                if self.simulated:
		    print ''
                    print 'Se movio una celda hacia adelante'
		else:
		    self.robot.advanceOneCell()

                if spin_off == 0:
                    y_off = y_off + 1
                elif spin_off == 1:
                    x_off = x_off - 1
                elif spin_off == 2:
                    y_off = y_off - 1
                elif spin_off == 3:
                    x_off = x_off + 1  
            else:
                # puede haber un error aqui con los offsets
                poss = possibleStart[0]
                row_off = 0
                col_off = 0
                if poss[2] == 'n':
                    shift = ['n','w','s','e']
                    self.orient = shift[spin_off]
                    row_off = y_off
                    col_off = x_off
                elif poss[2] == 'w': 
                    shift = ['w','s','e','n']
                    self.orient = shift[spin_off]
                    col_off = -y_off
                    row_off = x_off
                elif poss[2] == 's':
                    shift = ['s','e','n','w']
                    self.orient = shift[spin_off]
                    row_off = -y_off
                    col_off = -x_off
                elif poss[2] == 'e': 
                    shift = ['e','n','w','s']
                    self.orient = shift[spin_off]
                    col_off = y_off
                    row_off = -x_off
                self.row = poss[0] + row_off
                self.col = poss[1] + col_off
		self.robot.orientacionActual = self.orient
                
        if len(possibleStart) == 1:
            print ''
            print 'Punto de partida original: ' + str(possibleStart[0])
            print 'Posicion actual (row, col, orientacion): '  + str(self.row) + ", " + str(self.col) + ", " + str(self.orient)
	    print 'Orientacion actual segun robot: '  + str(self.robot.orientacionActual)
	    print ' '
	    self.robot.sound.say('I know where I am')
        else:
            print 'BÚSQUEDA FALLÓ'
    
    def readMap(self, fileName):
        f = open(fileName, 'r')
        mapFile = f.read()
        return mapFile

    def mapDimensions(self, mapFile):
        mapLines = mapFile.split('\n')
        mapLine = mapLines[0]
        lineData = mapLine.split(' ')
        n_rows = int(lineData[0])
        n_cols = int(lineData[1])
        return [n_rows, n_cols]

    def moveAndUpdate(self,move):
	if move == 'n':
		self.row = self.row + 1
		self.orient = 'n'
		self.robot.moveMaze(self.orient)
	elif move == 'w':
		self.col = self.col - 1
		self.orient = 'w'
		self.robot.moveMaze(self.orient)
	elif move == 's':
		self.row = self.row - 1
		self.orient = 's'
		self.robot.moveMaze(self.orient)
	elif move == 'e':
		self.col = self.col + 1
		self.orient = 'e'
		self.robot.moveMaze(self.orient)
	else:
		print 'invalid move ERROR'

    def startPositionMap(self, mapFile):
        mapLines = mapFile.split('\n')
        i = mapLines.index("START")
        mapLine = mapLines[i+2]
        lineData = mapLine.split(' ')
        row0 = int(lineData[0])
        col0 = int(lineData[1])
        orient0 = ''
        if lineData[2] == 'u':
            orient0 = 'n'
        elif lineData[2] == 'l':
            orient0 = 'w'
        elif lineData[2] == 'd':
            orient0 = 's'
        elif lineData[2] == 'r':
            orient0 = 'e'
        else:
            print 'MAP READ ERROR: START ORIENTATION'
        return [row0, col0, orient0]

    def goalPositionMap(self, mapFile):
        mapLines = mapFile.split('\n')
        i = mapLines.index("GOAL")
        mapLine = mapLines[i+2]
        lineData = mapLine.split(' ')
        row_goal = int(lineData[0])
        col_goal = int(lineData[1])
        return [row_goal, col_goal]

    def getCellsMap(self, mapFile):
        cellList = []
        mapLines = mapFile.split('\n')
        i = mapLines.index("START")
        cellLines = mapLines[1:i]
        for line in cellLines:
            lineData = line.split(' ')
            newCell = Cell(int(lineData[0]), int(lineData[1])) 
            newCell.defineWall('n',int(lineData[2]))
            newCell.defineWall('w',int(lineData[3]))
            newCell.defineWall('s',int(lineData[4]))
            newCell.defineWall('e',int(lineData[5]))
            cellList.append(newCell)    
        return cellList   
    
    def buildCurrentMap(self, cellList, n_rows, n_cols):
        currentMap = str(n_rows) + ' ' + str(n_cols) + '\n'
        for cell in cellList:
            currentMap = currentMap + cell.mapData()
        return currentMap

    def wallInFront(self):
	wall = 0
	if self.simulated:       
	    wall = input("Muro al frente?: ")
	else:
	    wall = self.robot.kinect.wallInFront()
	    print 'hay muro: ' + str(wall)
        return wall
    
    def searchCell(self):
	results = np.zeros(4, dtype=np.int)
	for i in range(0,4):
	    if self.robot.kinect.wallInFront():
		self.robot.correctWallInFront()
		#r = rospy.Rate(10)		
		#for i in range(0,2):
		#	r.sleep()
		if self.robot.kinect.detectarCara():
			self.robot.sound.playSound('/home/user/sounds/person.wav')
			print 'Hay cara en: ' + str(self.row) + '/' + str(self.col) + ' - ' + str(self.orient)
			results[0] = 1
		elif self.robot.kinect.detectarPuerta():
			self.robot.sound.playSound('/home/user/sounds/exit.wav')
			print 'Hay puerta en: ' + str(self.row) + '/' + str(self.col) + ' - ' + str(self.orient)
			results[2] = 1
		else:
			llave = 0			
			for i in range(0,5):
				llave = llave or self.robot.kinect.detectarLlave2()
			if llave:			
				self.robot.sound.playSound('/home/user/sounds/key.wav')
				print 'Hay llave en: ' + str(self.row) + '/' + str(self.col) + ' - ' + str(self.orient)
				results[1] = 1
	    self.robot.turnLeft()
	    #print "turning left"
	    self.updateOrientLeft()
	#print results
        return results
	
    def orientAtRight(self):
	if self.orient == 'n':
	    return'e'
	elif self.orient == 'w':
	    return 'n'
	elif self.orient == 's':
	    return 'w'
	elif self.orient == 'e':
	    return 's'
	else:
	    print 'INVALID ORIENT ERROR - RIGHT'

    def orientAtLeft(self):
	if self.orient == 'n':
	    return'w'
	elif self.orient == 'w':
	    return 's'
	elif self.orient == 's':
	    return 'e'
	elif self.orient == 'e':
	    return 'n'
	else:
	    print 'INVALID ORIENT ERROR - LEFT'

    def orientAtBack(self):
	if self.orient == 'n':
	    return's'
	elif self.orient == 'w':
	    return 'e'
	elif self.orient == 's':
	    return 'n'
	elif self.orient == 'e':
	    return 'w'
	else:
	    print 'INVALID ORIENT ERROR - BACK'

    def updateOrientLeft(self):
	newOrient = 'X'	
	if self.orient == 'n':
	    newOrient = 'w'
	elif self.orient == 'w':
	    newOrient = 's'
	elif self.orient == 's':
	    newOrient = 'e'
	elif self.orient == 'e':
	    newOrient = 'n'
	else:
	    print 'INVALID ORIENT ERROR - TURN LEFT'
	self.orient = newOrient

    def scanCell(self):
        walls = []
        for i in range(0,4):
            if self.simulated:
		walls.append(self.wallInFront())
            	#print 'Se giro una vez a la izquierda'
	    else:
		walls.append(self.wallInFront())
		self.robot.turnLeft()
        return walls
    
    def nextSearchCell(self, currentMap, visitedCells, row, col, n_rows, n_cols):
	search = SearchNode(row, col, 0)
        search.buildNodes(None, currentMap, n_rows, n_cols, self.row_goal, self.col_goal)
	nearestCell = []
	minDepth = 999999
	for r in range(0,n_rows):
	    for c in range(0,n_cols):
		[cell, cellParentList] = search.getCell(r,c,None)
		if cell != None:
			print str(r) + '/' + str(c) + ' depth: ' + str(cell.depth) + ' visited? ' + str(visitedCells[r,c])			
			if cell.depth < minDepth and cell.depth > 0 and visitedCells[r,c] == 0:
				minDepth = cell.depth				
				nearestCell = [r,c]
	return nearestCell[0], nearestCell[1]


    def routeToGoal(self, currentMap, row, col, row_goal, col_goal, n_rows, n_cols, show=1):
        moveList = []
        search = None
        search = SearchNode(row, col, 0)
        search.buildNodes(None, currentMap, n_rows, n_cols, row_goal, col_goal)
	print 'arbol armado'
        if search.moveToGoal(row_goal, col_goal, moveList):
            if show: print moveList
            return moveList
        else:
            return[]  
        








