import chess
import sys
import random




#This is for handling the partially observable board, it was getting a little hectic having everything in one game file, and this helps make sure that the real board is not being show to the AI
#This is real time unscrewing myself

#UPDATE! This feels so unreadable it might as well be written in hieroglyphics


#Useful for building a partially observable board
class Observation:

    #board is the full chess board
    #player is the player color where True is WHITE and False is BLACK, i didnt choose this
    def __init__(self, board: chess.Board, player: bool):
        self.board = board
        self.player = player
        self.visible_pieces = {} #kv pair where the key is square, The value is a chess.Piece(piece,color)
        self.visible_board = self.get_fog_board(board, player)  #Should really be named visible squares because it doesnt care abt the rest of the sqaures
    #Okay 
    def get_fog_board(self, board: chess.Board, player: bool):
        if board is None or player is None:
            print("Exception, board or player not supplied for get_fog_board")
            print(f"Board \n{board}\n Player {player}")
            return None
        visible_squares = set()
        #Gets visible sqaures by comparing legal moves to the respective piece that the mvoe results in and the piece that can make the move
        for move in board.legal_moves:
            if board.piece_at(move.from_square).color == player:      #Check if player color
                visible_squares.add(move.from_square)               #ADD BOTH SQUARE PIECE IS ON AND THE SQUARES IT CAN MOVE TO
                visible_squares.add(move.to_square)    
                self.visible_pieces[move.from_square] = chess.Piece(board.piece_type_at(move.from_square), player)

                if board.piece_at(move.to_square) and not board.piece_at(move.to_square).color == player:  #Keeps track of pieces that have been seen that are the enemies
                    self.visible_pieces[move.to_square] = chess.Piece(board.piece_type_at(move.to_square), not player)

        #This runs into an edge case where a piece can not have any moves (like the rook at the beginning of the game) but shouldnt be in the fog of war, this part handles that
        for square in chess.SQUARES:
            if board.piece_at(square) and board.piece_at(square).color == player:   #Nifty, if piece exists at square and if piece at square is same as input player color
                visible_squares.add(square)
                self.visible_pieces[square] = chess.Piece(board.piece_type_at(square), player)
        return visible_squares
    
    #optimize later todo
    #Assuming an 8x8 grid, we check each square returned in the player board (board that we know the player can see) with the actual board. 
    #If there is a square that the player should be seeing, we check if there is a piece on it or alternatively, if the square is being controlled/attacked by one of the pieces 
    #If it is a piece, we put the piece marking, see README. If an empty square, we put a ".", if non of the above (fog) then put a "?"
    def print_fog_board(self):
        #White
        if self.player:
            for row in reversed(range(8)):
                for col in range(8):     
                    square = chess.square(col, row)
                    if square in self.visible_board:
                        if square in self.visible_pieces:
                            print(self.visible_pieces[square].symbol(), end='')
                        else:
                            print(".", end='')
                    else:
                        print("?", end='')
                    print(" ", end='')
                print()
        else: #Black
            for row in range(8):
                for col in reversed(range(8)):     
                    square = chess.square(col, row)
                    if square in self.visible_board:
                        if square in self.visible_pieces:
                            print(self.visible_pieces[square].symbol(), end='')
                        else:
                            print(".", end='')
                    else:
                        print("?", end='')
                    print(" ", end='')
                print()

    #Only shows if piece type for class player color
    def isPieceAt(self, square : chess.square):
        if self.board.piece_at(square):
            return self.board.piece_type_at(square)
        else:
            return None
        
    def pieceColor(self, square):
        if self.board.piece_at(square):
            return self.board.piece_at(square).color
        else:
            return None
        
    def getBoard(self):
        return self.visible_board