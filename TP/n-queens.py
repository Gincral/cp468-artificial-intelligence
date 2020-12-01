from copy import deepcopy
import heapq
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
import random

class NQueens:
    def __init__(self, n):
        self.size = n
        self.puzzle = self.generatePuzzle()

    def generatePuzzle(self):
        nr = self.size
        board=[0]*nr
        if (nr%2==1 and nr%6!=3):
            for i in range(nr//2+1):
                board[i]=i*2
                if (i!=nr//2):
                    board[i+nr//2+1]=1+i*2
        else:
            
            board[0]=random.randint(0,nr-1)
            for i in range(nr//2):
                board[i+1]=i*2
            for i in range(nr//2,nr):
                board[i]=random.randint(0,nr-1)
        return board;

    def printPuzzle(self):
        print(self.puzzle)
        size = self.size
        for i in range(size):
            row = ['[ ]'] * size
            for col in range(size):
                if self.puzzle[col] == i:
                    row[col] = '[Q]'
            print(''.join(row))

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        
    def CreateConstraints():
        return None


def main():
    n = int(input("Enter the value of N: "))
    nqueens = NQueens(n)
    nqueens.printPuzzle()
    # print(nqueens.generatePuzzle(n));

if __name__ == "__main__":
    main()