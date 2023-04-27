import pygame
import numpy as np
from src.solver import Solver
from sudoku import Sudoku as SudokuGen

# inicialisation of font
pygame.font.init()
# title
pygame.display.set_caption("SUDOKU SOLVER USING SIMULATED ANNEALING")

# constants
BORDER_THICK = 7
THICK_PAD = BORDER_THICK / 2
DIFF = (500 - BORDER_THICK) / 9

# load fonts 
FONT1 = pygame.font.SysFont("Arial", 40)
FONT2 = pygame.font.SysFont("Arial", 20)


#function drawing grid and numbers
def draw(grid, def_grid, screen):
    for i in range(9):
        for j in range(9):
            # drawing blue squares over default values
            if def_grid[i][j]:
                pygame.draw.rect(screen, (0, 200, 255),
                                 (j * DIFF + THICK_PAD, i * DIFF + THICK_PAD, DIFF + 1, DIFF + 1))
            #drawing values
            if grid[i][j]:
                text1 = FONT1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (j * DIFF + 6 * THICK_PAD, i * DIFF + 2 * THICK_PAD))

    # drawing lines and frame
    for i in range(10):
        if i % 3 == 0:
            thick = BORDER_THICK
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * DIFF + THICK_PAD), (500, i * DIFF + THICK_PAD), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * DIFF + THICK_PAD, 0), (i * DIFF + THICK_PAD, 500 - THICK_PAD),
                         thick)



#instruction banner
def instruction(screen):
    text1 = FONT2.render("PRESS R TO RESET TO DEFAULT", 1, (0, 0, 0))
    text2 = FONT2.render("N TO GENERATE NEW SUDOKU", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))
#result banner
def result(screen):
    text1 = FONT2.render("FINISHED PRESS N or R", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
#function converting format of generated sudoku
def generate_new(gen):
    x = np.array(gen.difficulty(0.5).board)
    return np.where(x == None, 0, x)


if __name__ == "__main__":
    #setting screen
    screen = pygame.display.set_mode((500, 600))
    sudoku_gen = SudokuGen(3)

 
    def_grid = generate_new(sudoku_gen)
    sudokuSolver = Solver(def_grid)


    #run condition variable
    run = True
    #result condition variable
    rs = 0

    # game loop
    while run:
        #blank screen
        screen.fill((255, 255, 255))

        #event handler
        for event in pygame.event.get():
            #quiting window
            if event.type == pygame.QUIT:
                run = False
            #key handler
            if event.type == pygame.KEYDOWN:
                #key R - reset
                if event.key == pygame.K_r:
                    rs = 0
                    sudokuSolver.grid = np.copy(sudokuSolver.def_grid)
                #key N - new game
                if event.key == pygame.K_n:
                    sudokuSolver.def_grid = generate_new(sudoku_gen)
                    sudokuSolver.grid = np.copy(sudokuSolver.def_grid)
                    rs = 0
                #key S - solve
                if event.key == pygame.K_s:
                    sudokuSolver.grid = sudokuSolver.solve()
                    rs = 1
        if rs == 1:
            result(screen)
        else: 
            instruction(screen)

        draw(sudokuSolver.grid,sudokuSolver.def_grid,screen)

        # update window
        pygame.display.update()

    # quit
    pygame.quit()