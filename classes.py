from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, window):
        self.window = window
        self.x_one = None
        self.x_two = None
        self.y_one = None
        self.y_two = None
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
    
    def draw(self, x1, x2, y1, y2, fill_color):
        self.x_one = x1
        self.x_two = x2
        self.y_one = y1
        self.y_two = y2
        if self.has_left_wall:
            point1 = Point(self.x_one, self.y_one)
            point2 = Point(self.x_one, self.y_two)
            line = Line(point1, point2)
            self.window.draw_line(line, fill_color)
        if self.has_right_wall:
            point1 = Point(self.x_two, self.y_one)
            point2 = Point(self.x_two, self.y_two)
            line = Line(point1, point2)
            self.window.draw_line(line, fill_color)
        if self.has_top_wall:
            point1 = Point(self.x_one, self.y_one)
            point2 = Point(self.x_two, self.y_one)
            line = Line(point1, point2)
            self.window.draw_line(line, fill_color)
        if self.has_bottom_wall:
            point1 = Point(self.x_one, self.y_two)
            point2 = Point(self.x_two, self.y_two)
            line = Line(point1, point2)
            self.window.draw_line(line, fill_color)

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
        self.window.draw_line(line, fill_color)