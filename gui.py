import sys
import math
import random
import pandas as pd

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider
)
from PySide6.QtCore import Qt, QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Rectangle


class CricketReplayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(r"C:\Users\iadar\OneDrive\Desktop\cricket_match_replay\data\mockData.csv")
        self.total_balls = len(self.df)

        self.current_ball = 0
        self.total_runs = 0
        self.wickets = 0
        self.setWindowTitle("🏏 Cricket Match Replay")
        self.setGeometry(200, 200, 650, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Arial;
            }
            QLabel {
                padding: 6px;
            }
            QPushButton {
                background-color: #2563eb;
                padding: 8px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        self.main_layout = QVBoxLayout()
        title = QLabel("🏏 Cricket Match Replay")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(title)

        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(self.score_label)

        self.over_label = QLabel("Over: 0.0")
        self.over_label.setStyleSheet("font-size: 14px; color: #cbd5f5;")
        self.main_layout.addWidget(self.over_label)

        self.replay_label = QLabel("Press ▶ Play or Next Ball to start replay")
        self.replay_label.setWordWrap(True)
        self.replay_label.setStyleSheet("font-size: 16px;")
        self.main_layout.addWidget(self.replay_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.total_balls)
        self.slider.valueChanged.connect(self.seek_ball)
        self.main_layout.addWidget(self.slider)

        self.field_fig = Figure(figsize=(4, 4))
        self.field_canvas = FigureCanvas(self.field_fig)
        self.field_ax = self.field_fig.add_subplot(111)
        self.main_layout.addWidget(self.field_canvas)
        self.draw_field()

        self.status_label = QLabel("Ball: 0 / 0")
        self.status_label.setStyleSheet("font-size: 13px; color: #cbd5f5;")
        self.main_layout.addWidget(self.status_label)

        btn_layout = QHBoxLayout()

        self.play_button = QPushButton("▶ Play")
        self.play_button.clicked.connect(self.toggle_play)

        next_btn = QPushButton("Next Ball")
        next_btn.clicked.connect(self.show_next_ball)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_replay)

        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self.close)

        btn_layout.addWidget(self.play_button)
        btn_layout.addWidget(next_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(quit_btn)

        self.main_layout.addLayout(btn_layout)
        self.setLayout(self.main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_ball)

        self.update_status()

    def draw_field(self):
        self.field_ax.clear()
        self.field_ax.add_patch(Circle((0, 0), 75, fill=False, linewidth=2, color="white"))
        self.field_ax.add_patch(
            Circle((0, 0), 30, fill=False, linestyle="--", color="#94a3b8")
        )
        self.field_ax.add_patch(
            Rectangle((-3, -20), 6, 40, color="#a16207", alpha=0.85)
        )
        self.field_ax.scatter(0, 0, color="white", s=30)

        self.field_ax.set_xlim(-80, 80)
        self.field_ax.set_ylim(-80, 80)
        self.field_ax.set_aspect("equal")
        self.field_ax.axis("off")
        self.field_ax.set_title("Field View", color="white")

        self.field_canvas.draw()

    def animate_ball(self, runs):
        self.draw_field()

        if runs == 0:
            return

        angle = random.uniform(0, 2 * math.pi)

        if runs == 6:
            distance, color, width = 70, "#ef4444", 3
        elif runs == 4:
            distance, color, width = 55, "#22c55e", 2.5
        else:
            distance, color, width = 35, "#38bdf8", 2

        x = distance * math.cos(angle)
        y = distance * math.sin(angle)

        self.field_ax.plot([0, x], [0, y], color=color, linewidth=width)
        self.field_ax.scatter(x, y, color=color, s=60, edgecolors="white", zorder=5)

        self.field_canvas.draw()

    def calculate_state_until(self, index):
        self.total_runs = 0
        self.wickets = 0
        for i in range(index):
            self.total_runs += self.df.iloc[i]["runs"]
            if self.df.iloc[i]["is_wicket"] == 1:
                self.wickets += 1

    def show_next_ball(self):
        if self.current_ball >= self.total_balls:
            self.replay_label.setText("🏁 Match Finished")
            self.timer.stop()
            self.play_button.setText("▶ Play")
            return

        self.current_ball += 1
        self.calculate_state_until(self.current_ball)

        row = self.df.iloc[self.current_ball - 1]
        event = "WICKET!" if row["is_wicket"] == 1 else f"{row['runs']} run(s)"

        self.replay_label.setText(
            f"{row['over']}.{row['ball']} → {row['batsman']} vs {row['bowler']} : {event}"
        )
        self.score_label.setText(f"Score: {self.total_runs} / {self.wickets}")
        self.over_label.setText(f"Over: {row['over']}.{row['ball']}")

        self.animate_ball(row["runs"])
        self.slider.setValue(self.current_ball)
        self.update_status()

    def seek_ball(self, value):
        self.timer.stop()
        self.play_button.setText("▶ Play")

        self.current_ball = value
        self.calculate_state_until(self.current_ball)

        if value == 0:
            self.draw_field()
            self.replay_label.setText("Start of match")
        else:
            self.animate_ball(self.df.iloc[value - 1]["runs"])

        self.update_status()

    def toggle_play(self):
        if self.timer.isActive():
            self.timer.stop()
            self.play_button.setText("▶ Play")
        else:
            self.timer.start(1000)
            self.play_button.setText("⏸ Pause")

    def reset_replay(self):
        self.timer.stop()
        self.current_ball = 0
        self.total_runs = 0
        self.wickets = 0

        self.slider.setValue(0)
        self.play_button.setText("▶ Play")
        self.replay_label.setText("Replay reset. Press ▶ Play.")
        self.score_label.setText("Score: 0 / 0")
        self.over_label.setText("Over: 0.0")

        self.draw_field()
        self.update_status()

    def update_status(self):
        self.status_label.setText(f"Ball: {self.current_ball} / {self.total_balls}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CricketReplayApp()
    window.show()
    sys.exit(app.exec())
