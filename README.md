# FogOfWarChessEngine
Welcome to Capital Chess! Where Capital letters are white pieces and lowercase letters are black pieces

## Dependencies
```
pip install chess
```

# Notation Hint
##TODO


# Notes on Chess API

# Fog of War Chess/Dark Chess Overview
It is important to note that like chess.com, the visibility is determined by legal moves and not attacking moves. The difference here is probably only noticeable for pawns which capture/attack diagonally but normall move straight

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




