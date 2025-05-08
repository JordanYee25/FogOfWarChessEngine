# FogOfWarChessEngine
Welcome to Capital Chess! Where Capital letters are white pieces and lowercase letters are black pieces

## Dependencies
```
pip install chess

download the latest version of stockfish for windows and place in directory:

https://stockfishchess.org/download/

See notes below
```

# Notation Hint
To enter moves, enter in standard chess notation. Please reference python chess

An example set of moves for grading:
python game.py w
e4 (move the pawn on the e2 square to e4)

--Computer move

Nf3 (move the knight on g1 to f3)

--Computer move

Nc3

--Computer move

Bc4 (move the bishop on f1 to c4)

--Computer move

O-O (Castle your king and rook)

To promote a pawn to queen do :
e8=Q for example

despite white pieces being uppercase and black pieces lowercase, move input should be in the right capitalization
for example, to move the knight it is N not n

# Notes on Chess API

# Fog of War Chess/Dark Chess Overview
It is important to note that like chess.com, the visibility is determined by legal moves and not attacking moves. The difference here is probably only noticeable for pawns which capture/attack diagonally but normall move straight

The problem I am trying to solve relates to a variation made on chess called Fog of War Chess. This version is unique in one main way. It revolves around the idea of a “Fog of War” where part of the board is not observable to the opposing player. The squares that are visible are determined by whether the player’s pieces can move there or not. For example, the starting visibility will be up to the middle of the board because that is the furthest that either player could make their first move using their pawns.

# 5.1.2 State Space Description


## Natural language description of state space in draft report (5%)
The state space for this model is the 8x8 chess board. Even though the state is only partially observable for the AI, it will generate an entire board state with variables of pieces and thier position on the board.
There are constraints such as two pieces not being able to exist on the same chessboard square at the same time, and there not being more pieces than possible, like 9 pawns or 2 kings (of the same color).

The AI will hold belief states using a particle filter to generate possible states. The transitions come from possible piece movements and information that was revealed by vision of each piece. As the game contineus
and there are less pieces on the board, the particle states should become fewer and tighter.


## Complete mathematical description of states, transitions, actions, and observations (5%)

There is one state S or boardState that contains all pieces currently on the board and which players move it is currently. There are many belief states b for the boardState on the position of pieces that are non observable.

The transitions function from one state to another is T(s', a, s) which takes the current boardState, takes an action, and the resulting boardState after that action and compares that to any observations that are made which is then used to update existing belief states. 

The actions are piece movement either by the AI or the opponent both of which have the possibility to create new observations (a piece is moved to reveal a piece or a piece moves into previously existing line of sight of another piece)

The observations use an observation model of the observation made from the most probable board state given an action taken


# 5.1.3 Sate Space Implementation

 # Final Report
The problem I set out to solve was to create a partially observable chess engine that could play fog of war chess

There has been some github pages for dark chess but I have not seen them in python

To complete this I used particle filter and mcts to determine possible board states that the board could be in and use mcts to get the best moves

Implementation:
I first had to create the game space, I used python chess for their board operations. They dont have good options for making a partially observable board, so a large chunk of board.py, game.py is just setting up the game and making it playable. 

Observation.py gets an observation from the board using friendly pieces and fog of war chess rules to create a board for the user and the AI to use. It gives two main important pieces of info which are the visible pieces which are pieces that can be seen directly. And visible_board which I should have just named visible squares because it only holds information on seen squares and not the rest of the board, it is not a chess.Board object it is just a list

BeliefState.py is my particle filter attempt. It takes a board from the observation.py (A chess board with fog of war enabled) and created many variants of what the opponent player could have. It is not very smart, it just randomly places pieces down with the rule that it will not place down more pieces than possible, and it will always place down a king before returning. 


MCTS.py is my attempt at mcts, I unfortuneatly ran out of time to fully implement it, the code for mcts is widely online, but not for chess, and so I had to adapt lots of code from online references to get it to not crash. I hope I sufficiently noted them, but just in case:
Useful general Pseudocode for getting mcts set up https://webdocs.cs.ualberta.ca/~hayward/396/jem/mcts.html

Cross referenced for help with function definitions, also a general implementation of mcts:
https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/

I followed the general idea of mcts expansion and back propagation and tried to apply it to a chess state.


StockFish:
I used stockfish from their official website ONLY to evaluate boards. Stockfish is a chess engine and to my knowledge, doesnt have a fog of war mode. 

## Important note for running
I used the most recent download I can find, this may only work if you are on windows. 

https://stockfishchess.org/download/

Se line 25 in game.py for stockfish usage

I reverted the code back to a working version that didnt use MCTS, see get_ai_move for implementation





