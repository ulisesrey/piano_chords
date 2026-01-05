from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
)
from PySide6.QtCore import Qt
from piano_chords.chord_generator import Chord

class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Chord selection
        self.selected_notes = set()
        self.chord_buttons = {}

        note_layout = QHBoxLayout()
        for note in Chord.NOTES:
            btn = QPushButton(note)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=note: self.toggle_note(n))
            note_layout.addWidget(btn)
            self.chord_buttons[note] = btn

        # Chord types
        self.chord_types = set()
        type_layout = QHBoxLayout()

        self.chord_type_checkboxes = {}

        # TODO: Should read from config or other file
        formulas = list(Chord.FORMULAS.keys())

        for formula in formulas:
            cb = QCheckBox(formula)
            cb.toggled.connect(
                lambda checked, ct=formula: self.toggle_type(ct, checked)
            )
            type_layout.addWidget(cb)
            self.chord_type_checkboxes[formula] = cb

        # Interval
        interval_layout = QHBoxLayout()
        interval_label = QLabel("Interval (seconds):")
        self.interval_spin = QDoubleSpinBox()
        self.interval_spin.setRange(0.1, 30)
        self.interval_spin.setSingleStep(0.1) # step size
        self.interval_spin.setDecimals(1)
        self.interval_spin.setValue(3)
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_spin)

        # Start practice button
        self.start_btn = QPushButton("Start Practice")
        self.start_btn.clicked.connect(self.start_practice)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(note_layout)
        layout.addLayout(type_layout)
        layout.addLayout(interval_layout)
        layout.addWidget(self.start_btn)
        layout.addStretch()
        self.setLayout(layout)

    def toggle_note(self, note):
        if note in self.selected_notes:
            self.selected_notes.remove(note)
        else:
            self.selected_notes.add(note)
        print("Selected notes now:", self.selected_notes)

    def toggle_type(self, chord_type, checked):
        if checked:
            print("Adding chord type:", chord_type)
            self.chord_types.add(chord_type)
        else:
            print("Removing chord type:", chord_type)
            self.chord_types.discard(chord_type)

        print("Selected types now:", self.chord_types)

    def start_practice(self):
        if not self.selected_notes or not self.chord_types:
            print("Select at least one note and chord type")
            return
        interval = self.interval_spin.value()
        self.main_window.start_practice(
            self.selected_notes, self.chord_types, interval
        )
