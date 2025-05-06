import chess
import sys
import random
from board import boardState
from observation import Observation


# File for actually runnin the game
# Just thought this was the cleaner way to do it

# This will control stuff like move input, checking for win condition. The ping pong style of play between players and such
class game:
    def __init__(self, player_color):
        self.full_board = chess.Board()
        self.board_State = boardState(self.full_board)  #Actual Board, SHOULD NOT BE SHOWN DIRECTLY TO USER OR AI

        self.player = player_color

        self.player_board = set() #Keep set of visible squares of the current turn of the player
        
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
        return random.choice(list(self.board_State.board.legal_moves))

    #Run the game
    def start(self):
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
                move = self.get_ai_move()


            if self.board_State.board.turn:
                print(f"White played {move}!")
            else:
                print(f"Black played {move}!")
            
            self.board_State.board.push(move)
        return self.board_State.board.turn  #who ever this returns is the winner, because the loop beraks when the opponent cannot make any legal moves
        

# Command for starting game as white:    python game.py w
# Command for starting game as black:    python game.py b
# User must select either w/b
if __name__ == "__main__":
    
    player_color = chess.WHITE  #chess.WHITE equals True in the API
    
    if sys.argv[1] == 'w':
        player_color = chess.WHITE  
    elif sys.argv[1] == 'b':
        player_color = chess.BLACK
    else:
        print("Invalidplay er option chosen, likely mising parameter w or b in cmd argument, see game.py")
        exit()

    game = game(player_color)
    winner = game.start()

    ##################################################
    #MUST FIX, CURRENTLY BACKWARDS DUE TO LOGIC ERROR
    ##################################################
    print(f"{winner} Won!")