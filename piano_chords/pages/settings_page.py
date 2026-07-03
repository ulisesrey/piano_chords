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
import sys
from PySide6.QtCore import Qt
from piano_chords.chord_generator import Chord

class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.progressions_data = {}  # Cache for progressions
        
        # Set minimum size for better layout
        self.setMinimumWidth(750)

        # Option 1: Select Progression (Light Green Background)
        progression_group = QGroupBox("Option 1: Select a Progression")
        progression_group.setStyleSheet("""
            QGroupBox { 
                font-size: 18px; 
                font-weight: bold; 
                padding-top: 15px;
                background-color: rgba(76, 175, 80, 0.15);
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel { font-size: 17px; }
        """)
        progression_layout = QVBoxLayout()
        progression_layout.setSpacing(12)
        
        self.progression_combo = QComboBox()
        self.progression_combo.setMinimumHeight(45)
        self.progression_combo.setStyleSheet("QComboBox { font-size: 17px; }")
        self.progression_combo.addItem("-- Select Progression --")
        self.load_progressions()
        self.progression_combo.currentTextChanged.connect(self.on_progression_selected)
        
        root_layout = QHBoxLayout()
        root_label = QLabel("Root note:")
        self.root_combo = QComboBox()
        self.root_combo.setMinimumHeight(45)
        self.root_combo.setStyleSheet("QComboBox { font-size: 17px; }")
        for note in Chord.NOTES:
            self.root_combo.addItem(note)
        self.root_combo.currentTextChanged.connect(self.on_root_changed)
        root_layout.addWidget(root_label)
        root_layout.addWidget(self.root_combo)
        
        voicing_layout = QHBoxLayout()
        voicing_label = QLabel("Voicing:")
        self.voicing_combo = QComboBox()
        self.voicing_combo.setMinimumHeight(45)
        self.voicing_combo.setStyleSheet("QComboBox { font-size: 17px; }")
        self.voicing_combo.addItem("Triads")
        self.voicing_combo.addItem("7th Chords")
        self.voicing_combo.currentTextChanged.connect(self.on_voicing_changed)
        voicing_layout.addWidget(voicing_label)
        voicing_layout.addWidget(self.voicing_combo)
        
        self.preview_label = QLabel("")
        self.preview_label.setStyleSheet("color: #333; font-style: italic; font-size: 17px; padding: 12px; background-color: white; border-radius: 5px; border: 1px solid #ddd;")
        self.preview_label.setWordWrap(True)
        self.preview_label.setMinimumHeight(55)
        self.preview_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Make text selectable
        
        self.start_progression_btn = QPushButton("▶ Start Practice")
        self.start_progression_btn.setMinimumHeight(55)
        self.start_progression_btn.setStyleSheet("QPushButton { font-size: 18px; font-weight: bold; background-color: #4CAF50; color: white; border-radius: 5px; } QPushButton:hover { background-color: #45a049; }")
        self.start_progression_btn.clicked.connect(self.start_progression_practice)
        
        progression_layout.addWidget(QLabel("Progression:"))
        progression_layout.addWidget(self.progression_combo)
        progression_layout.addLayout(root_layout)
        progression_layout.addLayout(voicing_layout)
        progression_layout.addWidget(QLabel("Preview:"))
        progression_layout.addWidget(self.preview_label)
        progression_layout.addWidget(self.start_progression_btn)
        progression_group.setLayout(progression_layout)
        
        # Option 2: Custom Input (Light Blue Background)
        custom_group = QGroupBox("Option 2: Input Your Chord Progression")
        custom_group.setStyleSheet("""
            QGroupBox { 
                font-size: 18px; 
                font-weight: bold; 
                padding-top: 15px;
                background-color: rgba(33, 150, 243, 0.15);
                border: 2px solid #2196F3;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel { font-size: 17px; }
        """)
        custom_layout = QVBoxLayout()
        custom_layout.setSpacing(12)
        
        self.chord_input = QLineEdit()
        self.chord_input.setPlaceholderText("Em, A, G, F#")
        self.chord_input.setMinimumHeight(45)
        self.chord_input.setStyleSheet("QLineEdit { font-size: 17px; padding: 8px; }")
        
        self.start_custom_btn = QPushButton("▶ Start Practice")
        self.start_custom_btn.setMinimumHeight(55)
        self.start_custom_btn.setStyleSheet("QPushButton { font-size: 18px; font-weight: bold; background-color: #2196F3; color: white; border-radius: 5px; } QPushButton:hover { background-color: #0b7dda; }")
        self.start_custom_btn.clicked.connect(self.start_custom_practice)
        
        custom_layout.addWidget(self.chord_input)
        custom_layout.addWidget(self.start_custom_btn)
        custom_group.setLayout(custom_layout)
        
        # Common settings
        settings_group = QGroupBox("Settings")
        settings_group.setStyleSheet("""
            QGroupBox { 
                font-size: 18px; 
                font-weight: bold; 
                padding-top: 15px;
                border: 2px solid #999;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(20)
        
        self.random_checkbox = QCheckBox("Random order")
        self.random_checkbox.setChecked(False)
        self.random_checkbox.setStyleSheet("QCheckBox { font-size: 17px; }")
        
        interval_label = QLabel("Interval (seconds):")
        interval_label.setStyleSheet("QLabel { font-size: 17px; }")
        self.interval_spin = QDoubleSpinBox()
        self.interval_spin.setRange(0.1, 30)
        self.interval_spin.setSingleStep(1.0)
        self.interval_spin.setDecimals(1)
        self.interval_spin.setValue(3)
        self.interval_spin.setMinimumHeight(40)
        self.interval_spin.setStyleSheet("QDoubleSpinBox { font-size: 17px; }")
        
        settings_layout.addWidget(self.random_checkbox)
        settings_layout.addWidget(interval_label)
        settings_layout.addWidget(self.interval_spin)
        settings_layout.addStretch()
        settings_group.setLayout(settings_layout)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.addWidget(progression_group)
        layout.addWidget(custom_group)
        layout.addWidget(settings_group)
        layout.addStretch()
        self.setLayout(layout)
        
        # Set default progression after UI is initialized
        if self.progression_combo.count() > 1:
            self.progression_combo.setCurrentIndex(1)

    def load_progressions(self):
        """Load chord progressions from YAML file"""
        try:
            # Handle PyInstaller bundled path
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(__file__)
                """Because __file__ is calling the path of the current file (settings_page.py)
                we don't get the path of progression.yaml (which is one directory up)"""
                corrected_path = base_path[:-len("/pages")]
            yaml_path = os.path.join(corrected_path, 'progressions.yaml')
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                self.progressions_data = data.get('progressions', {})
                for name in self.progressions_data.keys():
                    self.progression_combo.addItem(name)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Could not load progressions: {e}")
            self.progressions_data = {}
    
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
    
    def on_voicing_changed(self):
        """Update progression when voicing changes"""
        if self.progression_combo.currentText() != "-- Select Progression --":
            self.transpose_and_load_progression()
    
    def transpose_and_load_progression(self):
        """Transpose progression to selected root"""
        progression_name = self.progression_combo.currentText()
        root = self.root_combo.currentText()
        voicing = self.voicing_combo.currentText()
        
        progression = self.progressions_data.get(progression_name, "")
        if progression:
            transposed = self.transpose_progression(progression, root, voicing)
            self.preview_label.setText(transposed)
    
    def transpose_progression(self, progression, root, voicing="Triads"):
        """Transpose Roman numeral progression to specific root"""
        # If already in chord notation, return as is
        if not any(numeral in progression for numeral in ['I', 'V', 'i', 'v', 'ii', 'iii', 'iv', 'vi', 'vii']):
            return progression
        
        root_idx = Chord.NOTES.index(root)
        
        # Major scale intervals
        major_intervals = {'I': 0, 'ii': 2, 'iii': 4, 'IV': 5, 'V': 7, 'vi': 9, 'vii': 11, 'bVII': 10, 'bIII': 3}
        quality_map = {'I': '', 'ii': 'm', 'iii': 'm', 'IV': '', 'V': '', 'vi': 'm', 'vii': '°', 'i': 'm', 'bVII': '', 'bIII': ''}
        
        # 7th chord extensions
        seventh_map = {'I': 'maj7', 'ii': '7', 'iii': '7', 'IV': 'maj7', 'V': '7', 'vi': '7', 'vii': '7', 'i': '7', 'bVII': '7', 'bIII': 'maj7'}
        
        result = []
        for chord in progression.split(','):
            chord = chord.strip()
            
            # Parse Roman numeral
            numeral = chord.rstrip('7maj+°ø')
            suffix = chord[len(numeral):]
            
            if numeral in major_intervals:
                interval = major_intervals[numeral]
                chord_root = Chord.NOTES[(root_idx + interval) % 12]
                
                if voicing == "7th Chords" and not suffix:
                    # Add 7th extension
                    base_quality = quality_map.get(numeral, '')
                    seventh = seventh_map.get(numeral, '7')
                    result.append(f"{chord_root}{base_quality}{seventh}")
                else:
                    # Use original suffix or base quality
                    base_quality = quality_map.get(numeral, '')
                    result.append(f"{chord_root}{suffix if suffix else base_quality}")
            else:
                result.append(chord)
        
        return ', '.join(result)
    
    def start_progression_practice(self):
        """Start practice with selected progression"""
        if self.progression_combo.currentText() != "-- Select Progression --" and self.preview_label.text():
            chords_text = self.preview_label.text()
            custom_chords = self.parse_chord_text(chords_text)
            if custom_chords:
                interval = self.interval_spin.value()
                random_mode = self.random_checkbox.isChecked()
                progression_title = self.progression_combo.currentText()
                self.main_window.start_practice_with_chords(custom_chords, interval, random_mode, progression_title)
        else:
            print("Select a progression first")
    
    def start_custom_practice(self):
        """Start practice with custom chord input"""
        custom_chords = self.parse_chord_input()
        if custom_chords:
            interval = self.interval_spin.value()
            random_mode = self.random_checkbox.isChecked()
            self.main_window.start_practice_with_chords(custom_chords, interval, random_mode, None)
        else:
            print("Enter custom chords first")
    
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
