from __future__ import nested_scopes
from checkers_game import *
from driver import *

cache = {} #you can use this to implement state caching!

#= ----------------------------------------------------------------------------------
#=                                 Helper Functions
#= ----------------------------------------------------------------------------------

def get_util (state, color) :
    
    result = 0
    
    # color is black
    if color == 'b' or color == 'B' :
        for i in range(len(state.board)) :
            for j in range(len(state.board[0])) :
                    
                # it is a PAWN
                if state.board[i][j] == 'b' :
                    result += 1
                # it is a KING
                if state.board[i][j] == 'B' :
                    result += 2
                    
    # color is red
    else :
        for i in range(len(state.board)) :
            for j in range(len(state.board[0])) :
                      
                # it is a PAWN
                if state.board[i][j] == 'r' :
                    result += 1
                # it is a KING
                if state.board[i][j] == 'R' :
                    result += 2
                    
    return result


def get_better_util (state, color) :
    
    result = 0
    
    # color is black
    if color == 'b' or color == 'B' :
        for i in range(len(state.board)) :
            for j in range(len(state.board[0])) :
                    
                # it is a PAWN
                if state.board[i][j] == 'b' :
                    result += 1
                    # also beside boundary
                    if j == 0 or j == len(state.board) :
                        result += 1
                # it is a KING
                elif state.board[i][j] == 'B' :
                    result += 3
                    # also beside boundary
                    if j == 0 or j == len(state.board) :
                        result += 1
                        
    # color is red
    else :
        for i in range(len(state.board)) :
            for j in range(len(state.board[0])) :
                      
                # it is a PAWN
                if state.board[i][j] == 'r' :
                    result += 1
                    # also beside boundary
                    if j == 0 or j == len(state.board) :
                        result += 1
                # it is a KING
                elif state.board[i][j] == 'R' :
                    result += 3
                    # also beside boundary
                    if j == 0 or j == len(state.board) :
                        result += 1
                    
    return result


def get_better_heuristic(state, color) :
    
    result = 0
    
    # color is black (PRE: BLACK PLAYER IS ALWAYS AT THE TOP OF THE BOARD)
    if color == 'b' or color == 'B' :
        for row in range(len(state.board)) :
            for col in range(len(state.board[0])) :
                
                # it is a PAWN
                if state.board[row][col] == 'b' :
                    result += (5 + row + 1)
                    # beside boundary
                    if col == 0 or col == len(state.board[0]) - 1 :
                        result += 1
                    # or in the middle area (middle 4 columns & middle 2 rows) of board (take control of the middle is advantageous)
                    elif col + 1 <= len(state.board[0]) * 0.75 and col + 1 >= len(state.board[0]) * 0.25 and row + 1 <= len(state.board) / 2 and row + 1 >= len(state.board) / 2 :
                        result += 1
                    # or in the back row (pieces at the back row can possiblely prevent opponent from getting a king and also prevent ours pieces from being taken)
                    elif row == 0 :
                        result += 1
                
                # it is a KING
                elif state.board[row][col] == 'B' :
                    result += 15
                    # beside boundary
                    if col == 0 or col == len(state.board[0]) - 1 :
                        result += 1
                    # or in the middle area (middle 4 columns & middle 2 rows) of board (take control of the middle is advantageous)
                    elif col + 1 <= len(state.board[0]) * 0.75 and col + 1 >= len(state.board[0]) * 0.25 and row + 1 <= len(state.board) / 2 and row + 1 >= len(state.board) / 2 :
                        result += 4
                    # or in the back row (pieces at the back row can possiblely prevent opponent from getting a king and also prevent ours pieces from being taken)
                    elif row == 0 :
                        result += 0
                        
    
    # color is red (PRE: BLACK PLAYER IS ALWAYS AT THE BOTTOM OF THE BOARD)
    else :
        for row in range(len(state.board)) :
            for col in range(len(state.board[0])) :
                
                # it is a PAWN
                if state.board[row][col] == 'r' :
                    result += (5 + len(state.board) - row - 1)
                    # beside boundary
                    if col == 0 or col == len(state.board[0]) - 1 :
                        result += 1
                    # or in the middle area (middle 4 columns & middle 2 rows) of board (take control of the middle is advantageous)
                    elif col + 1 <= len(state.board[0]) * 0.75 and col + 1 >= len(state.board[0]) * 0.25 and row + 1 <= len(state.board) / 2 and row + 1 >= len(state.board) / 2 :
                        result += 1
                    # or in the back row (pieces at the back row can possiblely prevent opponent from getting a king and also prevent ours pieces from being taken)
                    elif row == len(state.board) - 1 :
                        result += 1
                    
                # it is a KING
                elif state.board[row][col] == 'R' :
                    result += 15
                    # beside boundary
                    if col == 0 or col == len(state.board[0]) - 1 :
                        result += 1
                    # or in the middle area (middle 4 columns & middle 2 rows) of board (take control of the middle is advantageous)
                    elif col + 1 <= len(state.board[0]) * 0.75 and col + 1 >= len(state.board[0]) * 0.25 and row + 1 <= len(state.board) / 2 and row + 1 >= len(state.board) / 2 :
                        result += 4
                    # or in the back row (pieces at the back row can possiblely prevent opponent from getting a king and also prevent ours pieces from being taken)
                    elif row == len(state.board) - 1 :
                        result += 0
                        
    return result


def is_game_over(state) :
    
    red_count = 0
    black_count = 0
    
    for i in range(len(state.board)) :
            for j in range(len(state.board[0])) :
                
                if state.board[i][j] == 'r' or state.board[i][j] == 'R' :
                    red_count += 1
                elif state.board[i][j] == 'b' or state.board[i][j] == 'B' :
                    black_count += 1
    
    return (red_count == 0 or black_count == 0)


def get_opponent_color(color) :
    
    if color == 'b' or color == 'B' :
        return 'r'
    
    return 'b'
    
    
        

#= ----------------------------------------------------------------------------------




# Method to compute utility value of terminal state
def compute_utility(state, color):
    
    user_util = get_util(state, color)
    opponent_util = 0
    
    if (color == 'b' or color =='B') :
        opponent_util = get_util(state, 'r')
    else :
        opponent_util = get_util(state, 'b')
    
    return (user_util - opponent_util)


# Better heuristic value of board
def compute_heuristic(state, color): 
    
    user_util = get_better_heuristic(state, color)
    opponent_util = 0
    
    if (color == 'b' or color =='B') :
        opponent_util = get_better_heuristic(state, 'r')
    else :
        opponent_util = get_better_heuristic(state, 'b')
    
    return (user_util - opponent_util)
        
    


############ MINIMAX ###############################
def minimax_min_node(state, color, limit, caching=0):
    
    state_of_BEST_move = None
    minimum_utility = float("inf")
    possible_states_of_moves = successors(state, color)
    
    # If we are caching and we have the same situation in cache
    if caching and (state, color) in cache :
        return cache[(state, color)]
    
    # Game is over or depth limit reached
    if len(possible_states_of_moves) == 0 or is_game_over(state) or limit == 0 :
        return compute_utility(state, get_opponent_color(color)), state 

    # Loop every possible state
    for next_state in possible_states_of_moves :
        
        # Get the best utility from recursive call  
        next_utility = minimax_max_node(next_state, get_opponent_color(color), limit - 1, caching)[0]
        
        # Check if it has a better utility
        if next_utility < minimum_utility :
            
            state_of_BEST_move = next_state
            minimum_utility = next_utility
    
    # If we are caching, we need to record the best move and its utility        
    if caching :
        cache[(state, color)] = minimum_utility, state_of_BEST_move
    
    return minimum_utility, state_of_BEST_move


def minimax_max_node(state, color, limit, caching=0):
    
    state_of_BEST_move = None
    maximum_utility = float("-inf")
    possible_states_of_moves = successors(state, color)
    
    # If we are caching and we have the same state in cache
    if caching and (state, color) in cache :
        return cache[(state, color)]
    
    # Game is over or depth limit reached
    if len(possible_states_of_moves) == 0 or is_game_over(state) or limit == 0 :
        return compute_utility(state, color), state
    
    # Loop every possible state
    for next_state in possible_states_of_moves :
        
        # Get the best utility from recursive call      
        next_utility = minimax_min_node(next_state, get_opponent_color(color), limit - 1, caching)[0]
        
        # Check if it has a better utility
        if next_utility > maximum_utility :
            
            state_of_BEST_move = next_state
            maximum_utility = next_utility
    
    # If we are caching, we need to record the best move and its utility      
    if caching :
        cache[(state, color)] = maximum_utility, state_of_BEST_move
    
    return maximum_utility, state_of_BEST_move


def select_move_minimax(state, color, limit, caching=0):
    """
        Given a state (of type Board) and a player color, decide on a move.
        The return value is a list of tuples [(i1,j1), (i2,j2)], where
        i1, j1 is the starting position of the piece to move
        and i2, j2 its destination.  Note that moves involving jumps will contain
        additional tuples.

        Note that other parameters are accepted by this function:
        If limit is a positive integer, your code should enforce a depth limit that is equal to the value of the parameter.
        Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
        value (see compute_utility)
        If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
        If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    cache.clear()
    return minimax_max_node(state, color, limit, caching)[1].move


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(state, color, alpha, beta, limit, caching=0, ordering=0):
    
    state_of_BEST_move = None
    minimum_utility = float("inf")
    possible_states_of_moves = successors(state, color)
    
    # If we are caching and we have the same situation in cache
    if caching and (state, color) in cache :
        return cache[(state, color)]
    
    # Game is over
    if len(possible_states_of_moves) == 0 or is_game_over(state) or limit == 0 :
        return compute_utility(state, get_opponent_color(color)), state
    
    # If we are ordering
    if ordering :
        possible_states_of_moves.sort(key = lambda x : compute_utility(x, color), reverse = False)
    
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
        return compute_utility(state, color), state
    
    # If we are ordering
    if ordering :
        possible_states_of_moves.sort(key = lambda x : compute_utility(x, color), reverse = True)

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
            

def select_move_alphabeta(state, color, limit, caching=0, ordering=0):
    """
    Given a state (of type Board) and a player color, decide on a move. 
    The return value is a list of tuples [(i1,j1), (i2,j2)], where
    i1, j1 is the starting position of the piece to move
    and i2, j2 its destination.  Note that moves involving jumps will contain
    additional tuples.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enforce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    cache.clear()
    return alphabeta_max_node(state, color, float("-inf"), float("inf"), limit, caching, ordering)[1].move


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
        if alphabeta:
            result = select_move_alphabeta(Board(state), PLAYER, limit, caching, ordering)
        else:
            result = select_move_minimax(Board(state), PLAYER, limit, caching)

        return result
