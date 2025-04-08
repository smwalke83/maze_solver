import unittest
from classes import Maze, Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1.cells), num_cols)
        self.assertEqual(len(m1.cells[0]), num_rows)

    def test_maze_no_cells(self):
        num_cols = 0
        num_rows = 0
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1.cells), num_cols)

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(m1.cells[0][0].has_top_wall, False)
        self.assertEqual(m1.cells[num_cols - 1][num_rows - 1].has_bottom_wall, False)

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(m1.cells[0][0].visited, False)
        self.assertEqual(m1.cells[1][1].visited, False)
        self.assertEqual(m1.cells[num_cols - 1][num_rows - 1].visited, False)

if __name__ == "__main__":
    unittest.main()