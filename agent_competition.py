# You can use the functions to write your AI for competition
from __future__ import nested_scopes
from checkers_game import *
from agent import *
from driver import *

cache = {}

import random
import sys
import time

def alphabeta_min_node(state, color, alpha, beta, limit, caching=0, ordering=0):
    
    state_of_BEST_move = None
    minimum_utility = float("inf")
    possible_states_of_moves = successors(state, color)
    
    # If we are caching and we have the same situation in cache
    if caching and (state, color) in cache :
        return cache[(state, color)]
    
    # Game is over
    if len(possible_states_of_moves) == 0 or is_game_over(state) or limit == 0 :
        return compute_heuristic(state, get_opponent_color(color)), state
    
    # If we are ordering
    if ordering :
        possible_states_of_moves.sort(key = lambda x : compute_heuristic(x, color), reverse = False)
    
    # Loop every possible state
    for next_state in possible_states_of_moves :
        
        # Get the best utility from recursive call
        next_utility = alphabeta_max_node(next_state, get_opponent_color(color), alpha, beta, limit - 1, caching)[0]
        
        # Check if it has a better utility
        if next_utility < minimum_utility :
            
            state_of_BEST_move = next_state
            minimum_utility = next_utility
        
        # Check if pruning needed
        beta = min(beta, next_utility)
        if beta <= alpha : break
        
    # If we are caching, we need to record the best move and its utility        
    if caching :
        cache[(state, color)] = minimum_utility, state_of_BEST_move
    
    return minimum_utility, state_of_BEST_move
        

def alphabeta_max_node(state, color, alpha, beta, limit, caching=0, ordering=0):
    
    state_of_BEST_move = None
    maximum_utility = float("-inf")
    possible_states_of_moves = successors(state, color)
    
    # If we are caching and we have the same situation in cache
    if caching and (state, color) in cache :
        return cache[(state, color)]
    
    # Game is over or depth limit reached
    if len(possible_states_of_moves) == 0 or is_game_over(state) or limit == 0 :
        return compute_heuristic(state, color), state
    
    # If we are ordering
    if ordering :
        possible_states_of_moves.sort(key = lambda x : compute_heuristic(x, color), reverse = True)

    # Loop every possible state
    for next_state in possible_states_of_moves :
        
        # Get the best utility from recursive call      
        next_utility = alphabeta_min_node(next_state, get_opponent_color(color), alpha, beta, limit - 1, caching)[0]
        
        # Check if it has a better utility
        if next_utility > maximum_utility :
            
            state_of_BEST_move = next_state
            maximum_utility = next_utility
        
        # Check if pruning needed
        alpha = max(alpha, next_utility)
        if beta <= alpha : break
            
    # If we are caching, we need to record the best move and its utility      
    if caching :
        cache[(state, color)] = maximum_utility, state_of_BEST_move
    
    return maximum_utility, state_of_BEST_move
            

def select_move_alphabeta(state, color, limit, caching=1, ordering=1):
    """
    Given a state (of type Board) and a player color, decide on a move. 
    The return value is a list of tuples [(i1,j1), (i2,j2)], where
    i1, j1 is the starting position of the piece to move
    and i2, j2 its destination.  Note that moves involving jumps will contain
    additional tuples.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enforce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_heuristic)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    cache.clear()
    return alphabeta_max_node(state, color, float("-inf"), float("inf"), limit, caching, ordering)[1].move



# If you choose to try MCTS, you can make use of the code below
class MCTS_state():
    """
            This sample code gives you a idea of how to store records for each node
            in the tree. However, you are welcome to modify this part or define your own
            class.
    """
    def __init__(self, ID, parent, child, reward, total, board):
        self.ID = ID
        self.parent = parent    # a list of states
        self.child = child      # a list of states
        self.reward = reward    # number of win
        self.total = total      # number of simulation for self and (grand*)children
        self.board = board
        self.visited = 0        # 0 -> not visited yet, 1 -> already visited


def select_move_MCTS(state, color):
    """
               You can add additional help functions as long as this function will return a position tuple
    """
    initial_state = MCTS_state(0, [], [], 0, 0, board) # this is just an example. delete it when you start to code.
    pass

# ======================== Class GameEngine =======================================
class GameEngine:
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    # The return value should be a move that is denoted by a list
    def nextMove(self, state, alphabeta, limit, caching, ordering):
        global PLAYER
        PLAYER = self.str
        result = select_move_alphabeta(Board(state), PLAYER, limit, caching, ordering)

        return result