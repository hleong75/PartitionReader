# PartitionReader Examples

This document provides detailed examples of using PartitionReader.

## Quick Start Examples

### Example 1: Parse and Display Information

```bash
python3 partition_reader.py examples/simple_scale.abc
```

Output:
```
Reading partition file: examples/simple_scale.abc
============================================================
Title: Simple C Major Scale
Tempo: 120 BPM
Time Signature: 4/4
Key: C
Number of notes: 8
============================================================
```

### Example 2: Play Music (Digital Musician Mode)

```bash
python3 partition_reader.py examples/twinkle_twinkle.abc --play
```

This will play the music using MIDI. If no MIDI device is available, it will simulate playback showing each note being played with timing information.

### Example 3: Convert to LaTeX

```bash
python3 partition_reader.py examples/melody.abc --latex output.ly
```

This generates a LilyPond file that can be compiled to beautiful sheet music.

### Example 4: Full LaTeX Document

```bash
python3 partition_reader.py examples/ode_to_joy.abc --latex-doc beethoven.lytex
```

This creates a complete LaTeX document with embedded music notation.

To compile:
```bash
lilypond-book --pdf beethoven.lytex
cd out/
pdflatex beethoven.tex
```

### Example 5: Export to MIDI

```bash
python3 partition_reader.py examples/simple_scale.abc --midi scale.mid
```

This exports the music to a standard MIDI file that can be opened in any MIDI-compatible software.

### Example 6: Combined Operations

```bash
python3 partition_reader.py examples/twinkle_twinkle.abc \
  --play \
  --latex twinkle.ly \
  --midi twinkle.mid
```

This will:
1. Play the music
2. Convert to LilyPond format
3. Export to MIDI file

## Creating Your Own ABC Files

ABC notation is simple and intuitive. Here's how to create your own:

### Basic Structure

```abc
X:1
T:Your Title
Q:120
M:4/4
K:C
C D E F G A B c
```

### Headers

- `X:` - Reference number (always 1 for single tunes)
- `T:` - Title of the piece
- `Q:` - Tempo in beats per minute
- `M:` - Time signature (e.g., 4/4, 3/4, 6/8)
- `K:` - Key signature (C, G, D, A, E, B, F, Bb, Eb, Ab, Db, Gb, F#, C#)

### Notes

- **Basic notes**: `C D E F G A B`
- **Octaves**:
  - Uppercase = lower octave (C3-B3)
  - Lowercase = higher octave (C4-B4)
  - Add commas for lower octaves: `C,, C, C`
  - Add apostrophes for higher octaves: `c c' c''`

### Duration

- Default duration is a quarter note
- Numbers multiply duration: `C2` = half note, `C4` = whole note
- Slashes divide duration: `C/2` = eighth note, `C/4` = sixteenth note
- Can combine: `C3/2` = dotted quarter note

### Accidentals

- `^C` = C sharp
- `_B` = B flat
- `=C` = C natural (cancel previous accidental)

### Rests

- `z` = rest (same duration rules apply)

### Bar Lines

- `|` = single bar line
- `||` = double bar line
- `|]` = final bar line

## Example Pieces Included

### 1. Simple Scale (`simple_scale.abc`)
A basic C major scale - perfect for testing and learning.

### 2. Twinkle Twinkle Little Star (`twinkle_twinkle.abc`)
A complete familiar melody with proper phrasing.

### 3. Simple Melody (`melody.abc`)
A short original melody in 3/4 time, key of G major.

### 4. Ode to Joy (`ode_to_joy.abc`)
Beethoven's famous theme with more complex rhythms including eighth notes.

## Advanced Usage

### Verbose Mode

See all parsed notes:
```bash
python3 partition_reader.py examples/melody.abc --verbose
```

### Override Tempo

Change playback speed:
```bash
python3 partition_reader.py examples/twinkle_twinkle.abc --play --tempo 140
```

### Batch Processing

Process multiple files:
```bash
for file in examples/*.abc; do
    python3 partition_reader.py "$file" --latex "output/$(basename $file .abc).ly"
done
```

## Integration Examples

### Use in Python Scripts

```python
from partition_parser import PartitionParser
from music_player import MusicPlayer
from latex_converter import LaTeXConverter

# Parse a file
parser = PartitionParser()
notes = parser.parse_file('my_music.abc')
metadata = parser.get_metadata()

# Play it
player = MusicPlayer(tempo=metadata['tempo'])
player.play_notes(notes)

# Convert to LaTeX
converter = LaTeXConverter(metadata)
converter.save_to_file(notes, 'output.ly', full_document=True)
```

### Create Notes Programmatically

```python
from partition_parser import Note
from music_player import MusicPlayer

# Create a simple melody
notes = [
    Note('C', 4, 1.0),
    Note('E', 4, 1.0),
    Note('G', 4, 1.0),
    Note('C', 5, 2.0)
]

# Play it
player = MusicPlayer(tempo=120)
player.play_notes(notes)
```

## Troubleshooting

### MIDI Playback Issues

If you get ALSA or MIDI errors, the system will automatically fall back to simulation mode, which shows you what would be played without requiring MIDI hardware.

### LaTeX Compilation

To compile LaTeX documents with music:
1. Install LilyPond: `sudo apt-get install lilypond`
2. Use `lilypond-book` to process the .lytex file
3. Use `pdflatex` to compile the resulting .tex file

### ABC Notation Not Parsing

- Make sure headers (T:, Q:, M:, K:) are on separate lines
- The K: header must be the last header before the music
- Bar lines (|) are optional but recommended for readability

## Resources

- ABC Notation Standard: http://abcnotation.com/
- LilyPond Documentation: http://lilypond.org/
- MIDI File Format: https://www.midi.org/

## Tips

1. **Start simple**: Begin with basic scales and melodies
2. **Use bar lines**: They make the music easier to read
3. **Test early**: Parse and play your music frequently while composing
4. **Listen first**: Always use --play to hear how your notation sounds
5. **Version control**: ABC files are plain text - perfect for git!

## Next Steps

- Try modifying the example files
- Create your own melodies
- Experiment with different time signatures and keys
- Share your ABC files with others
- Contribute new examples to the repository!
