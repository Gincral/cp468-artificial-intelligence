import numpy as np
import random
import sys
class node:
    # TODO: Are we allowed to store the heuristic cost on the node?
    def __init__(self, parent, state, action, pathCost, heuristicCost):
        self.parent=parent          #parent node
        self.state=state            #state/data, position of all tiles
        self.action=action          #action required to get to this state from parent
        self.pathCost=pathCost      #cost from initial state to this node
        self.heuristicCost = heuristicCost #informed heuristic cost
        self.children= []           #list of Children

    
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.state == other.state

class FrontierPriorityQueue:
    def __init__(self):
        self.queue = []
        
    def isEmpty(self):
        return len(self.queue) == 0

    def add(self, node):
        if (len(self.queue) == 0):
            self.queue.append(node)
        else:
            i = 0
            while i < len(self.queue) and (node.pathCost + node.heuristicCost) > (self.queue[i].pathCost + self.queue[i].heuristicCost):
                i += 1
            self.queue.insert(i, node)     

    # Removes the node from the top and expands children nodes to add to the queue
    def pop(self):
        topNode = None
        nodesExpanded = 0
        if len(self.queue) > 0:
            topNode = self.queue.pop(0)
        return topNode


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

    def calculateHeuristicCost(self, puzzle):
        if self.heuristic == "h1":
            # Calculation for h1: Number of misplaced tiles
            h1 = 0
            for row in range(len(puzzle)):
                for col in range(len(puzzle)):
                    if puzzle[row][col] != 0 and puzzle[row][col] != self.goal[row][col]:
                        h1 += 1
            return h1
        elif self.heuristic == "h2":
            # Calculation for h2: Total Manhattan distance
            h2 = 0
            for row in range(len(puzzle)):
                for col in range(len(puzzle)):
                    if puzzle[row][col] != 0:
                        tile = puzzle[row][col]
                        goalPos = self.findTile(self.goal, tile)
                        manhattan = abs(row - goalPos[0]) + abs(col - goalPos[1])
                        h2 += manhattan
            return h2
        elif self.heuristic == "h3":
            # Calculation for h3: Nilsson's Sequence Score: h(n) = P(n) + 3 S(n)
            h3 = 0
            for row in range(len(puzzle)):
                for col in range(len(puzzle)):
                    if puzzle[row][col] != 0:
                        tile = puzzle[row][col]
                        goalPos = self.findTile(self.goal, tile)
                        manhattan = abs(row - goalPos[0]) + abs(col - goalPos[1])
                        h3 += manhattan
                        if(manhattan != 0):
                            if (len(puzzle)==3):
                                if(row ==1 and col ==1): h3 += 3
                                else: h3 += 6
                            elif (len(puzzle)==4):
                                if((row ==2 and col ==2) or (row ==1 and col ==1)): h3 += 3
                                else: h3 += 6
                            elif (len(puzzle)==5):
                                if(row ==2 and col ==2): h3 += 3
                                else: h3 += 6
                        
            return h3
        

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

    def expandNode(self, parentNode):
        print('expanding node')
        emptyTilePos = np.where(parentNode.state == 0)
        row = int(emptyTilePos[0])
        col = int(emptyTilePos[1])
        children = []
        # Try to create up to 4 new possible states by moving a tile into the empty space
        # Move tile up
        print('parent state:')
        print(parentNode.state)
        if int(row) > 0:
            newState = np.reshape(parentNode.state.copy(), (self.size,self.size))
            newState[row][col] = parentNode.state[row-1][col]
            newState[row-1][col] = 0
            print('move tile up')
            print(newState)
            children.append(node(parentNode, newState, None, parentNode.pathCost + 1, self.calculateHeuristicCost(newState)))
        # Move tile down
        if int(row) < self.size - 1:  
            newState = np.reshape(parentNode.state.copy(), (self.size,self.size))
            newState[row][col] = parentNode.state[row+1][col]
            newState[row+1][col] = 0
            print('move tile down')
            print(newState)
            children.append(node(parentNode, newState, None, parentNode.pathCost + 1, self.calculateHeuristicCost(newState)))
        # Move tile right
        if int(col) > 0:
            newState = np.reshape(parentNode.state.copy(), (self.size,self.size))  
            newState[row][col] = parentNode.state[row][col-1]
            newState[row][col-1] = 0
            print('move tile left')
            print(newState)
            children.append(node(parentNode, newState, None, parentNode.pathCost + 1, self.calculateHeuristicCost(newState)))
        # Move tile left
        if int(col) < self.size - 1:
            newState = np.reshape(parentNode.state.copy(), (self.size,self.size))  
            newState[row][col] = parentNode.state[row][col+1]
            newState[row][col+1] = 0
            print('move tile right')
            print(newState)
            children.append(node(parentNode, newState, None, parentNode.pathCost + 1, self.calculateHeuristicCost(newState)))
        return children

    def setHeuristic(self, heuristic):
        self.heuristic = heuristic

    def solve(self):
        root = node(None, self.data, None, 0, self.calculateHeuristicCost(self.data))
        frontier = FrontierPriorityQueue()
        frontier.add(root)
        steps = 0
        nodesExpanded = 0
        reached = {}
        reached[str(root.state)] = root
        print('solving...')
        # temp variable just so it doesn't infinitely loop
        i = 0
        newNode = None
        while not (frontier.isEmpty()):
            newNode = frontier.pop()
            print('popped node:')
            print(newNode.state)
            if (np.array_equal(newNode.state, self.goal)):
                print('goal reached!')
                print('result:')
                print(newNode.state)
                return nodesExpanded, steps
            else:
                childNodes = self.expandNode(newNode)
                nodesExpanded += len(childNodes)
                # TODO: check if state has been seen and check cost before adding to frontier
                for child in childNodes:
                    key = str(child.state)
                    print(key not in reached)
                    print('Child cost: ' + str(child.pathCost + child.heuristicCost))
                    if key in reached:
                        reachedCost = reached[key].pathCost + reached[key].heuristicCost
                        print('Reached state cost: ' + str(reachedCost))
                    if key not in reached or (child.pathCost + child.heuristicCost) < (reached[key].pathCost + reached[key].heuristicCost):
                        print('adding child:')
                        print(child.state)
                        reached[key] = child
                        frontier.add(child)
                steps += 1
        raise Exception("Failed to solve puzzle with start state:" + self.data)

def main():
    if len(sys.argv) == 1 or sys.argv[1] == '0':
        print("Please enter a valid puzzle size")
        print("Enter 3, 4, 5 for 8, 15 and 24 puzzle respectively")
        sys.exit()
    size=int(sys.argv[1]) # 3, 4, 5 for 8, 15 and 24 puzzle respectively
    goal = np.reshape([*range(size*size)],(size,size))

    puzzle = N_Puzzle(goal,size)

    for i in range(1):
        puzzle.generateRandomPuzzle()
        print("Puzzle #"+str(i+1))
        print(puzzle.data)
        puzzle.setHeuristic("h2")
        puzzle.solve()
        print("\n")
        
    print("The goal state is:")
    print(goal)


if __name__ == "__main__":
    main()