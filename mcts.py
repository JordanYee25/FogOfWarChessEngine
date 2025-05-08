# The hard part, imo (in my opinion)

#REFERENCES 
# Heavily referenced this mcts. The mcts is general form and not specialized for chess
# Useful general Pseudocode for getting mcts set up https://webdocs.cs.ualberta.ca/~hayward/396/jem/mcts.html
#
#Cross referenced for help with function definitions, also a general implementation of mcts:
# https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
# Deeeeep copy https://docs.python.org/3/library/copy.html

import chess.engine #Stock fishy
import chess
import time
import copy
import random
from board import boardState
from observation import Observation
from beliefState import beliefState

class MCTSNode:
    def __init__(self, board:chess.Board, move, parent):
        self.board: chess.Board = board
        self.move = move
        self.parent = parent
        self.children: list[MCTSNode] = []

        self.score = 0
        self.visits = 0


    def  expand(self):
        if not self.board.is_game_over():
            for move in self.board.legal_moves:
                new_board = self.board.copy()
                new_board.push(move)
                child = MCTSNode(new_board,move, self)
                self.children.append(child)

    def update(self, r):
        self.visits += 1
        self.score += r
    
    def is_leaf(self):
        return len(self.children) == 0

    def has_parent(self):
        return self.parent is not None

    #child with highest visits
    def best_child(self):
        best = -1
        bestChild = None
        for child in self.children:
            if child.visits > best:
                best = child.visits
                bestChild = child

        return bestChild


class MCTS:
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\stockfish-windows-x86-64-avx2.exe")


    def mcts(self, board: chess.Board):
        startTime = time.time()
        runTime = 1.0 #how long to let mcts run
        rootBoard = copy.deepcopy(board)
        rootNode = MCTSNode(rootBoard, None, None)
        while time.time() - startTime < runTime:

            node = rootNode
            
            while not node.is_leaf():
                node = node.best_child()
                rootBoard.push(node.move)

            node.expand()

            node = node.best_child()

            #Simulate till end of game
            #Instead of simulating through random moves (which will likely be innacurate due to the nature of chess)
            #Use stockfish to get an evaluation of the score, which initself kind of simulates anyways
            #while not rootBoard.is_game_over():
            #    rootBoard.push(random.choice(list(rootBoard.legal_moves)))
            #Heavily referenced chess.engine docs
            info = self.engine.analyse(rootBoard, chess.engine.Limit(depth=20))
            score = info["score"]
            eval = score.white().score(mate_score=100000)   #Extracts score in numeric value
            if rootBoard.turn == chess.WHITE:
                result = float(eval)
            else:
                result = -float(eval)


            while node.has_parent():
                node.update(result)
                node = node.parent

        return rootNode.best_child().move

            