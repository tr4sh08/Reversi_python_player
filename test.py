from player import MyPlayer
import copy
from board import Board, BOARD_SIZE

FIRST_PLAYER = 0
SECOND_PLAYER = 1


def is_correct_move(move, board, board_size=BOARD_SIZE):
    dx = [-1, -1, -1, 0, 1, 1, 1, 0]
    dy = [-1, 0, 1, 1, 1, 0, -1, -1]
    for i in range(len(dx)):
        if confirm_direction(move, dx[i], dy[i], board, board_size):
            return True
    return False


def confirm_direction(move, dx, dy, board, board_size):
    posx = move[0] + dx
    posy = move[1] + dy
    if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
        if board[posx][posy] == 0:
            while (posx >= 0) and (posx <= (board_size - 1)) and (posy >= 0) and (posy <= (board_size - 1)):
                posx += dx
                posy += dy
                if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
                    if board[posx][posy] == -1:
                        return False
                    if board[posx][posy] == 1:
                        return True


def select_move(board):
    board_size = len(board)
    possible = []
    for x in range(board_size):
        for y in range(board_size):
            if (board[x][y] == -1) and is_correct_move([x, y], board, board_size):
                possible.append((x, y))
    return possible


def print_board(new_board):
    print('\t', end='  ')
    for i in range(8):
        print(i, end='  ')
    print()
    print('\t', end='  ')
    for i in range(8):
        print('-', end='  ')
    print()
    for r in range(8):
        print(r, '|', end='  ')
        for c in range(8):
            if new_board[r][c] == -1:
                print(' .', end=' ')
            else:
                print('', new_board[r][c], end=' ')
        print()


if __name__ == '__main__':

    main_board = [
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1,  1,  0, -1, -1, -1],
        [-1, -1, -1,  0,  1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1]
    ]

    game = Board(FIRST_PLAYER, main_board)
    print_board(main_board)
    bot = MyPlayer(FIRST_PLAYER, SECOND_PLAYER)
    who_turn = FIRST_PLAYER
    while True:
        if who_turn == FIRST_PLAYER:
            turn = bot.select_move(copy.deepcopy(game.get_board()))
            print(turn)
            if turn is not None:
                game.move(*turn)
                who_turn = SECOND_PLAYER
            else:
                print("No moves, ", SECOND_PLAYER, " turn")
                who_turn = SECOND_PLAYER
        elif who_turn == SECOND_PLAYER:
            print_board(game.get_board())
            possibles = select_move(game.board)
            print('0 player chips, 1 player chips: ', game.get_score())
            print('Possible moves')
            if possibles is not None:
                for key in list(possibles):
                    print(key, end=' ')
                print()
                row = input('your turn, choose the row ')
                column = input('choose the column ')
                if row.isdigit() and column.isdigit():
                    row = int(row)
                    column = int(column)
                else:
                    print('Incorrect move')
                    continue
                if (row, column) in possibles:
                    game.move(row, column)
                    who_turn = FIRST_PLAYER
                else:
                    print('Incorrect move')
            else:
                print("No moves, ", FIRST_PLAYER, " turn")
                who_turn = FIRST_PLAYER
        elif select_move(game.get_board()) is None:
            print("No moves")
            print_board(game.get_board())
            adv = game.get_score()
            adv = adv[0] - adv[1]
            if adv > 0:
                print("MyPlayer wins by" , adv)
            elif adv < 0:
                print("You win by", adv)
            else:
                print("Draw")
            break