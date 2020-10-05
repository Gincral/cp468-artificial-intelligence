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

    def calculateHeuristicCost(self):
        print("Calculate Stuff")

    def generateRandomPuzzle(self):
        print("Shake things up here")

    def solve(self):
        print("Do Stuff")


def main():
    goal8=[[0,1,2],
          [3,4,5],
          [6,7,8]]
    goal15=[    [0 ,1 ,2,  3],
                [4 ,5 ,6,  7],
                [8 ,9 ,10,11],
                [12,13,14,15]]
    goals24=[[0 ,1 ,2, 3, 4],
             [5, 6, 7, 8, 9 ],
             [10,11,12,13,14],
             [15,16,17,18,19],
             [20,21,22,23,24]]


    puzzle = N_Puzzle(goal8,8)
    puzzle.generateRandomPuzzle()

    puzzle.solve()


if __name__ == "__main__":
    main()