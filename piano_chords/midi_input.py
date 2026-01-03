import mido
from threading import Thread

class MidiListener:
    def __init__(self, callback):
        self.callback = callback
        self.running = False

    def start(self, device_name=None):
        self.running = True
        self.thread = Thread(target=self._listen, args=(device_name,), daemon=True)
        self.thread.start()

    def _listen(self, device_name):
        if device_name is None:
            device_name = mido.get_input_names()[0]  # pick first device
        with mido.open_input(device_name) as inport:
            while self.running:
                for msg in inport.iter_pending():
                    if msg.type in ['note_on', 'note_off']:
                        self.callback(msg)
