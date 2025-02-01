"""Contains class Board with function to analyse it"""

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
CORNERS = ((7, 0), (0, 7), (0, 0), (7, 7))
BOARD_SIZE = 8
P1_COLOR = 0
P2_COLOR = 1


class Board:
    """class that represents game board to simulate the game"""
    def __init__(self, current_player, board=None):
        if board is None:
            self.board = [[] for _ in range(BOARD_SIZE)]
            for row in range(BOARD_SIZE):
                self.board[row] = [0] * BOARD_SIZE
        else:
            self.board = board
        self.my_color = current_player
        self.opponent_color = int(not self.my_color)



    def flip_chips(self, row, col):
        """flip chips in right directions"""
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            to_flip = []
            while valid_indices(r, c) and self.board[r][c] == self.opponent_color:
                to_flip.append((r, c))
                r += dr
                c += dc
                if valid_indices(r, c) and self.board[r][c] == self.my_color:
                    for fr, fc in to_flip:
                        self.board[fr][fc] = self.my_color

    def is_right_move(self, row, column):
        if self.board[row][column] != -1:
            return False
        for dr, dc in DIRECTIONS:
            r, c = row + dr, column + dc
            while valid_indices(r, c) and self.board[r][c] == self.opponent_color:
                r += dr
                c += dc
                if valid_indices(r, c) and self.board[r][c] == self.my_color:
                    return True
        return False

    def move(self, row, col):
        if self.is_right_move(row, col):
            self.board[row][col] = self.my_color
            self.flip_chips(row, col)
            self.my_color, self.opponent_color = self.opponent_color, self.my_color
        else:
            return False

    def analyse_board(self):
        """Gives list of moves
        :returns
            list(tuples(int, int)): list of tuples with coordinates of moves
        """
        moves = []
        for r in range(8):
            for c in range(8):
                if self.is_right_move(r, c):
                    moves.append((r, c))
        return moves

    def check_game_end(self):
        return not self.analyse_board()

    def get_board(self):
        return self.board

    def get_score(self):
        stones = [0 , 0]
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == 0:
                    stones[0] += 1
                if self.board[x][y] == 1:
                    stones[1] += 1
        return stones

def valid_indices(r, c):
    """checks validity of indexes"""
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


