
# coding: utf-8

# In[1]:

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
        if direction == 'N':
            self.wallN = wall
        elif direction == 'W':
            self.wallW = wall
        elif direction == 'S':
            self.wallS = wall
        elif direction == 'E':
            self.wallE = wall
        else:
            print 'Invalid direction'
    
    def getWalls(self,direction):
        if direction == 'N':
            return [self.wallN, self.wallW, self.wallS, self.wallE]
        elif direction == 'W':
            return [self.wallW, self.wallS, self.wallE, self.wallN]
        elif direction == 'S':
            return [self.wallS, self.wallE, self.wallN, self.wallW]
        elif direction == 'E':
            return [self.wallE, self.wallN, self.wallW, self.wallS]
        else:
            print 'Invalid direction'
    
    def mapData(self):
        return '{0} {1} {2} {3} {4} {5}\n'.format(self.row, self.col, 
                                               self.wallN, self.wallW, 
                                               self.wallS, self.wallE)


# In[3]:

'''
def buildCurrentMap(cellList, n_rows, n_cols):
    currentMap = str(n_rows) + ' ' + str(n_cols) + '\n'
    for cell in cellList:
        currentMap = currentMap + cell.mapData()
    return currentMap

def wallInFront():
    wall = input("Muro al frente?: ")
    return wall
'''

class SearchNode:
    def __init__(self, row, col, depth):
        self.row = row
        self.col = col
        self.nodeList = []
        self.depth = depth
        
        #print 'fila: ' + str(self.row) + " - columna: " + str(self.col) + ' - depth: ' + str(self.depth)

    def buildNodes(self, startNode, cellMap, n_rows, n_cols):
        if(startNode == None):
            startNode = self
        
        ## esto puede optimizarse actualizando los depths
        
        # NORTH NODE
        if ((self.row+1<n_rows) and (self.wallInDirection(cellMap,'N') != 1)):
            [targetCell, targetCellParentList] = startNode.getCell(self.row+1, self.col, None)
            if not startNode.hasCell(self.row+1, self.col):
                node = SearchNode(self.row+1, self.col, self.depth+1)
                self.nodeList.append(node)
            elif startNode.hasCell(self.row+1, self.col) and targetCell.depth > self.depth+1:
                #print 'REMOVED: fila: ' + str(targetCell.row) + " - columna: " + str(targetCell.col) + ' - depth: ' + str(targetCell.depth)
                #for node in targetCellParentList:
                #    print "node row: " + str(node.row) + " - node col: " + str(node.col)
                targetCellParentList.remove(targetCell)
                node = SearchNode(self.row+1, self.col, self.depth+1)
                self.nodeList.append(node)
        # WEST NODE
        if (self.col-1>-1) and (self.wallInDirection(cellMap,'W') != 1):
            [targetCell, targetCellParentList] = startNode.getCell(self.row, self.col -1, None)
            if not startNode.hasCell(self.row, self.col-1):
                node = SearchNode(self.row, self.col-1, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)
            elif startNode.hasCell(self.row, self.col-1) and targetCell.depth > self.depth+1:
                #print 'REMOVED: fila: ' + str(targetCell.row) + " - columna: " + str(targetCell.col) + ' - depth: ' + str(targetCell.depth)
                targetCellParentList.remove(targetCell)
                node = SearchNode(self.row, self.col-1, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)                
        # SOUTH NODE
        if (self.row-1>-1) and (self.wallInDirection(cellMap,'S') != 1):
            [targetCell, targetCellParentList] = startNode.getCell(self.row-1, self.col, None)
            if not startNode.hasCell(self.row-1, self.col):
                node = SearchNode(self.row-1, self.col, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)
            elif startNode.hasCell(self.row-1, self.col) and targetCell.depth > self.depth+1:
                #print 'REMOVED: fila: ' + str(targetCell.row) + " - columna: " + str(targetCell.col) + ' - depth: ' + str(targetCell.depth)
                targetCellParentList.remove(targetCell)
                node = SearchNode(self.row-1, self.col, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)
        # EAST NODE
        if (self.col+1<n_cols) and (self.wallInDirection(cellMap,'E') != 1):
            [targetCell, targetCellParentList] = startNode.getCell(self.row, self.col+1, None)
            if not startNode.hasCell(self.row, self.col+1):
                node = SearchNode(self.row, self.col+1, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)
            elif startNode.hasCell(self.row, self.col+1) and targetCell.depth > self.depth+1:
                #print 'REMOVED: fila: ' + str(targetCell.row) + " - columna: " + str(targetCell.col) + ' - depth: ' + str(targetCell.depth)
                targetCellParentList.remove(targetCell)
                node = SearchNode(self.row, self.col+1, self.depth+1)#, startNode, cellMap, n_rows, n_cols)
                self.nodeList.append(node)
        
        for node in self.nodeList:
            node.buildNodes(startNode, cellMap, n_rows, n_cols)
    
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
                if direction == 'N':
                    return int(lineData[2])
                elif direction == 'W':
                    return int(lineData[3])
                elif direction == 'S':
                    return int(lineData[4])
                elif direction == 'E':
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
                    moveList.append('N')
                    if node.moveToGoal(row_goal, col_goal, moveList):
                        return 1
                elif node.col < self.col:
                    moveList.append('W')
                    if node.moveToGoal(row_goal, col_goal, moveList):
                        return 1
                elif node.row < self.row:
                    moveList.append('S')
                    if node.moveToGoal(row_goal, col_goal, moveList):
                        return 1
                elif node.col > self.col:
                    moveList.append('E')
                    if node.moveToGoal(row_goal, col_goal, moveList):
                        return 1
            #print 'row: ' + str(self.row) + ' - col: ' + str(self.col)
            #print 'row: ' + str(self.nodeList[0].row) + ' - col: ' + str(self.nodeList[0].col)
            moveList.pop()
            return 0

'''
def routeToGoal(currentMap, row, col, row_goal, col_goal, n_rows, n_cols, show=0):
    moveList = []
    search = None
    search = SearchNode(row, col, 0)
    search.buildNodes(None, currentMap, n_rows, n_cols)

    if search.moveToGoal(row_goal, col_goal, moveList):
        if show: print moveList
        return moveList
    else:
        return[] 
'''


# In[4]:

'''
def readMap(fileName):
    f = open(fileName, 'r')
    mapFile = f.read()
    return mapFile

def mapDimensions(mapFile):
    mapLines = mapFile.split('\n')
    mapLine = mapLines[0]
    lineData = mapLine.split(' ')
    n_rows = int(lineData[0])
    n_cols = int(lineData[1])
    
    return [n_rows, n_cols]

def startPositionMap(mapFile):
    mapLines = mapFile.split('\n')
    i = mapLines.index("START")
    mapLine = mapLines[i+2]
    lineData = mapLine.split(' ')
    row0 = int(lineData[0])
    col0 = int(lineData[1])
    orient0 = ''
    if lineData[2] == 'u':
        orient0 = 'N'
    elif lineData[2] == 'l':
        orient0 = 'W'
    elif lineData[2] == 'd':
        orient0 = 'S'
    elif lineData[2] == 'r':
        orient0 = 'E'
    else:
        print 'MAP READ ERROR: START ORIENTATION'
    
    return [row0, col0, orient0]

def goalPositionMap(mapFile):
    mapLines = mapFile.split('\n')
    i = mapLines.index("GOAL")
    mapLine = mapLines[i+2]
    lineData = mapLine.split(' ')
    row_goal = int(lineData[0])
    col_goal = int(lineData[1])
    
    return [row_goal, col_goal]

def getCellsMap(mapFile):
    cellList = []
    mapLines = mapFile.split('\n')
    i = mapLines.index("START")
    cellLines = mapLines[1:i]
    for line in cellLines:
        lineData = line.split(' ')
        newCell = Cell(int(lineData[0]), int(lineData[1])) 
        newCell.defineWall('N',int(lineData[2]))
        newCell.defineWall('W',int(lineData[3]))
        newCell.defineWall('S',int(lineData[4]))
        newCell.defineWall('E',int(lineData[5]))
        cellList.append(newCell)    
    return cellList   
'''


# In[5]:

'''
mapKnown = 1
startKnown = 0

mapFile = readMap('mapa.txt')
#[row0, col0, orient0] = startPositionMap(mapFile)
[row_goal, col_goal] = goalPositionMap(mapFile)
[n_rows, n_cols] = mapDimensions(mapFile)

print 'Fila objetivo: ' + str(row_goal)
print 'Columna objetivo: ' + str(col_goal)
print 'Numero de filas: ' + str(n_rows)
print 'Numero de columnas: ' + str(n_cols)

row = 0 
col = 0 
orient = 'X'

startCell = None
if startKnown:
    [row0, col0, orient0] = startPositionMap(mapFile)
    startCell = Cell(row0, col0) 
    row = row0 
    col = col0 
    orient = orient0
#else:
    
cellList = []
if mapKnown:
    cellList = getCellsMap(mapFile)
else:
    cellList = [startCell]

currentMap = buildCurrentMap(cellList, n_rows, n_cols)
'''


# In[6]:

'''
def scanCell():
    walls = []
    for i in range(0,4):
        walls.append(wallInFront())
        print 'Se giro una vez a la izquierda'
    return walls
'''
'''
if (not startKnown):
    possibleStart = []
    for r in range(0,n_rows):
        for c in range(0,n_cols):
            for ori in ['N','W','S','E']:
                possibleStart.append([r,c,ori])
    
    #for poss in possibleStart:
    #    print poss
    
    #for cell in cellList:
    #    print cell.getWalls('E')
    
    x_off = 0
    y_off = 0
    spin_off = 0
    while len(possibleStart)>1:       
        print " "
        print "Quedan " + str(len(possibleStart)) + " posibilidades." 
        # scan current cell
        walls = scanCell()
        # select possibilities to remove from list
        updatedList = []
        for poss in possibleStart:
            possible = 0
            for cell in cellList:
                row_off = 0
                col_off = 0
                scan_dir = poss[2]
                if poss[2] == 'N':
                    shift = ['N','W','S','E']
                    scan_dir = shift[spin_off]
                    row_off = y_off
                    col_off = x_off
                elif poss[2] == 'W': 
                    shift = ['W','S','E','N']
                    scan_dir = shift[spin_off]
                    col_off = -y_off
                    row_off = x_off
                elif poss[2] == 'S':
                    shift = ['S','E','N','W']
                    scan_dir = shift[spin_off]
                    row_off = -y_off
                    col_off = -x_off
                elif poss[2] == 'E': 
                    shift = ['E','N','W','S']
                    scan_dir = shift[spin_off]
                    col_off = y_off
                    row_off = -x_off
                else:
                    print 'POSSIBLITY INTERPRET ERROR'
                if cell.row == poss[0]+row_off and cell.col == poss[1]+col_off: #incorporar x_off y y_off aqui
                    cellWalls = cell.getWalls(scan_dir)
                    if cellWalls == walls:
                        possible = 1
                        #print str(cell.row) + " - " +str(cell.col) + ": " + str(cellWalls)
                        #break
            if possible:
                updatedList.append(poss)
                        
        possibleStart = updatedList
        if len(possibleStart) > 1:
            blocked = wallInFront()
            spinDir = randint(0,1)
            while blocked:
                if spinDir == 0: 
                    spin_off = spin_off + 1
                    print 'Se giro una vez a la izquierda'
                else:
                    spin_off = spin_off - 1
                    print 'Se giro una vez a la derecha'
                if spin_off > 3: spin_off = 0
                if spin_off < 0: spin_off = 3
                blocked = wallInFront()

            print ''
            print 'Se movio una celda hacia adelante'

            if spin_off == 0:
                y_off = y_off + 1
            elif spin_off == 1:
                x_off = x_off - 1
            elif spin_off == 2:
                y_off = y_off - 1
            elif spin_off == 3:
                x_off = x_off + 1  
        else:
            poss = possibleStart[0]
            row_off = 0
            col_off = 0
            if poss[2] == 'N':
                shift = ['N','W','S','E']
                orient = shift[spin_off]
                row_off = y_off
                col_off = x_off
            elif poss[2] == 'W': 
                shift = ['W','S','E','N']
                orient = shift[spin_off]
                col_off = -y_off
                row_off = x_off
            elif poss[2] == 'S':
                shift = ['S','E','N','W']
                orient = shift[spin_off]
                row_off = -y_off
                col_off = -x_off
            elif poss[2] == 'E': 
                shift = ['E','N','W','S']
                orient = shift[spin_off]
                col_off = y_off
                row_off = -x_off
            row = poss[0] + row_off
            col = poss[1] + col_off
                
    
    if len(possibleStart) == 1:
        print ''
        print 'Punto de partida original: ' + str(possibleStart[0])
        print 'Posicion actual (row, col, orientacion): '  + str(row) + ", " + str(col) + ", " + str(orient)
    else:
        print 'BÚSQUEDA FALLÓ'
'''       
        
        


# In[28]:

class Navigator:
    
    def __init__(self, robot, fileName, mapKnown, startKnown):
	self.robot = robot        
	self.mapKnown = mapKnown
        self.startKnown = startKnown
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

        startCell = None
        if self.startKnown:
            [row0, col0, orient0] = self.startPositionMap(self.mapFile)
            startCell = Cell(row0, col0) 
            self.row = row0 
            self.col = col0 
            self.orient = orient0
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
    
    def goToGoal(self):
        goalReached = 0
        while(not goalReached):
            # revisar si se llego a la meta
            if self.row == self.row_goal and self.col == self.col_goal:
                goalReached = 1
                break    
            # buscar ruta hacia meta 
            moveList = self.routeToGoal(self.currentMap, self.row, self.col, self.row_goal, self.col_goal, self.n_rows, self.n_cols)
            # revisar si hay ruta posible
            if len(moveList) == 0:
                print 'cannot reach goal ERROR'
                break
            else:
                # girar el robot
                self.orient = moveList[0]
            # revisar si hay muro en frente y actualizar orientacion
            pathBlocked = 1
            while pathBlocked and (not self.mapKnown):       
                # imprimir posicion actual
                print ''
                print 'ROW: ' + str(self.row) + ' - COL: ' + str(self.col) + ' - ORIENT: ' + str(self.orient)
                # imprimir mapa actual
                print ''
                print 'MAPA ACTUAL'
                self.currentMap = self.buildCurrentMap(self.cellList, self.n_rows, self.n_cols) 
                print self.currentMap
                # revisar muro en frente
                print ''
                wall = self.wallInFront()
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
                pathBlocked = wall
                # buscar ruta hacia meta 
                moveList = self.routeToGoal(self.currentMap, self.row, self.col, self.row_goal, self.col_goal, self.n_rows, self.n_cols)
                # revisar si hay ruta posible
                if len(moveList) == 0:
                    print 'cannot reach goal ERROR'
                    break
                else:
                    # girar el robot
                    self.orient = moveList[0]

            # moverse hacia meta 
            if moveList[0] == 'N':
                self.row = self.row + 1
                self.orient = 'N'
            elif moveList[0] == 'W':
                self.col = self.col - 1
                self.orient = 'W'
            elif moveList[0] == 'S':
                self.row = self.row - 1
                self.orient = 'S'
            elif moveList[0] == 'E':
                self.col = self.col + 1
            else:
                print 'invalid move ERROR'
                break
            print 'Se movio hacia ' + str(moveList[0])

        # imprimir mapa final
        if goalReached:
            print ''
            print 'MAPA FINAL'
            self.currentMap = self.buildCurrentMap(self.cellList, self.n_rows, self.n_cols) 
            print self.currentMap        
    
    def locateStart(self):
        possibleStart = []
        for r in range(0,self.n_rows):
            for c in range(0,self.n_cols):
                for ori in ['N','W','S','E']:
                    possibleStart.append([r,c,ori])
        x_off = 0
        y_off = 0
        spin_off = 0
        while len(possibleStart)>1:       
            print " "
            print "Quedan " + str(len(possibleStart)) + " posibilidades." 
            # scan current cell
            walls = scanCell()
            # select possibilities to remove from list
            updatedList = []
            for poss in possibleStart:
                possible = 0
                for cell in cellList:
                    # add offset to current cell from initial cell
                    row_off = 0
                    col_off = 0
                    scan_dir = poss[2]
                    if poss[2] == 'N':
                        shift = ['N','W','S','E']
                        scan_dir = shift[spin_off]
                        row_off = y_off
                        col_off = x_off
                    elif poss[2] == 'W': 
                        shift = ['W','S','E','N']
                        scan_dir = shift[spin_off]
                        col_off = -y_off
                        row_off = x_off
                    elif poss[2] == 'S':
                        shift = ['S','E','N','W']
                        scan_dir = shift[spin_off]
                        row_off = -y_off
                        col_off = -x_off
                    elif poss[2] == 'E': 
                        shift = ['E','N','W','S']
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
                        print 'Se giro una vez a la izquierda'
                    else:
                        spin_off = spin_off - 1
                        print 'Se giro una vez a la derecha'
                    if spin_off > 3: spin_off = 0
                    if spin_off < 0: spin_off = 3
                    blocked = self.wallInFront()

                print ''
                print 'Se movio una celda hacia adelante'

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
                if poss[2] == 'N':
                    shift = ['N','W','S','E']
                    self.orient = shift[spin_off]
                    row_off = y_off
                    col_off = x_off
                elif poss[2] == 'W': 
                    shift = ['W','S','E','N']
                    self.orient = shift[spin_off]
                    col_off = -y_off
                    row_off = x_off
                elif poss[2] == 'S':
                    shift = ['S','E','N','W']
                    self.orient = shift[spin_off]
                    row_off = -y_off
                    col_off = -x_off
                elif poss[2] == 'E': 
                    shift = ['E','N','W','S']
                    self.orient = shift[spin_off]
                    col_off = y_off
                    row_off = -x_off
                self.row = poss[0] + row_off
                self.col = poss[1] + col_off
                
        if len(possibleStart) == 1:
            print ''
            print 'Punto de partida original: ' + str(possibleStart[0])
            print 'Posicion actual (row, col, orientacion): '  + str(row) + ", " + str(col) + ", " + str(orient)
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

    def startPositionMap(self, mapFile):
        mapLines = mapFile.split('\n')
        i = mapLines.index("START")
        mapLine = mapLines[i+2]
        lineData = mapLine.split(' ')
        row0 = int(lineData[0])
        col0 = int(lineData[1])
        orient0 = ''
        if lineData[2] == 'u':
            orient0 = 'N'
        elif lineData[2] == 'l':
            orient0 = 'W'
        elif lineData[2] == 'd':
            orient0 = 'S'
        elif lineData[2] == 'r':
            orient0 = 'E'
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
            newCell.defineWall('N',int(lineData[2]))
            newCell.defineWall('W',int(lineData[3]))
            newCell.defineWall('S',int(lineData[4]))
            newCell.defineWall('E',int(lineData[5]))
            cellList.append(newCell)    
        return cellList   
    
    def buildCurrentMap(self, cellList, n_rows, n_cols):
        currentMap = str(n_rows) + ' ' + str(n_cols) + '\n'
        for cell in cellList:
            currentMap = currentMap + cell.mapData()
        return currentMap

    # debe reemplazarse 
    def wallInFront(self):
        wall = input("Muro al frente?: ")
        return wall
    
    # debe reemplazarse
    def scanCell():
        walls = []
        for i in range(0,4):
            walls.append(wallInFront())
            print 'Se giro una vez a la izquierda'
        return walls
    
    def routeToGoal(self, currentMap, row, col, row_goal, col_goal, n_rows, n_cols, show=0):
        moveList = []
        search = None
        search = SearchNode(row, col, 0)
        search.buildNodes(None, currentMap, n_rows, n_cols)

        if search.moveToGoal(row_goal, col_goal, moveList):
            if show: print moveList
            return moveList
        else:
            return[]  
        


# In[29]:

'''
goalReached = 0
while(not goalReached):
    
    # revisar si se llego a la meta
    if row == row_goal and col == col_goal:
        goalReached = 1
        break
       
    pathBlocked = 1
    
    # buscar ruta hacia meta 
    moveList = routeToGoal(currentMap, row, col, row_goal, col_goal, n_rows, n_cols)
    
    if len(moveList) == 0:
        print 'cannot reach goal ERROR'
        break
    else:
        orient = moveList[0]
    
    while pathBlocked and (not mapKnown):       
        # imprimir posicion actual
        print ''
        print 'ROW: ' + str(row) + ' - COL: ' + str(col) + ' - ORIENT: ' + str(orient)
        
        # imprimir mapa actual
        print ''
        print 'MAPA ACTUAL'
        currentMap = buildCurrentMap(cellList,n_rows,n_cols) 
        print currentMap
        
        # revisar muro en frente
        print ''
        wall = wallInFront()

        # actualizar muro en celda actual
        cellFound = 0
        for cell in cellList:
            if row == cell.row and col == cell.col:
                cellFound = 1
                cell.defineWall(orient,wall)
        if not cellFound:
            newCell = Cell(row,col)
            cellList.append(newCell)
            newCell.defineWall(orient,wall)
        currentMap = buildCurrentMap(cellList, n_rows, n_cols)
        
        pathBlocked = wall
        
         # buscar ruta hacia meta 
        moveList = routeToGoal(currentMap, row, col, row_goal, col_goal, n_rows, n_cols)

        if len(moveList) == 0:
            print 'cannot reach goal ERROR'
            break
        else:
            orient = moveList[0]

    # moverse hacia meta 
    if moveList[0] == 'N':
        row = row + 1
        orient = 'N'
    elif moveList[0] == 'W':
        col = col - 1
        orient = 'W'
    elif moveList[0] == 'S':
        row = row - 1
        orient = 'S'
    elif moveList[0] == 'E':
        col = col + 1
    else:
        print 'invalid move ERROR'
        break
    print 'Se movio hacia ' + str(moveList[0])

# imprimir mapa final
if goalReached:
    print ''
    print 'MAPA FINAL'
    currentMap = buildCurrentMap(cellList,n_rows,n_cols) 
    print currentMap
'''







