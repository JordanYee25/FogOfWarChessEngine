import chess
import sys
import random
from board import boardState



# File for actually runnin the game
# Just thought this was the cleaner way to do it

# This will control stuff like move input, checking for win condition. The ping pong style of play between players and such
class game:
    def __init__(self, player_color):
        self.full_board = chess.Board()
        self.board_State = boardState(self.full_board)  #Actual Board, SHOULD NOT BE SHOWN DIRECTLY TO USER OR AI

        self.player = player_color

        self.player_board = set() #Keep set of visible squares of the current turn of the player
        
    #This will work by making almost like a filter (not math filter) of squares that player pieces currently attack
    def get_player_squares(self):
        visible_squares = set()
        for square in chess.SQUARES:
            if self.board_State.board.piece_at(square) is not None: #There is a piece on this square   
                if self.board_State.board.piece_at(square).color == self.player:    #And is the player's piece
                    #NEED TO ADD BOTH ATTACKED SQUARE AND SQUARE PIECE IS ON
                    visible_squares.add(square)
                    visible_squares.update(self.board_State.board.attacks(square))
        return visible_squares

    #This assumes the board is only printed for player moves, AI moves happen in the background
    #Also, pychess doesnt support setting up a position (at least in an easier way than just manually making a board)
    def print_player_board(self):
        self.player_board = self.get_player_squares()

        #Assuming an 8x8 grid, we check each square returned in the player board (board that we know the player can see) with the actual board. 
        #If there is a square that the player should be seeing, we check if there is a piece on it or alternatively, if the square is being controlled/attacked by one of the pieces 
        #If it is a piece, we put the piece marking, see README. If an empty square, we put a ".", if non of the above (fog) then put a "?"
        for row in reversed(range(8)):
            for col in range(8):
                square = chess.square(col, row)
                if square in self.player_board:
                    piece = self.board_State.board.piece_type_at(square)
                    if piece:
                        print(chess.piece_symbol(piece), end='')
                    else:
                        print(".", end='')
                else:
                    print("?", end='')
                print(" ", end='')
            print()

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
                self.print_player_board()
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