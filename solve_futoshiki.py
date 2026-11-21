import sys


def read_order(text):
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        return int(line)
    print("The file does not contain an order.")
    return None


def split_sign(token):
    pieces = []
    word = ""
    for character in token:
        if character == "<" or character == ">":
            if word != "":
                pieces.append(word)
                word = ""
            pieces.append(character)
        else:
            word = word + character
    if word != "":
        pieces.append(word)
    return pieces


def read_grid(text, order):
    rows = []
    inequalities = []
    skipped_order = False
    row_number = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        if skipped_order == False:
            skipped_order = True
            continue
        row_number = row_number + 1
        tokens = []
        for token in line.split():
            for piece in split_sign(token):
                tokens.append(piece)
        row = []
        sign = ""
        for token in tokens:
            if token == "<" or token == ">":
                if len(row) == 0 or sign != "":
                    print("A sign must sit between two cells.")
                    return None
                sign = token
            elif token == "." or token.isdigit():
                if token == ".":
                    number = None
                else:
                    number = int(token)
                    if number < 1 or number > order:
                        print("A cell number must be from 1 to", order)
                        return None
                if sign != "":
                    left_column = len(row)
                    right_column = left_column + 1
                    inequalities.append([row_number, left_column, sign, row_number, right_column])
                    sign = ""
                row.append(number)
            else:
                print("A cell must be a number or a dot, and a sign must be < or >.")
                return None
        if sign != "":
            print("A sign must sit between two cells.")
            return None
        if len(row) != order:
            print("A grid row must contain", order, "cells.")
            return None
        rows.append(row)
        if len(rows) == order:
            return [rows, inequalities]
    print("The file does not contain", order, "grid rows.")
    return None


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
    result = read_grid(text, order)
    if result is None:
        return
    grid = result[0]
    inequalities = result[1]
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
