import random
from random import choice
import numpy as np
import math
import statistics


class SudokuSolver:
    def __init__(self, def_grid):
        self.def_grid = def_grid
        self.grid = np.copy(self.def_grid)

    # Cost Function
    def get_errors_number(self, grid):
        final_error = 0
        for i in range(0, 9):
            final_error += self.get_row_column_errors(i, i, grid)
        return final_error

    def get_row_column_errors(self, row, column, grid):
        row_column_error = (
            9 - len(np.unique(grid[:, column]))) + (9 - len(np.unique(grid[row, :])))
        return row_column_error

    def get_list_of_blocks(self):
        final_list_of_blocks = []
        for r in range(0, 9):
            tmp_list = []
            first_block = [i + 3 * ((r) % 3) for i in range(0, 3)]
            second_block = [i + 3 * math.trunc((r) / 3) for i in range(0, 3)]
            for x in first_block:
                for y in second_block:
                    tmp_list.append([x, y])
            final_list_of_blocks.append(tmp_list)
        return final_list_of_blocks

    def rnd_fill(self, grid, list_of_blocks):
        for block in list_of_blocks:
            for box in block:
                if grid[box[0], box[1]] == 0:
                    curr_block = grid[block[0][0]:(
                        block[-1][0] + 1), block[0][1]:(block[-1][1] + 1)]
                    grid[box[0], box[1]] = choice(
                        [i for i in range(1, 10) if i not in curr_block])
        return grid

    def get_block_sum(self, grid, block):
        final_sum = 0
        for box in block:
            final_sum += grid[box[0], box[1]]
        return final_sum

    def get_two_rnd_boxes(self,  block):
        while True:
            first_box = random.choice(block)
            second_box = choice([box for box in block if box is not first_box])

            if not (self.is_def(first_box, )) and not (self.is_def(second_box)):
                return ([first_box, second_box])

    def flip_boxes(self, grid, boxes_to_flip):
        proposed_sudoku = np.copy(grid)
        place_holder = proposed_sudoku[boxes_to_flip[0][0], boxes_to_flip[0][1]]
        proposed_sudoku[boxes_to_flip[0][0], boxes_to_flip[0][1]
                       ] = proposed_sudoku[boxes_to_flip[1][0], boxes_to_flip[1][1]]
        proposed_sudoku[boxes_to_flip[1][0], boxes_to_flip[1][1]] = place_holder
        return proposed_sudoku

    def get_proposed_state(self, grid,  list_of_blocks):

        while True:
            random_block = random.choice(list_of_blocks)
            if self.number_of_def(random_block) < 8:
                break

        boxes_to_flip = self.get_two_rnd_boxes(random_block)
        proposed_sudoku = self.flip_boxes(grid, boxes_to_flip)
        return ([proposed_sudoku, boxes_to_flip])

    def number_of_def(self, random_block):
        i = 0
        for x in random_block:
            if self.is_def(x, ):
                i += 1
        print(i)
        return i

    def is_def(self, indexes):
        return bool(self.def_grid[indexes[0]][indexes[1]])

    def choose_new_state(self, current_grid,  list_of_blocks, sigma):
        proposal = self.get_proposed_state(current_grid,  list_of_blocks)
        new_grid = proposal[0]
        boxes_to_check = proposal[1]
        curr_cost = self.get_row_column_errors(boxes_to_check[0][0], boxes_to_check[0][1],
                                                            current_grid) + self.get_row_column_errors(boxes_to_check[1][0],
                                                                                                                  boxes_to_check[1][1],
                                                                                                                  current_grid)
        new_cost = self.get_row_column_errors(boxes_to_check[0][0], boxes_to_check[0][1],
                                                        new_grid) + self.get_row_column_errors(boxes_to_check[1][0],
                                                                                                          boxes_to_check[1][1],
                                                                                                          new_grid)
        cost_diff = new_cost - curr_cost
        rho = math.exp(-cost_diff / sigma)
        if (np.random.uniform(1, 0, 1) < rho):
            return ([new_grid, cost_diff])
        return ([current_grid, 0])

    def get_itteration_number(self):
        itter_number = 0
        for i in range(0, 9):
            for j in range(0, 9):
                if self.is_def([i, j], ):
                    itter_number += 1
        return itter_number

    def get_initial_sigma(self, grid, list_of_blocks):
        diff_list = []
        tmp_grid = grid
        for i in range(1, 10):
            tmp_grid = self.get_proposed_state(tmp_grid,  list_of_blocks)[0]
            diff_list.append(self.get_errors_number(tmp_grid))
        return (statistics.pstdev(diff_list))

    def solve(self):

        sol_found = 0
        while (sol_found == 0):
            print("start")
            decrease_fact = 0.99
            stuck_count = 0
            list_of_blocks = self.get_list_of_blocks()
            tmp_grid = self.rnd_fill(self.grid, list_of_blocks)
            sigma = self.get_initial_sigma(self.grid, list_of_blocks)
            score = self.get_errors_number(tmp_grid)
            itterations = self.get_itteration_number()
            if score <= 0:
                sol_found = 1

            while sol_found == 0:

                prev_score = score
                for i in range(0, itterations):
                    new_state = self.choose_new_state(
                        tmp_grid,  list_of_blocks, sigma)
                    tmp_grid = new_state[0]
                    score_diff = new_state[1]
                    score += score_diff
                    print(score)
                    if score <= 0:
                        sol_found = 1
                        break

                sigma *= decrease_fact
                if score <= 0:
                    sol_found = 1
                    break
                if score >= prev_score:
                    stuck_count += 1
                else:
                    stuck_count = 0
                if (stuck_count > 80):
                    sigma += 2
                if (self.get_errors_number(tmp_grid) == 0):
                    break

        return (tmp_grid)
