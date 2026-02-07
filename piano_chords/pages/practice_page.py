import random
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer, Signal
from piano_chords.midi_input import MidiListener
from piano_chords.chord_generator import Chord

class PracticePage(QWidget):

    note_pressed = Signal(tuple)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.selected_roots = [] 
        self.chord_types = []
        self.custom_chords = []
        self.random_mode = True
        self.chord_index = 0
        self.progression_title = None
        self.interval = 5

        self.previous_chord = None
        self.current_pressed = set()
        self.chord_completed = False
        self.first_note_pressed = False
        self.current_chord = None

        # Blinking
        self.blink_timer = QTimer()
        self.blink_timer.setSingleShot(True)
        self.blink_timer.timeout.connect(self.show_chord_label)
        
        # Feedback delay timer
        self.feedback_timer = QTimer()
        self.feedback_timer.setSingleShot(True)
        self.feedback_timer.timeout.connect(self.update_feedback)

        # MIDI error label (top)
        self.midi_error_label = QLabel("")
        self.midi_error_label.setAlignment(Qt.AlignCenter)
        self.midi_error_label.setStyleSheet("color: red; font-size: 20px; font-weight: bold; padding: 10px;")

        # Progression title label
        self.title_label = QLabel("")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; color: #2c3e50; font-weight: bold; padding: 15px;")

        # Label for the chord (MAIN ELEMENT - vertically centered)
        self.chord_label = QLabel("")
        self.chord_label.setAlignment(Qt.AlignCenter)
        self.chord_label.setStyleSheet("font-size: 280px; color: #27ae60; font-weight: bold;")
        self.chord_label.setMinimumHeight(400)

        # Feedback label
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 120px; font-weight: bold; padding: 20px;")
        self.feedback_label.setMinimumHeight(150)

        # Midi listener
        self.midi_listener = MidiListener(
            self.on_midi_input,
            error_callback=self.on_midi_error
            )
        self.note_pressed.connect(self.on_note_pressed)

        # Back button
        self.back_btn = QPushButton("← Back to Settings")
        self.back_btn.setMinimumHeight(60)
        self.back_btn.setStyleSheet("""
            QPushButton { 
                font-size: 18px; 
                font-weight: bold; 
                background-color: #95a5a6; 
                color: white; 
                border-radius: 8px;
                padding: 10px;
            } 
            QPushButton:hover { 
                background-color: #7f8c8d; 
            }
        """)
        self.back_btn.clicked.connect(self.back_to_settings)

        # Layout with proper spacing and centering
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(30, 20, 30, 30)
        
        layout.addWidget(self.midi_error_label)
        layout.addWidget(self.title_label)
        layout.addStretch(1)  # Push chord to center
        layout.addWidget(self.chord_label)
        layout.addStretch(1)  # Keep chord centered
        layout.addWidget(self.feedback_label)
        layout.addStretch(1)
        layout.addWidget(self.back_btn)
        
        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_chord)

    def setup(self, selected_roots, chord_types, interval):
        """Called when practice starts with note/type selection"""
        self.selected_roots = list(selected_roots)
        self.chord_types = list(chord_types)
        self.custom_chords = []
        self.random_mode = True
        self.chord_index = 0
        self.progression_title = None
        self.interval = interval * 1000
        
        self.title_label.setText("")
        self.feedback_label.setText("Get ready..")
        self.feedback_label.setStyleSheet("font-size: 60px; color: #3498db; font-weight: bold; padding: 20px;")
        self.next_chord()
        self.timer.start(self.interval)
        self.midi_error_label.setText("")
        self.midi_listener.start()
    
    def setup_with_chords(self, chords, interval, random_mode, progression_title=None):
        """Called when practice starts with custom chord input"""
        self.custom_chords = chords
        self.random_mode = random_mode
        self.chord_index = 0
        self.progression_title = progression_title
        self.selected_roots = []
        self.chord_types = []
        self.interval = interval * 1000
        
        if self.progression_title:
            self.title_label.setText(self.progression_title)
        else:
            self.title_label.setText("")
        
        self.feedback_label.setText("Get ready..")
        self.feedback_label.setStyleSheet("font-size: 60px; color: #3498db; font-weight: bold; padding: 20px;")
        self.next_chord()
        self.timer.start(self.interval)
        self.midi_error_label.setText("")
        self.midi_listener.start()

    def on_midi_error(self, message):
        self.midi_error_label.setText(
            f"⚠️ MIDI Error: {message}\nPlease connect a MIDI keyboard and restart."
        )

    def next_chord(self):
        """Pick a random chord to display"""
        if self.custom_chords:
            if self.random_mode:
                self.current_chord = random.choice(self.custom_chords)
            else:
                self.current_chord = self.custom_chords[self.chord_index]
                self.chord_index = (self.chord_index + 1) % len(self.custom_chords)
        elif self.selected_roots and self.chord_types:
            root = random.choice(self.selected_roots)
            quality = random.choice(self.chord_types)
            self.current_chord = Chord(root, quality)
        else:
            self.chord_label.setText("No chords selected")
            return

        if self.random_mode and self.current_chord == self.previous_chord and len(self.custom_chords if self.custom_chords else self.selected_roots) > 1:
            if self.custom_chords:
                available = [c for c in self.custom_chords if c != self.previous_chord]
                if available:
                    self.current_chord = random.choice(available)
            else:
                idx = self.selected_roots.index(self.current_chord.root)
                next_idx = (idx + 1) % len(self.selected_roots)
                self.current_chord = Chord(self.selected_roots[next_idx], self.current_chord.quality)

        self.previous_chord = self.current_chord

        # Blink effect
        self.chord_label.setText("")
        self.feedback_label.setText("")
        self.current_pressed.clear()
        self.chord_completed = False
        self.first_note_pressed = False
        self.feedback_timer.stop()

        self.blink_timer.start(250)

    def show_chord_label(self):
        self.chord_label.setText(self.current_chord.symbol)

    def on_midi_input(self, msg):
        note_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 
                    'F#', 'G', 'G#', 'A', 'A#', 'B'][msg.note % 12]
        if msg.type == 'note_on' and msg.velocity > 0:
            self.note_pressed.emit(("on", note_name))
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            self.note_pressed.emit(("off", note_name))

    def on_note_pressed(self, msg):
        action, note_name = msg
        if action == "on":
            self.current_pressed.add(note_name)
            if set(self.current_chord.notes).issubset(self.current_pressed):
                self.feedback_timer.stop()
                self.show_correct_feedback()
            else:
                if not self.first_note_pressed:
                    self.first_note_pressed = True
                self.feedback_timer.stop()
                self.feedback_timer.start(150)
        else:
            self.current_pressed.discard(note_name)
            if self.first_note_pressed and not self.chord_completed:
                self.feedback_timer.stop()
                self.feedback_timer.start(150)

    def update_feedback(self):
        """Called after delay to show initial feedback"""
        self.check_chord()
    
    def show_correct_feedback(self):
        """Show correct feedback immediately"""
        self.chord_completed = True
        self.feedback_label.setText("✓ Correct!")
        self.feedback_label.setStyleSheet("color: #27ae60; font-size: 120px; font-weight: bold; padding: 20px;")
    
    def check_chord(self):
        if not self.current_chord:
            return

        required_notes = set(self.current_chord.notes)
        pressed_correct = required_notes & self.current_pressed
        num_correct = len(pressed_correct)
        num_required = len(required_notes)

        if required_notes.issubset(self.current_pressed):
            self.show_correct_feedback()
        elif not self.chord_completed:
            self.feedback_label.setText(f"{num_correct}/{num_required} notes")
            self.feedback_label.setStyleSheet("color: #e67e22; font-size: 120px; font-weight: bold; padding: 20px;")

    def back_to_settings(self):
        self.timer.stop()
        self.midi_listener.stop()
        self.main_window.back_to_settings()
