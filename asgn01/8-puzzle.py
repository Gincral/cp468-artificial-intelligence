import numpy as np
import random
import sys
class node:
    def __init__(self, parent, state, action, pathCost):
        self.parent=parent          #parent node
        self.state=state            #state/data, position of all tiles
        self.action=action          #action required to get to this state from parent
        self.pathCost=pathCost      #cost from initial state to this node
        self.children= []           #list of Children

    
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.state == other.state


class N_Puzzle:
    nodesExplored=0 #Do we even need to store this like this?

    def __init__(self, goalState, size):
        self.goal=goalState
        self.size=size #length of rectangle, 3 for 8 puzzle, 4 for 15 puzlle 5 for 24 puzzle

    #What other functions will we need in the N_puzzle Class
    def findTile(self,puzzle,tile):
        for row in range(len(puzzle)):
            for col in range(len(puzzle)):
                if puzzle[row][col]==tile:
                    return row,col

    def generateMoves(self,puzzle): #will check where empty tile is and see which directions the tiles can move from
        moves=[]
        row, col =self.findTile(puzzle,0)
        if (row>0):
            moves.append([row-1,col]) #not first row so row before can move in
        if (row<self.size-1):
            moves.append([rows+1,col])#not last row so row after can move in
        if (col>0):
            moves.append([row,col-1])#not first column so column before can move in
        if (col<self.size-1):
            moves.append([row,col+1])#not last column so column before can move in
        return moves

    def slide(self, puzzle, move)
        row,col=self.findTile(puzzle,0)
        puzzle[row][col]=puzzle[move[0]][move[1]]
        puzzle[move[0]][move[1]]=0
        return puzzle

    def calculateHeuristicCost(self, heuristic):
        if heuristic == "h1":
            # Calculation for h1: number of misplaced tiles
            h1 = 0
            for i in range(self.data.shape[0]):
                for j in range(self.data.shape[1]):
                    if self.data[i][j] != 0 and self.data[i][j] != self.goal[i][j]:
                        h1 += 1
            self.h1 = h1
        elif heuristic == "h2":
            # Calculation for h2: Total Manhattan distance
            h2 = 0
            for i in range(self.data.shape[0]):
                for j in range(self.data.shape[1]):
                    if self.data[i][j] != 0:
                        tile = self.data[i][j]
                        goalPos = self.findTile(self.goal, tile)
                        manhattan = abs(i - goalPos[0]) + abs(j - goalPos[1])
                        h2 += manhattan
            self.h2 = h2

    def generateRandomPuzzle(self):
        solvable=False
        values=[0,*range(1,self.size*self.size)]

        while (not solvable):
            random.shuffle(values)
            puzzle= np.reshape(values,(self.size,self.size))
            solvable=self.checkIfSolvable(puzzle)
        self.data=puzzle

    def checkIfSolvable(self,puzzle):
        size=len(puzzle)
        inversions = 0
        for i in range(size*size-1):
            for j in range(i+1,size*size):
                tile1=puzzle[i//size][i%size]
                tile2=puzzle[j//size][j%size]
                #Make sure not to count the empty tile
                if(tile1 != 0 and tile2 != 0 and tile1 > tile2):
                    inversions+=1
            
        
        if (size%2==1 ):
            return inversions%2 == 0
        else:
            row,col=self.findTile(puzzle,0)
            if (row%2==1 and inversions%2==1) or (row%2==0 and inversions%2==0):
                return True
            else:
                return False
        

    def solve(self):
        print("Do Stuff")

def main():
    size=int(sys.argv[1]) # 3, 4, 5 for 8, 15 and 24 puzzle respectively
    goal = np.reshape([*range(size*size)],(size,size))

    puzzle = N_Puzzle(goal,size)

    for i in range(10):
        puzzle.generateRandomPuzzle()
        puzzle.calculateHeuristicCost("h1")
        puzzle.calculateHeuristicCost("h2")
        print("Puzzle #"+str(i+1))
        print(puzzle.data)
        print("h1(S) = " + str(puzzle.h1))
        print("h2(S) = " + str(puzzle.h2))
        puzzle.solve()
        print("\n")
        
    print("The goal state is:")
    print(goal)

    print('heuristic test (from lecture notes):')
    testGoal = np.reshape([*range(3*3)],(3,3))
    testPuzzle = N_Puzzle(testGoal, 3)
    values = [7, 2, 4, 5, 0, 6, 8, 3, 1]
    testPuzzle.data = np.reshape(values, (3, 3))
    print(testPuzzle.data)
    testPuzzle.calculateHeuristicCost("h1")
    testPuzzle.calculateHeuristicCost("h2")
    print("h1(S) = " + str(testPuzzle.h1))
    print("h2(S) = " + str(testPuzzle.h2))


if __name__ == "__main__":
    main()