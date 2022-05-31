# tictactoe
TicTacToe-playing AI using minimax algorithm & alpha-beta pruning.

To use: python runners.py

Done as part of Harvard's CS50AI course (https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/).
Runners.py (for GUI) was implemented by the course instructors. 
Function list of tictactoe.py was provided by course instructors. Functions were implemented by me.

A few changes over original implementation:
1. Edited to allow for flexible sizing of board (i.e. n x n instead of hard-coded 3 x 3)
     - To modify: Change BOARD_SIZE variable in tictactoe.py to desired n
     - However, any board size above 3 is too slow to run on my PC
