from tkinter import Tk, BOTH, Canvas
import time, random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Runner")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg = "white", height = height, width = width)
        self.__canvas.pack()
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed.")
        
    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, x_coordinate, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate

class Line():
    def __init__(self, point_one, point_two):
        self.point_one = point_one
        self.point_two = point_two

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point_one.x, self.point_one.y, self.point_two.x, self.point_two.y, fill = fill_color, width = 2)

class Cell():
    def __init__(self, win = None):
        self.win = win
        self.x_one = None
        self.x_two = None
        self.y_one = None
        self.y_two = None
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
    
    def draw(self, x1, x2, y1, y2, fill_color):
        self.x_one = x1
        self.x_two = x2
        self.y_one = y1
        self.y_two = y2
        if self.has_left_wall:
            point1 = Point(self.x_one, self.y_one)
            point2 = Point(self.x_one, self.y_two)
            line = Line(point1, point2)
            self.win.draw_line(line, fill_color)
        else:
            point1 = Point(self.x_one, self.y_one)
            point2 = Point(self.x_one, self.y_two)
            line = Line(point1, point2)
            self.win.draw_line(line, "white")
        if self.has_right_wall:
            point1 = Point(self.x_two, self.y_one)
            point2 = Point(self.x_two, self.y_two)
            line = Line(point1, point2)
            self.win.draw_line(line, fill_color)
        else:
            point1 = Point(self.x_two, self.y_one)
            point2 = Point(self.x_two, self.y_two)
            line = Line(point1, point2)
            self.win.draw_line(line, "white")
        if self.has_top_wall:
            point1 = Point(self.x_one, self.y_one)
            point2 = Point(self.x_two, self.y_one)
            line = Line(point1, point2)
            self.win.draw_line(line, fill_color)
        else:
            point1 = Point(self.x_one, self.y_one)
            point2 = Point(self.x_two, self.y_one)
            line = Line(point1, point2)
            self.win.draw_line(line, "white")
        if self.has_bottom_wall:
            point1 = Point(self.x_one, self.y_two)
            point2 = Point(self.x_two, self.y_two)
            line = Line(point1, point2)
            self.win.draw_line(line, fill_color)
        else:
            point1 = Point(self.x_one, self.y_two)
            point2 = Point(self.x_two, self.y_two)
            line = Line(point1, point2)
            self.win.draw_line(line, "white")

    def draw_move(self, to_cell, undo = False):
        if undo:
            fill_color = "gray"
        else:
            fill_color = "red"
        self.mid_x = (self.x_one + self.x_two)//2
        self.mid_y = (self.y_one + self.y_two)//2
        to_cell.mid_x = (to_cell.x_one + to_cell.x_two)//2
        to_cell.mid_y = (to_cell.y_one + to_cell.y_two)//2
        self.mid_point = Point(self.mid_x, self.mid_y)
        to_cell.mid_point = Point(to_cell.mid_x, to_cell.mid_y)
        line = Line(self.mid_point, to_cell.mid_point)
        self.win.draw_line(line, fill_color)
    
class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            random.seed(seed)
        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        self.reset_cells_visited()
    
    def create_cells(self):
        self.cells = []
        for i in range(0, self.num_cols):
            self.cells.append([])
            for j in range(0, self.num_rows):
                cell = Cell(self.win)
                self.cells[i].append(cell)
                self.draw_cell(i, j)

    def draw_cell(self, i, j):
        if self.win is None:
            return
        x1 = self.x1 + (i * self.cell_size_x)
        y1 = self.y1 + (j * self.cell_size_y)
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, x2, y1, y2, "black")
        self.animate()

    def animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.01)

    def break_entrance_and_exit(self):
        if self.num_rows == 0 or self.num_cols == 0:
            return
        self.cells[0][0].has_top_wall = False
        self.draw_cell(0, 0)
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.draw_cell(self.num_cols - 1, self.num_rows - 1)

    def break_walls_r(self, i, j):
        if self.num_rows == 0 or self.num_cols == 0:
            return
        current_cell = self.cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = []
            if j + 1 < self.num_rows and not self.cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            if j - 1 >= 0 and not self.cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if i + 1 < self.num_cols and not self.cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if i - 1 >= 0 and not self.cells[i-1][j].visited:
                to_visit.append((i - 1, j))
            if len(to_visit) == 0:
                self.draw_cell(i, j)
                return
            new_indexes = to_visit[random.randrange(len(to_visit))]
            new_i = new_indexes[0]
            new_j = new_indexes[1]
            new_cell = self.cells[new_i][new_j]
            if i == new_i:
                if new_j > j:
                    current_cell.has_bottom_wall = False
                    self.draw_cell(i, j)
                    new_cell.has_top_wall = False
                    self.draw_cell(new_i, new_j)
                if new_j < j:
                    current_cell.has_top_wall = False
                    self.draw_cell(i, j)
                    new_cell.has_bottom_wall = False
                    self.draw_cell(new_i, new_j)
            if j == new_j:
                if new_i > i:
                    current_cell.has_right_wall = False
                    self.draw_cell(i, j)
                    new_cell.has_left_wall = False
                    self.draw_cell(new_i, new_j)
                if new_i < i:
                    current_cell.has_left_wall = False
                    self.draw_cell(i, j)
                    new_cell.has_right_wall = False
                    self.draw_cell(new_i, new_j)
            self.break_walls_r(new_i, new_j)

    def reset_cells_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self.solve_r(0, 0)
    
    def solve_r(self, i, j):
        self.animate()
        self.cells[i][j].visited = True
        current_cell = self.cells[i][j]
        if self.cells[i][j] == self.cells[self.num_cols - 1][self.num_rows - 1]:
            return True
        if not current_cell.has_right_wall and i + 1 < self.num_cols and not self.cells[i + 1][j].visited:
            current_cell.draw_move(self.cells[i + 1][j])
            if self.solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(self.cells[i + 1][j], undo = True)
        if not current_cell.has_left_wall and i - 1 >= 0 and not self.cells[i - 1][j].visited:
            current_cell.draw_move(self.cells[i - 1][j])
            if self.solve_r(i - 1, j):
                return True
            else:
                current_cell.draw_move(self.cells[i - 1][j], undo = True)
        if not current_cell.has_bottom_wall and j + 1 < self.num_rows and not self.cells[i][j + 1].visited:
            current_cell.draw_move(self.cells[i][j + 1])
            if self.solve_r(i, j + 1):
                return True
            else:
                current_cell.draw_move(self.cells[i][j + 1], undo = True)
        if not current_cell.has_top_wall and j - 1 >= 0 and not self.cells[i][j - 1].visited:
            current_cell.draw_move(self.cells[i][j - 1])
            if self.solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(self.cells[i][j - 1], undo = True)
        return False


