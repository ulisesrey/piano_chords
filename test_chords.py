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


class TestChordTransposition:
    """Test chord progression transposition"""
    
    @pytest.fixture
    def settings_page_mock(self):
        """Create a mock settings page with transpose_progression method"""
        class MockSettingsPage:
            def transpose_progression(self, progression, root, voicing="Triads"):
                from piano_chords.chord_generator import Chord
                
                if not any(numeral in progression for numeral in ['I', 'V', 'i', 'v', 'ii', 'iii', 'iv', 'vi', 'vii']):
                    return progression
                
                root_idx = Chord.NOTES.index(root)
                major_intervals = {'I': 0, 'ii': 2, 'iii': 4, 'IV': 5, 'V': 7, 'vi': 9, 'vii': 11, 'bVII': 10, 'bIII': 3}
                quality_map = {'I': '', 'ii': 'm', 'iii': 'm', 'IV': '', 'V': '', 'vi': 'm', 'vii': '°', 'i': 'm', 'bVII': '', 'bIII': ''}
                seventh_map = {'I': 'maj7', 'ii': '7', 'iii': '7', 'IV': 'maj7', 'V': '7', 'vi': '7', 'vii': '7', 'i': '7', 'bVII': '7', 'bIII': 'maj7'}
                
                result = []
                for chord in progression.split(','):
                    chord = chord.strip()
                    numeral = chord.rstrip('7maj+°ø')
                    suffix = chord[len(numeral):]
                    
                    if numeral in major_intervals:
                        interval = major_intervals[numeral]
                        chord_root = Chord.NOTES[(root_idx + interval) % 12]
                        
                        if voicing == "7th Chords" and not suffix:
                            base_quality = quality_map.get(numeral, '')
                            seventh = seventh_map.get(numeral, '7')
                            result.append(f"{chord_root}{base_quality}{seventh}")
                        else:
                            base_quality = quality_map.get(numeral, '')
                            result.append(f"{chord_root}{suffix if suffix else base_quality}")
                    else:
                        result.append(chord)
                
                return ', '.join(result)
        
        return MockSettingsPage()
    
    def test_transpose_i_v_vi_iv_c_major_triads(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("I, V, vi, IV", "C", "Triads")
        assert result == "C, G, Am, F"
    
    def test_transpose_i_v_vi_iv_d_major_triads(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("I, V, vi, IV", "D", "Triads")
        assert result == "D, A, Bm, G"
    
    def test_transpose_i_v_vi_iv_g_major_triads(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("I, V, vi, IV", "G", "Triads")
        assert result == "G, D, Em, C"
    
    def test_transpose_i_v_vi_iv_c_major_7th_chords(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("I, V, vi, IV", "C", "7th Chords")
        assert result == "Cmaj7, G7, Am7, Fmaj7"
    
    def test_transpose_i_v_vi_iv_d_major_7th_chords(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("I, V, vi, IV", "D", "7th Chords")
        assert result == "Dmaj7, A7, Bm7, Gmaj7"
    
    def test_transpose_ii_v_i_c_major_triads(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("ii, V, I", "C", "Triads")
        assert result == "Dm, G, C"
    
    def test_transpose_ii_v_i_c_major_7th_chords(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("ii, V, I", "C", "7th Chords")
        assert result == "Dm7, G7, Cmaj7"
    
    def test_transpose_with_sharp_root(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("I, V, vi, IV", "F#", "Triads")
        assert result == "F#, C#, D#m, B"
    
    def test_non_roman_numeral_progression_unchanged(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("A7, D7, E7", "C", "Triads")
        assert result == "A7, D7, E7"
    
    def test_12_bar_blues_c_triads(self, settings_page_mock):
        result = settings_page_mock.transpose_progression("I7, I7, I7, I7, IV7, IV7, I7, I7, V7, IV7, I7, V7", "C", "Triads")
        assert result == "C7, C7, C7, C7, F7, F7, C7, C7, G7, F7, C7, G7"


class TestChordParsing:
    """Test chord symbol parsing"""
    
    @pytest.fixture
    def settings_page_mock(self):
        """Create a mock settings page with parse_chord_symbol method"""
        class MockSettingsPage:
            def parse_chord_symbol(self, symbol):
                from piano_chords.chord_generator import Chord
                
                symbol = symbol.strip()
                
                if len(symbol) >= 2 and symbol[1] == '#':
                    root = symbol[:2]
                    suffix = symbol[2:]
                else:
                    root = symbol[0]
                    suffix = symbol[1:]
                
                if root not in Chord.NOTES:
                    return None, None
                
                suffix_map = {
                    '': 'Major',
                    'm': 'Minor',
                    '°': 'Diminished',
                    '+': 'Augmented',
                    'maj7': 'Major 7',
                    '7': 'Dominant 7',
                    'm7': 'Minor 7',
                    'ø7': 'Half-diminished 7',
                    '°7': 'Diminished 7'
                }
                
                quality = suffix_map.get(suffix)
                return root, quality
        
        return MockSettingsPage()
    
    def test_parse_major_chord(self, settings_page_mock):
        root, quality = settings_page_mock.parse_chord_symbol("C")
        assert root == "C"
        assert quality == "Major"
    
    def test_parse_minor_chord(self, settings_page_mock):
        root, quality = settings_page_mock.parse_chord_symbol("Am")
        assert root == "A"
        assert quality == "Minor"
    
    def test_parse_dominant_7(self, settings_page_mock):
        root, quality = settings_page_mock.parse_chord_symbol("G7")
        assert root == "G"
        assert quality == "Dominant 7"
    
    def test_parse_major_7(self, settings_page_mock):
        root, quality = settings_page_mock.parse_chord_symbol("Cmaj7")
        assert root == "C"
        assert quality == "Major 7"
    
    def test_parse_sharp_root(self, settings_page_mock):
        root, quality = settings_page_mock.parse_chord_symbol("F#")
        assert root == "F#"
        assert quality == "Major"
    
    def test_parse_sharp_minor(self, settings_page_mock):
        root, quality = settings_page_mock.parse_chord_symbol("D#m")
        assert root == "D#"
        assert quality == "Minor"
