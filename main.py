from classes import Window, Point, Line, Cell

def main():
    win = Window(800, 600)
    cell1 = Cell(win)
    cell1.has_left_wall = False
    cell2 = Cell(win)
    cell2.has_bottom_wall = False
    cell1.draw(5, 100, 5, 100, "black")
    cell2.draw(105, 200, 105, 200, "red")
    cell1.draw_move(cell2)
    win.wait_for_close()

main()