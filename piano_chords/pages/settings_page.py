from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QDoubleSpinBox,
    QLineEdit,
    QComboBox,
    QGroupBox,
)
import yaml
import os
from PySide6.QtCore import Qt
from piano_chords.chord_generator import Chord

class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Option 1: Select Progression
        progression_group = QGroupBox("Option 1: Select a Progression")
        progression_layout = QVBoxLayout()
        
        self.progression_combo = QComboBox()
        self.progression_combo.addItem("-- Select Progression --")
        self.load_progressions()
        self.progression_combo.currentTextChanged.connect(self.on_progression_selected)
        
        root_layout = QHBoxLayout()
        root_label = QLabel("Root note:")
        self.root_combo = QComboBox()
        for note in Chord.NOTES:
            self.root_combo.addItem(note)
        self.root_combo.currentTextChanged.connect(self.on_root_changed)
        root_layout.addWidget(root_label)
        root_layout.addWidget(self.root_combo)
        
        self.preview_label = QLabel("")
        self.preview_label.setStyleSheet("color: gray; font-style: italic;")
        self.preview_label.setWordWrap(True)
        
        progression_layout.addWidget(QLabel("Progression:"))
        progression_layout.addWidget(self.progression_combo)
        progression_layout.addLayout(root_layout)
        progression_layout.addWidget(QLabel("Preview:"))
        progression_layout.addWidget(self.preview_label)
        progression_group.setLayout(progression_layout)
        
        # Option 2: Custom Input
        custom_group = QGroupBox("Option 2: Input Your Chord Progression")
        custom_layout = QVBoxLayout()
        
        self.chord_input = QLineEdit()
        self.chord_input.setPlaceholderText("Em, A, G, F#")
        
        custom_layout.addWidget(self.chord_input)
        custom_group.setLayout(custom_layout)
        
        # Common settings
        settings_layout = QHBoxLayout()
        
        self.random_checkbox = QCheckBox("Random order")
        self.random_checkbox.setChecked(True)
        
        interval_label = QLabel("Interval (seconds):")
        self.interval_spin = QDoubleSpinBox()
        self.interval_spin.setRange(0.1, 30)
        self.interval_spin.setSingleStep(0.1)
        self.interval_spin.setDecimals(1)
        self.interval_spin.setValue(3)
        
        settings_layout.addWidget(self.random_checkbox)
        settings_layout.addWidget(interval_label)
        settings_layout.addWidget(self.interval_spin)
        settings_layout.addStretch()

        # Start practice button
        self.start_btn = QPushButton("Start Practice")
        self.start_btn.clicked.connect(self.start_practice)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(progression_group)
        layout.addWidget(custom_group)
        layout.addLayout(settings_layout)
        layout.addWidget(self.start_btn)
        layout.addStretch()
        self.setLayout(layout)

    def load_progressions(self):
        """Load chord progressions from YAML file"""
        try:
            yaml_path = os.path.join(os.path.dirname(__file__), '..', 'progressions.yaml')
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                for name in data['progressions'].keys():
                    self.progression_combo.addItem(name)
        except Exception as e:
            print(f"Could not load progressions: {e}")
    
    def on_progression_selected(self, progression_name):
        """Load selected progression into chord input"""
        if progression_name == "-- Select Progression --":
            self.preview_label.setText("")
            return
        self.transpose_and_load_progression()
    
    def on_root_changed(self):
        """Transpose progression when root changes"""
        if self.progression_combo.currentText() != "-- Select Progression --":
            self.transpose_and_load_progression()
    
    def transpose_and_load_progression(self):
        """Transpose progression to selected root"""
        progression_name = self.progression_combo.currentText()
        root = self.root_combo.currentText()
        
        try:
            yaml_path = os.path.join(os.path.dirname(__file__), '..', 'progressions.yaml')
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                progression = data['progressions'].get(progression_name, "")
                transposed = self.transpose_progression(progression, root)
                self.preview_label.setText(transposed)
        except Exception as e:
            print(f"Could not load progression: {e}")
    
    def transpose_progression(self, progression, root):
        """Transpose Roman numeral progression to specific root"""
        # If already in chord notation, return as is
        if not any(numeral in progression for numeral in ['I', 'V', 'i', 'v', 'ii', 'iii', 'iv', 'vi', 'vii']):
            return progression
        
        root_idx = Chord.NOTES.index(root)
        
        # Major scale intervals
        major_intervals = {'I': 0, 'ii': 2, 'iii': 4, 'IV': 5, 'V': 7, 'vi': 9, 'vii': 11, 'bVII': 10, 'bIII': 3}
        quality_map = {'I': '', 'ii': 'm', 'iii': 'm', 'IV': '', 'V': '', 'vi': 'm', 'vii': '°', 'i': 'm', 'bVII': '', 'bIII': ''}
        
        result = []
        for chord in progression.split(','):
            chord = chord.strip()
            
            # Parse Roman numeral
            numeral = chord.rstrip('7maj+°ø')
            suffix = chord[len(numeral):]
            
            if numeral in major_intervals:
                interval = major_intervals[numeral]
                chord_root = Chord.NOTES[(root_idx + interval) % 12]
                base_quality = quality_map.get(numeral, '')
                result.append(f"{chord_root}{suffix if suffix else base_quality}")
            else:
                result.append(chord)
        
        return ', '.join(result)
    
    def parse_chord_text(self, chord_text):
        """Parse chord text into list of Chord objects"""
        chord_text = chord_text.strip()
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
    
    def parse_chord_input(self):
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
        # Check if progression is selected (Option 1)
        if self.progression_combo.currentText() != "-- Select Progression --" and self.preview_label.text():
            chords_text = self.preview_label.text()
            custom_chords = self.parse_chord_text(chords_text)
            if custom_chords:
                interval = self.interval_spin.value()
                random_mode = self.random_checkbox.isChecked()
                progression_title = self.progression_combo.currentText()
                self.main_window.start_practice_with_chords(custom_chords, interval, random_mode, progression_title)
                return
        
        # Check if custom chords are entered (Option 2)
        custom_chords = self.parse_chord_input()
        if custom_chords:
            interval = self.interval_spin.value()
            random_mode = self.random_checkbox.isChecked()
            self.main_window.start_practice_with_chords(custom_chords, interval, random_mode, None)
        else:
            print("Select a progression or enter custom chords")
