from sudoku import Sudoku
import numpy as np

a = Sudoku(3).difficulty(0.5)
a.show()
b = np.array(a.board)
pass