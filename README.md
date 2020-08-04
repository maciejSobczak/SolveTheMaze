# SolveTheMaze
Finds the shortest path in a maze

The script operates on array of pixels thanks to Python Pillow imaging library

# Algoritm
The simplest way I figured out is to first mark an auxiliary path tracking right tunnel wall from entry to the exit of the maze.
Then in second iteration algorithm tracks noth edge of the mark which is the shortest path to solve the labirynth.

# Difficulties
Once the final iteration meets bottom border of the maze, some obstacles appear in following the auxiliary mark along the bottom border.
This results from algorithm looking around to find the shortest way while following the mark.

# Manual
To run the app on specific maze you have insert the file into maze folder and insert its name in code ("file_name" attribute in Main.py)
