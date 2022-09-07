# maze-solver

This maze solver uses a 2D maze input along with an inputted starting position and desired ending position. There are three available algorithms Breadth First Search, 
Uniform Cost Search and A*. Since the maze is grid based and movement along it is limited to four directions, a manhattan distance heuristic is used to determine the optimal 
path. 

# Input File
## Positions
- The starting line of the input text file indicates the x and y dimensions of the maze area
- The second line indicates the starting position
- The third line indicates the desired ending position

## The Map
- The map input must match the dimensions specified in line 1 or it will produce an error
- Each number on the grid denotes a potential movement cost. For example if a grid number is 5, it will be of movement cost 5 and the solver will consider this more
'difficult terrain' than a grid number of 1. 
- X represents the walls of the maze. Movement cannot occur in these sections.

# Usage
To run the solver simply run the python file with 2 arguments: the input maze text file, the desired algorithm (bfs, ucs or astar)
The output will produce the same inputted however the determined path will be displayed in * symbols.

### Example
python3 pathfinder.py input.txt astar 
