from midi_input import MidiListener

def print_note(msg):
    note_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][msg.note % 12]
    action = "ON" if msg.type == "note_on" and msg.velocity > 0 else "OFF"
    print(f"{note_name} {action} at speed {msg.velocity} (MIDI {msg.note})")

listener = MidiListener(print_note)
listener.start()

print("Listening for MIDI input... Press Ctrl+C to exit.")

# keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    listener.stop()
    print("Stopped MIDI listener.")
