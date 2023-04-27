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
    def CalculateNumberOfErrors(self,grid):
        numberOfErrors = 0
        for i in range(0, 9):
            numberOfErrors += self.CalculateNumberOfErrorsRowColumn(i, i, grid)
        return (numberOfErrors)


    def CalculateNumberOfErrorsRowColumn(self, row, column, grid):
        numberOfErrors = (9 - len(np.unique(grid[:, column]))) + (9 - len(np.unique(grid[row, :])))
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


    def RandomlyFill3x3Blocks(self,grid, listOfBlocks):
        for block in listOfBlocks:
            for box in block:
                if grid[box[0], box[1]] == 0:
                    currentBlock = grid[block[0][0]:(block[-1][0] + 1), block[0][1]:(block[-1][1] + 1)]
                    grid[box[0], box[1]] = choice([i for i in range(1, 10) if i not in currentBlock])
        return grid


    def SumOfOneBlock(self, grid, oneBlock):
        finalSum = 0
        for box in oneBlock:
            finalSum += grid[box[0], box[1]]
        return (finalSum)


    def TwoRandomBoxesWithinBlock(self,  block):
        while True:
            firstBox = random.choice(block)
            secondBox = choice([box for box in block if box is not firstBox])

            if not(self.is_def(firstBox, )) and not(self.is_def(secondBox, )):
                return ([firstBox, secondBox])


    def FlipBoxes(self,grid, boxesToFlip):
        proposedSudoku = np.copy(grid)
        placeHolder = proposedSudoku[boxesToFlip[0][0], boxesToFlip[0][1]]
        proposedSudoku[boxesToFlip[0][0], boxesToFlip[0][1]] = proposedSudoku[boxesToFlip[1][0], boxesToFlip[1][1]]
        proposedSudoku[boxesToFlip[1][0], boxesToFlip[1][1]] = placeHolder
        return (proposedSudoku)


    def ProposedState(self,grid,  listOfBlocks):

        while True:
            randomBlock = random.choice(listOfBlocks)
            if self.number_of_def( randomBlock) < 8:
                break

        boxesToFlip = self.TwoRandomBoxesWithinBlock( randomBlock)
        proposedSudoku = self.FlipBoxes(grid, boxesToFlip)
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

    def ChooseNewState(self, current_grid,  listOfBlocks, sigma):
        proposal = self.ProposedState(current_grid,  listOfBlocks)
        new_grid = proposal[0]
        boxesToCheck = proposal[1]
        currentCost = self.CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1],
                                                    current_grid) + self.CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0],
                                                                                                        boxesToCheck[1][1],
                                                                                                        current_grid)
        newCost = self.CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1],
                                                new_grid) + self.CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0],
                                                                                                boxesToCheck[1][1],
                                                                                                new_grid)
        costDifference = newCost - currentCost
        rho = math.exp(-costDifference / sigma)
        if (np.random.uniform(1, 0, 1) < rho):
            return ([new_grid, costDifference])
        return ([current_grid, 0])


    def ChooseNumberOfItterations(self,):
        numberOfItterations = 0
        for i in range(0, 9):
            for j in range(0, 9):
                if self.is_def([i, j], ):
                    numberOfItterations += 1
        return numberOfItterations


    def CalculateInitialSigma(self, grid, listOfBlocks):
        listOfDifferences = []
        tmp_grid = grid
        for i in range(1, 10):
            tmp_grid = self.ProposedState(tmp_grid,  listOfBlocks)[0]
            listOfDifferences.append(self.CalculateNumberOfErrors(tmp_grid))
        return (statistics.pstdev(listOfDifferences))


    def solveSudoku(self):

        solutionFound = 0
        while (solutionFound == 0):
            print("start")
            decreaseFactor = 0.99
            stuckCount = 0
            listOfBlocks = self.CreateList3x3Blocks()
            tmp_grid = self.RandomlyFill3x3Blocks(self.grid, listOfBlocks)
            sigma = self.CalculateInitialSigma(self.grid, listOfBlocks)
            score = self.CalculateNumberOfErrors(tmp_grid)
            itterations = self.ChooseNumberOfItterations()
            if score <= 0:
                solutionFound = 1

            while solutionFound == 0:

                previousScore = score
                for i in range(0, itterations):
                    newState = self.ChooseNewState(tmp_grid,  listOfBlocks, sigma)
                    tmp_grid = newState[0]
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
                if (self.CalculateNumberOfErrors(tmp_grid) == 0):

                    break
        return (tmp_grid)





