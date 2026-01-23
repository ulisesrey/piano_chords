from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QLineEdit,
)
from PySide6.QtCore import Qt
from piano_chords.chord_generator import Chord

class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Custom chord input
        chord_input_label = QLabel("Enter chords (e.g., Em, A, G, F#):")
        self.chord_input = QLineEdit()
        self.chord_input.setPlaceholderText("Em, A, G, F#")
        self.random_checkbox = QCheckBox("Random order")
        self.random_checkbox.setChecked(True)
        
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
        layout.addWidget(chord_input_label)
        layout.addWidget(self.chord_input)
        layout.addWidget(self.random_checkbox)
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

    def toggle_type(self, chord_type, checked):
        if checked:
            self.chord_types.add(chord_type)
        else:
            self.chord_types.discard(chord_type)

    def parse_chord_input(self):
        """Parse chord input like 'Em, A, G, F#' into list of Chord objects"""
        chord_text = self.chord_input.text().strip()
        if not chord_text:
            return []
        
        chords = []
        for chord_str in chord_text.split(','):
            chord_str = chord_str.strip()
            if not chord_str:
                continue
                
            # Parse chord symbol to root and quality
            root, quality = self.parse_chord_symbol(chord_str)
            if root and quality:
                chords.append(Chord(root, quality))
        return chords
    
    def parse_chord_symbol(self, symbol):
        """Parse chord symbol like 'Em' or 'F#' into root and quality"""
        symbol = symbol.strip()
        
        # Check for sharp notes first (2 characters)
        if len(symbol) >= 2 and symbol[1] == '#':
            root = symbol[:2]
            suffix = symbol[2:]
        else:
            root = symbol[0]
            suffix = symbol[1:]
        
        if root not in Chord.NOTES:
            return None, None
            
        # Map suffixes to quality names
        suffix_map = {
            '': 'Major',
            'm': 'Minor', 
            '°': 'Diminished',
            '+': 'Augmented',
            'maj7': 'Major 7',
            '7': 'Dominant 7',
            'm7': 'Minor 7',
            'ø7': 'Half-diminished 7',
            '°7': 'Diminished 7'
        }
        
        quality = suffix_map.get(suffix)
        return root, quality

    def start_practice(self):
        # Check if custom chords are entered
        custom_chords = self.parse_chord_input()
        if custom_chords:
            interval = self.interval_spin.value()
            random_mode = self.random_checkbox.isChecked()
            self.main_window.start_practice_with_chords(custom_chords, interval, random_mode)
        elif self.selected_notes and self.chord_types:
            interval = self.interval_spin.value()
            self.main_window.start_practice(
                self.selected_notes, self.chord_types, interval
            )
        else:
            print("Enter chords or select at least one note and chord type")
