import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chord Selector (Multi-Select)")
        self.resize(500, 200)

        self.selected_label = QLabel("Selected chords: None")
        self.selected_label.setAlignment(Qt.AlignCenter)

        self.buttons: dict[str, QPushButton] = {}
        self.selected_chords: set[str] = set()

        chords = ["A", "B", "C", "D", "E", "F", "G"]

        button_layout = QHBoxLayout()
        for chord in chords:
            button = QPushButton(chord)
            button.setCheckable(True)  # 🔑 make it toggleable
            button.clicked.connect(lambda checked, c=chord: self.toggle_chord(c))
            button_layout.addWidget(button)
            self.buttons[chord] = button

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.selected_label)

        self.setLayout(main_layout)

    def toggle_chord(self, chord: str) -> None:
        button = self.buttons[chord]
        if chord in self.selected_chords:
            self.selected_chords.remove(chord)
            button.setStyleSheet("")  # reset color
        else:
            self.selected_chords.add(chord)
            button.setStyleSheet("background-color: lightblue")  # highlight

        if self.selected_chords:
            self.selected_label.setText(
                "Selected chords: " + ", ".join(sorted(self.selected_chords))
            )
        else:
            self.selected_label.setText("Selected chords: None")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
