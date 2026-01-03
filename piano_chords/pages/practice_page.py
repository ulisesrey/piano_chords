import random
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer, Signal
from midi_input import MidiListener
from chords_dict import CHORDS

class PracticePage(QWidget):

    note_pressed = Signal(tuple)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.selected_chords = [] # TODO: Rename to selected chords for clarity
        self.chord_types = []
        self.interval = 5

        # Current pressed
        self.current_pressed = set() # currently pressed notes

        # Current Chord
        self.current_chord = ""

        # Blinking
        self.blink_timer = QTimer()
        self.blink_timer.setSingleShot(True)
        self.blink_timer.timeout.connect(self.show_chord_label)

        # Label for the chord
        self.chord_label = QLabel("")
        self.chord_label.setAlignment(Qt.AlignCenter)
        self.chord_label.setStyleSheet("font-size: 72px; color: darkgreen;")

        # Feedback label
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 24px; color: blue;")  # color optional

        # Midi listener
        self.midi_listener = MidiListener(self.on_midi_input)
        self.note_pressed.connect(self.on_note_pressed) # GUI-safe handler

        # Back button
        self.back_btn = QPushButton("Back to Settings")
        self.back_btn.clicked.connect(self.back_to_settings)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.chord_label)
        layout.addWidget(self.feedback_label)  # NEW
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_chord)

    def setup(self, selected_notes, chord_types, interval):
        """Called when practice starts"""
        self.selected_chords = list(selected_notes)
        self.chord_types = list(chord_types)
        self.interval = interval * 1000  # milliseconds
        
        self.feedback_label.setText("Get ready..")  # reset feedback
        self.next_chord()
        self.timer.start(self.interval)
        # Start MIDI listener
        self.midi_listener.start()


    def next_chord(self):
        """Pick a random chord to display"""
        if not self.selected_chords or not self.chord_types:
            self.chord_label.setText("No chords selected")
            return
        # Select randomly the note and chord
        note = random.choice(self.selected_chords)
        chord_type = random.choice(self.chord_types)

        self.current_chord = f"{note}" if chord_type == "Major" else f"{note}m"

        # Blink effect
        self.chord_label.setText("")            # hide chord
        self.feedback_label.setText("")        # clear feedback
        self.current_pressed.clear()

        self.blink_timer.start(250)              # show after 150ms


    def show_chord_label(self):
        self.chord_label.setText(self.current_chord)

    
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
        else:
            self.current_pressed.discard(note_name)
        self.check_chord()
    
    def check_chord(self):
        target_notes = CHORDS.get(self.chord_label.text(), [])
        if set(target_notes) == self.current_pressed:
            self.feedback_label.setText("Correct!")
            self.feedback_label.setStyleSheet("color: green; font-size: 24px;")
        else:
            self.feedback_label.setText("Play all notes")
            self.feedback_label.setStyleSheet("color: red; font-size: 24px;")


    def back_to_settings(self):
        self.timer.stop()
        self.main_window.back_to_settings()
