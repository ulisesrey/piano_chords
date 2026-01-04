import mido
from threading import Thread

class MidiListener:
    def __init__(self, callback, error_callback=None):
        self.callback = callback
        self.error_callback = error_callback
        self.running = False

    def start(self, device_name=None):
        try:
            inputs = mido.get_input_names()
            if not inputs:
                raise RuntimeError("No MIDI input devices found")

            if device_name is None:
                device_name = inputs[0]

            self.running = True
            self.thread = Thread(
                target=self._listen,
                args=(device_name,),
                daemon=True
            )
            self.thread.start()

        except Exception as e:
            self.running = False
            if self.error_callback:
                self.error_callback(str(e))

    def _listen(self, device_name):
        try:
            with mido.open_input(device_name) as inport:
                while self.running:
                    for msg in inport.iter_pending():
                        if msg.type in ("note_on", "note_off"):
                            self.callback(msg)
        except Exception as e:
            if self.error_callback:
                self.error_callback(str(e))
