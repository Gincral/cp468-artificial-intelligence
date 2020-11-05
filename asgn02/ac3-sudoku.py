rows =['A','B','C','D','E','F','G','H','I']
class AC3:

    def __init__(self, data,constraints):
        self.binConstraints=constraints
        self.values={}
        cols= [x for x in range(1,10)]
        self.variables = [row+str(col) for row in rows for col in cols]
        i = 0
        for var in self.variables:
            if data[i] == '0':
                self.values[var]=[1,2,3,4,5,6,7,8,9]
            else:
                self.values[var]=[int(data[i])]
            i += 1
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




def main():
    # data = input("enter 81 length string: ")
    # if len(data) != 81 or data.isdigit()==False:
    #     print("wrong input")
    #     return 0

    data = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
    
    x = AC3(data,CreateConstraints())
    print(x.ac3())
    # print(x.related_cells)
    print(x.values)

if __name__ == "__main__":
    main()