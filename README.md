# CSC384-Checkers-AI
University of Toronto CSC384(Introduction to Artificial Intelligence) Assignment 2

Minimax Algorithm & Alpha-Beta Pruning (with state caching, depth limit, node ordering)


Checkers is a 2-player board game that is played with distinct pieces that are typically black on one side and red on the other side, each side belonging to one player. Our version of the game is played on an 8x8 chess board, which is standard. Players (red and black) take turns moving pieces on the board.

Moving the pieces is dictated by the rules of the game, and can result in capturing the opponent's pieces. An overview of Checkers is provided at https://en.wikipedia.org/wiki/Draughts.  (Links to an external site.)Note that the version of Checkers that we will be coding is Standard English Draughts; the rules are explained here. (Links to an external site.) English Draughts includes mandatory captures.

Objective: The player’s goal is to have a majority of the remaining pieces.

Game Ending: The game ends as soon as one of the players has no pieces remaining or no legal moves left.

Rules: At the beginning of the game, each player has 12 pieces of red or black colour. The pieces are placed on the dark squares of the board across the first three rows on each side (Figure 1. at left). The black player makes the first move.

Each piece can only move forward diagonally in two ways: 1) moving one space, if the adjacent space is empty (Figure 1, at left), or 2) moving two spaces if the adjacent space is occupied by the opponent, and space beyond that is empty (Figure 1, in the middle). In the second case, the player 'captures' the opponent's piece that was jumped over. If a move leads to capture, and the piece ends up sitting at a position that can jump over another opponent's piece, the player can move it again and capture another piece of the opponent. This sequence of moves does not need to be on a straight line and can be 'zigzag'.

When one of the pieces reaches the last row of the board (or the first row from the opponent's side), it turns into a "king" and will be granted a unique power: it can move both forward and backward. In our GUI a king is a piece with a yellow border. 

We recommend that you start this assignment by playing some games of checkers to develop a better understanding of how the game works and what strategies can give you an advantage.  An online version of the game that allows you to compete against an AI can be found at this link. (Links to an external site.)

Starter Code
The starter code contains 6 files. You can download all the code and supporting files as a Zipped file archive.  In that archive you will find the following files:

Files you can use to test your solution:
autograder.py	A file with some basic tests of the functions you must write.
Files you'll edit and submit on Markus:
agent.py	The file where you will implement your game agent; this will be graded.
agent_competition.py	A file you can use if you choose to help write an agent  for the Checkers competition (which is optional).  
Files you might want to look at (look but don't modify):
driver.py	This contains a simple graphical user interface (GUI) for Checkers; and the game ”manager” that stores the current game state and communicates with different player AIs. 
checkers_game.py	This contains functions for computing legal moves, captured pieces, and successor game states. These are shared between the game manager, the GUI, and the AI players.
randy.py	A simple agent that picks moves at random that you can use to see the game in operation.
Game State Representation: Each game state contains two pieces of information: The current player and the current pieces on the board. Throughout our implementation, Player 1 (black) is represented using a 'b', and Player 2 (red) is represented using an 'r'.

The board is represented as a list of lists. The inner lists represents each row of the board. Each entry in the rows is either an empty square (indicated with a '.'), a black piece (a 'b'), or a red piece (an 'r').  Black pieces that are kings are indicated with a 'B' and red pieces that are kings are indicated with an 'R'.  For example, an 8x8 board might look like this at the start of the game:

[ ['b','.','b','.','b','.','b','.'],\
['.','b','.','b','.','b','.','b'],\
['b','.','b','.','b','.','b','.'],\
['.','.','.','.','.','.','.','.'],\
['.','.','.','.','.','.','.','.'],\
['.','r','.','r','.','r','.','r'],\
['r','.','r','.','r','.','r','.'],\
['.','r','.','r','.','r','.','r'] \
]
Each move is represented as a list of tuples.  For example, a move that takes a piece from position 5,1 to position 4,2 will be represented as:
[(5, 1), (4, 2)]
A move that contains a jump and which takes a piece from position 6,3 to position 4,5 and then to 2,7 via jumps will be represented as:
[(6, 3), (4, 5), (2, 7)]
Note that your starter code (checkers_game.py) contains a class of type Board that has two attributes: a board (which is a list of lists) and a move (which is a list of tuples).  Be mindful of the distinction between an object that is of type Board and the board representation itself, which is a list of lists.  
Running the code: You can run two AI agents against one another via the Checkers GUI. Running the code will bring up a game window.  Each agent will alternate turns. 
Our GUI takes two AI programs as command line parameters. When two AIs are specified at the command line you will be able to watch them play against each other. We have included one AI named Randy (and which is coded in the file randy.py) that will select checkers moves at random.  To see Randy play against itself, type

$python3 driver.py randy randy
You will write your own agent in the agent.py file.  Once you create an agent, you may want to try playing it against those that are made by your friends.
The GUI is rather minimalistic, so you need to close the window and then restart to play a new game.

Time Constraints: When we test your AI player, we will be expecting it to make a move within 10 seconds. If no move has been selected, the AI will lose the game. 

Mark Breakdown
Minimax [30 pts]

The first thing you will do is to write a function compute utility(state, color) that computes the utility of a final game board state.  Note that state will be an object of type Board; to access the board as a list of lists you will want to evaluate the board attribute of that state (i.e. state.board which will be in the format described above). The utility should be based on the number of pieces of the player's colour minus the number of pieces of the opponent. Make each regular piece worth one point and each king worth 2.  If your agent has a single king and six regular pieces, assign this a value of 2*1 + 6 = 8.  If your agent's opponent has two kings and 3 regular pieces, assign this a value of 2*2 + 3 = 7 points.  The difference in points between agents, and the result of compute_utility, will therefore be 8-7 = 1.

Then, implement the method select_move_minimax(state, color, limit = 5, caching = 0).   For the time being, you can ignore the limit and caching parameters that the function will also accept; we will return to these later.  This will accept a state (which is an object of type Board) as well as the player's colour ('r' or 'b').  It will return a single move that corresponds with the minimax strategy. More specifically, your function should select the action that leads to the state with the highest minimax value.  The return value should be a list of tuples that represent the move, as above.  Implement minimax recursively by writing two functions minimax_max_node(state, color, limit, caching) and minimax_min_node(state, color, limit, caching). Again, you can just ignore the limit and caching parameters for now.

Hints: Use the successors(state,player) function in checkers_game.py, which returns all the the successive states (which includes moves and successive board representations) for a given player. Pay attention to which player should make a move for min nodes and max nodes.

While you can test some of the functions in your MINIMAX algorithm using the autograder, if you try to run it with driver.py you may end up with a stack overflow! This is because the game of checkers is large.  We will have to implement a depth limit to realize an agent that can operate in a tractable amount of time and memory.

Depth Limit [10 pts]

To make your agent really functional, you must implement a depth limit. Your starter code is structured to do this by using the '-d' flag at the command line. For example, if you type

$python3 driver agent agent -d 6 
the game manager will call your agent’s MINIMAX routine with a depth limit of 6. Note that the code implements a default depth limit of 5, which you can override.

Change your Minimax code to recursively send the ’limit’ parameter to both minimax_min_node and  minimax_max_node. In order to enforce the depth limit in your code, you will want to decrease the limit parameter at each recursion. When you arrive at your depth limit (i.e. when the ’limit’ parameter is zero), use a heuristic function to define the value any non-terminal state. You can call the compute utility function as your heuristic to estimate non-terminal state quality.

What is the largest depth limit you can play without needing more than 10 seconds per move?

Alpha-Beta Pruning [30 pts]

The simple minimax approach is quite slow. To ameliorate this we will write the function select_move_alphabeta(state, color, limit=5, caching=0, ordering=0) to compute the best move using alpha-beta pruning. The parameters and return values will be the same as for minimax. You can ignore the caching, and ordering parameters that the function will also accept for the time being; we will return to these later. Much like Minimax, your alpha-beta implementation should recursively call two helper functions: alphabeta_min_node(state, color, alpha, beta, limit, caching=0, ordering=0)  and alphabeta_max_node(state, color, alpha, beta, limit, caching=0, ordering=0). As with Minimax, recursively sends the ’limit’ parameter to alphabeta_min_node and alphabeta_max_node. When you arrive at your depth limit, call compute_utility to generate a utility value for each given state.

Playing with pruning should speed up decisions for the AI, but you may still need to use a fairly shallow depth. Use the command

$driver agent agent -d 6 -a
to play against your agent using the ALPHA-BETA algorithm with a depth limit of 6.

What is the largest depth limit you can play without needing more than 10 seconds per move?

Caching States [10 pts]

We can try to speed up the AI even more by caching states we’ve seen before. To do this, we will want to alter your program so that it responds to the -c flag at the command line. To implement state caching you will need to create a dictionary in your AI player (this can just be stored in a global variable on the top level of the file) that maps board states to their Minimax value, or that checks values against stored alpha and beta parameters. Modify your Minimax and alpha-beta pruning functions to store states in that dictionary after their value is known. Then check the dictionary at the beginning of each function. If a state is already in the dictionary and do not explore it again. The starter code is structured so that if you type

$driver agent agent -d 6 -c
the game manager will call your agent’s Minimax routines with the ’caching’ flag on. If instead you type
$driver agent agent -d 6 -a -c 
the game manager will call your agent’s ALPHA-BETA routines with the ’caching’ flag on.
Your Own Heuristic [10 pts]

The prior steps should give you a good AI player, but we have only scratched the surface. There are many possible improvements that would create an even better AI. To improve your AI, create your own game heuristic. You can use this in place of computing utility in your alpha-beta or Minimax routines. 

When you submit your code, however, please use compute_utility as the heuristic you use when you hit the depth limit in your game agent.  This will facilitate marking!  You can use your own heuristic in your agent_competition.py file, however.

Some Ideas for Heuristic Functions for Checkers Game

Consider board locations where pieces are stable, i.e. where they cannot be captured anymore.
Consider the number of moves you and your opponent can make given the current board configuration.
Use a different strategy in the opening, mid-game, and end-game.
You can also do your own research to find a wide range of other good heuristics (for example, here is a good start: https://www.ultraboardgames.com/checkers/tips.php).

In addition to engineering your own heuristic, please include a (short) description that details your heuristic as a comment at the start of your solution file.

Node Ordering Heuristic [10 pts]

Finally, note that alpha-beta pruning works better if nodes that lead to a better utility are explored first. To do this, in the Alpha-beta pruning functions, try using your heuristic to order the nodes that you explore.  If your heuristic makes reasonably good estimates of non-terminal state values, this should lead to a little bit of a speed up because a good ordering will lead to more pruning.  Note that you can use your own heuristic to order nodes when you submit your code.  Use compute_utility to assess values of nodes when you hit the depth limit, however.

To run your code with node ordering, use the -o flag.  More specifically if you type:

$driver agent agent -d 6 -a -c -o

You will run your agent against itself using alpha-beta with a depth limit of 6 and both caching and node ordering ON. 