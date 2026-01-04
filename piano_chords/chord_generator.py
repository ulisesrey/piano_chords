import random

class Chord:
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    FORMULAS = {
        "Major": [0, 4, 7],
        "Minor": [0, 3, 7],
        "Diminished": [0, 3, 6],
        "Augmented": [0, 4, 8],
        "Major 7": [0, 4, 7, 11]
    }

    def __init__(self, root, quality):
        self.root = root
        self.quality = quality
        self.notes = self._calculate_notes()

    def _calculate_notes(self):
        start_idx = self.NOTES.index(self.root)
        intervals = self.FORMULAS[self.quality]
        return [self.NOTES[(start_idx + i) % 12] for i in intervals]

    def __repr__(self):
        return f"{self.root} {self.quality}: {', '.join(self.notes)}"

if __name__ == "__main__":
    # Generating a random chord
    random_root = random.choice(Chord.NOTES)
    random_quality = random.choice(list(Chord.FORMULAS.keys()))

    my_chord = Chord(random_root, random_quality)
    print(f"Challenge: Play this chord -> {my_chord}")