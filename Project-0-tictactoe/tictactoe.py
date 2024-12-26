"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
initList = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def initial_state():
    """
    Returns starting state of the board.
    """
    return initList


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initList:
        return "X"
    if terminal(board):
        return "X"
    x = 0
    o = 0
    for ls in board:
        for it in ls:
            if it == "X":
                x += 1
            elif it == "O":
                o += 1
    if x>o:
        return "O"
    return "X"

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    ret = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j]==EMPTY:
                ret.add((i, j))
    return ret


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action is None:
        raise ValueError("Action cannot be None.")
    
    i, j = action
    
    if i < 0 or i >= 3 or j < 0 or j >= 3:
        raise ValueError(f"Invalid action: {action}. Move is out of bounds.")
    
    if board[i][j] is not EMPTY:
        raise ValueError(f"Invalid action: {action}. Cell is already occupied.")

    nB = copy.deepcopy(board)
    nB[action[0]][action[1]] = player(board)
    return nB


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    won = check("O", board)
    if won:
        return "O"
    won = check("X", board)
    if won:
        return "X"
    return EMPTY

def check(player, b):
    patterns = [[[0, 0],[0, 1],[0, 2]],[[1, 0], [1, 1], [1, 2]],[[2, 0], [2, 1], [2, 2]],
                [[0, 0], [1, 0], [2, 0]], [[0, 1], [1, 1], [2, 1]], [[0, 2], [1, 2], [2, 2]],
                [[0, 0], [1, 1], [2, 2]], [[2, 0], [1, 1], [0, 2]]]
    for move in patterns:
            if b[move[0][0]][move[0][1]]!=EMPTY and b[move[1][0]][move[1][1]]!=EMPTY and b[move[2][0]][move[2][1]]!=EMPTY:
                if b[move[0][0]][move[0][1]]==player and b[move[1][0]][move[1][1]]==player and b[move[2][0]][move[2][1]]==player:
                    return True
    return False

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != EMPTY:
        return True
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j]==EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)
    return 1 if won == "X" else (-1 if won == "O" else 0)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None  

    turn = player(board)  

    if turn == "X":
        max_eval = float('-inf')
        best_action = None
        for action in actions(board):
            eval = evaluate(result(board, action), False)  
            if eval > max_eval:
                max_eval = eval
                best_action = action
        return best_action

    else:
        min_eval = float('inf')
        best_action = None
        for action in actions(board):
            eval = evaluate(result(board, action), True)  
            if eval < min_eval:
                min_eval = eval
                best_action = action
        return best_action


def evaluate(board, is_maximizing):
    """
    Returns the utility score of a given board recursively.
    """
    if terminal(board):
        return utility(board)  

    turn = player(board)

    if is_maximizing:
        max_eval = float('-inf')
        for action in actions(board):
            eval = evaluate(result(board, action), False)  
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for action in actions(board):
            eval = evaluate(result(board, action), True)  
            min_eval = min(min_eval, eval)
        return min_eval