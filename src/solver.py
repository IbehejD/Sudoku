import random
import numpy as np
import math
from random import choice
import statistics


class Solver:
    def __init__(self,def_grid):
        self.def_grid= def_grid
        self.grid = np.copy(self.def_grid)

    # Cost Function
    def CalculateNumberOfErrors(self,sudoku):
        numberOfErrors = 0
        for i in range(0, 9):
            numberOfErrors += self.CalculateNumberOfErrorsRowColumn(i, i, sudoku)
        return (numberOfErrors)


    def CalculateNumberOfErrorsRowColumn(self, row, column, sudoku):
        numberOfErrors = (9 - len(np.unique(sudoku[:, column]))) + (9 - len(np.unique(sudoku[row, :])))
        return (numberOfErrors)


    def CreateList3x3Blocks(self):
        finalListOfBlocks = []
        for r in range(0, 9):
            tmpList = []
            block1 = [i + 3 * ((r) % 3) for i in range(0, 3)]
            block2 = [i + 3 * math.trunc((r) / 3) for i in range(0, 3)]
            for x in block1:
                for y in block2:
                    tmpList.append([x, y])
            finalListOfBlocks.append(tmpList)
        return (finalListOfBlocks)


    def RandomlyFill3x3Blocks(self,sudoku, listOfBlocks):
        for block in listOfBlocks:
            for box in block:
                if sudoku[box[0], box[1]] == 0:
                    currentBlock = sudoku[block[0][0]:(block[-1][0] + 1), block[0][1]:(block[-1][1] + 1)]
                    sudoku[box[0], box[1]] = choice([i for i in range(1, 10) if i not in currentBlock])
        return sudoku


    def SumOfOneBlock(self, sudoku, oneBlock):
        finalSum = 0
        for box in oneBlock:
            finalSum += sudoku[box[0], box[1]]
        return (finalSum)


    def TwoRandomBoxesWithinBlock(self,  block):
        while True:
            firstBox = random.choice(block)
            secondBox = choice([box for box in block if box is not firstBox])

            if not(self.is_def(firstBox, )) and not(self.is_def(secondBox, )):
                return ([firstBox, secondBox])


    def FlipBoxes(self,sudoku, boxesToFlip):
        proposedSudoku = np.copy(sudoku)
        placeHolder = proposedSudoku[boxesToFlip[0][0], boxesToFlip[0][1]]
        proposedSudoku[boxesToFlip[0][0], boxesToFlip[0][1]] = proposedSudoku[boxesToFlip[1][0], boxesToFlip[1][1]]
        proposedSudoku[boxesToFlip[1][0], boxesToFlip[1][1]] = placeHolder
        return (proposedSudoku)


    def ProposedState(self,sudoku,  listOfBlocks):
        correct = True

        while True:
            randomBlock = random.choice(listOfBlocks)
            if self.number_of_def( randomBlock) < 8:
                break

        boxesToFlip = self.TwoRandomBoxesWithinBlock( randomBlock)
        proposedSudoku = self.FlipBoxes(sudoku, boxesToFlip)
        return ([proposedSudoku, boxesToFlip])

    def number_of_def(self, randomBlock):
        i = 0
        for x in randomBlock:
            if self.is_def(x, ):
                i += 1
        print(i)
        return i
    def is_def(self, indexes, ):
        return bool(self.def_grid[indexes[0]][indexes[1]])

    def ChooseNewState(self, currentSudoku,  listOfBlocks, sigma):
        proposal = self.ProposedState(currentSudoku,  listOfBlocks)
        newSudoku = proposal[0]
        boxesToCheck = proposal[1]
        currentCost = self.CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1],
                                                    currentSudoku) + self.CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0],
                                                                                                        boxesToCheck[1][1],
                                                                                                        currentSudoku)
        newCost = self.CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1],
                                                newSudoku) + self.CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0],
                                                                                                boxesToCheck[1][1],
                                                                                                newSudoku)
        # currentCost = CalculateNumberOfErrors(currentSudoku)
        # newCost = CalculateNumberOfErrors(newSudoku)
        costDifference = newCost - currentCost
        rho = math.exp(-costDifference / sigma)
        if (np.random.uniform(1, 0, 1) < rho):
            return ([newSudoku, costDifference])
        return ([currentSudoku, 0])


    def ChooseNumberOfItterations(self,):
        numberOfItterations = 0
        for i in range(0, 9):
            for j in range(0, 9):
                if self.is_def([i, j], ):
                    numberOfItterations += 1
        return numberOfItterations


    def CalculateInitialSigma(self, sudoku, listOfBlocks):
        listOfDifferences = []
        tmpSudoku = sudoku
        for i in range(1, 10):
            tmpSudoku = self.ProposedState(tmpSudoku,  listOfBlocks)[0]
            listOfDifferences.append(self.CalculateNumberOfErrors(tmpSudoku))
        return (statistics.pstdev(listOfDifferences))


    def solveSudoku(self,sudoku):

        solutionFound = 0
        while (solutionFound == 0):
            print("start")
            decreaseFactor = 0.99
            stuckCount = 0
            listOfBlocks = self.CreateList3x3Blocks()
            tmpSudoku = self.RandomlyFill3x3Blocks(sudoku, listOfBlocks)
            sigma = self.CalculateInitialSigma(sudoku, listOfBlocks)
            score = self.CalculateNumberOfErrors(tmpSudoku)
            itterations = self.ChooseNumberOfItterations()
            if score <= 0:
                solutionFound = 1

            while solutionFound == 0:

                previousScore = score
                for i in range(0, itterations):
                    newState = self.ChooseNewState(tmpSudoku,  listOfBlocks, sigma)
                    tmpSudoku = newState[0]
                    scoreDiff = newState[1]
                    score += scoreDiff
                    print(score)
                    if score <= 0:
                        solutionFound = 1
                        break

                sigma *= decreaseFactor
                if score <= 0:
                    solutionFound = 1
                    break
                if score >= previousScore:
                    stuckCount += 1
                else:
                    stuckCount = 0
                if (stuckCount > 80):
                    sigma += 2
                if (self.CalculateNumberOfErrors(tmpSudoku) == 0):

                    break
        return (tmpSudoku)





