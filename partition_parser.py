"""
Partition Parser Module
Parses ABC notation music files into structured music data
"""

import re
from typing import List, Dict, Any, Tuple


class Note:
    """Represents a musical note"""
    
    # Note name to MIDI number mapping (C4 = middle C = 60)
    NOTE_TO_MIDI = {
        'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
    }
    
    def __init__(self, name: str, octave: int = 4, duration: float = 1.0, accidental: str = ''):
        self.name = name.upper()
        self.octave = octave
        self.duration = duration
        self.accidental = accidental  # '', '#', or 'b'
        
    def to_midi(self) -> int:
        """Convert note to MIDI number"""
        midi_base = self.NOTE_TO_MIDI.get(self.name, 0)
        midi_num = midi_base + (self.octave * 12) + 12  # +12 to start at octave 0
        
        if self.accidental == '#':
            midi_num += 1
        elif self.accidental == 'b':
            midi_num -= 1
            
        return midi_num
    
    def to_latex(self) -> str:
        """Convert note to LaTeX/LilyPond format"""
        note_name = self.name.lower()
        
        # Add accidental
        if self.accidental == '#':
            note_name += 'is'
        elif self.accidental == 'b':
            note_name += 'es'
        
        # Add octave markers (relative to middle octave)
        if self.octave > 4:
            note_name += "'" * (self.octave - 4)
        elif self.octave < 4:
            note_name += "," * (4 - self.octave)
        
        # Add duration
        if self.duration == 0.25:
            note_name += '16'
        elif self.duration == 0.5:
            note_name += '8'
        elif self.duration == 1.0:
            note_name += '4'
        elif self.duration == 2.0:
            note_name += '2'
        elif self.duration == 4.0:
            note_name += '1'
        
        return note_name
    
    def __repr__(self):
        return f"Note({self.name}{self.accidental}, octave={self.octave}, duration={self.duration})"


class PartitionParser:
    """Parser for ABC notation music files"""
    
    def __init__(self):
        self.title = "Untitled"
        self.tempo = 120
        self.time_signature = "4/4"
        self.key = "C"
        self.notes: List[Note] = []
        
    def parse_abc(self, abc_content: str) -> List[Note]:
        """Parse ABC notation content"""
        lines = abc_content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            # Parse headers
            if line.startswith('T:'):
                self.title = line[2:].strip()
            elif line.startswith('Q:'):
                self.tempo = int(line[2:].strip())
            elif line.startswith('M:'):
                self.time_signature = line[2:].strip()
            elif line.startswith('K:'):
                self.key = line[2:].strip()
            elif not line.startswith(('X:', 'L:', 'C:', 'A:', 'B:', 'D:', 'F:', 'G:', 'H:', 'I:', 'N:', 'O:', 'P:', 'R:', 'S:', 'U:', 'V:', 'W:', 'w:', 'Z:')):
                # This is a music line
                self._parse_music_line(line)
        
        return self.notes
    
    def _parse_music_line(self, line: str):
        """Parse a line of ABC music notation"""
        i = 0
        default_duration = 1.0  # Quarter note by default
        octave = 4  # Middle octave
        
        while i < len(line):
            char = line[i]
            
            # Skip whitespace and bar lines
            if char in ' \t|[]':
                i += 1
                continue
            
            # Check for note
            if char.upper() in 'ABCDEFG':
                note_name = char.upper()
                accidental = ''
                
                # Check for accidental before note
                if i > 0 and line[i-1] in '^_=':
                    if line[i-1] == '^':
                        accidental = '#'
                    elif line[i-1] == '_':
                        accidental = 'b'
                
                # Determine octave based on case
                if char.islower():
                    note_octave = octave + 1
                else:
                    note_octave = octave
                
                # Look ahead for duration
                duration = default_duration
                j = i + 1
                
                # Check for duration number
                if j < len(line) and line[j].isdigit():
                    dur_str = ''
                    while j < len(line) and (line[j].isdigit() or line[j] == '/'):
                        dur_str += line[j]
                        j += 1
                    
                    if '/' in dur_str:
                        parts = dur_str.split('/')
                        if len(parts) == 2 and parts[1]:
                            duration = default_duration / float(parts[1])
                        else:
                            duration = default_duration / 2
                    else:
                        duration = default_duration * float(dur_str)
                    
                    i = j - 1
                
                note = Note(note_name, note_octave, duration, accidental)
                self.notes.append(note)
            
            # Check for accidental markers (when they appear before notes)
            elif char in '^_=':
                pass  # Will be handled when we encounter the note
            
            # Check for rest
            elif char in 'zZ':
                # For now, skip rests - could add Rest class if needed
                pass
            
            i += 1
    
    def parse_file(self, filename: str) -> List[Note]:
        """Parse an ABC notation file"""
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse_abc(content)
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get parsed metadata"""
        return {
            'title': self.title,
            'tempo': self.tempo,
            'time_signature': self.time_signature,
            'key': self.key
        }
