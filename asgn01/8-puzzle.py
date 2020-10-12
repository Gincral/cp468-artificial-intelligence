import numpy as np
import random
import heapq
import sys
import csv
class node:
    def __init__(self, state, action, pathCost, heuristicCost):
        self.state=state            #state/data, position of all tiles
        self.action=action          #action required to get to this state from parent
        self.pathCost=pathCost      #cost from initial state to this node
        self.heuristicCost = heuristicCost #informed heuristic cost

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.state == other.state

class N_Puzzle:
    def __init__(self, goalState, size):
        self.goal=goalState
        self.goalIndex={}
        self.numRows=int(np.sqrt(size))
        for i in range(size):
            self.goalIndex[goalState[i]]=i

        self.size=size #length of array, 3 for 8 puzzle, 4 for 15 puzlle 5 for 24 puzzle

    #What other functions will we need in the N_puzzle Class
    def findTile(self,puzzle,tile):
        for row in range(self.size):
                if puzzle[row]==tile:
                    return row

    def calculateHeuristicCost(self, puzzle):
        if self.heuristic == "h1":
            # Calculation for h1: Number of misplaced tiles
            h1 = 0
            for space in range(self.size):
                    if puzzle[space] != 0 and puzzle[space] != self.goal[space]:
                        h1 += 1
            return h1
        elif self.heuristic == "h2":
            # Calculation for h2: Total Manhattan distance
            h2 = 0
            for row in range(self.size):
                    if puzzle[row] != 0:
                        tile = puzzle[row]
                        goalPos = self.goalIndex[tile]
                        manhattan = abs(row//self.numRows - goalPos//self.numRows) + abs(row%self.numRows - goalPos%self.numRows)
                        h2 += manhattan
            return h2
        elif self.heuristic == "h3":
            # Linear Conflict + Manhattan Distance/Taxicab geometry 
            h3 = 0
            conflictCount = 0
            for row in range(self.size):
                    if puzzle[row] != 0:
                        tile = puzzle[row]
                        goalPos = self.goalIndex[tile]
                        manhattan = abs(row//self.numRows - goalPos//self.numRows) + abs(row%self.numRows - goalPos%self.numRows)
                        h3 += manhattan
                        conflictCount = self.linearConflict(row, tile, puzzle,self.goal)
                        h3 += conflictCount*2
            return h3
    
    def linearConflict(self, tileLocation, tile, puzzle, goal):
        conflictCount = 0
        tileGoal = self.goalIndex[tile]
        if (tileLocation//self.numRows==tileGoal//self.numRows and (tileGoal%self.numRows-tileLocation%self.numRows)>0): #right row
            for i in range((tileLocation%self.numRows)+1, self.numRows):
                target = puzzle[self.numRows*(tileLocation//self.numRows)+i]
                if target!=0:
                    targetGoal = self.goalIndex[target]
                    if (targetGoal//self.numRows==tileGoal//self.numRows and targetGoal%self.numRows<tileGoal%self.numRows): conflictCount+=1
        elif (tileLocation//self.numRows==tileGoal//self.numRows and (tileGoal%self.numRows-tileLocation%self.numRows)>0):
            for i in range(tileLocation//self.numRows+1, self.numRows):
                target = puzzle[i%self.numRows+self.numRows*(tileLocation//self.numRows)]
                if target!=0:
                    targetGoal = self.goalIndex[target]
                    if (targetGoal%self.numRows==tileLocation%self.numRows and targetGoal//self.numRows<tileGoal//self.numRows): conflictCount+=1
        return conflictCount
    
    def calcInversions(self,puzzle):
        size=self.size
        inversions = 0
        for i in range(size):
            for j in range(i+1,size):
                tile1=puzzle[i]
                tile2=puzzle[j]
                #Make sure not to count the empty tile
                if(tile1 != 0 and tile2 != 0 and tile1 > tile2):
                    inversions+=1
        return inversions


    def generateRandomPuzzle(self):
        solvable=False
        values=[0,*range(1,self.size)]

        while (not solvable):
            random.shuffle(values)
            puzzle= values


            solvable=self.checkIfSolvable(puzzle)
        self.data=puzzle

    def checkIfSolvable(self,puzzle):
        size=self.size
        inversions = self.calcInversions(puzzle)  
        if (size%2==1 ):
            return inversions%2 == 0
        else:
            row=self.findTile(puzzle,0)//self.numRows
            if (row%2==1 and inversions%2==1) or (row%2==0 and inversions%2==0):
                return True
            else:
                return False

    def setHeuristic(self, heuristic):
        self.heuristic = heuristic

    def expandNode(self, parentNode):
        #print('expanding node')
        emptyTilePos = self.findTile(parentNode.state,0)
        row = int(emptyTilePos//self.numRows)
        col = int(emptyTilePos%self.numRows)
        children = []
        # Try to create up to 4 new possible states by moving a tile into the empty space
        # Move tile up
        if int(row) > 0 and parentNode.action!="DOWN":
            newState = parentNode.state.copy()
            newState[self.numRows*row+col] = parentNode.state[self.numRows*(row-1)+col]
            newState[self.numRows*(row-1)+col] = 0
            children.append(node( newState, "UP", parentNode.pathCost + 1, self.calculateHeuristicCost(newState)))
        # Move tile down
        if int(row) < self.numRows - 1 and parentNode.action!="UP":  
            newState = parentNode.state.copy()
            newState[self.numRows*row+col] = parentNode.state[self.numRows*(row+1)+col]
            newState[self.numRows*(row+1)+col] = 0
            children.append(node( newState, "DOWN", parentNode.pathCost + 1, self.calculateHeuristicCost(newState)))
        # Move tile right
        if int(col) > 0 and parentNode.action!="RIGHT":
            newState = parentNode.state.copy()
            newState[self.numRows*row+col] = parentNode.state[self.numRows*row+col-1]
            newState[self.numRows*row+col-1] = 0
            children.append(node( newState, "LEFT", parentNode.pathCost + 1, self.calculateHeuristicCost(newState)))
        # Move tile left
        if int(col) < self.numRows - 1 and parentNode.action!="LEFT":
            newState = parentNode.state.copy()
            newState[self.numRows*row+col] = parentNode.state[self.numRows*row+col+1]
            newState[self.numRows*row+col+1] = 0
            children.append(node( newState, "RIGHT", parentNode.pathCost + 1, self.calculateHeuristicCost(newState)))
        return children

    def solve(self):
        root = (self.calculateHeuristicCost(self.data),0,node(self.data, None, 0, self.calculateHeuristicCost(self.data)))
        frontier = []
        heapq.heappush(frontier,root)
        reached = {}
        print('solving...')
        i=0
        # temp variable just so it doesn't infinitely loop
        nodesExpanded = 0
        newNode = None
        while (frontier) and nodesExpanded<15000000:

            newNode = heapq.heappop(frontier)[2] # Retrives first Node in priority Queue
            if nodesExpanded%50000==0:
                #print("\n")
                print(nodesExpanded)

                print(newNode.state)
                print(newNode.heuristicCost)
                print(newNode.pathCost)
 
            childNodes = self.expandNode(newNode)
            nodesExpanded += 1
            for child in childNodes:
                key = str(child.state)
                #print(key)
                if key in reached:
                    reachedCost = reached[key].pathCost + reached[key].heuristicCost
                    #print('Reached state cost: ' + str(reachedCost))
                if key not in reached or reachedCost>child.heuristicCost+child.pathCost:
                    reached[key] = child
                    childTuple=(child.heuristicCost+child.pathCost+child.heuristicCost/100.0,i,child)
                    #print(childTuple)
                    heapq.heappush(frontier,childTuple)
                    i+=1
                if (child.state==self.goal):
                    return nodesExpanded, newNode.pathCost+1
               
        return (nodesExpanded,-1)

def main():
    if len(sys.argv) == 1 or sys.argv[1] == '0':
        print("Please enter a valid puzzle size")
        print("Enter 3, 4, 5 for 8, 15 and 24 puzzle respectively")
        sys.exit()
    size=int(sys.argv[1]) # 3, 4, 5 for 8, 15 and 24 puzzle respectively
    goal = [*range(size*size)]

    myFile = open('8WithHeapRow.csv', 'w')
    writer = csv.writer(myFile)
    
    for i in range(100):
        puzzle = N_Puzzle(goal,size*size)
        puzzle.generateRandomPuzzle()
        print("Puzzle #"+str(i+1))
        print(puzzle.data)
        resulth1=[0,0]
        puzzle.setHeuristic("h1")
        resulth1=puzzle.solve()
        puzzle.setHeuristic("h2")
        resulth2=puzzle.solve()
        puzzle.setHeuristic("h3")
        resulth3=puzzle.solve()
        results=[[resulth1[0],resulth1[1],resulth2[0],resulth2[1],resulth3[0],resulth3[1]]]
    

        writer.writerows(results)
    
if __name__ == "__main__":
    main()