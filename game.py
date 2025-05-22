import chess
import sys
import random
import chess.engine #Stock fish for evaluating AI moves/partial board. Only for choosing next move, nothing more. Stockfish is just the engine being used, actual function calls are stil in the python chess api
import sunfish
from sunfish import Position, Searcher

from board import boardState
from observation import Observation
from beliefState import beliefState
from mcts import MCTS

# File for actually runnin the game
# Just thought this was the cleaner way to do it

# This will control stuff like move input, checking for win condition. The ping pong style of play between players and such
class game:
    def __init__(self, player_color, debug=False):
        self.full_board = chess.Board()
        self.board_State = boardState(self.full_board)  #Actual Board, SHOULD NOT BE SHOWN DIRECTLY TO USER OR AI

        self.player = player_color
        self.debug = debug

        self.player_board = set() #Keep set of visible squares of the current turn of the player

        self.beliefState = beliefState(not self.player) #Belief state is only for AI which is the opposite of player color
        
        self.fish_engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\stockfish-windows-x86-64-avx2.exe")
        self.sunfish_engine = Searcher()
        
        self.mcts = MCTS()
        
        
    def get_player_move(self):
        while True:
            player_move = input("Please enter move\n").strip()
            try:
                #Convert string input into api readable notation
                move = self.board_State.board.parse_san(player_move)
                #move = chess.Move.from_uci(move)
                if move in self.board_State.board.legal_moves:
                    return move
                else:
                    print("Illegal move")
            except:
                print("Invalid uci format, see README for notation hints")


    def get_ai_move(self):
        #Make observation
        #make move
        #update observation/belief state
        select_board = None
        for board in range(100): #Because 100 particles
            select_board = random.choice(self.beliefState.particles)
            if select_board.is_valid():
                break

        # move = self.mcts.mcts(select_board)
        # if move is None:
        #     print("ERROR NONE MOVE")
        #print(select_board)
        result = self.fish_engine.play(select_board, chess.engine.Limit(time=0.1))
        move = result.move

        if move not in self.board_State.board.legal_moves:
          #  print("Stockfish chose ILLEGAL move")
            return random.choice(list(self.board_State.board.legal_moves))
        return move

    #Run the game
    def start(self):
        observation = Observation(self.board_State.board, not self.player)
        self.beliefState.generate_particles(observation, True) #Yes it is move 0 so the particles should all be the same initial board

        while not self.board_State.isGameOver():
            

            if self.board_State.board.turn:
                print("\nWhite to move!")
            else:
                print("\nBlack to move!")

            #if player is white they go first
            if self.player == self.board_State.board.turn:
                observation = Observation(self.board_State.board, self.player)
                observation.print_fog_board()
                move = self.get_player_move()
            else:
                observation = Observation(self.board_State.board, not self.player)
                self.beliefState.update(observation)
                
                move = self.get_ai_move()


            self.board_State.board.push(move)
            
            if self.debug:

                if self.board_State.board.turn:
                    print(f"White played {move}!")
                else:
                    print(f"Black played {move}!")
                
                print(self.board_State.board)

        
        self.fish_engine.quit()
        if self.board_State.board.turn == chess.BLACK:
            return "white"
        else:
            return "black"
        

# Command for starting game as white:    python game.py w
# Command for starting game as black:    python game.py b
# User must select either w/b
if __name__ == "__main__":
    debug = False
    player_color = chess.WHITE  #chess.WHITE equals True in the API
    
    if sys.argv[1] == 'w':
        player_color = chess.WHITE  
    elif sys.argv[1] == 'b':
        player_color = chess.BLACK
    else:
        print("Invalid player option chosen, likely mising parameter w or b in cmd argument, see game.py")
        exit()
    if sys.argv[2] == "--debug":
        debug = True

    game = game(player_color, debug)
    winner = game.start()

    print(f"{winner} Won!")