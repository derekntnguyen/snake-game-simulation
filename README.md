# Snake Game Simulation

## Intro
The aim of this project was to explore the snake simulation to a greater degree than previously.
In that project snakes were modeled to move randomly on a 2d lattice. They could not intersect with other snakes or themselves.
The lattice was customizable in that it could have different sizes and it also included different boundary
conditions in which the snake could either move across the boundary of the lattice or they would
become stuck on the boundary. The snakes themselves could be set in different initial starting positions,
lengths, and orientations.

This project built upon the snake simulation assignment by adding in a rewarding element utilizing
methods from evolutionary algorithm and cellular automata. To explore the addition of evolutionary
algorithm, snakes could grow if they came into contact with food. This rewarding system was similar to
the one used in evolver project. In that assignment, points were awarded to different character
strings in attempt to create a more English looking phrase. Similarly, the rewarding system used in this
project allowed for snakes to increase their length and this resulted in greater competition between
snakes. This ultimately resulted in a program where the longest (strongest) snake prevailed to the end.
In order to incorporate aspects of cellular automata, a food distribution system was used similarly to the
one used in insect infestation project. To initially distribute the trees that were to be infested by the insects,
the numpy.random.binomial was utilized to create an array of locations where trees were present. In
this project, numpy.random.uniform was utilized to create two different randomly distributed arrays of
x and y coordinates which placed the locations of the food for the snakes. The number of foods initially
present can be specified by the user.

## Results
![image](https://user-images.githubusercontent.com/79728577/109375651-6d556680-788c-11eb-87fc-49efc0b10c2c.png)
Figure 1: Initial run the program with 10 available foods and 3 snakes
![image](https://user-images.githubusercontent.com/79728577/109375663-8100cd00-788c-11eb-9485-a6182ea40d25.png)
Figure 2: Running the program with 100 foods
![image](https://user-images.githubusercontent.com/79728577/109375668-89590800-788c-11eb-93a9-514055df0e3d.png)
Figure 3: Running the program with 500 foods
