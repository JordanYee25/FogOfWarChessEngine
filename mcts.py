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
    def __init__(self, board:chess.board, move, parent):
        self.board: chess.Board = board
        self.move = move
        self.parent = parent
        self.children: list[MCTSNode] = []

        self.wins = 0
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
        if r == True:
            self.wins += 1
    
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




    def MCTS(self, board: chess.Board):
        startTime = time.time()
        runTime = 1.0 #how long to let mcts run

        while time.time() - startTime < runTime:
            rootBoard = copy.deepcopy(board)
            rootNode = MCTSNode(rootBoard, None, None)
            node = rootNode
            
            while not node.is_leaf():
                node = node.best_child()
                rootBoard.push(node.move)

            node.expand(rootBoard)

            node = node.best_child()

            #Simulate till end of game
            while not rootBoard.is_game_over():
                rootBoard.push(random.choice(list(rootBoard.legal_moves)))
            result = self.evaluate(rootBoard)