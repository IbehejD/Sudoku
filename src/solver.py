import math
import random
import statistics
from random import choice

import numpy as np
import pygame
from sudoku import Sudoku

from sudokuGui import *


def FixSudokuValues(fixed_sudoku):
    for i in range(0, 9):
        for j in range(0, 9):
            if fixed_sudoku[i, j] != 0:
                fixed_sudoku[i, j] = 1

    return (fixed_sudoku)


# Cost Function
def CalculateNumberOfErrors(sudoku):
    numberOfErrors = 0
    for i in range(0, 9):
        numberOfErrors += CalculateNumberOfErrorsRowColumn(i, i, sudoku)
    return (numberOfErrors)


def CalculateNumberOfErrorsRowColumn(row, column, sudoku):
    numberOfErrors = (9 - len(np.unique(sudoku[:, column]))) + (9 - len(np.unique(sudoku[row, :])))
    return (numberOfErrors)


def CreateList3x3Blocks():
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


def RandomlyFill3x3Blocks(sudoku, listOfBlocks):
    for block in listOfBlocks:
        for box in block:
            if sudoku[box[0], box[1]] == 0:
                currentBlock = sudoku[block[0][0]:(block[-1][0] + 1), block[0][1]:(block[-1][1] + 1)]
                sudoku[box[0], box[1]] = choice([i for i in range(1, 10) if i not in currentBlock])
    return sudoku


def SumOfOneBlock(sudoku, oneBlock):
    finalSum = 0
    for box in oneBlock:
        finalSum += sudoku[box[0], box[1]]
    return (finalSum)


def TwoRandomBoxesWithinBlock(fixedSudoku, block):
    for i in range(0, 25):
        firstBox = random.choice(block)
        secondBox = choice([box for box in block if box is not firstBox])


        if fixedSudoku[firstBox[0], firstBox[1]] != 1 and fixedSudoku[secondBox[0], secondBox[1]] != 1:
            return ([firstBox, secondBox])
        
    return([firstBox, firstBox])


def FlipBoxes(sudoku, boxesToFlip):
    proposedSudoku = np.copy(sudoku)
    placeHolder = proposedSudoku[boxesToFlip[0][0], boxesToFlip[0][1]]
    proposedSudoku[boxesToFlip[0][0], boxesToFlip[0][1]] = proposedSudoku[boxesToFlip[1][0], boxesToFlip[1][1]]
    proposedSudoku[boxesToFlip[1][0], boxesToFlip[1][1]] = placeHolder
    return (proposedSudoku)


def ProposedState(sudoku, fixedSudoku, listOfBlocks):
    randomBlock = random.choice(listOfBlocks)

    boxesToFlip = TwoRandomBoxesWithinBlock(fixedSudoku, randomBlock)
    proposedSudoku = FlipBoxes(sudoku, boxesToFlip)
    return ([proposedSudoku, boxesToFlip])


def ChooseNewState(currentSudoku, fixedSudoku, listOfBlocks, sigma):
    proposal = ProposedState(currentSudoku, fixedSudoku, listOfBlocks)
    newSudoku = proposal[0]
    boxesToCheck = proposal[1]
    currentCost = CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1],
                                                   currentSudoku) + CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0],
                                                                                                     boxesToCheck[1][1],
                                                                                                     currentSudoku)
    newCost = CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1],
                                               newSudoku) + CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0],
                                                                                             boxesToCheck[1][1],
                                                                                             newSudoku)
    # currentCost = CalculateNumberOfErrors(currentSudoku)
    # newCost = CalculateNumberOfErrors(newSudoku)
    costDifference = newCost - currentCost
    rho = math.exp(-costDifference / sigma)
    if (np.random.uniform(1, 0, 1) < rho):
        return ([newSudoku, costDifference])
    return ([currentSudoku, 0])


def ChooseNumberOfItterations(fixed_sudoku):
    numberOfItterations = 0
    for i in range(0, 9):
        for j in range(0, 9):
            if fixed_sudoku[i, j] != 0:
                numberOfItterations += 1
    return numberOfItterations


def CalculateInitialSigma(sudoku, fixedSudoku, listOfBlocks):
    listOfDifferences = []
    tmpSudoku = sudoku
    for i in range(1, 10):
        tmpSudoku = ProposedState(tmpSudoku, fixedSudoku, listOfBlocks)[0]
        listOfDifferences.append(CalculateNumberOfErrors(tmpSudoku))
    return (statistics.pstdev(listOfDifferences))


def solveSudoku(sudoku):

    f = open("demofile2.txt", "a")
    solutionFound = 0
    while (solutionFound == 0):
        print("start")
        decreaseFactor = 0.99
        stuckCount = 0
        fixedSudoku = np.copy(sudoku)

        FixSudokuValues(fixedSudoku)
        listOfBlocks = CreateList3x3Blocks()
        tmpSudoku = RandomlyFill3x3Blocks(sudoku, listOfBlocks)
        sigma = CalculateInitialSigma(sudoku, fixedSudoku, listOfBlocks)
        score = CalculateNumberOfErrors(tmpSudoku)
        itterations = ChooseNumberOfItterations(fixedSudoku)
        if score <= 0:
            solutionFound = 1

        while solutionFound == 0:

            previousScore = score
            for i in range(0, itterations):
                newState = ChooseNewState(tmpSudoku, fixedSudoku, listOfBlocks, sigma)
                tmpSudoku = newState[0]
                scoreDiff = newState[1]
                score += scoreDiff
                print(score)
                f.write(str(score) + '\n')
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
            if (CalculateNumberOfErrors(tmpSudoku) == 0):

                break
    f.close()
    return (tmpSudoku)
def generate_new(gen):
    x = np.array(gen.difficulty(0.5).board)
    return np.where(x == None, 0, x)




if __name__ == "__main__":

    screen = pygame.display.set_mode((500, 600))
    sudoku_gen = Sudoku(3)
    # def_grid = generate_new(sudoku_gen)
    def_grid = np.array([
        [0, 0, 0, 0, 0, 0, 0, 5, 6],
        [5, 1, 3, 6, 0, 7, 8, 2, 4],
        [0, 0, 0, 0, 5, 0, 3, 9, 1],
        [8, 3, 0, 0, 0, 6, 0, 7, 5],
        [9, 0, 6, 5, 7, 4, 1, 0, 0],
        [7, 4, 0, 0, 3, 0, 0, 6, 0],
        [6, 0, 4, 0, 1, 0, 9, 0, 2],
        [0, 5, 0, 0, 0, 0, 6, 1, 7],
        [0, 0, 8, 0, 6, 2, 0, 0, 0]])
    grid = np.copy(def_grid)


    run = True
    rs = 0
    # The loop thats keep the window running
    while run:
        screen.fill((255, 255, 255))
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                run = False
            # Get the number to be inserted if key pressed
            if event.type == pygame.KEYDOWN:
                # If D is pressed reset the board to default
                if event.key == pygame.K_d:
                    rs = 0
                    grid = np.copy(def_grid)
                if event.key == pygame.K_r:
                    def_grid = generate_new(sudoku_gen)
                    grid = np.copy(def_grid)
                    rs == 0
                if event.key == pygame.K_s:
                    grid = solveSudoku(grid)
                    rs == 1
        if rs == 1:
            result(screen)

        draw(grid, def_grid, screen)
        instruction(screen)
        # Update window
        pygame.display.update()

    # Quit pygame window
    pygame.quit()
