#!/bin/bash
# Demo script for PartitionReader
# Shows all the features of the partition reader

echo "========================================"
echo "PartitionReader Demo"
echo "========================================"
echo ""

# Create output directory
mkdir -p output

echo "1. Parsing a simple scale..."
python3 partition_reader.py examples/simple_scale.abc
echo ""
echo "Press Enter to continue..."
read

echo "2. Parsing with verbose output..."
python3 partition_reader.py examples/simple_scale.abc --verbose
echo ""
echo "Press Enter to continue..."
read

echo "3. Converting to LilyPond format..."
python3 partition_reader.py examples/twinkle_twinkle.abc --latex output/twinkle.ly
echo ""
echo "Generated LilyPond file:"
head -20 output/twinkle.ly
echo ""
echo "Press Enter to continue..."
read

echo "4. Converting to full LaTeX document..."
python3 partition_reader.py examples/melody.abc --latex-doc output/melody.lytex
echo ""
echo "Generated LaTeX document (first 30 lines):"
head -30 output/melody.lytex
echo ""
echo "Press Enter to continue..."
read

echo "5. Exporting to MIDI file..."
python3 partition_reader.py examples/simple_scale.abc --midi output/scale.mid
echo ""
echo "MIDI file created:"
ls -lh output/scale.mid
file output/scale.mid
echo ""
echo "Press Enter to continue..."
read

echo "6. Playing music (simulated playback)..."
timeout 10 python3 partition_reader.py examples/simple_scale.abc --play || true
echo ""
echo "Press Enter to continue..."
read

echo "7. Combined operation: Parse, play, and convert to LaTeX..."
timeout 15 python3 partition_reader.py examples/melody.abc --play --latex output/melody_combined.ly --midi output/melody_combined.mid || true
echo ""

echo "========================================"
echo "Demo completed!"
echo "========================================"
echo ""
echo "Generated files in output/:"
ls -lh output/
echo ""
echo "To compile LaTeX documents with music notation:"
echo "  1. Install LilyPond: apt-get install lilypond"
echo "  2. Run: lilypond-book --pdf output/melody.lytex"
echo "  3. Run: cd out/ && pdflatex melody.tex"
