# MasyuSolver
This is a builder and solver for Masyu puzzles.  It supports puzzles ranging
from 5x5 to 15x15.

As the user builds a puzzle board, the solver attempts to solve the puzzle in
realtime, using the basic puzzle solving rules.  But if the basic rules are not
enough to solve the puzzle, then the user can ask that the 'brute-force' solver
be used.

Brute-force solving involves looking for places in the puzzle where making a 
guess has a high likelihood of helping the solver to solve the puzzle.

The solver has a feature called 'smart placement mode' .. this tends to 
slow down the solver, but after each change made to the puzzle board (by
the user), it analyzes the board, and disables any cells into which the
currently selected item (a black circle or a white circle) cannot legally
be placed; this prevents the user from building an invalid puzzle.  By
disabling the cells (stippling them), the user can immediately see where
the currently selected item can and cannot be placed.

If you turn off 'smart placement mode', then the solver runs significantly
faster .. but the user will not be shown which cells are disabled. However,
if the user tries to place an item into a cell, and it turns out to be an
invalid location, the user will be notified and the change will not be
allowed.  It also prevents the user from building an invalid puzzle!

Puzzle boards can be saved to a file, and then loaded again later.
