from copy import deepcopy
from sys import argv

rows =['A','B','C','D','E','F','G','H','I']
class AC3:

    def __init__(self, data,constraints):
        self.binConstraints=constraints
        self.values={}
        cols= [x for x in range(1,10)]
        self.variables = [row+str(col) for row in rows for col in cols]
        i = 0
        if isinstance(data, str):
            for var in self.variables:
                if data[i] == '0':
                    self.values[var]=[1,2,3,4,5,6,7,8,9]
                else:
                    self.values[var]=[int(data[i])]
                i += 1
        else:
            self.values = data
        self.generate_related_cells()

    def generate_related_cells(self):
        related_cells = {}

        #for each one of the 81 cells
        for cell in self.variables:

            related_cells[cell] = []

            # related cells are the ones that current cell has constraints with
            for constraint in self.binConstraints:
                if cell == constraint[0] and constraint[1] not in related_cells[cell]:
                    related_cells[cell].append(constraint[1])

        self.related_cells=related_cells

    def ac3(self):
        while len(self.binConstraints) > 0:
            arc = self.binConstraints.pop(0)
            x = arc[0]
            y = arc[1]
            if self.revise(x, y):
                if len(self.values[x]) == 0:
                    return False
                for cell in self.related_cells[x]:
                    if [cell, x] not in self.binConstraints:
                        self.binConstraints.append([cell,x])
        return True

    def revise(self, x, y):
        if len(self.values[y]) == 1:
            yvalue = self.values[y]
            try:
                index = self.values[x].index(yvalue[0])
                self.values[x].pop(index)
                return True
            except:
                return False
        return False

    def printInFormat(self):
        for row in rows:
            print(self.values[row+'1'],self.values[row+'2'],self.values[row+'3'],self.values[row+'4'],self.values[row+'5'],self.values[row+'6'],self.values[row+'7'],self.values[row+'8'],self.values[row+'9'],'\n')

    def find_unsolved_square(self):
        for item in self.values.items():
            if len(item[1]) > 1:
                return item[0]
        return None        

def CreateConstraints():

    constraintPairs=[]

    for row in rows:
        rowVariables=[row+str(x) for x in range(1,10)]
        
        for var1 in rowVariables:
            for var2 in rowVariables:
                if var1!=var2:
                    constraintPairs.append([var1,var2])
    for col in range(1,10):
        colVariables=[alpha+str(col) for alpha in rows]
        for var1 in colVariables:
            for var2 in colVariables:
                if var1!=var2 and [var1,var2] not in constraintPairs:
                    constraintPairs.append([var1,var2])
    for i in range(3):
        for j in range(3):
            squareVariables=[]
            for k in range(1,4):
                squareVariables.append(rows[3*i]+str(3*j+k))
                squareVariables.append(rows[3*i+1]+str(3*j+k))
                squareVariables.append(rows[3*i+2]+str(3*j+k))
            # print(squareVariables)
            for var1 in squareVariables:
                for var2 in squareVariables:
                    if var1!=var2 and [var1,var2] not in constraintPairs:
                        constraintPairs.append([var1,var2])

    return constraintPairs


class BacktrackSearch:
    def __init__(self, partial_assignment):
        self.partial_assignment=partial_assignment

    def backtrack_search(self):
        return self.backtrack(self.partial_assignment)
    
    def backtrack(self, possible_solution):
        unsolved = possible_solution.find_unsolved_square()
        if unsolved is None:
            return possible_solution
        # TODO: create a getter for values
        unsolved_domain = possible_solution.values[unsolved]
        # For each possible assignment, try to solve the puzzle
        for value in unsolved_domain:
            solution = AC3(deepcopy(possible_solution.values), CreateConstraints())
            solution.values[unsolved] = [value]
            # If the value did not result in an inconsistency, go to the next unassigned square
            if solution.ac3():
                result = self.backtrack(solution)
                if result is not False:
                    return result
        
        return False

def main():
    file = open(argv[1], "r")
    inputArray = file.readlines()
    puzzleIndex = 0
    puzzles = [""]*10
    for line in inputArray:
        line=line.strip()
        if line!="":
            puzzles[puzzleIndex]+=line
            
        else:
            puzzles.append([])
            puzzleIndex+=1
    for i in range(puzzleIndex+1):
        data = puzzles[i]
        print("\nsolving:")
        for index in range(9):
            print(str(inputArray[i*10+index]).strip())
        x = AC3(data,CreateConstraints())
        solvable = x.ac3()
        if solvable:
            if (x.find_unsolved_square() is None):
                print('solved')
                x.printInFormat()  
            else:
                print("backtracking")
                search = BacktrackSearch(x)
                solution = search.backtrack_search()
                if (solution):
                    print("Solved")
                    solution.printInFormat()
                else:
                    print("Puzzle Cannot be Solved\n")
        else:
            print("Puzzle Cannot be Solved\n")

if __name__ == "__main__":
    main()