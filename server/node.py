import numpy as np

class Area:
    def __init__(self, area):
        self.area = np.zeros((area, area)) #Needs the second set of parenthesis for some reason
    
    def place(self, xPos, yPos, pillarOBJ):
        for y in range(pillarOBJ.width):
            if (y + yPos < len(self.area)):
               for x in range(pillarOBJ.length):
                   if (x + xPos < len(self.area[y])):
                       self.area[y + yPos][x + xPos] = pillarOBJ.repNum
    
    def instructGen(self):
        start = False
        instruction = []

        for row in range(len(self.area)):
            for col in range(len(self.area[row])):
                if ((self.area[row][col] != 0) and (start == False)):
                    instruction.append([col, row])
                    start = True

                if ((self.area[row][col] == 0) and (start == True)):
                    instruction.append([col, row])
                    start = False
                    
            if (start == True):
                instruction.append([len(self.area), row])
                start = False
        
        return instruction

class Pillar:
    def __init__(self, repNum, length, width):
        self.repNum = repNum
        self.length = length
        self.width = width


class Node:
    def __init__(self, posX, posY, origin, orientation, endNode):
        #Set origin/endnode to None if the node is the start node or the end node
        self.posX = posX
        self.posY = posY
        self.origin = origin #origin is the node object right before itself.
        
        if self.origin == None: #None is like null in java, set origin to None if the node itself is the origin
            self.gCost = 0
        else: 
            self.gCost = self.origin.gCost + (10 + (4 * orientation)) #1 for a diagonal, 0 for a straight
        
        if endNode == None:
            self.hCost = 0
        else:
            self.hCost = self.calcHcost(endNode) #end node is the goal
        
        self.visited = False
    
    def __eq__(self, value):
        if(not isinstance(value, Node)):
            return False
        
        if ((self.posX == value.posX) and (self.posY == value.posY)):
            return True
        else:
            return False
             
    
    def calcHcost(self, endNode):
        #h = min(dx, dy) * 14 + abs(dx - dy) * 10
        dx = abs(endNode.posX - self.posX)
        dy = abs(endNode.posY - self.posY)

        hCost = (min(dx, dy) * 14) + (abs(dx - dy) * 10)
        return hCost
    
    def visit(self, pathMap):
        self.visited = True
        trueNode = pathMap.map[self.posY][self.posX]
        nodeList = []
        node1 = Node(self.posX, (self.posY + 1), trueNode, 0, pathMap.end)
        node2 = Node(self.posX, (self.posY - 1), trueNode, 0, pathMap.end)
        node3 = Node((self.posX + 1), self.posY, trueNode, 0, pathMap.end)
        node4 = Node((self.posX - 1), self.posY, trueNode, 0, pathMap.end)
        node5 = Node((self.posX + 1), (self.posY + 1), trueNode, 1, pathMap.end)
        node6 = Node((self.posX - 1), (self.posY + 1), trueNode, 1, pathMap.end)
        node7 = Node((self.posX + 1), (self.posY - 1), trueNode, 1, pathMap.end)
        node8 = Node((self.posX - 1), (self.posY - 1), trueNode, 1, pathMap.end)

        nodeList.append(node1)
        nodeList.append(node2)
        nodeList.append(node3)
        nodeList.append(node4)
        nodeList.append(node5)
        nodeList.append(node6)
        nodeList.append(node7)
        nodeList.append(node8)

        return nodeList
    
    def toString(self):
        return -1

class BlockNode:
    def __init__(self):
        pass

    def toString(self):
        return 1

class PathMap:
    def __init__(self, map, startNode, endNode):
        self.map = self.generateMap(map, startNode, endNode)
        self.start = startNode
        self.end = endNode
        #area is an Area, startNode and endNode are both nodes
        
    def generateMap(self, map, startNode, endNode):
        mapCopy = map.area.copy().tolist()

        for y in range(len(mapCopy)):
            for x in range(len(mapCopy[y])):
                if(mapCopy[y][x] > 0):
                    mapCopy[y][x] = BlockNode()
        
        startX = startNode.posX
        startY = startNode.posY
        endX = endNode.posX
        endY = endNode.posY

        if(not(isinstance(mapCopy[startY][startX], BlockNode) or isinstance(mapCopy[endY][endX], BlockNode))):
            mapCopy[startY][startX] = startNode
            mapCopy[endY][endX] = endNode

        return mapCopy
    
    
    
    def put(self, node):
        posX = node.posX
        posY = node.posY

        if (posY < 0 or posY >= len(self.map)):
            return False
        
        if (posX < 0 or posX >= len(self.map[0])):
            return False
        
        item = self.map[posY][posX]

        if (isinstance(item, BlockNode)):
            return False
        
        if (item == 0):
            self.map[posY][posX] = node
            return True

        if (isinstance(item, Node)):
            if(((node.gCost) < (item.gCost)) and (not item.visited)):
                self.map[posY][posX].origin = node.origin
                self.map[posY][posX].gCost = node.gCost

        if ((item.posX == self.end.posX) and (item.posY == self.end.posY)):
            self.end.visited = True
            self.end.origin = node.origin

        return False
    
    def findMin(self, array):
        minNode = array[0]

        for node in array:
            if ((node.gCost + node.hCost) < (minNode.gCost + minNode.hCost)):
                minNode = node
        
        return minNode #returns position

    def startPath(self):
        nonVisitedArray = [self.start]
        start = self.start
        end = self.end

        if((isinstance(self.map[start.posY][start.posX], BlockNode) or isinstance(self.map[end.posY][end.posX], BlockNode))):
            return

        while (self.end.visited == False and (len(nonVisitedArray) > 0)):
            node = self.findMin(nonVisitedArray) #returns [posX, posY]
            putNodes = node.visit(self)
            nonVisitedArray.remove(node)
            for item in putNodes:
                check = self.put(item)
                if(check):
                    nonVisitedArray.append(item)

    def returnPath(self): #ONLY call this after doing a startPath

        if(not self.end.visited):
            return []
        
        node = self.end
        path = [self.end]
        while(not (node.__eq__(self.start))):
            path.append(node.origin)
            node = node.origin

        return path




    def toString(self):
        exList = np.zeros((len(self.map), len(self.map)))
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if isinstance(self.map[y][x], BlockNode):
                    exList[y][x] = 1
                elif isinstance(self.map[y][x], Node):
                    exList[y][x] = -1
        
        return exList
    










