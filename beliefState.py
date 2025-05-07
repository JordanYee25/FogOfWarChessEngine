# This is the interesting stuff, holds the many many possible chess board states. Observations for AI only 
from observation import Observation
import chess, random


class beliefState:
    def __init__(self, player_color: bool, num_particles=100):
        self.num_particles: int = num_particles #Default 100
        self.particles = [] #Particles for the almighty particle filter 
        self.player_color = player_color

    #Generates initial particles given num particles
    def generate_particles(self, observation):
        for particle in range(self.num_particles):
            new_particle = self.guesstimate(observation)
            self.particles.append(new_particle)



    #Guesstimates the full board based on the observation which is a partially observable board
    #IT IS VERY IMPORTANT THAT THE ACTUAL BOARD IS NOT PASSED IN. THAT WOULD BE CHEATING!!!
    def guesstimate(self, observation : Observation):
        board = chess.Board()
        board.clear_board() 

        #For when placing pieces, keep track of what pieces have been placed, also if there is already an ENEMY piece observed, subtract
        unplaced_pieces = { 
            chess.PAWN: 8,
            chess.ROOK: 2,
            chess.KNIGHT: 2,
            chess.BISHOP: 2,
            chess.QUEEN: 1,
            chess.KING: 1
        }
        #Add pieces that are ours, get function for some level of safety
        for square in observation.visible_board:
            piece = observation.isPieceAt(square)
            if piece is not None:
                if not observation.pieceColor(sqaure) == self.player_color
                board.set_piece_at(square, piece)

        #Fun part!
        #Randomly generate board in non observable areas

        for sqaure in chess.SQUARES:
            if square not in observation.visible_board:
                if 


