from copy import deepcopy
import time
import heapq
from more_itertools import locate
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
import random
import csv
import math
from PIL import Image, ImageDraw

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
        size = self.size
        if size<16:
            for i in range(size):
                row = ['[ ]'] * size
                for col in range(size):
                    if self.puzzle[col] == i:
                        row[col] = '[Q]'
                print(''.join(row))

    # Creates and exports a visual representation of a chess board with the N-queens' solution
    def exportPuzzle(self):
        print("Exporting solution to queens-output.png...")
        size = self.size
        imgDimens = 1 + (50 * size)
        if self.size > 1000:
            imgDimens = self.size
        elif imgDimens > 10000:
            imgDimens = 10000
        cellSize = math.floor(imgDimens / size)

        board = Image.new('RGB', (imgDimens,imgDimens))
        draw = ImageDraw.Draw(board)

        if self.size > 50:
            self.exportPuzzleLarge(draw, cellSize)
        else:
            self.exportPuzzleSmall(draw, cellSize)
            
        board.save('queens-output.png')
        print("Success")

    # Draws a traditional chess board with the N-queens marked as red squares
    def exportPuzzleSmall(self, draw, cellSize):
        size = self.size
        posX = 0
        posY = 0
        fill = (255,255,255)
        for i in range(size):
            for col in range(size):
                if (i+col) % 2 == 0:
                    fill = (255,255,255)
                else:
                    fill = (169,169,169)
                # Draws a chess board tile
                draw.rectangle(
                    (posX, posY, posX + cellSize, posY + cellSize),
                    fill=fill,
                    outline=(169,169,169))
                # Indicates the position of a queen on the board
                if self.puzzle[col] == i:
                    midX = math.ceil(posX + (cellSize / 4))
                    midY = posY + (cellSize / 4)
                    draw.rectangle(
                        (midX, midY, math.ceil(midX + (cellSize / 2)), math.ceil(midY + (cellSize / 2))),
                        fill=(255,0,0),
                        outline=None)
                posX += cellSize
            posY += cellSize
            posX = 0

    # Draws a checkered board where the N-queens are marked as grey tiles (n <= 1000) on a white background
    # For n > 1000, N-queens are marked as white pixels on a black background
    def exportPuzzleLarge(self, draw, cellSize):
        size = self.size
        posX = 0
        posY = 0
        if size > 1000:
            outline = None
            fill = (255,255,255)
            for i in range(len(self.puzzle)):
                posX = cellSize * i
                posY = cellSize * self.puzzle[i]
                draw.rectangle(
                    (posX, posY, posX + cellSize, posY + cellSize),
                    fill=fill,
                    outline=outline)
        else: 
            outline = (169,169,169)
            for i in range(size):
                for col in range(size):
                    if self.puzzle[col] == i:
                        fill = (169,169,169)
                    else:
                        fill = (255,255,255)
                    # Draws a chess board tile
                    draw.rectangle(
                        (posX, posY, posX + cellSize, posY + cellSize),
                        fill=fill,
                        outline=outline)
                    posX += cellSize
                posY += cellSize
                posX = 0

    def conflicts(self, col, row):
        total = 0
        rowLen=len(self.rowsInd[row])
        total+=rowLen-1
        diag1Len = len(self.diag1Ind[row+col])
        total+=diag1Len-1
        diag2Len=len(self.diag2Ind[(self.size-row)+col])
        total+=diag2Len-1
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
            # if i%100==0 or sumCon<0:
            #     print(sumCon)
            if sumCon == 0:
                with open('Steps.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([i,self.size])
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
            self.puzzle[position] = n
            if prev!=n:
                self.updateConflicts(prev,n,position)
            
        return False
        
    def updateConflicts(self,prev,n,position):
        self.rowsInd[n].append(position)
        self.rowsInd[prev].remove(position)
        self.diag1Ind[n+position].append(position)
        self.diag1Ind[prev+position].remove(position)
        self.diag2Ind[(self.size-n)+position].append(position)
        self.diag2Ind[(self.size-prev)+position].remove(position)

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


def main():
    n = int(input("Enter the value of N: "))
    if n == 0:
        puzzle = input("Enter the puzzle: ").split(" ")
        puzzle = [ int(x) for x in puzzle ]
        nqueens = NQueens(len(puzzle))
        nqueens.puzzle = puzzle
        nqueens.populateFrequencies()
        con = [nqueens.conflicts(i, nqueens.puzzle[i]) for i in range(nqueens.size)]
        print(con)
        if sum(con) == 0:
            print("this is an answer for", nqueens.size,"queens")
            nqueens.exportPuzzle()
        else:
            print("this is not an answer for", nqueens.size,"queens")
    else:
        nqueens = NQueens(n)
        start=time.time()
        if nqueens.minConflicts():
            print("Solved! Number of queens: ", n)
            print(nqueens.puzzle)
            if(n< 30): nqueens.printPuzzle()
        else:
            print("Puzzle cant be solved, try upper the iteraition")
        end = time.time()-start
        print(str(n)+"-Queens took "+str(end))
        print("\n")
        if n <= 50000:
            nqueens.exportPuzzle()


if __name__ == "__main__":
    main()