"""
CSCI-630: Lab 1
Author: Shivam Mahajan

An implementation to generating optimal paths
for orienteering during different seasons
"""


import sys

from PIL import Image
from queue import PriorityQueue
import math

weights = {(248, 148, 18, 255): ['Open land', 20], (255, 192, 0, 255): ['Rough meadow', 30],
     (255, 255, 255, 255): ['Easy movement forest', 40]
    , (2, 208, 60, 255): ['Slow run forest', 50], (2, 136, 40, 255): ['Walk forest', 60],
     (5, 73, 24, 255): ['Impassible vegetation', float('inf')], (0, 0, 255, 255): ['Lake/Swamp/Marsh', float('inf')],
     (71, 51, 3, 255): ['Paved road', 1], (0, 0, 0, 255): ['Footpath', 10],
     (205, 0, 101, 255): ['Out of bounds', float('inf')]}

X = 10.29
Y = 7.55

im = Image.open(sys.argv[1])
imLoad = im.load()
col, row = im.size


def elevationData():
    elevationList2D = []
    with open(sys.argv[2]) as mpp:
        for line in mpp.readlines():
            line = line.split()
            elevationList2D.append(line[:col])

    return elevationList2D


def readPath():
    pathList = []
    with open(sys.argv[3]) as t:
        for line in t.readlines():
            line = line.split()
            pathList.append(line)

    return pathList


class Nodes:
    __slots__ = "x", "y", "z", "weight", "gn", "fn", "prev"

    def __init__(self, x, y, z, weight):
        self.x = x
        self.y = y
        self.z = z
        self.weight = weight
        self.gn = 0
        self.fn = 0
        self.prev = None


    def __lt__(self, other):
        return self.fn < other.fn


def getNeighbours(graph,x,y):
    neighbours = []

    if x == 0:
        if y == 0:
            neighbours.append(graph[x+1][y])

            neighbours.append(graph[x][y+1])

        elif y == col - 1:

            neighbours.append(graph[x+1][y])
            neighbours.append(graph[x][y - 1])

        elif y > 0 and y < col - 1:

            neighbours.append(graph[x][y - 1])

            neighbours.append(graph[x+1][y])

            neighbours.append(graph[x][y + 1])

    elif y == 0:

        if x == row - 1:

            neighbours.append(graph[x-1][y])

            neighbours.append(graph[x][y + 1])

        elif x > 0 and x < row - 1:

            neighbours.append(graph[x-1][y])

            neighbours.append(graph[x][y + 1])

            neighbours.append(graph[x+1][y])


    elif x == row - 1:
        if y > 0 and y < col - 1:

            neighbours.append(graph[x][y - 1])

            neighbours.append(graph[x-1][y])

            neighbours.append(graph[x][y + 1])

        elif y == col - 1:
            neighbours.append(graph[x][y-1])
            neighbours.append(graph[x-1][y])

    elif y == col - 1:
        if x > 0 and x < row - 1:

            neighbours.append(graph[x+1][y])

            neighbours.append(graph[x][y - 1])

            neighbours.append(graph[x-1][y])

    else:

        neighbours.append(graph[x-1][y])

        neighbours.append(graph[x+1][y])

        neighbours.append(graph[x][y - 1])

        neighbours.append(graph[x][y+1])
    return neighbours

def makeGraph():

    elevationList = elevationData()
    node = []
    for i in range(row):
        lst = []
        for j in range(col):

            lst.append(Nodes(i, j, elevationList[i][j], weights[imLoad[j,i]]))
        node.append(lst)

    return node


def hn(node1, node2):
    value1 = (((node1.x - node2.x)*X) ** 2) + (((node1.y - node2.y)*Y) ** 2) + ((float(node1.z) - float(node2.z)) ** 2)

    value2 = math.sqrt(value1)
    return value2

def distance2D(node1, node2):
    value1 = (((node1.x - node2.x)) ** 2) + (((node1.y - node2.y)) ** 2)

    value2 = math.sqrt(value1)
    return value2

def gn(node1, node2):

    value = hn(node1, node2)
    value = (value / 2) * (node1.weight[1]) + (value / 2) * (node2.weight[1])

    return value


def AstarSearch(graph,pathList):

    openQueue = PriorityQueue()
    closedSet = set()
    path = []
    endPath = []
    start = pathList[0]
    current = graph[int(start[1])][int(start[0])]

    for i in range(1,len(pathList)):

        target = pathList[i]

        dest = graph[int(target[1])][int(target[0])]

        current.gn = 0
        current.fn = current.gn + hn(current, dest)

        while(current is not dest):

            neighbours = getNeighbours(graph,current.x,current.y)

            for n in neighbours:
                if n not in closedSet:
                    gn1 = current.gn + gn(current, n)
                    fnCostNode = gn1 + hn(n, dest)

                    if fnCostNode < n.fn or n.fn == 0:

                        n.fn = fnCostNode
                        n.gn = gn1

                        n.prev = current

                        openQueue.put(n)

            closedSet.add(current)
            current = openQueue.get()

        while(current.prev is not None):
            path.append(current)

            current = current.prev

        path.append(current)
        path.reverse()

        for p in range(row):
            for q in range(col):
                graph[p][q].fn = 0
                graph[p][q].gn = 0
                graph[p][q].prev = None

        current = dest
        openQueue = PriorityQueue()
        closedSet = set()

    sum=0

    for k in path:
        if k not in endPath:
            endPath.append(k)

    for index in range(0,len(endPath)-1):
        sum += hn(endPath[index],endPath[index+1])
    print("Path Length: ",sum)

    for i in endPath:
        im.putpixel((i.y,i.x),(255,0,0))
    im.show()
    im.save(sys.argv[5])


def fallChange(graph):

    for i in range(row):
        for j in range(col):
            current = graph[i][j]
            if current.weight[0] == 'Easy movement forest':

                neighbours = getNeighbours(graph,current.x,current.y)
                for n in neighbours:
                    if n.weight[0] == 'Paved road':
                        im.putpixel((n.y,n.x),(204,204,0))
                        n.weight[1] = 5
                    elif n.weight[0] == 'Footpath':
                        im.putpixel((n.y, n.x), (204, 204, 0))
                        n.weight[1] = 15
    return graph

def winterChange(graph):
    lst = []
    waterList = []
    for i in range(row):
        for j in range(col):
            current = graph[i][j]
            if current.weight[0] == 'Lake/Swamp/Marsh':
                waterList.append(current)
                neighbours = getNeighbours(graph, current.x, current.y)
                for n in neighbours:
                    if n.weight[0] != 'Lake/Swamp/Marsh':
                        lst.append(current)
                        break


    return lst

def winterBFS(graph, start):
    winterQueue = []

    winterSet = set()
    winterQueue.append(start)
    winterSet.add(start)
    winterList = []

    while len(winterQueue) > 0:
        current = winterQueue.pop(0)
        distance = distance2D(start, current)

        if distance > 7:
            break
        neighbours = getNeighbours(graph,current.x,current.y)
        for n in neighbours:
            if n.weight[0] != 'Lake/Swamp/Marsh':
                continue
            if n not in winterSet:
                winterList.append(n)
                winterSet.add(n)
                winterQueue.append(n)


    return winterList

def springChange(graph):
    lst = []

    for i in range(row):
        for j in range(col):
            current = graph[i][j]
            if current.weight[0] != 'Lake/Swamp/Marsh' and current.weight[0] != 'Out of bounds':

                neighbours = getNeighbours(graph, current.x, current.y)
                for n in neighbours:
                    if (abs(float(n.z) - float(current.z))) <= 1:
                        lst.append(current)
                        break


    return lst

def springBFS(graph, start):
    springQueue = []

    springSet = set()
    springQueue.append(start)
    springSet.add(start)
    springList = []

    while len(springQueue) > 0:
        current = springQueue.pop(0)
        distance = distance2D(start, current)

        if distance > 15:
            break
        neighbours = getNeighbours(graph,current.x,current.y)
        for n in neighbours:
            if n.weight[0] == 'Lake/Swamp/Marsh':
                continue
            if n not in springSet:
                springList.append(n)
                springSet.add(n)
                springQueue.append(n)



    return springList

def main():
    pathList = readPath()
    graph = makeGraph()
    if(len(sys.argv)==6):

        if sys.argv[4] == 'summer':

            AstarSearch(graph,pathList)

        elif sys.argv[4] == 'winter':
            lst = winterChange(graph)
            w=[]
            for l in lst:
                w += winterBFS(graph,l)
            for node in w:
                node.weight[1] = 15
                im.putpixel((node.y, node.x), (128, 234, 255))
            AstarSearch(graph, pathList)


        elif sys.argv[4] == 'fall':

            fallGraph = fallChange(graph)
            AstarSearch(fallGraph,pathList)

        elif sys.argv[4] == 'spring':
            lst = springChange(graph)
            w = []
            for l in lst:
                w += springBFS(graph, l)
            for node in w:
                node.weight[1] = 100000
                im.putpixel((node.y, node.x), (128,85,0))
            AstarSearch(graph, pathList)

        else:
            print("Incorrect season name")

    else:
        print("Incorrect inputs")

if __name__ == '__main__':
    main()
