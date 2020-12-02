from copy import deepcopy
import time
import heapq
from more_itertools import locate
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
import random

class NQueens:
    def __init__(self, n):
        self.size = n
        self.puzzle = self.generatePuzzle()
        self.queensRow=[0]*n
        self.rowsInd=[[] for j in range(self.size)] 
        self.diag1Ind=[[] for j in range(self.size*2+2)] 
        self.diag2Ind=[[] for j in range(self.size*2+2)]


    def generatePuzzle(self):
        nr = self.size
        board=[0]*nr
        board[0]=random.randint(0,nr-1)
        for i in range(nr//2):
            board[i+1]=i*2
        for i in range(nr//2,nr):
            board[i]=random.randint(0,nr-1)
        return board

    def printPuzzle(self):
        #print(self.puzzle)
        size = self.size
        for i in range(size):
            row = ['[ ]'] * size
            for col in range(size):
                if self.puzzle[col] == i:
                    row[col] = '[Q]'
            print(''.join(row))
            

    def conflicts(self, col, row):
        total = 0
        rowLen=len(self.rowsInd[row])
        total+=rowLen-1
        diag1Len = len(self.diag1Ind[row+col])
        total+=diag1Len-1
        diag2Len=len(self.diag2Ind[(self.size-row)+col])
        total+=diag2Len-1
        #print("row ind:"+str(self.rowsInd[row]))
        #print("col:"+str(col)+", "+str(rowLen)+" , "+ str(diag1Len)+" , "+str(diag2Len))
        return total

    def populateFrequencies(self):
        for i in range(self.size):
            row=self.puzzle[i]
            self.rowsInd[row].append(i)
            self.diag1Ind[row+i].append(i)
            self.diag2Ind[(self.size-row)+i].append(i)



    def minConflicts(self, maxSteps=100000):
        self.populateFrequencies()
        self.allConflicts = [self.conflicts(col, self.puzzle[col]) for col in range(self.size)] 
        for i in range(maxSteps):
            sumCon=sum(self.allConflicts)
            if i%100==0 or sumCon<0:
                print(sumCon)
                #self.printPuzzle()
            #print("Row indices before"+str(self.rowsInd))
            #print(self.allConflicts)
            if sumCon == 0:
                return True
            conflicting=[]
            for col in range(self.size):
                if self.allConflicts[col]!=0:
                    conflicting.append(col)
            position = conflicting[random.randrange(0, len(conflicting))]
            list = [self.conflicts(position, value) for value in range(self.size)]
            minimum=min(list)
            n = random.choice([i for i in range(self.size) if list[i] == minimum])
            prev=self.puzzle[position]
            #self.printPuzzle()
            
            """print("diag 1 ind "+str(self.diag1Ind))
               print("diag 2 ind "+str(self.diag2Ind))"""
            self.puzzle[position] = n
            self.rowsInd[n].append(position)
            self.rowsInd[prev].remove(position)
            self.diag1Ind[n+position].append(position)
            self.diag1Ind[prev+position].remove(position)
            self.diag2Ind[(self.size-n)+position].append(position)
            self.diag2Ind[(self.size-prev)+position].remove(position)
            #self.printPuzzle()
            #print("Row indices"+str(self.rowsInd))

            """print("diag 1 ind "+str(self.diag1Ind))
               print("diag 2 ind "+str(self.diag2Ind))"""
           

            for j in self.rowsInd[n]:
                self.allConflicts[j]=self.conflicts(j,n)
            for j in self.rowsInd[prev]:
                self.allConflicts[j]=self.conflicts(j,prev)
            for j in self.diag1Ind[position+n]:
                self.allConflicts[j]=self.conflicts(j,self.puzzle[j])
            for j in self.diag1Ind[position+prev]:
                self.allConflicts[j]=self.conflicts(j,self.puzzle[j])
            for j in self.diag2Ind[self.size-n+position]:
                self.allConflicts[j]=self.conflicts(j,self.puzzle[j])
            for j in self.diag2Ind[self.size-prev+position]:
                self.allConflicts[j]=self.conflicts(j,self.puzzle[j])
            #print(self.allConflicts)
            #print("\n")
            
        return False
    


def main():
    n = int(input("Enter the value of N: "))
    times=[]
    for i in range(100,n,100):
        nqueens = NQueens(i)
        #nqueens.printPuzzle()
        start=time.time()
        #print(start)
        if nqueens.minConflicts():
            print("solved")
            #nqueens.printPuzzle()
        else:
            print("Puzzle cant be solved, try upper the iteraition")
        times.append(time.time()-start)
    for i in range(len(times)):
        print(str(5+200*i)+"-Queens took "+str(times[i])+"s")

if __name__ == "__main__":
    main()