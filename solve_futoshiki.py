import sys


def read_order(text):
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        return int(line)
    print("The file does not contain an order.")
    return None


def read_position(token, order):
    parts = token.split(",")
    if len(parts) != 2 or parts[0].isdigit() == False or parts[1].isdigit() == False:
        print("A cell on a sign line must look like 1,2")
        return None
    row = int(parts[0])
    column = int(parts[1])
    if row < 1 or row > order or column < 1 or column > order:
        print("A cell position must be from 1 to", order)
        return None
    return [row, column]


def share_a_side(first, second):
    row_gap = first[0] - second[0]
    if row_gap < 0:
        row_gap = -row_gap
    column_gap = first[1] - second[1]
    if column_gap < 0:
        column_gap = -column_gap
    if row_gap + column_gap == 1:
        return True
    return False


def read_sign_line(line, order, inequalities):
    tokens = line.split()
    sign = ""
    cell = None
    cell_needs_sign = False
    for token in tokens:
        if token == "<" or token == ">":
            if cell is None or sign != "":
                print("A sign must sit between two cells.")
                return None
            sign = token
            cell_needs_sign = False
        else:
            position = read_position(token, order)
            if position is None:
                return None
            if sign != "":
                if share_a_side(cell, position) == False:
                    print("A sign must join two cells that share a side.")
                    return None
                inequalities.append([cell[0], cell[1], sign, position[0], position[1]])
                sign = ""
                cell = position
                cell_needs_sign = False
            else:
                if cell_needs_sign == True:
                    print("A sign must sit between two cells.")
                    return None
                cell = position
                cell_needs_sign = True
    if sign != "" or cell_needs_sign == True:
        print("A sign must sit between two cells.")
        return None
    return inequalities


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
        if len(rows) == order:
            if read_sign_line(line, order, inequalities) is None:
                return None
            continue
        row_number = row_number + 1
        tokens = line.split()
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


def variable_number(row, column, value, order):
    return ((row - 1) * order + (column - 1)) * order + value


def cell_has_a_number(order):
    clauses = []
    for row in range(1, order + 1):
        for column in range(1, order + 1):
            clause = []
            for value in range(1, order + 1):
                clause.append(variable_number(row, column, value, order))
            clause.append(0)
            clauses.append(clause)
    return clauses


def cell_has_at_most_one(order):
    clauses = []
    for row in range(1, order + 1):
        for column in range(1, order + 1):
            for first in range(1, order + 1):
                for second in range(first + 1, order + 1):
                    clause = []
                    clause.append(-variable_number(row, column, first, order))
                    clause.append(-variable_number(row, column, second, order))
                    clause.append(0)
                    clauses.append(clause)
    return clauses


def row_has_a_number(order):
    clauses = []
    for row in range(1, order + 1):
        for value in range(1, order + 1):
            clause = []
            for column in range(1, order + 1):
                clause.append(variable_number(row, column, value, order))
            clause.append(0)
            clauses.append(clause)
    return clauses


def row_has_at_most_one(order):
    clauses = []
    for row in range(1, order + 1):
        for value in range(1, order + 1):
            for first in range(1, order + 1):
                for second in range(first + 1, order + 1):
                    clause = []
                    clause.append(-variable_number(row, first, value, order))
                    clause.append(-variable_number(row, second, value, order))
                    clause.append(0)
                    clauses.append(clause)
    return clauses


def column_has_a_number(order):
    clauses = []
    for column in range(1, order + 1):
        for value in range(1, order + 1):
            clause = []
            for row in range(1, order + 1):
                clause.append(variable_number(row, column, value, order))
            clause.append(0)
            clauses.append(clause)
    return clauses


def column_has_at_most_one(order):
    clauses = []
    for column in range(1, order + 1):
        for value in range(1, order + 1):
            for first in range(1, order + 1):
                for second in range(first + 1, order + 1):
                    clause = []
                    clause.append(-variable_number(first, column, value, order))
                    clause.append(-variable_number(second, column, value, order))
                    clause.append(0)
                    clauses.append(clause)
    return clauses


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
    print("Row 1 column 1 value 1 is variable", variable_number(1, 1, 1, order))
    print("At least one number")
    for clause in cell_has_a_number(order):
        print(clause)
    at_most_one = cell_has_at_most_one(order)
    print("At most one number, clause count", len(at_most_one))
    print("At most one number, row 3 column 4")
    low = variable_number(3, 4, 1, order)
    high = variable_number(3, 4, order, order)
    for clause in at_most_one:
        number = -clause[0]
        if number >= low and number <= high:
            print(clause)
    print("Each number appears in a row")
    for clause in row_has_a_number(order):
        print(clause)
    row_once = row_has_at_most_one(order)
    print("A number appears at most once in a row, clause count", len(row_once))
    print("Row 1, value 1")
    targets = []
    for column in range(1, order + 1):
        targets.append(variable_number(1, column, 1, order))
    for clause in row_once:
        number = -clause[0]
        found = False
        for target in targets:
            if number == target:
                found = True
        if found == True:
            print(clause)
    print("Each number appears in a column")
    for clause in column_has_a_number(order):
        print(clause)
    column_once = column_has_at_most_one(order)
    print("A number appears at most once in a column, clause count", len(column_once))
    print("Column 1, value 1")
    targets = []
    for row in range(1, order + 1):
        targets.append(variable_number(row, 1, 1, order))
    for clause in column_once:
        number = -clause[0]
        found = False
        for target in targets:
            if number == target:
                found = True
        if found == True:
            print(clause)


if __name__ == "__main__":
    main()
