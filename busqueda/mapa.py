#!/usr/bin/python
# -*- coding: latin-1 -*-
from busqueda.celda import *

NORTH = 0
EAST = 1
SOUTH =2
WEST=3

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
                #print("detecci�n de muros")
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
                #print("detecci�n de start")
                if len(data) == 3:
                    #print("cantidad de datos correcta")

                    y = int(data[0])
                    x = int(data[1])
                    print(" partida detectada en %i, %i " % (x,y))
                    self.startDirection = data[2]
                    self.estructura[x][y].start = True
                    self.startCelda= self.estructura[x][y]

            elif goaldetect == True:
                #print("iniciando detecci�n de goal")
                if len(data) == 3:
                    #print("cantidad de datos Ok ")

                    y = int(data[0])
                    x = int(data[1])
                    direction = data[2]
                    print("final detectado en %i, %i, con direcci�n %s " %(x,y, direction))
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


    def _debugSetStartCeld(self):
        self.debugStartCeld = self.estructura[1][1]
        self.debugStartPositionAndCeld = (self.debugStartCeld,SOUTH)
        self.debugCurrentPositionCeld = self.debugStartPositionAndCeld
        print(" seteada posicion celda inicial de depuraci�n, %s con direccion %i " % (str(self.debugCurrentPositionCeld[0]), self.debugCurrentPositionCeld[1]))

    def _debugIsWallInFront(self):
        if self.debugCurrentPositionCeld[1] == NORTH:
            
            if self.debugCurrentPositionCeld[0].north == WALL:
                print("muro en norte")
                return(True)
        if self.debugCurrentPositionCeld[1] == EAST:
            if self.debugCurrentPositionCeld[0].east == WALL:
                print("muro en este")
                return(True)

        if self.debugCurrentPositionCeld[1] == SOUTH:
            if self.debugCurrentPositionCeld[0].south == WALL:
                print("muro en sur")
                return(True)

        if self.debugCurrentPositionCeld[1] == WEST:
            if self.debugCurrentPositionCeld[0].west == WALL:
                print("muro en oeste")
                return(True)

        return(False)

    def _debugTurnRight(self):
        if self.debugCurrentPositionCeld[1] == WEST:
            self.debugCurrentPositionCeld = (self.debugCurrentPositionCeld[0], NORTH)
        else:
            self.debugCurrentPositionCeld = (self.debugCurrentPositionCeld[0], self.debugCurrentPositionCeld[1]+1)
        print("cambiada horientasion a %i " % self.debugCurrentPositionCeld[1])

            
    def _debugTurnLeft(self):
        if self.debugCurrentPositionCeld[1] ==NORTH:
            self.debugCurrentPositionCeld = (self.debugCurrentPositionCeld[0], WEST)

        else:
            self.debugCurrentPositionCeld = (self.debugCurrentPositionCeld[0], self.debugCurrentPositionCeld[1]-1)
        print("cambiada horientasion a %i " % self.debugCurrentPositionCeld[1])

    def _debugAdvanceOneCeld(self):
        print("movilizando al robot debug desde  la celda %s, con direccion %i " % (str(self.debugCurrentPositionCeld[0]), self.debugCurrentPositionCeld[1]))
        if self.debugCurrentPositionCeld[1] == NORTH:
            self.debugCurrentPositionCeld=(self.debugCurrentPositionCeld[0].north, NORTH)
        if self.debugCurrentPositionCeld[1] == EAST:
            self.debugCurrentPositionCeld=(self.debugCurrentPositionCeld[0].east, EAST)
        if self.debugCurrentPositionCeld[1] == SOUTH:
            self.debugCurrentPositionCeld=(self.debugCurrentPositionCeld[0].south, SOUTH)
        if self.debugCurrentPositionCeld[1] == WEST:
            self.debugCurrentPositionCeld=(self.debugCurrentPositionCeld[0].west, WEST)
        print("movilizado el robot debug a la celda %s, con direccion %i " % (str(self.debugCurrentPositionCeld[0]), self.debugCurrentPositionCeld[1]))

    def detectMyCeld(self,robot):
        celdasConcideradas = self.estructura
        movimientosRealizados=[]


        datosConocidos = []
        datosConocidos.append([])
        
        celdasYPosiciones= []
        for x in celdasConcideradas:
            for y in x:


                celdasYPosiciones.append((y,NORTH))
                celdasYPosiciones.append((y,EAST))
                celdasYPosiciones.append((y,SOUTH))
                celdasYPosiciones.append((y,WEST))

        robot.sound.say("starting to find my celda ")
        #self._debugSetStartCeld()
        celda= self._detectMyCeldRecursiveStep(robot, celdasConcideradas, celdasYPosiciones, datosConocidos, movimientosRealizados)
        if celda== None:
            #robot.sound.say("can't enconter my start position. I wana cry ")
            print("no se encontro celda inicial")
        else:
            self.startCelda=celda[0]
            if celda[1] == NORTH:
                self.startDirection='n' 
            elif celda[1] == EAST:
                self.startDirection='e'
            elif celda[1] == SOUTH:
                self.startDirection='s'
            elif celda[1]== WEST:
                self.startDirection='w' 



            robot.sound.say("start celd encontered in position %i, %i, proceed with find my path" % (celda[0].x,celda[0].y))
            print("start celd encontered in position %i, %i, proceed with find my path" % (celda[0].x,celda[0].y))

        
        #regresar al robot a la celda inicial



    def _detectMyCeldRecursiveStep(self,robot,celdasConcideradas, celdasYPosiciones, datosConocidos, movimientosRealizados):
        celda = None
        robot.sound.say("viewing sides")
        print("analizando lados")
        for x in range(0,4):
            if robot.kinect.wallInFront():
            #if self._debugIsWallInFront():
                datosConocidos[-1].append(WALL)
            else:
                datosConocidos[-1].append(UNDEFINEDPATH)
            robot.turnRight()
            #self._debugTurnRight()

        descartables = []
        print("Datos optenidos hasta ahora: " + str(datosConocidos))
        print("hay un total de %i celdas y posisiones con las que comparar " % len(celdasYPosiciones))
        for x in range(0,len(celdasYPosiciones)):
            print(" revisando celda numero %i de la lista " % x)
            dato = celdasYPosiciones[x]
            borrable = self._detectDescartable(dato, datosConocidos, movimientosRealizados)
            if borrable:
                descartables.append(dato)

        for x in descartables:
            celdasYPosiciones.remove(x)
        robot.sound.say("discarded %i celds and positions " % len(descartables))
        print("descatadas %i celdas, quedan %i" % (len(descartables), len(celdasYPosiciones)))
        if len(celdasYPosiciones) == 1:
            celda=   celdasYPosiciones[-1]

        else:
            for x in range(0,len(datosConocidos[-1])):
                
                print("estamos analizando el numero %i en la lista de objetos %s " % (x,str(datosConocidos[-1])))
                

                if datosConocidos[-1][x] == WALL:
                    print("muro detectado, saltamos esta horientacion ")
                    robot.sound.say("wall detected, skyp this position")
                    robot.turnRight()
                    #self._debugTurnRight()
                    continue
                movimientosRealizados.append(x)
                robot.sound.say("go into near celd")
                print("go to near celd ")
                robot.advanceOneCell()
                #self._debugAdvanceOneCeld()
                print("yendo en direccionn %i " % x)
                datosConocidos.append([])
                celda= self._detectMyCeldRecursiveStep(robot, celdasConcideradas, celdasYPosiciones, datosConocidos,movimientosRealizados)
                robot.sound.say("returning to previows celd")
                print("regresando a celda previa")
                robot.turnRight()
                robot.turnRight()
                #self._debugTurnRight()
                #self._debugTurnRight()
                robot.advanceOneCell()
                #self._debugAdvanceOneCeld()
                robot.turnRight()
                robot.turnRight()
                #self._debugTurnRight()
                #self._debugTurnRight()

                
                del movimientosRealizados[-1]
                del datosConocidos[-1]
                if celda != None:
                    robot.sound.say("returning to start position... I am sick.")
                    #print("regresando posicoin inicial")
                    for y in range(0,x+1):
                        robot.turnLeft()
                        #self._debugTurnLeft()
                    break
                else:
                    robot.turnRight()
                    #self._debugTurnRight()

        return(celda)

    def _detectDescartable(self, dato, datosConocidos, movimientos):

        dir= dato[1]
        if len(movimientos) == 0:

            celd = dato[0]
        else:
            print("deteccion con mas movimientos")
            celd = dato[0]

            for x in movimientos:
                direction = (dir+x)%4
                print("buscando datos en cadena, direccion encontrada %i " % direction)
                if direction== NORTH:
                    celd= celd.north
                elif direction == EAST:
                    celd = celd.east
                elif direction == SOUTH:
                    celd = celd.south
                elif direction == WEST:
                    celd = celd.west
                print("celda seleccionada para continuar " + str(celd))
                if celd== WALL or celd==ENDPOINT:
                    return(True)
                else:
                    dir=direction


        if celd.north == WALL:
            northdata = WALL
        else:
            northdata = UNDEFINEDPATH
        if celd.east == WALL:
            eastdata = WALL
        else:
            eastdata = UNDEFINEDPATH
        if celd.south == WALL:
            southdata = WALL
        else:
            southdata = UNDEFINEDPATH
        if celd.west==WALL:
            westdata=WALL
        else:
            westdata= UNDEFINEDPATH

        if dir== NORTH:
            lista= [northdata,eastdata,southdata,westdata]
        elif dir== EAST:
            lista = [eastdata,southdata,westdata,northdata]
        elif dir==SOUTH:
            lista=[southdata,westdata,northdata,eastdata]
        else:
            lista= [westdata,northdata,eastdata,southdata]

        for x in range(0,4):
            print("comparando %i con %i " % (datosConocidos[-1][x], lista[x]))
                    
            if datosConocidos[-1][x] != lista[x]:
                print("descartada celda %s, con direcci�n %i " % (str(celd), dir))
                return(True)
                            

        return(False)


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






