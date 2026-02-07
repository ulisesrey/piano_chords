import mido
from threading import Thread
import time

class MidiListener:
    def __init__(self, callback, error_callback=None):
        self.callback = callback
        self.error_callback = error_callback
        self.running = False
        self.thread = None

    def start(self, device_name=None):
        # Stop any existing listener first
        if self.running:
            self.stop()
        
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
                            try:
                                self.callback(msg)
                            except Exception as callback_error:
                                # Don't let callback errors stop the listener
                                if self.error_callback:
                                    self.error_callback(f"Callback error: {callback_error}")
                    time.sleep(0.001)  # Small sleep to avoid busy-waiting
        except Exception as e:
            self.running = False
            if self.error_callback:
                self.error_callback(str(e))
    
    def stop(self):
        """Stop the MIDI listener thread"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
