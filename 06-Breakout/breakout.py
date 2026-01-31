import json
import os
import sys
from records_dialog import RecordsDialog
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem, \
    QMessageBox, QInputDialog, QLineEdit, QMenuBar, QHBoxLayout, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QPixmap, QBrush, QColor, QPen, QAction
from PySide6.QtCore import Qt, QTimer


class Breakout(QWidget):
    def __init__(self):
        super().__init__()

        self.scene_width = 780
        self.scene_height = 700

        self.score = 0
        self.lives = 3
        self.difficulty = 1

        self.setWindowTitle("Breakout")
        self.setFixedSize(self.scene_width, self.scene_height)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.menu_bar_widget = QWidget()
        self.menu_bar_layout = QHBoxLayout(self.menu_bar_widget)
        self.top_bar_widget = QWidget()
        self.top_bar_layout = QHBoxLayout(self.top_bar_widget)

        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("&File")
        records_action = QAction("Records", self)
        records_action.triggered.connect(self.show_records_window)
        file_menu.addAction(records_action)

        self.difficulty_label = QLabel(f"Difficulty: {self.difficulty}", self)
        self.difficulty_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.score_label = QLabel(f"Score: {self.score}", self)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lives_label = QLabel(f"Lives: {self.lives}", self)
        self.lives_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.menu_bar_layout.addWidget(menu_bar)
        self.top_bar_layout.addWidget(self.difficulty_label)
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.score_label)
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.lives_label)

        self.view = QGraphicsView()
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)
        self.view.setScene(self.scene)

        self.main_layout.addWidget(self.menu_bar_widget)
        self.main_layout.addWidget(self.top_bar_widget)
        self.main_layout.addWidget(self.view)

        self.bricks = []
        self.setup_bricks()

        self.paddle = None
        self.setup_paddle()

        self.ball = None
        self.setup_ball()
        self.ball_dy = -5
        self.ball_dx = 5

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()
        self.keys_pressed = set()

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_tick)

        self.start_button = QPushButton("Start")
        self.start_button.setShortcut("Space")
        self.start_button.clicked.connect(self.start_game)
        self.main_layout.addWidget(self.start_button)

    def start_game(self):
        self.start_button.hide()
        self.timer.start(16)

    def setup_bricks(self):
        for row in range(5):
            if row == 0:
                color = "red"
            elif row == 1:
                color = "blue"
            elif row == 2:
                color = "green"
            elif row == 3:
                color = "yellow"
            else:
                color = "purple"
            for col in range(12):
                brick = self.scene.addRect(0, 0, 60, 30)
                self.bricks.append(brick)
                brick.setPen(QPen(QColor("black")))
                brick.setBrush(QBrush(QColor(color)))
                brick.setPos(col * 65 , row * 35 + 50)

    def setup_ball(self):
        radius = 5
        self.ball = QGraphicsEllipseItem(0, 0, radius * 2, radius * 2)

        self.ball.setBrush(QBrush(QColor("white")))
        self.ball.setPen(QPen(QColor("white"), 2))

        self.scene.addItem(self.ball)
        self.ball.setPos(400, 500)

    def setup_paddle(self):
        paddle_pixmap = QPixmap("./assets/paddle.png").scaled(100, 20)
        self.paddle = QGraphicsPixmapItem(paddle_pixmap)
        self.scene.addItem(self.paddle)
        self.paddle.setPos((self.scene_width / 2) - (paddle_pixmap.width() / 2),
                           self.scene_height - paddle_pixmap.height() - 40)

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

    def update_ball(self):
        bx = self.ball.x()
        by = self.ball.y()
        ball_width = self.ball.boundingRect().width()
        px = self.paddle.x()
        py = self.paddle.y()
        paddle_width = self.paddle.boundingRect().width()
        paddle_height = self.paddle.boundingRect().height()

        if not (px <= bx <= (px + paddle_width)) and by > py:
            return False

        if bx <= 0 or bx >= self.scene_width - ball_width:
            self.ball_dx *= -1

        if by <= 50 :
            self.ball_dy *= -1

        if px <= bx <= (px + paddle_width) and py <= by <= (py + paddle_height):
            self.ball_dy *= -1

        self.ball.setPos(bx + self.ball_dx, by + self.ball_dy)

        return True

    def game_tick(self):
        game_is_on = self.update_ball()
        speed_additive_factor = 0 if self.difficulty == 1 else self.difficulty

        for brick in self.bricks[:]:
            if self.ball.collidesWithItem(brick):
                self.scene.removeItem(brick)
                self.bricks.remove(brick)
                self.ball_dy *= -1
                self.score = self.difficulty * 60 - len(self.bricks)
                self.score_label.setText("Score: " + str(self.score))

        if len(self.bricks) == 0:
            self.setup_bricks()
            self.difficulty += 1
            self.difficulty_label.setText("Difficulty: " + str(self.difficulty))
            self.ball_dy = -5 - speed_additive_factor
            self.ball_dx = 5 + speed_additive_factor

        step = 5 + speed_additive_factor
        x = self.paddle.x()
        if Qt.Key.Key_Left in self.keys_pressed and x > 0:
            self.paddle.setX(x - step)
        if Qt.Key.Key_Right in self.keys_pressed and x + self.paddle.boundingRect().width() < self.scene_width:
            self.paddle.setX(x + step)

        if not game_is_on:
            self.lives -= 1
            self.lives_label.setText("Lives: " + str(self.lives))
            if self.lives != 0:
                self.ball.setPos(400, 500)
                self.ball_dy = -5 - speed_additive_factor
                self.ball_dx = 5 + speed_additive_factor
            else:
                self.game_over()

    def game_over(self):
        self.timer.stop()

        msg = QMessageBox()
        msg.setWindowTitle("Game Over" + " " * 50)
        msg.setText("Score: " + str(self.score))
        msg.exec()

        reply = QMessageBox().question(self, "Save Record", "Do you want to save this record?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.save_record(self.score)

        reply = QMessageBox().question(self, "Start Again", "Do you want to start again?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.restart_game()

    def save_record(self, score):
        file_path = "records.json"

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        name, ok = QInputDialog.getText(self, "New Record!",
                                        "Enter your name:",
                                        QLineEdit.EchoMode.Normal)

        if ok and name:
            name = name.lower().strip().title()
            if name not in data or data[name] < score:
                data[name] = score

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def show_records_window(self):
        try:
            with open("records.json", "r") as file:
                data = json.load(file)
        except:
            data = {"No records yet": 0}

        dialog = RecordsDialog(data)
        dialog.exec()

    def restart_game(self):
        self.difficulty = 1
        self.difficulty_label.setText("Difficulty: " + str(self.difficulty))
        self.score = 0
        self.score_label.setText("Score: " + str(self.score))
        self.lives = 3
        self.lives_label.setText("Lives: " + str(self.lives))
        self.ball.setPos(400, 500)
        self.ball_dy = -5
        self.ball_dx = 5
        self.bricks.clear()
        self.scene.clear()
        self.setup_bricks()
        self.setup_ball()
        self.setup_paddle()
        self.keys_pressed.clear()
        self.start_button.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Breakout()
    game.show()
    sys.exit(app.exec())