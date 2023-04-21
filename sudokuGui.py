import pygame

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


class SudokuGui:
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 600))
        self.quit = pygame.QUIT
        self.key = pygame.KEYDOWN
        self.key_d = pygame.K_d
        self.key_s = pygame.K_s

    @staticmethod
    def display_update():
        pygame.display.update()

    # Function to draw required lines for making Sudoku grid
    def draw(self, grid, def_grid):
        # Draw the lines
        for i in range(9):
            for j in range(9):
                if def_grid[i][j] != 0:
                    # Fill blue color in already numbered grid
                    pygame.draw.rect(self.screen, (0, 200, 255),
                                     (j * DIFF + THICK_PAD, i * DIFF + THICK_PAD, DIFF + 1, DIFF + 1))

                if grid[i][j] != 0:
                    # Fill grid with default numbers specified
                    text1 = FONT1.render(str(grid[i][j]), 1, (0, 0, 0))
                    self.screen.blit(text1, (j * DIFF + 6 * THICK_PAD, i * DIFF + 2 * THICK_PAD))

        # Draw lines horizontally and verticallyto form grid
        for i in range(10):
            if i % 3 == 0:
                thick = BORDER_THICK
            else:
                thick = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * DIFF + THICK_PAD), (500, i * DIFF + THICK_PAD), thick)
            pygame.draw.line(self.screen, (0, 0, 0), (i * DIFF + THICK_PAD, 0), (i * DIFF + THICK_PAD, 500 - THICK_PAD),
                             thick)

    # Display instruction for the game
    def instruction(self):
        text1 = FONT2.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY", 1, (0, 0, 0))
        text2 = FONT2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
        self.screen.blit(text1, (20, 520))
        self.screen.blit(text2, (20, 540))

    # Display options when solved
    def result(self):
        text1 = FONT1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
        self.screen.blit(text1, (20, 570))
