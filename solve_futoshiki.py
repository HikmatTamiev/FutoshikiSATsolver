import sys


def read_order(text):
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        return int(line)
    print("The file does not contain an order.")
    return None


def read_grid(text, order):
    rows = []
    skipped_order = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        if skipped_order == False:
            skipped_order = True
            continue
        cells = line.split()
        if len(cells) != order:
            print("A grid row must contain", order, "cells.")
            return None
        row = []
        for cell in cells:
            if cell == ".":
                row.append(None)
            elif cell.isdigit():
                number = int(cell)
                if number < 1 or number > order:
                    print("A cell number must be from 1 to", order)
                    return None
                row.append(number)
            else:
                print("A cell must be a number or a dot.")
                return None
        rows.append(row)
        if len(rows) == order:
            return rows
    print("The file does not contain", order, "grid rows.")
    return None


def read_inequalities(text, order):
    inequalities = []
    skipped_order = False
    rows_left = order
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        if skipped_order == False:
            skipped_order = True
            continue
        if rows_left > 0:
            rows_left = rows_left - 1
            continue
        parts = line.split()
        if len(parts) != 5 or (parts[2] != "<" and parts[2] != ">"):
            print("An inequality must look like: 1 2 < 1 3")
            return None
        if parts[0].isdigit() == False or parts[1].isdigit() == False or parts[3].isdigit() == False or parts[4].isdigit() == False:
            print("An inequality's positions must be whole numbers.")
            return None
        left_row = int(parts[0])
        left_column = int(parts[1])
        right_row = int(parts[3])
        right_column = int(parts[4])
        if left_row < 1 or left_row > order or left_column < 1 or left_column > order or right_row < 1 or right_row > order or right_column < 1 or right_column > order:
            print("An inequality's positions must be from 1 to", order)
            return None
        row_gap = left_row - right_row
        if row_gap < 0:
            row_gap = -row_gap
        column_gap = left_column - right_column
        if column_gap < 0:
            column_gap = -column_gap
        if row_gap + column_gap != 1:
            print("An inequality must join two cells that share a side.")
            return None
        inequalities.append([left_row, left_column, parts[2], right_row, right_column])
    return inequalities


def main():
    if len(sys.argv) < 2:
        print("Add the file name: python solve_futoshiki.py instances/grid.txt")
        return
    path = sys.argv[1]
    with open(path) as handle:
        text = handle.read()
    order = read_order(text)
    if order is None:
        return
    grid = read_grid(text, order)
    if grid is None:
        return
    inequalities = read_inequalities(text, order)
    if inequalities is None:
        return
    print("Futoshiki order", order)
    for row in grid:
        print(row)
    print("Inequalities")
    if len(inequalities) == 0:
        print("none")
    for item in inequalities:
        print(item[0], item[1], item[2], item[3], item[4])


if __name__ == "__main__":
    main()
