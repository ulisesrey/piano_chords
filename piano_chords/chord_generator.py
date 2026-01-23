class Chord:
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    FORMULAS = {
        # Triads
        "Major": [0, 4, 7],
        "Minor": [0, 3, 7],
        "Diminished": [0, 3, 6],
        "Augmented": [0, 4, 8],

        # Seventh chords (core jazz harmony)
        "Major 7": [0, 4, 7, 11],
        "Dominant 7": [0, 4, 7, 10],
        "Minor 7": [0, 3, 7, 10],
        "Half-diminished 7": [0, 3, 6, 10],
        "Diminished 7": [0, 3, 6, 9],
    }


    SYMBOLS = {
        "Major": "",
        "Minor": "m",
        "Diminished": "°",
        "Augmented": "+",
        "Major 7": "maj7",
        "Dominant 7": "7",
        "Minor 7": "m7",
        "Half-diminished 7": "ø7",
        "Diminished 7": "°7",
    }

    def __init__(self, root, quality):
        self.root = root
        self.quality = quality # Major, minor, augmented..
        self.notes = self._calculate_notes()

    def _calculate_notes(self):
        start_idx = self.NOTES.index(self.root)
        intervals = self.FORMULAS[self.quality]
        return [self.NOTES[(start_idx + i) % 12] for i in intervals]

    @property
    def symbol(self):
        """Chord symbol for UI (e.g. Em, Cmaj7)"""
        return f"{self.root}{self.SYMBOLS[self.quality]}"

    def __repr__(self):
        return f"{self.symbol}: {', '.join(self.notes)}"
    
    def __eq__(self, other):
        if not isinstance(other, Chord):
            return False
        return self.root == other.root and self.quality == other.quality

