#!/usr/bin/python
# -*- coding: latin-1 -*-
from busqueda.celda import *

class Mapa(object):
    """Clase que representa a un mapa del problema """
    def __init__(self, archname= ""):
        self.estructura = []
        self._xSize = -1
        self._ySize = -1
        self.startCelda = None
        self.endCelda = None
        self.startDirection = 'n'
        self.endDirection= "n"

        self._celdasFinal = None
        self._finalPath = None


        if archname  != "":
            self.loadFile(archname)


    def loadFile(self, archname):
        arch = open(archname, 'r')
        text = ""
        walldetect = False
        startdetect = False
        goaldetect = False
        print(" cargando archivo ")
        for l in arch:
            l = l[:-1]
            data = l.split(' ')
            #print(l)

            if l== "START":
                #print("start detectado")
                startdetect =True
                walldetect=False
            elif l=="GOAL":
                #print("goal detectado")
                goaldetect= True
                startdetect=False
            else:
                
                if len(data) ==2:
                    #print("walldetect detectado")

                    #print("construyendo estructura")
                    walldetect= True
                    self._xSize= int(data[0])
                    self._ySize= int(data[1])
                    for x in range(0,self._xSize):
                        self.estructura.append(list())
                        for y in range(0,self._ySize):
                            c = Celda(x,y)
                            if x==0:
                                c.west=-1
                            elif x == self._xSize-1:
                                c.east=-1
                            if y == 0:
                                c.south= -1
                            elif y == self._ySize-1:
                                c.north=-1


                            self.estructura[x].append(c)

                    for x in range(0,self._xSize):
                        for y in range(0,self._ySize):
                            
                            c = self.estructura[x][y]
                            if c.north != -1:
                                c.north = self.estructura[x][y+1]
                            if c.south != -1:
                                c.south= self.estructura[x][y-1]
                            if c.west != -1:
                                c.west= self.estructura[x-1][y]
                            if c.east != -1:
                                c.east=self.estructura[x+1][y]

            if walldetect==True:
                #print("detección de muros")
                if len(data) == 6:
                    #print("cantidad de datos correcta")

                    y = int(data[0])
                    x = int(data[1])
                    
                    if data[2] == "1":

                        self.estructura[x][y].north= -1*int(data[2])
                    if data[3] == "1":
                        self.estructura[x][y].west = -1*int(data[3])
                    if data[4] == "1":
                        self.estructura[x][y].south = -1*int(data[4])
                    if data[5] == "1":
                        self.estructura[x][y].east = -1*int(data[5])

            elif startdetect == True:
                #print("detección de start")
                if len(data) == 3:
                    #print("cantidad de datos correcta")

                    y = int(data[0])
                    x = int(data[1])
                    print(" partida detectada en %i, %i " % (x,y))
                    self.startDirection = data[2]
                    self.estructura[x][y].start = True
                    self.startCelda= self.estructura[x][y]

            elif goaldetect == True:
                #print("iniciando detección de goal")
                if len(data) == 3:
                    #print("cantidad de datos Ok ")

                    y = int(data[0])
                    x = int(data[1])
                    direction = data[2]
                    print("final detectado en %i, %i, con dirección %s " %(x,y, direction))
                    self.endDirection = direction
                    
                    self.estructura[x][y].goal= True
                    if direction== 'u':
                        self.estructura[x][y].north =ENDPOINT
                    elif direction == 'l':
                        self.estructura[x][y].west = ENDPOINT
                    elif direction == 'd':
                        self.estructura[x][y].south = ENDPOINT
                    elif direction == 'r':
                        self.estructura[x][y].east= ENDPOINT
                    self.endCelda=self.estructura[x][y]



        arch.close()



    def resetCostAndPath(self):
        for x in range(0,self._xSize):
            for y in range(0,self._ySize):
                
                self.estructura[x][y].currentTotalCost = 99999999
                self.estructura[x][y].euristicCost = 99999999
                self.estructura[x][y].currentCost = 99999999 

    def getStartDirection(self):
	if(self.startDirection == 'l'):
		return 'w'
	elif(self.startDirection == 'u'):
		return 'n'
	elif(self.startDirection == 'd'):
		return 's'
	elif(self.startDirection == 'r'):
		return 'e'
	else:
		return 'error'

    def getCompletePath(self):
        return(self._finalPath)

    def getFinalCeldas(self):
        return(self._celdasFinal)

    def getPosition(self, x, y):
        if x>= self._xSize or y >= self._ySize:
            return(None)
        else:

            return(self.estructura[x][y])

    def solveMap(self):
        self.resetCostAndPath()
        self._celdasFinal= None
        self._finalPath=None
        self.startCelda.currentCost = 0
        self.startCelda.euristicCost = self.__calculateEuristic(self.startCelda)
        self.startCelda.currentTotalCost = self.startCelda.currentCost + self.startCelda.euristicCost
        self.__recursiveStep(self.startCelda, None)

        celdas = []
        c= self.endCelda
        while c != UNDEFINEDPATH:
            celdas.append(c)
            c = c.previousCelda
        celdas.reverse()
        self._celdasFinal=celdas
        pat = self._ProcessPath(celdas)
        self._finalPath= pat
        #print(pat)
        return(pat)

    def _ProcessPath(self, celdas):
        pathlist=[]
        for x in range(0,len(celdas)):
            if not celdas[x].goal:
                if celdas[x].north == celdas[x+1]:
                    pathlist.append("n")
                if celdas[x].west == celdas[x+1]:
                    pathlist.append("w")
                if celdas[x].south == celdas[x+1]:
                    pathlist.append("s")
                if celdas[x].east == celdas[x+1]:
                    pathlist.append("e")
                    



        return(pathlist)


    def __recursiveStep(self, celda, previous):
        #print(" paso recursivo para " + str(celda))
        #print(" llegando desde " + str(previous))

        if celda.north != WALL and celda.north != ENDPOINT and celda.north != UNDEFINEDPATH:
            
            c = celda.north
            #print("yendo al norte:  " + str(c))
            if c!= previous:
                #print("entrada correcta ")

                c.euristicCost = self.__calculateEuristic(c)
                newCost = celda.currentCost+1
                newCurrentTotalCost =newCost + c.euristicCost
                if newCurrentTotalCost <= c.currentTotalCost:
                    c.currentCost = newCost
                    c.currentTotalCost = newCurrentTotalCost
                    c.previousCelda = celda

                    self.__recursiveStep(c,celda)

        if celda.west != WALL and celda.west != ENDPOINT and celda.west != UNDEFINEDPATH:
            c = celda.west
            #print("yendo al oeste:  " + str(c))
            if c != previous:
                #print("entrada correcta ")

                c.euristicCost = self.__calculateEuristic(c)
                newCost = celda.currentCost+1
                newCurrentTotalCost = newCost + c.euristicCost
                if newCurrentTotalCost <= c.currentTotalCost:
                    c.currentCost = newCost
                    c.currentTotalCost = newCurrentTotalCost
                    c.previousCelda =celda

                    self.__recursiveStep(c,celda)

        if celda.south != WALL and celda.south != ENDPOINT and celda.south != UNDEFINEDPATH:
            c = celda.south
            #print("yendo al sur:  " + str(c))
            if c != previous:
                #print("entrada correcta ")

                c.euristicCost = self.__calculateEuristic(c)
                newCost = celda.currentCost+1
                newCurrentTotalCost = newCost + c.euristicCost
                if newCurrentTotalCost <= c.currentTotalCost:
                    c.currentCost = newCost
                    c.currentTotalCost = newCurrentTotalCost
                    c.previousCelda =celda

                    self.__recursiveStep(c,celda)

        if celda.east != WALL and celda.east != ENDPOINT and celda.east != UNDEFINEDPATH:
            c = celda.east
            #print("yendo al este:  " + str(c))
            if c != previous:
                #print("entrada correcta ")

                c.euristicCost = self.__calculateEuristic(c)
                newCost = celda.currentCost+1
                newCurrentTotalCost = newCost + c.euristicCost
                if newCurrentTotalCost <= c.currentTotalCost:
                    c.currentCost = newCost
                    c.currentTotalCost = newCurrentTotalCost
                    c.previousCelda =celda

                    self.__recursiveStep(c,celda)


    def __calculateEuristic(self, celda):
        xdist = self.endCelda.x - celda.x
        ydist = self.endCelda.y - celda.y
        if xdist<0:
            xdist*=-1
        if ydist<0:
            ydist*=-1
        return(xdist+ydist)






