X_player = True

def button_action_listener(btn):
    global X_player
    X_player = not X_player
    if X_player:
        return 'X'
    else:
        return 'O'

def check_win(buttons):
    if buttons[0].objectName() == buttons[1].objectName() == buttons[2].objectName() and buttons[0].objectName() != "":
        return [True, X_player]

    elif buttons[3].objectName() == buttons[4].objectName() == buttons[5].objectName() and buttons[3].objectName() != "":
        return [True, X_player]

    elif buttons[6].objectName() == buttons[7].objectName() == buttons[8].objectName() and buttons[6].objectName() != "":
        return [True, X_player]

    elif buttons[0].objectName() == buttons[3].objectName() == buttons[6].objectName() and buttons[0].objectName() != "":
        return [True, X_player]

    elif buttons[1].objectName() == buttons[4].objectName() == buttons[7].objectName() and buttons[1].objectName() != "":
        return [True, X_player]

    elif buttons[2].objectName() == buttons[5].objectName() == buttons[8].objectName() and buttons[2].objectName() != "":
        return [True, X_player]

    elif buttons[0].objectName() == buttons[4].objectName() == buttons[8].objectName() and buttons[0].objectName() != "":
        return [True, X_player]

    elif buttons[2].objectName() == buttons[4].objectName() == buttons[6].objectName() and buttons[2].objectName() != "":
        return [True, X_player]

    else:
        return [False, X_player]

def check_draw(buttons):
    for btn in buttons:
        if btn.objectName() == "":
            return False
    return True