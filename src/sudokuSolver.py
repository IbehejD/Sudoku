import random
from random import choice
import numpy as np

import math
import statistics


class SudokuSolver():
    def __init__(self, def_grid):
        self.def_grid = def_grid
        self.grid = np.copy(self.def_grid)

    # solve function
    def solve(self):

        solution_found = 0
        while (solution_found == 0):
            print("start")
            decrease_factor = 0.99
            stuck_count = 0
            list_of_blocks = self.get_block_list()
            tmp_grid = self.rnd_fill_blocks(self.grid, list_of_blocks)
            sigma = self.get_initial_sigma(self.grid, list_of_blocks)
            score = self.get_error_number(tmp_grid)
            itterations = self.get_iterations_number()
            if score <= 0:
                solution_found = 1

            while solution_found == 0:

                previous_score = score
                for i in range(0, itterations):
                    new_state = self.get_new_state(
                        tmp_grid, list_of_blocks, sigma)
                    tmp_grid = new_state[0]
                    score_diff = new_state[1]
                    score += score_diff
                    print(score)
                    if score <= 0:
                        solution_found = 1
                        break

                sigma *= decrease_factor
                if score <= 0:
                    solution_found = 1
                    break
                if score >= previous_score:
                    stuck_count += 1
                else:
                    stuck_count = 0
                if (stuck_count > 80):
                    sigma += 2
                if (self.get_error_number(tmp_grid) == 0):

                    break
        return tmp_grid

    # cost function
    def get_error_number(self, tmp_grid):
        errors_num = 0
        for i in range(0, 9):
            errors_num += self.get_row_column_error(i, i, tmp_grid)
        return errors_num

    # row column cost function
    def get_row_column_error(self, row, column, tmp_grid):
        errors_num = (
            9 - len(np.unique(tmp_grid[:, column]))) + (9 - len(np.unique(tmp_grid[row, :])))
        return errors_num

    # converting grid to list of blocks
    def get_block_list(self):
        final_block_list = []
        for r in range(0, 9):
            tmp_list = []
            block1 = [i + 3 * ((r) % 3) for i in range(0, 3)]
            block2 = [i + 3 * math.trunc((r) / 3) for i in range(0, 3)]
            for x in block1:
                for y in block2:
                    tmp_list.append([x, y])
            final_block_list.append(tmp_list)
        return final_block_list

    # fil missing numbers in block
    def rnd_fill_blocks(self, grid, block_list):
        for block in block_list:
            for box in block:
                if grid[box[0], box[1]] == 0:
                    current_block = grid[block[0][0]:(block[-1][0] + 1),
                                         block[0][1]:(block[-1][1] + 1)]
                    grid[box[0], box[1]] = choice(
                        [i for i in range(1, 10) if i not in current_block])
        return grid

    # sum of numbers in block
    def block_sum(self, grid, block):
        sum = 0
        for box in block:
            sum += grid[box[0], box[1]]
        return sum

    # choose two random boxes in block
    def rnd_block_boxes(self, block):
        while True:
            first_box = random.choice(block)
            second_box = choice([box for box in block if box is not first_box])

            if not (self.is_def(first_box)) and not (self.is_def(second_box)):
                return ([first_box, second_box])

    # switch two values in box
    def flip_boxes(self, tmp_grid, boxes):
        proposed_grid = np.copy(tmp_grid)
        place_holder = proposed_grid[boxes[0][0], boxes[0][1]]
        proposed_grid[boxes[0][0], boxes[0][1]
                      ] = proposed_grid[boxes[1][0], boxes[1][1]]
        proposed_grid[boxes[1][0], boxes[1][1]] = place_holder
        return proposed_grid

    # generate random state of whole grid
    def get_proposed_state(self, tmp_grid, block_list):
        # condition to handle boxes with only one empty box
        while True:
            rnd_block = random.choice(block_list)
            if self.number_of_def(rnd_block) < 8:
                break

        boxes = self.rnd_block_boxes(rnd_block)
        proposed_grid = self.flip_boxes(tmp_grid, boxes)
        return ([proposed_grid, boxes])

    # number of default values in block
    def number_of_def(self, rnd_block):
        i = 0
        for x in rnd_block:
            if self.is_def(x):
                i += 1
        print(i)
        return i

    # return if value is default or not
    def is_def(self, indexes):
        return bool(self.def_grid[indexes[0]][indexes[1]])

    # choose new state
    def get_new_state(self, current_grid, block_list, sigma):
        proposal = self.get_proposed_state(current_grid, block_list)
        new_grid = proposal[0]
        boxes_to_check = proposal[1]
        current_cost = (self.get_row_column_error(
            boxes_to_check[0][0], boxes_to_check[0][1], current_grid)
            + self.get_row_column_error(
            boxes_to_check[1][0], boxes_to_check[1][1], current_grid)
        )
        new_cost = self.get_row_column_error(
            boxes_to_check[0][0], boxes_to_check[0][1], new_grid)
        + self.get_row_column_error(
            boxes_to_check[1][0],  boxes_to_check[1][1], new_grid)

        cost_diff = new_cost - current_cost
        rho = math.exp(-cost_diff / sigma)

        if (np.random.uniform(1, 0, 1) < rho):
            return ([new_grid, cost_diff])

        return ([current_grid, 0])

    # get number of iterations needed
    def get_iterations_number(self):
        iteration_number = 0
        for i in range(0, 9):
            for j in range(0, 9):
                if self.is_def([i, j]):
                    iteration_number += 1

        return iteration_number

    # get number of initial sigma variable
    def get_initial_sigma(self, grid, block_list):
        diff_list = []
        tmp_grid = grid
        for i in range(1, 10):
            tmp_grid = self.get_proposed_state(tmp_grid, block_list)[0]
            diff_list.append(self.get_error_number(tmp_grid))

        return (statistics.pstdev(diff_list))
