-   How do we apply constraint propagation to solve the naked twins problem?

 

The naked twins constraint is evident when two boxes in a unit share an
identical

2 digit value. This means that both boxes have exactly the same possibilities

for their solution. So if A1=’12’ and C3=’12’ then A1 must be 1 or 2 and C3 must
be 1 or 2. The implication of this is that no other box in their shared unit can
be 1 or 2 (in this the shared unit is a sub-square). This means we can remove
digits 1 and 2 from all other boxes in their sub-square unit.  This is a general
principle that can be applied across the puzzle.

 

We have employed this method in the code. It is applied iteratively along with
the logic to perform elimination of known values and only choice. Each iteration
produces a better solution. This continues until the puzzle is solved or the
solution stops improving. By employing naked twins we can solve puzzles that
would be insoluble by elimination and only choice alone and speed up the time to
produce a solution considerably.

 

If not solved then once the best solution possible has been arrived at via these
methods the puzzle is passed on for search processing.

 

-   How do we apply constraint propagation to solve the diagonal sudoku problem?

 

In a diagonal solution type problem we add a further constraint whereby each

digit 1-9 may only appear once in each of the main diagonals.

 

We have added this constraint to the code meaning that it attempts to satisfy
the constraint. The logic is applied iteratively along with elimination of known
values, naked twins and only choice. Each solution should be better than the
last. If not solved the best solution possible has been arrived at via these
methods and the puzzle is passed on for search processing.

 
