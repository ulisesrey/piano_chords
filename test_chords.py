import pytest
from piano_chords.chord_generator import Chord


class TestChordGeneration:
    """Test basic chord generation"""
    
    def test_major_chord(self):
        chord = Chord('C', 'Major')
        assert chord.notes == ['C', 'E', 'G']
        assert chord.symbol == 'C'
    
    def test_minor_chord(self):
        chord = Chord('A', 'Minor')
        assert chord.notes == ['A', 'C', 'E']
        assert chord.symbol == 'Am'
    
    def test_dominant_7_chord(self):
        chord = Chord('G', 'Dominant 7')
        assert chord.notes == ['G', 'B', 'D', 'F']
        assert chord.symbol == 'G7'
    
    def test_major_7_chord(self):
        chord = Chord('C', 'Major 7')
        assert chord.notes == ['C', 'E', 'G', 'B']
        assert chord.symbol == 'Cmaj7'
    
    def test_minor_7_chord(self):
        chord = Chord('D', 'Minor 7')
        assert chord.notes == ['D', 'F', 'A', 'C']
        assert chord.symbol == 'Dm7'
    
    def test_sharp_root(self):
        chord = Chord('F#', 'Major')
        assert chord.notes == ['F#', 'A#', 'C#']
        assert chord.symbol == 'F#'
    
    def test_diminished_chord(self):
        chord = Chord('B', 'Diminished')
        assert chord.notes == ['B', 'D', 'F']
        assert chord.symbol == 'B°'