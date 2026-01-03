import random
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer


class PracticePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.selected_notes = []
        self.chord_types = []
        self.interval = 5

        # Label for the chord
        self.chord_label = QLabel("")
        self.chord_label.setAlignment(Qt.AlignCenter)
        self.chord_label.setStyleSheet("font-size: 72px; color: darkgreen;")

        # Back button
        self.back_btn = QPushButton("Back to Settings")
        self.back_btn.clicked.connect(self.back_to_settings)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.chord_label)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_chord)

    def setup(self, selected_notes, chord_types, interval):
        """Called when practice starts"""
        self.selected_notes = list(selected_notes)
        self.chord_types = list(chord_types)
        self.interval = interval * 1000  # milliseconds
        self.next_chord()
        self.timer.start(self.interval)

    def next_chord(self):
        """Pick a random chord to display"""
        if not self.selected_notes or not self.chord_types:
            self.chord_label.setText("No chords selected")
            return
        note = random.choice(self.selected_notes)
        ctype = random.choice(self.chord_types)
        if ctype == "Major":
            self.chord_label.setText(f"{note}  ")
        if ctype == "Minor":
            self.chord_label.setText(f"{note}m")

    def back_to_settings(self):
        self.timer.stop()
        self.main_window.back_to_settings()
