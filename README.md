# FutoshikiSATsolver
## 1. Problem Description

I wrote a Python program that solves Futoshiki by turning the puzzle into a SAT problem and solving it with the Glucose 4.2.1 SAT solver.

In Futoshiki:
- The grid is n × n, and each cell holds a number from 1 to n.
- Each row and each column must contain the numbers 1…n exactly once.
- Some cells already have a number (givens), and those stay.
- Some neighboring cells have a `<` or `>` sign between them. The sign can be between two cells in a row, or between a cell and the cell below it. The number on the small side of the sign must be smaller.

There are no boxes like in Sudoku.

My program creates a CNF file, runs Glucose, and then prints SAT or UNSAT, the solver time, and the solved grid.

---

## 2. What Each Function Does

### read_order(text)
This reads the first number in the puzzle file, which is the size n of the grid.
Comment lines starting with `#` and empty lines are skipped.

---

### read_grid(text, order)
This reads the n grid rows. A number is a given, a `.` is an empty cell, and a `<` or `>` between two cells is a sign.
After the grid, it sends every remaining line to `read_sign_line`.
It returns the grid and the list of signs, or prints an error message if the file is wrong.

---

### read_sign_line(line, order, inequalities)
This reads a line written after the grid, like `1,4 < 2,4`.
I need these lines for signs between a cell and the cell below it, because those cells are on different rows.

---

### read_position(token, order) and share_a_side(first, second)
`read_position` turns a text like `1,4` into a row and a column and checks they are inside the grid.
`share_a_side` checks that the two cells of a sign are next to each other.

---

### variable_number(row, column, value, order)
This function turns a triple (row, column, value) into a single SAT variable number.
SAT solvers only understand variables like 1, 2, 3, so I convert each (row, column, value) into one integer.

---

### The clause functions
Each of these makes the clauses for one rule:
- `cell_has_a_number`: each cell has at least one value.
- `cell_has_at_most_one`: each cell has at most one value.
- `row_has_a_number` and `row_has_at_most_one`: each number is exactly once in every row.
- `column_has_a_number` and `column_has_at_most_one`: each number is exactly once in every column.
- `given_number`: the given numbers stay in their cells.
- `sign_clauses`: every `<` and `>` sign holds.

`all_clauses` puts all of them into one big list.

---

### write_cnf(path, order, clauses)
This writes the SAT instance in *DIMACS CNF format* to `futoshiki.cnf`.
The Glucose solver can then read this file.

---

### run_glucose(cnf_path, glucose_path)
This starts Glucose with the CNF file, prints SAT or UNSAT from Glucose's exit code (10 or 20), and returns Glucose's output text.

---

### grid_from_model(output, order)
This reads the SAT solver output, extracts all *true* variables, and rebuilds the solved grid.
If Glucose says UNSAT, there are no true variables, and the program prints "No valid solution exists."

---

### read_cpu_time(output)
This reads the solving time from Glucose's `c CPU time` line.

---

### main()
This is the main part of the script.
Here I:
- read the puzzle file,
- generate the CNF clauses,
- write the CNF file,
- run Glucose,
- and print the time and the final solution.

---

## 3. CNF Encoding (How I Translate the Puzzle)

### Variables
I use SAT variables of the form:

```text
X(r, c, v) = the cell at row r and column c contains value v
```

Mapped into a single integer with:

```text
variable_number(r, c, v) = ((r - 1) * n + (c - 1)) * n + v
```

Rows, columns, and values start at 1, so the variable numbers go from 1 to n³.

### Constraints
- *Cell:*
  each cell has at least one value and at most one value.
- *Rows:*
  each number 1…n appears exactly once in every row.
- *Columns:*
  each number appears exactly once in every column.
- *Givens:*
  a given number k in a cell becomes a clause with only that one variable.
- *Signs:*
  for A < B, every pair of values (a, b) with a ≥ b becomes a forbidden clause `-A_a -B_b`.
  For A > B, every pair with a ≤ b is forbidden.

"At most one" is written as a forbidden clause for every pair of values. This encoding is simple but becomes very large for big puzzles.

---

## 4. Puzzle File Format

```text
5
. . . > . .
. . 5 > . > 1
1 < . . . > .
. > 1 < . 5 3
2 . > 1 . < .
1,4 < 2,4
1,5 > 2,5
```

- The first line is n.
- Then n rows. A number is a given, `.` is empty, and `<` or `>` between two cells is a sign.
- After the grid, each line holds signs written as `row,column < row,column`. I use these for signs between a cell and the cell below it.
- Everything must be separated by spaces.

---

## 5. How to Run the Script

1. Build Glucose 4.2.1 from https://github.com/audemard/glucose/releases/tag/4.2.1.
2. Put `glucose.exe` in the project folder.
3. Run:

```text
python solve_futoshiki.py instances/easy.txt
```

The program:
- creates `futoshiki.cnf`,
- calls Glucose,
- prints SAT or UNSAT, the solver time, and the solved grid or "No valid solution exists."

---

## 6. Puzzle Instances I Included

All puzzle files are in the `instances` folder.

- *easy.txt:*
  A small 4×4 puzzle with exactly one solution. I created it myself so it is easy to check by hand. It uses both row signs and column signs.

- *unsat.txt:*
  A small 4×4 puzzle with no solution. Row 1 has `<` between every cell, so it must be 1 2 3 4. The last line says row 1 column 1 is bigger than the cell below it, which is impossible because that cell is 1.

---

## 7. Experiment Results

| Puzzle | Size | Result | Time |
|--------|------|--------|------|
| easy.txt | 4×4 | SAT | 0.016 s |
| unsat.txt | 4×4 | UNSAT | 0.013 s |
| Generated (slowest) | 16×16 | SAT | 0.08 s |

The small puzzles work instantly.

The assignment asks for a puzzle that takes at least 10 seconds, but I could not find one. I generated bigger puzzles from a filled solution grid, kept some of the numbers, and added signs that agree with it. I tried sizes up to 16×16 with different amounts of givens and signs. The slowest took about 0.08 seconds. Most of Glucose's time went to reading the CNF file, not searching, because the clauses for rows, columns, and cells let Glucose fill in many cells right away.

---
