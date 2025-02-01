"""Minimax algorithm with alpha-beta pruning that gives best move"""
import time
from board import Board, CORNERS
MAX, MIN = float('inf'), float('-inf') #Maximum and minimum score possible in reversi
TIME_OUT = 985 #Time to end
MAX_DEPTH = 4

def current_milli_time():
    return time.time()

def get_best_move(board, depth=MAX_DEPTH):
    """Returns best move in the game using minimax
    :arg
        class Board: game board right now
        int: depth of minimax, by default is 4
    :returns
        tuple(int, int): coordinates of best move
    """
    start_time = current_milli_time()
    evaluation, move = minimax(board, depth, start_time)
    return move


def minimax(board, depth, start_time, maximizing_player=True, alpha=MIN, beta=MAX):
    """Minimax algorithm looks on possible states of the game and gives the best move
    :arg
        class Board: game board right now
        int: depth of looking
        float: when algorithm started
        bool: true: is MyPlayer's turn false: opponent's turn
        float or int: -infinity from start then changes to the best evaluation for MyPlayer
        float or int: infinity from start then changes to the best evaluation for opponent\
    :returns
        int, tuple(int, int): evaluation and two coordinates of the best move
    """

    #checking current depth and time to end algorithm
    if depth == 0 or board.check_game_end() or (current_milli_time() - start_time)*1000 >= TIME_OUT:
        return rate_position(board), None

    moves = board.analyse_board()

    if maximizing_player:
        max_eval = MIN
        best_move = None

        for move in moves:
            next_board = Board(board.my_color)
            for row, count in zip(board.board, range(8)):
                next_board.board[count] = row[:]
            next_board.move(move[0], move[1])

            #looking deeper and changing turn to opponent's
            evaluation, new_move = minimax(next_board, depth - 1, start_time, False, alpha, beta)

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = MAX
        best_move = None

        for move in moves:
            next_board = Board(board.my_color)
            for row, count in zip(board.board, range(8)):
                next_board.board[count] = row[:]
            next_board.move(move[0], move[1])

            #looking deeper and changing turn to MyPlayer
            evaluation, new_move = minimax(next_board, depth - 1, start_time, True, alpha, beta)

            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move

            beta = min(beta, evaluation)
            if beta <= alpha:
                break

        return min_eval, best_move

# Returns rating of position
def rate_position(position):
    """Rates game position depending on some factors:
    :argument
        class Board: position of the game
    :returns
        int: rating of the game
    """
    #coefficients for calculating rating of position
    chips_diff_coeff = 2
    mobility_coeff = 4
    corner_coeff = 10
    edges_coeff = 5

    my_chips = 0
    opponents_chips = 0
    for row in position.board:
        my_chips += row.count(position.my_color)
        opponents_chips += row.count(position.opponent_color)
    chips_diff = my_chips - opponents_chips #different of amount of chips between players

    corners = 0
    for r,  c in CORNERS:
        if position.board[r][c] == -1:
            continue
        elif position.board[r][c] == position.my_color:
            corners += 1
        else:
            corners -= 1

    player_moves = len(position.analyse_board())
    opponent_moves = len(Board(position.opponent_color, position.board).analyse_board())
    mobility = player_moves - opponent_moves #different of amount of moves between players

    up_bottom_edges = 0
    left_right_edges = 0
    for i in [0, 7]:
        for j in range(1, 7):
            if position.board[i][j] == position.my_color:
                up_bottom_edges += 1
            elif position.board[i][j] == position.opponent_color:
                up_bottom_edges -= 1
    for j in [0, 7]:
        for i in range(1, 7):
            if position.board[i][j] == position.my_color:
                left_right_edges += 1
            elif position.board[i][j] == position.opponent_color:
                left_right_edges -= 1

    edges = up_bottom_edges + left_right_edges #how many chips are on edges of the board

    rating = chips_diff * chips_diff_coeff\
        + mobility * mobility_coeff\
        + corners * corner_coeff\
        + edges * edges_coeff

    return rating

