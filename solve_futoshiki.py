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


def main():
    path = sys.argv[1]
    with open(path) as handle:
        text = handle.read()
    order = read_order(text)
    if order is None:
        return
    grid = read_grid(text, order)
    if grid is None:
        return
    print("Futoshiki order", order)
    for row in grid:
        print(row)


if __name__ == "__main__":
    main()
