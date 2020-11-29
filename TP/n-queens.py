from copy import deepcopy
import heapq
import numpy as np
import matplotlib.pyplot as plt
from sys import argv


class NQueens:
    def __init__(self, n, puzzle):
        if puzzle == None:
            self.puzzle = generatePuzzle(n)
        else:
            self.puzzle = puzzle
    def generatePuzzle(size):
        return None


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        
    def CreateConstraints():
        return None


def main():
    n = input("Enter the value of N: ")
    puzzle = input("Enter the N-Queen puzzle: ")
    nqueens = NQueens(n, puzzle);

if __name__ == "__main__":
    main()
    input("Hit enter if Finished")