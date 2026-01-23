import random
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer, Signal
from piano_chords.midi_input import MidiListener
from piano_chords.chord_generator import Chord
# from chords_dict import CHORDS

class PracticePage(QWidget):

    note_pressed = Signal(tuple)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.selected_roots = [] 
        self.chord_types = []
        self.custom_chords = []  # For custom chord input
        self.interval = 5

        # Previous Chord
        self.previous_chord = None
        # Current pressed
        self.current_pressed = set() # currently pressed notes

        # Current Chord
        self.current_chord = "" # TODO: Should replace to None?

        # Blinking
        self.blink_timer = QTimer()
        self.blink_timer.setSingleShot(True)
        self.blink_timer.timeout.connect(self.show_chord_label)

        # Label for the chord
        self.chord_label = QLabel("")
        self.chord_label.setAlignment(Qt.AlignCenter)
        self.chord_label.setStyleSheet("font-size: 200px; color: darkgreen;")

        # Feedback label
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 24px; color: blue;")  # color optional

        # Midi listener
        self.midi_listener = MidiListener(
            self.on_midi_input,
            error_callback=self.on_midi_error
            )
        self.note_pressed.connect(self.on_note_pressed) # GUI-safe handler

        self.midi_error_label = QLabel("")
        self.midi_error_label.setAlignment(Qt.AlignCenter)
        self.midi_error_label.setStyleSheet(
            "color: red; font-size: 16px; font-weight: bold;"
        )

        # Back button
        self.back_btn = QPushButton("Back to Settings")
        self.back_btn.clicked.connect(self.back_to_settings)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.midi_error_label)
        layout.addWidget(self.chord_label)
        layout.addWidget(self.feedback_label)
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
        self.interval = interval * 1000  # milliseconds
        
        self.feedback_label.setText("Get ready..")  # reset feedback
        self.next_chord()
        self.timer.start(self.interval)
        # Remove error message
        self.midi_error_label.setText("")
        # Start MIDI listener
        self.midi_listener.start()
    
    def setup_with_chords(self, chords, interval):
        """Called when practice starts with custom chord input"""
        self.custom_chords = chords
        self.selected_roots = []
        self.chord_types = []
        self.interval = interval * 1000  # milliseconds
        
        self.feedback_label.setText("Get ready..")  # reset feedback
        self.next_chord()
        self.timer.start(self.interval)
        # Remove error message
        self.midi_error_label.setText("")
        # Start MIDI listener
        self.midi_listener.start()

    def on_midi_error(self, message):
        self.midi_error_label.setText(
            f"⚠️ MIDI Error: {message}\nPlease connect a MIDI keyboard and restart."
        )

    def next_chord(self):
        """Pick a random chord to display"""
        if self.custom_chords:
            # Use custom chords
            self.current_chord = random.choice(self.custom_chords)
        elif self.selected_roots and self.chord_types:
            # Use note/type selection
            root = random.choice(self.selected_roots)
            quality = random.choice(self.chord_types)
            self.current_chord = Chord(root, quality)
        else:
            self.chord_label.setText("No chords selected")
            return

        # If it's the same as previous, pick another
        if self.current_chord == self.previous_chord and len(self.custom_chords or self.selected_roots) > 1:
            if self.custom_chords:
                # For custom chords, pick a different one
                available = [c for c in self.custom_chords if c != self.previous_chord]
                if available:
                    self.current_chord = random.choice(available)
            else:
                # For note/type selection, pick next root
                idx = self.selected_roots.index(self.current_chord.root)
                next_idx = (idx + 1) % len(self.selected_roots)
                self.current_chord = Chord(self.selected_roots[next_idx], self.current_chord.quality)

        self.previous_chord = self.current_chord

        # Blink effect
        self.chord_label.setText("")            # hide chord
        self.feedback_label.setText("")        # clear feedback
        self.current_pressed.clear()

        self.blink_timer.start(250)              # show after 250ms


    def show_chord_label(self):
        self.chord_label.setText(self.current_chord.symbol)

    
    def on_midi_input(self, msg):
        # TODO: SHould come from chord generator
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
        else:
            self.current_pressed.discard(note_name)
        self.check_chord()
    

    def check_chord(self):
        if not self.current_chord:
            return

        if set(self.current_chord.notes).issubset(self.current_pressed):
            self.feedback_label.setText("Correct!")
            self.feedback_label.setStyleSheet("color: green; font-size: 100px;")
        else:
            self.feedback_label.setText("Play all notes")
            self.feedback_label.setStyleSheet("color: red; font-size: 100px;")


    def back_to_settings(self):
        self.timer.stop()
        self.main_window.back_to_settings()
