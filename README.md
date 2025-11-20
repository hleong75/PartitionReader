# PartitionReader

A Python program to read music partition files (in ABC notation), play them in real-time using MIDI, and convert them to LaTeX format using LilyPond syntax.

## Features

- 📖 **Parse ABC Notation**: Read music files in the simple and widely-used ABC notation format
- 🎵 **Real-time Playback**: Play the music through MIDI (acts as a digital musician)
- 📄 **LaTeX Conversion**: Convert music notation to LaTeX format using LilyPond for beautiful sheet music typesetting
- 💾 **MIDI Export**: Save parsed music as MIDI files for use in other applications

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hleong75/PartitionReader.git
cd PartitionReader
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) For LaTeX output compilation, install LilyPond:
```bash
# On Ubuntu/Debian
sudo apt-get install lilypond

# On macOS
brew install lilypond

# On Windows
# Download from: http://lilypond.org/download.html
```

## Usage

### Basic Usage

Parse and display partition information:
```bash
python partition_reader.py examples/simple_scale.abc
```

### Play Music

Play the partition file using MIDI:
```bash
python partition_reader.py examples/twinkle_twinkle.abc --play
```

### Convert to LaTeX

Convert to LilyPond format (can be embedded in LaTeX):
```bash
python partition_reader.py examples/melody.abc --latex output.ly
```

Convert to a full LaTeX document:
```bash
python partition_reader.py examples/melody.abc --latex-doc output.lytex
```

To compile the LaTeX document with embedded music:
```bash
lilypond-book --pdf output.lytex
cd out/
pdflatex output.tex
```

### Export to MIDI

Save as a MIDI file:
```bash
python partition_reader.py examples/simple_scale.abc --midi output.mid
```

### Combined Operations

You can combine multiple operations:
```bash
python partition_reader.py examples/twinkle_twinkle.abc --play --latex output.ly --midi output.mid
```

## ABC Notation Quick Reference

ABC notation is a simple text-based music notation system:

- **Notes**: `C D E F G A B` (uppercase = lower octave, lowercase = higher octave)
- **Accidentals**: `^` (sharp), `_` (flat), `=` (natural)
- **Duration**: Number after note (`2` = half note, `/2` = eighth note)
- **Headers**:
  - `X:` - Reference number
  - `T:` - Title
  - `Q:` - Tempo (BPM)
  - `M:` - Time signature
  - `K:` - Key signature

Example ABC file:
```abc
X:1
T:Simple Scale
Q:120
M:4/4
K:C
C D E F G A B c
```

## Examples

The `examples/` directory contains sample partition files:

- `simple_scale.abc` - A basic C major scale
- `twinkle_twinkle.abc` - Twinkle Twinkle Little Star
- `melody.abc` - A simple melody in 3/4 time

## Project Structure

```
PartitionReader/
├── partition_reader.py   # Main application entry point
├── partition_parser.py   # ABC notation parser
├── music_player.py       # MIDI playback engine
├── latex_converter.py    # LaTeX/LilyPond converter
├── requirements.txt      # Python dependencies
├── examples/            # Sample partition files
│   ├── simple_scale.abc
│   ├── twinkle_twinkle.abc
│   └── melody.abc
└── README.md
```

## Requirements

- Python 3.6+
- `mido` - MIDI library for Python
- `python-rtmidi` - Python bindings for RtMidi (for MIDI playback)
- (Optional) LilyPond - For compiling LaTeX documents with music notation

## How It Works

1. **Parser**: The `PartitionParser` reads ABC notation files and converts them into structured `Note` objects
2. **Player**: The `MusicPlayer` takes the parsed notes and plays them using MIDI, acting as a digital musician
3. **Converter**: The `LaTeXConverter` transforms the notes into LilyPond syntax, which can be embedded in LaTeX documents for beautiful sheet music typesetting

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.