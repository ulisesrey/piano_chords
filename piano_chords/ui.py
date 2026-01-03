import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chord Selector")
        self.resize(800, 800)
        self.selected_label = QLabel("Selected chord: None")
        self.selected_label.setAlignment(Qt.AlignCenter)
        self.buttons: dict[str, QPushButton] = {}

        chords = ["A", "B", "C", "D", "E", "F", "G"]

        button_layout = QHBoxLayout()

        for chord in chords:
            button = QPushButton(chord)
            button.clicked.connect(lambda _, c=chord: self.select_chord(c))
            button_layout.addWidget(button)
            self.buttons[chord] = button
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.selected_label)

        self.setLayout(main_layout)
    
    def select_chord(self, chord: str) -> None:
        self.selected_label.setText(f"Selected chord: {chord}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
