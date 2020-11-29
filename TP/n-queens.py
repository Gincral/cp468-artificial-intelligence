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


class BacktrackSearch:
    def __init__(self, partial_assignment):
        self.partial_assignment=partial_assignment
        self.nodes_expanded = 0

    def backtrack_search(self):
        return self.backtrack(self.partial_assignment)
    
    def backtrack(self, possible_solution):
        # Selects a variable with the fewest remaining values
        unsolved = possible_solution.minimum_remaining_values()
        self.nodes_expanded += 1
        if self.nodes_expanded%100==0:
            print('nodes expanded: ' + str(self.nodes_expanded))
        if unsolved is False:
            return False
        # If every variable has an assignment, return this solution
        elif unsolved is None:
            return possible_solution
        
        # Sorts the list of possible assignments in order of least to most constraining
        lcvs = possible_solution.least_constraining_value(unsolved)
        # For each possible assignment, try to solve the puzzle
        for value in lcvs:
            # Verify that the solution is still arc-consistent after assigning the current value
            solution = AC3(deepcopy(possible_solution.values), CreateConstraints())
            solution.values[unsolved] = [value]
            # If the value did not result in an inconsistency, check for the next unassigned square
            if solution.ac3(graph=False):
                result = self.backtrack(solution)
                if result is not False:
                    return result
        
        return False

def main():
    n = input("Enter the value of N: ")
    puzzle = input("Enter the N-Queen puzzle: ")
    nqueens = NQueens(n, puzzle);

if __name__ == "__main__":
    main()
    input("Hit enter if Finished")