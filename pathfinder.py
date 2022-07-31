from array import *

import sys
import os
import copy
import heapq
from collections import deque
from queue import PriorityQueue
from math import sqrt


map_input = sys.argv[1]
algorithm = sys.argv[2]

if len(sys.argv) > 3:
    heuristic = sys.argv[3]

map = []

xlen = 0
ylen = 0

class node:
    def __init__(self, parent, pos, cost):
        self.parent = parent
        self.pos = pos
        self.cost = cost


# Reads the input file and creates a map
def read_goal():
    global start
    global end

    file = open(map_input,'r')
    list = file.read().splitlines()
    startList = list[1].split(' ')
    start = (int(startList[0]) - 1,int(startList[1]) - 1)
    endList = list[2].split(' ')
    end = (int(endList[0]) - 1,int(endList[1]) - 1)

def read_file():
    global xlen
    global ylen
    global start
    global end


    file = open(map_input,'r')
    list = file.read().splitlines()
    lengthList = list[0].split(' ')
    xlen = int(lengthList[0])
    ylen = int(lengthList[1])
    del list[0],list[0],list[0]

    for i in range(len(list)):
        templist = list[i].split(' ')
        for j in range(0, len(templist)):
            if(templist[i] != 'X'):
                templist[i] = int(templist[i])
        map.append(templist)

    return map

# Utility function to print the map
def print_array(array):
    for i in range(0, len(array)):
        for j in range(0, len(array)):
            if (j < len(array) - 1):
                print(array[i][j], end = " ")
            else:
                print(array[i][j], end = '')
        print()

def sortkey(node):
    return node.cost

#Given a node, get its valid children and their cumilitve cost
def getChildren(parent, tracker):
    new_children = []
    #Defines the range of movement
    move = [[-1,0], # up
            [1,0], # down
            [0,-1], # left
            [0,1]] # right


    for i in range(0, len(move)):
        new_pos = move[i]

        #Move to next position
        next_pos = (parent.pos[0] + new_pos[0], parent.pos[1] + new_pos[1])

        # Check for valid position
        if(next_pos[0] == -1 or next_pos[1] == -1 or next_pos[0] >= xlen or next_pos[1] >= ylen):
            continue
        elif(map[next_pos[0]][next_pos[1]] == 'X'):
            continue
        elif(tracker[next_pos[0]][next_pos[1]] == True):
            continue
        else:
            new_cost = int(map[next_pos[0]][next_pos[1]]) + parent.cost

            new_node = node(parent, next_pos, new_cost)
            new_children.append(new_node)


    return new_children

#Given a node, get its valid children and their cost including heuristic
def getChildrenAstar(parent, tracker, goal):
    new_children = []
    #Defines the range of movement
    move = [[-1,0], # up
            [1,0], # down
            [0,-1], # left
            [0,1]] # right


    for i in range(0, len(move)):
        new_pos = move[i]

        #Move to next position
        next_pos = (parent.pos[0] + new_pos[0], parent.pos[1] + new_pos[1])

        # Check for valid position
        if(next_pos[0] == -1 or next_pos[1] == -1 or next_pos[0] >= xlen or next_pos[1] >= ylen):
            continue
        elif(map[next_pos[0]][next_pos[1]] == 'X'):
            continue
        elif(tracker[next_pos[0]][next_pos[1]] == True):
            continue
        else:

            g =  int(map[next_pos[0]][next_pos[1]]) + parent.cost

            #Manhattan Heuristic Calculation -> h = |xstart - xdestination| + |ystart - ydestination|
            if (heuristic == "manhattan"):
                h = abs((next_pos[0] - goal[0])) + abs((next_pos[1] - goal[1]))

            #Euclidean Heuristic Calculation -> h = sqrt((xstart - xdestination)^2 + (ystart - ydestination)^2)
            if (heuristic == "euclidean"):
                h = sqrt(((next_pos[0] - goal[0]) ** 2) + ((next_pos[1] - goal[1]) ** 2))

            f = g + h
            new_cost = f
            new_node = node(parent, next_pos, new_cost)
            new_children.append(new_node)


    return new_children

def bfs(start_c, end_c):
    map = read_file()

    #Initialize the visited array
    visited = []
    for i in range (0, xlen):
        templist = []
        for j in range (0, ylen):
            templist.append(False)
        visited.append(templist)

    start = node("None", start_c, 0)
    current = start
    queue = deque([])
    visited[start.pos[0]][start.pos[1]] = True
    queue.append(start)


    while queue:
        #Pop the current node
        current = queue.popleft()

        #Check is current is end
        if(current.pos == end_c):
            break

        #Get the children of current
        children = getChildren(current, visited)

        #Mark as visited and add to queue
        for i in range(0, len(children)):
            visited[children[i].pos[0]][children[i].pos[1]] = True
            queue.append(children[i])


    # Step back through the map to update the shortest path
    while current.parent != "None":
        map[current.pos[0]][current.pos[1]] = '*'
        current = current.parent
    map[current.pos[0]][current.pos[1]] = '*'

    print_array(map)

def ucs(start_c, end_c):
    map = read_file()

    #Initialize the visited array
    visited = []
    for i in range (0, xlen):
        templist = []
        for j in range (0, ylen):
            templist.append(False)
        visited.append(templist)

    start = node("None", start_c, 0)
    current = start
    queue = deque([])
    visited[start.pos[0]][start.pos[1]] = True
    queue.append(start)

    found = False

    while queue:
        #Pop the current node
        current = queue.popleft()

        #Check is current is end
        if(current.pos == end_c):
            found = True
            break

        #Get the children of current
        children = getChildren(current, visited)

        #Sort children by cost
        children.sort(key=sortkey)

        #Mark as visited and add to queue
        for i in range(0, len(children)):
            visited[children[i].pos[0]][children[i].pos[1]] = True
            queue.append(children[i])


    # Step back through the map to update the shortest path
    if(found == True):
        while current.parent != "None":
            map[current.pos[0]][current.pos[1]] = '*'
            current = current.parent
        map[current.pos[0]][current.pos[1]] = '*'

        print_array(map)

    else:
        print("null")

def astar(start_c, end_c):
    map = read_file()

    #Initialize the visited array
    visited = []
    for i in range (0, xlen):
        templist = []
        for j in range (0, ylen):
            templist.append(False)
        visited.append(templist)

    start = node("None", start_c, 0)
    current = start
    queue = deque([])
    visited[start.pos[0]][start.pos[1]] = True
    queue.append(start)

    found = False

    while queue:
        #Pop the current node
        current = queue.popleft()

        #Check is current is end
        if(current.pos == end_c):
            found = True
            break

        #Get the children of current
        children = getChildrenAstar(current, visited, end_c)

        #Sort children by cost
        children.sort(key=sortkey)

        #Mark as visited and add to queue
        for i in range(0, len(children)):
            visited[children[i].pos[0]][children[i].pos[1]] = True
            queue.append(children[i])


    # Step back through the map to update the shortest path
    if(found == True):
        while current.parent != "None":
            map[current.pos[0]][current.pos[1]] = '*'
            current = current.parent
        map[current.pos[0]][current.pos[1]] = '*'

        print_array(map)

    else:
        print("null")

read_goal()

if(algorithm == "bfs"):
    bfs((0,0),(9,9))
elif(algorithm == "ucs"):
    ucs((0,0),(9,9))
elif(algorithm == "astar"):
    astar((start),(end))
else:
    print("this is for other command line arguments")
