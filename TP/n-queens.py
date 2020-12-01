from copy import deepcopy
import heapq
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
import random

class NQueens:
    def __init__(self, n):
        self.size = n
        self.puzzle = list(range(n))

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

    def conflicts(self, col, value):
        total = 0
        for i in range(self.size):
            if i == col:
                continue
            if self.puzzle[i] == value or abs(i - col) == abs(self.puzzle[i] - value):
                total += 1
        return total

    def minConflicts(self, maxSteps=1000):
        for i in range(maxSteps):
            conflicts = [self.conflicts(col, self.puzzle[col]) for col in range(self.size)] 
            print('sum: ', sum(conflicts))
            if sum(conflicts) == 0:
                return True
            position = random.randrange(0, 10)
            print('random position: ',position)
            list = [self.conflicts(position, value) for value in range(self.size)]
            print(list)
            minPosition = min(list)
            self.puzzle[position] = list.index(minPosition)
            print(self.puzzle)
        return False
    


def main():
    # n = int(input("Enter the value of N: "))
    nqueens = NQueens(10)
    nqueens.printPuzzle()
    if nqueens.minConflicts():
        nqueens.printPuzzle()
    else:
        print("Puzzle cant be solved, try upper the iteraition")

if __name__ == "__main__":
    main()