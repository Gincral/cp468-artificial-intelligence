from copy import deepcopy
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
        self.queensDiag1=[0]*(2*n)
        self.queensDiag2=[0]*(2*n)

    def generatePuzzle(self):
        nr = self.size
        board=[0]*nr
        if (nr%6!=2 and nr%6!=3):
            for i in range(nr//2+1):
                if i!=nr//2:
                    board[i]=i*2+1
                board[i+nr//2]=i*2
                    
        else:
            
            board[0]=random.randint(0,nr-1)
            for i in range(nr//2):
                board[i+1]=i*2
            for i in range(nr//2,nr):
                board[i]=random.randint(0,nr-1)
        return board

    def printPuzzle(self):
        print(self.puzzle)
        size = self.size
        for i in range(size):
            row = ['[ ]'] * size
            for col in range(size):
                if self.puzzle[col] == i:
                    row[col] = '[Q]'
            print(''.join(row))
            

    def conflicts(self, col, row):
        total = 0
        total+=self.queensRow[row]
        total+=self.queensDiag1[row+col]
        total+=self.queensDiag2[self.size-row+col]-3
        return total

    def populateFrequencies(self):
        for i in range(self.size):
            row=self.puzzle[i]
            self.queensRow[row]+=1
            self.queensDiag1[row+i]+=1
            self.queensDiag2[self.size-row+i]+=1


    def minConflicts(self, maxSteps=100000):
        self.populateFrequencies()
        for i in range(maxSteps):
            conflicts = [self.conflicts(col, self.puzzle[col]) for col in range(self.size)] 
            sumCon=sum(conflicts)
            if i%100==0:
                print(sumCon)
            if sumCon == 0:
                return True
            conflicting=[]
            for i in range(len(conflicts)):
                if conflicts[i]!=0:
                    conflicting.append(i)
            position = conflicting[random.randrange(0, len(conflicting))]
            list = [self.conflicts(position, value) for value in range(self.size)]
            minimum=min(list)
            n = random.choice([i for i in range(self.size) if list[i] == minimum])
            prev=self.puzzle[position]
            self.puzzle[position] = n
            self.queensRow[n]+=1
            self.queensRow[prev]-=1
            self.queensDiag1[n+position]+=1
            self.queensDiag1[prev+position]-=1
            self.queensDiag2[self.size-n+position]+=1
            self.queensDiag2[self.size-prev+position]-=1
        return False
    


def main():
    n = int(input("Enter the value of N: "))
    nqueens = NQueens(n)
    nqueens.printPuzzle()
    if nqueens.minConflicts():
        print("solved")
        nqueens.printPuzzle()
    else:
        print("Puzzle cant be solved, try upper the iteraition")

if __name__ == "__main__":
    main()