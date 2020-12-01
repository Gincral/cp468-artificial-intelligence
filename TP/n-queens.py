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

    def printPuzzle(self):
        size = self.size
        for i in range(size):
            row = ['[ ]'] * size
            for col in range(size):
                if self.puzzle[col] == self.size - 1 - i:
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