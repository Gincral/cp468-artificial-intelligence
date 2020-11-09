from copy import deepcopy
import heapq
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

    def minimum_remaining_values(self):
        mrv = None
        for item in self.values.items():
            if len(item[1]) == 0:
                return False
            elif mrv is None and len(item[1]) > 1:
                mrv = item[0]
            elif mrv is not None and len(item[1]) > 1 and len(item[1]) == len(self.values.get(mrv)):
                # print('update mrv: ' + item[0])
                mrv = item[0]
            elif mrv is not None and len(item[1]) > 1 and len(item[1]) < len(self.values.get(mrv)):
                # print('update mrv: ' + item[0])
                mrv = item[0]
        return mrv

    def least_constraining_value(self, mrv):
        values = self.values.get(mrv)
        lcv_index = {}
        for value in values:
            lcv_index[value] = 0
        for cell in self.related_cells.get(mrv):
            for i in range(len(values)):
                if values[i] in self.values.get(cell):
                    lcv_index[values[i]] += 1
        return sorted(lcv_index, key=lcv_index.get)

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

    # print("There are 81 Variables.\nThere are "+ str(len(constraintPairs))+ " Arcs")
    return constraintPairs


class BacktrackSearch:
    def __init__(self, partial_assignment):
        self.partial_assignment=partial_assignment

    def backtrack_search(self):
        return self.backtrack(self.partial_assignment)
    
    def backtrack(self, possible_solution):
        # MRV implementation
        unsolved = possible_solution.minimum_remaining_values()
        # print('mrv = ')
        # print(unsolved)
        # print('unsolved domain = ')
        # print(possible_solution.values[unsolved])
        # print('Unsolved:')
        # print('key = ' + unsolved)
        # print('------------------------------')
        # print(possible_solution.printInFormat())
        # print('------------------------------')
        # print('value = ' + str(possible_solution.values[unsolved]))
        # # ---- Uninformed implementation ----
        # unsolved = possible_solution.find_unsolved_square()
        if unsolved is False:
            return False
        elif unsolved is None:
            return possible_solution
        # TODO: create a getter for values
        unsolved_domain = possible_solution.values[unsolved]
        # # ---- MRV + LCV implementation ----
        lcvs = possible_solution.least_constraining_value(unsolved)
        # print('lcvs =')
        # print(lcvs)
        # For each possible assignment, try to solve the puzzle
        for value in lcvs:
        # for value in unsolved_domain:
            solution = AC3(deepcopy(possible_solution.values), CreateConstraints())
            solution.values[unsolved] = [value]
            # print('TRY WITH: ' + str(solution.values[unsolved]))
            # If the value did not result in an inconsistency, check for the next unassigned square
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
            print(puzzleIndex)
    # data = "026000378058637400047000561000720900000308250802000010469501000001900740030040090"
    
    for i in range(puzzleIndex+1):
        data = puzzles[i]
        print("solving:")
        for index in range(9):
            print(str(inputArray[i*10+index]).strip())

        # data = "020000003600031000500000084370000501000060009000400000000007800200090040050200100"
        
        # The "world's hardest Sudoku"
        # https://puzzling.stackexchange.com/questions/252/how-do-i-solve-the-worlds-hardest-sudoku
        # data = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"


        x = AC3(data,CreateConstraints())
        x.ac3()
        #x.printInFormat()
        if (x.find_unsolved_square() is None):
            print('solved')
            x.printInFormat()  
        else:
            print("backtracking")
            search = BacktrackSearch(x)
            solution = search.backtrack_search()
            solution.printInFormat()

if __name__ == "__main__":
    main()