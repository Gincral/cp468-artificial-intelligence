rows =['A','B','C','D','E','F','G','H','I']
class AC3:

    def __init__(self, data):
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
            for k in range(3):
                squareVariables= [rows[3*i]+str(3*j+k), rows[3*i+1]+str(3*j+k),rows[3*i+2]+str(3*j+k)]
            for var1 in squareVariables:
                for var2 in squareVariables:
                    if var1!=var2 and [var1,var2] not in constraintPairs:
                        constraintPairs.append([var1,var2])

    print("There are 81 Variables.\nThere are "+ str(len(constraintPairs))+ " Arcs")




def main():
    # data = input("enter 81 length string: ")
    # if len(data) != 81 or data.isdigit()==False:
    #     print("wrong input")
    #     return 0

    data = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
    CreateConstraints()
    x = AC3(data)
    print(x.variables)
    print(x.values)

if __name__ == "__main__":
    main()