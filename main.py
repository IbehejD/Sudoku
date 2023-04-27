import pygame
from src.solver import *
from sudoku import Sudoku

# initialise the pygame font
pygame.font.init()
# Title and Icon
pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
# Total window

BORDER_THICK = 7
THICK_PAD = BORDER_THICK / 2
DIFF = (500 - BORDER_THICK) / 9

# Load test fonts for future use
FONT1 = pygame.font.SysFont("Arial", 40)
FONT2 = pygame.font.SysFont("Arial", 20)

# Function to draw required lines for making Sudoku grid

def draw(grid, def_grid, screen):
    # Draw the lines
    for i in range(9):
        for j in range(9):
            if def_grid[i][j] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (0, 200, 255),
                                 (j * DIFF + THICK_PAD, i * DIFF + THICK_PAD, DIFF + 1, DIFF + 1))

            if grid[i][j] != 0:
                # Fill grid with default numbers specified
                text1 = FONT1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (j * DIFF + 6 * THICK_PAD, i * DIFF + 2 * THICK_PAD))

    # Draw lines horizontally and verticallyto form grid
    for i in range(10):
        if i % 3 == 0:
            thick = BORDER_THICK
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * DIFF + THICK_PAD), (500, i * DIFF + THICK_PAD), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * DIFF + THICK_PAD, 0), (i * DIFF + THICK_PAD, 500 - THICK_PAD),
                         thick)

# Display instruction for the game

def instruction(screen):
    text1 = FONT2.render("PRESS D TO RESET TO DEFAULT", 1, (0, 0, 0))
    text2 = FONT2.render("R TO GENERATE NEW SUDOKU", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))

# Display options when solved

def result(screen):
    text1 = FONT1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))

if __name__ == "__main__":

    screen = pygame.display.set_mode((500, 600))
    sudoku_gen = Sudoku(3)
    def_grid = generate_new(sudoku_gen)
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
                    grid = solveSudoku(grid, def_grid)
                    rs == 1
        if rs == 1:
            result(screen)

        draw(grid, def_grid, screen)
        instruction(screen)
        # Update window
        pygame.display.update()

    # Quit pygame window
    pygame.quit()