import sys
import logic
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
QApplication,
QWidget,
QGridLayout,
QPushButton,
QMessageBox,
)

def set_button_image(btn, resource):
    btn.setIcon(QIcon(resource))
    btn.setIconSize(QSize(150, 150))
    btn.setEnabled(False)

def set_x_or_o(btn, row, column):
    if logic.button_action_listener(row, column) == "X":
        set_button_image(btn, "resources/X.png")
    else:
        set_button_image(btn, "resources/O.png")

def show_winner(winner):
    msg = QMessageBox()
    msg.setWindowTitle("Game Over!")
    msg.setText(f"{winner}")
    msg.setIcon(QMessageBox.Information)
    msg.exec()

def check_win_or_draw():
    some_one_won, winner = logic.check_win()
    if some_one_won:
        if winner:
            show_winner("X Player won the game!")
        else:
            show_winner("O Player won the game!")

        for btn in buttons:
            btn.setEnabled(False)

    elif logic.check_draw():
        show_winner("Draw!")

def render_x_o(btn, row, column):
    set_x_or_o(btn, row, column)
    check_win_or_draw()

def start_app():
    window.show()
    sys.exit(app.exec())

def reset_app():
    for btn in buttons:
        btn.setIcon(QIcon())
        btn.setObjectName("")
        btn.setEnabled(True)
    logic.game_reset()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Tic Tac Toe")
window.setFixedSize(600, 600)

grid = QGridLayout()
grid.setSpacing(10)
grid.setContentsMargins(10, 10, 10, 10)

window.setLayout(grid)

buttons = []
for r in range(3):
    for c in range(3):
        button = QPushButton("")
        button.setFixedSize(150, 150)
        buttons.append(button)
        grid.addWidget(button, r, c)
        button.clicked.connect(
            lambda checked=False, b=button, row=r, column=c: render_x_o(b, row, column)
        )

reset_button = QPushButton("Reset")
reset_button.setFixedSize(150, 50)
reset_button.clicked.connect(reset_app)
grid.addWidget(reset_button, 3, 2)

