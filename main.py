from classes import Window, Point, Line, Cell, Maze

def main():
    win = Window(800, 600)
    margin = 10
    rows = 40
    cols = 40
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - (margin * 2)) / cols
    cell_size_y = (screen_y - (margin *2)) / rows
    maze = Maze(margin, margin, rows, cols, cell_size_x, cell_size_y, win)
    print("New Maze Generated")
    solvable = maze.solve()
    if not solvable:
        print("Maze cannot be solved.")
    else:
        print("Maze solved!")
    win.wait_for_close()

main()