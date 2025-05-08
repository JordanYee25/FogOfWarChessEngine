# This is the interesting stuff, holds the many many possible chess board states. Observations for AI only 


#################
#REFERENCES
#################

#For high level understanding of MCTS and particle filter algorithm
# https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/12-Particle-Filters.ipynb


from observation import Observation
import chess, random


class beliefState:

    #For color put in the color that the AI is when calling
    def __init__(self, color: bool, num_particles=100):
        self.num_particles: int = num_particles #Default 100
        self.particles: list[chess.Board] = [] #Particles for the almighty particle filter 
        self.color = color

    #Generates initial particles given num particles
    ###################
    #CLEARRS PARTICLES#
    ###################
    #Added isTurn0 which helps the particles because we know the board psiton at turn 0 even though there is fog
    def generate_particles(self, observation, isTurn0 = False):
        self.particles = [] #Clear lsit of particles since every new update generates a new list/removes old particles

        for particle in range(self.num_particles):
            new_particle = None

            if isTurn0 is False:
                new_particle = self.guesstimate(observation)
            else:
                new_particle = chess.Board()
                new_particle.turn = self.color

            self.particles.append(new_particle)

    #Based on an observation and particles, update the particles if they match/plasuibly match the observation
    #Puts the filter in particle filter
    def update(self, observation: Observation):
        new_particles = []
        #If a square that is not revealed does not match the observation, Goes through each particle(board), checks if for every piece
        #In the observation if the particle board matches with what is visible
        for particle in self.particles:
            for square, piece in observation.visible_pieces.items():
                if particle.piece_at(square) is None: #If there is not a piece where there should be one, filter out
                    break
                if particle.piece_at(square) != piece: #Case where there is a piece on the square but it is the wrong kind
                    break
            else: #Something cool I learned today, you can use an else statement on a for loop!
                new_particles.append(particle) #If it passes, add to new particle list
        
        #Replenish particles if less than num particles
        if len(new_particles) < self.num_particles:
            while len(new_particles) < self.num_particles:
                new_particles.append(self.guesstimate(observation))
        
        self.particles = new_particles  #Update particles

        
       

    #Guesstimates the full board based on the observation which is a partially observable board
    #IT IS VERY IMPORTANT THAT THE ACTUAL BOARD IS NOT PASSED IN. THAT WOULD BE CHEATING!!!
    def guesstimate(self, observation : Observation):
        board = chess.Board()
        board.turn = self.color
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

        #Add pieces that are ours
        for square, piece in observation.visible_pieces.items():
            board.set_piece_at(square, piece)
    
            #Note if enemy piece was added
            if piece.color is not self.color:
                unplaced_pieces[piece.piece_type] -= 1
        
        #Fun part!
        #Randomly generate board in non observable areas
        for square in chess.SQUARES:
            if square not in observation.visible_board:
                if random.random() > .65:   #35 percent chance to place a piece on a square
                    remaining_pieces = []

                    for piece, count in unplaced_pieces.items():
                        if count > 0:
                            remaining_pieces.append(piece)

                    if remaining_pieces:
                        piece = random.choice(remaining_pieces)
                        color = not self.color  

                        board.set_piece_at(square, chess.Piece(piece, color))
                        unplaced_pieces[piece] -= 1

        #Make sure there is a king, if not loop until it is placed
        if unplaced_pieces[chess.KING] == 1: #Meaning it hasnt been used yet
            remainingSquares4TheKing = []
            king_Square = None

            for square in chess.SQUARES:
                if square not in observation.visible_board:
                    if not board.piece_at(square):
                        remainingSquares4TheKing.append(square)
            if len(remainingSquares4TheKing) == 0:
                fogOfWar = [square for square in chess.SQUARES if square not in observation.visible_board]
                king_Square = random.choice(fogOfWar)
            else:
                king_Square = random.choice(remainingSquares4TheKing)
            
            board.set_piece_at(king_Square, chess.Piece(chess.KING, not self.color))
            unplaced_pieces[chess.KING] -= 1
            
        return board
