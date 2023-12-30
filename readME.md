A chess game that works in the terminal and (hopefully) a working AI.

Day 1:
Wrote function to evaluate material. The calculation for material is based on
the tables in tables.py. Also referenced https://www.chessprogramming.org/Simplified_Evaluation_Function.

Day 2:
Wrote minimax algorithm based on https://www.youtube.com/watch?v=l-hh51ncgDI. The minimax algorithm
becomes extremely slow if you increase depth beyond 3. I'm pretty sure it's an issue of depth, that's
why the AI makes some very weird moves.

To-do: Add alpha-beta pruning and move validation for human users tomorrow.