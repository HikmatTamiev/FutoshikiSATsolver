import os
import subprocess
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


def given_number(grid, order):
    clauses = []
    for row in range(1, order + 1):
        for column in range(1, order + 1):
            number = grid[row - 1][column - 1]
            if number == None:
                continue
            clause = []
            clause.append(variable_number(row, column, number, order))
            clause.append(0)
            clauses.append(clause)
    return clauses


def sign_clauses(inequalities, order):
    clauses = []
    for item in inequalities:
        left_row = item[0]
        left_column = item[1]
        sign = item[2]
        right_row = item[3]
        right_column = item[4]
        for left_value in range(1, order + 1):
            for right_value in range(1, order + 1):
                broken = False
                if sign == ">" and left_value <= right_value:
                    broken = True
                if sign == "<" and left_value >= right_value:
                    broken = True
                if broken == True:
                    clause = []
                    clause.append(-variable_number(left_row, left_column, left_value, order))
                    clause.append(-variable_number(right_row, right_column, right_value, order))
                    clause.append(0)
                    clauses.append(clause)
    return clauses


def all_clauses(grid, inequalities, order):
    clauses = []
    for clause in cell_has_a_number(order):
        clauses.append(clause)
    for clause in cell_has_at_most_one(order):
        clauses.append(clause)
    for clause in row_has_a_number(order):
        clauses.append(clause)
    for clause in row_has_at_most_one(order):
        clauses.append(clause)
    for clause in column_has_a_number(order):
        clauses.append(clause)
    for clause in column_has_at_most_one(order):
        clauses.append(clause)
    for clause in given_number(grid, order):
        clauses.append(clause)
    for clause in sign_clauses(inequalities, order):
        clauses.append(clause)
    return clauses


def write_cnf(path, order, clauses):
    variable_count = order * order * order
    clause_count = len(clauses)
    with open(path, "w") as handle:
        handle.write("p cnf " + str(variable_count) + " " + str(clause_count) + "\n")
        for clause in clauses:
            for number in clause:
                handle.write(str(number) + " ")
            handle.write("\n")
    print("Wrote", path)
    print(variable_count, "variables")
    print(clause_count, "clauses")


def run_glucose(cnf_path, glucose_path):
    if os.path.isfile(glucose_path) == False:
        print("Glucose was not found at", glucose_path)
        return None
    completed = subprocess.run([glucose_path, "-model", cnf_path], capture_output=True, text=True)
    if completed.returncode == 10:
        print("SAT")
    elif completed.returncode == 20:
        print("UNSAT")
    else:
        print("Glucose stopped with code", completed.returncode)
    return completed.stdout


def grid_from_model(output, order):
    true_numbers = []
    for line in output.splitlines():
        if line.startswith("v "):
            for token in line.split():
                if token == "v":
                    continue
                number = int(token)
                if number > 0:
                    true_numbers.append(number)
    if len(true_numbers) == 0:
        return None
    solved = []
    for row in range(1, order + 1):
        solved_row = []
        for column in range(1, order + 1):
            for value in range(1, order + 1):
                if variable_number(row, column, value, order) in true_numbers:
                    solved_row.append(value)
        solved.append(solved_row)
    return solved


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
    clauses = all_clauses(grid, inequalities, order)
    write_cnf("futoshiki.cnf", order, clauses)
    output = run_glucose("futoshiki.cnf", "glucose.exe")
    if output is None:
        return
    solved = grid_from_model(output, order)
    if solved is None:
        print("No valid solution exists.")
        return
    print("Solved grid")
    for solved_row in solved:
        line = ""
        for value in solved_row:
            line = line + str(value) + " "
        print(line)


if __name__ == "__main__":
    main()
