X_player = False

board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""],
]

def button_action_listener(row, column):
    global X_player
    X_player = not X_player
    if X_player:
        board[row][column] = "X"
        return 'X'
    else:
        board[row][column] = "O"
        return 'O'

def check_win():
    if board[0][0] == board[0][1] == board[0][2] and board[0][0] != "":
        return [True, X_player]

    elif board[1][0] == board[1][1] == board[1][2] and board[1][0] != "":
        return [True, X_player]

    elif board[2][0] == board[2][1] == board[2][2] and board[2][0] != "":
        return [True, X_player]

    elif board[0][0] == board[1][0] == board[2][0] and board[0][0] != "":
        return [True, X_player]

    elif board[0][1] == board[1][1] == board[2][1] and board[0][1] != "":
        return [True, X_player]

    elif board[0][2] == board[1][2] == board[2][2] and board[0][2] != "":
        return [True, X_player]

    elif board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return [True, X_player]

    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return [True, X_player]

    else:
        return [False, X_player]

def check_draw():
    for row in range(3):
        for column in range(3):
            if board[row][column] == "":
                return False
    return True

def game_reset():
    global X_player
    global board
    X_player = False
    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
    ]