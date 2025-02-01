from board import Board
from minimax import get_best_move




class MyPlayer:
    """Class MyPlyer plays reversi and uses minimax-heuristic strategy"""
    def __init__(self, my_color, opponent_color):
        self.my_color = my_color
        self.opponent_color = opponent_color


    def select_move(self, new_board):
        """Selects move using minimax-heuristic strategy"""
        return get_best_move(Board(self.my_color, new_board))
















