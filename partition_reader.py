#!/usr/bin/env python3
"""
Partition Reader - Main Application
Reads music partition files, plays them, and converts to LaTeX
"""

import argparse
import sys
from partition_parser import PartitionParser
from music_player import MusicPlayer
from latex_converter import LaTeXConverter


def main():
    parser = argparse.ArgumentParser(
        description='Read music partitions, play them, and convert to LaTeX',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s input.abc                    # Parse and display information
  %(prog)s input.abc --play             # Parse and play the music
  %(prog)s input.abc --latex output.ly  # Convert to LilyPond format
  %(prog)s input.abc --latex-doc output.lytex  # Convert to full LaTeX document
  %(prog)s input.abc --midi output.mid  # Export to MIDI file
  %(prog)s input.abc --play --latex output.ly  # Play and convert to LaTeX

ABC Notation Quick Reference:
  - Notes: C D E F G A B (uppercase = low octave, lowercase = high octave)
  - Accidentals: ^ (sharp), _ (flat), = (natural)
  - Duration: number after note (2 = half note, /2 = eighth note)
  - Headers: T: (title), Q: (tempo), M: (time signature), K: (key)
        '''
    )
    
    parser.add_argument('input_file', help='Input partition file (ABC notation)')
    parser.add_argument('--play', action='store_true', 
                       help='Play the music using MIDI')
    parser.add_argument('--latex', metavar='FILE',
                       help='Convert to LilyPond format and save to FILE')
    parser.add_argument('--latex-doc', metavar='FILE',
                       help='Convert to full LaTeX document and save to FILE')
    parser.add_argument('--midi', metavar='FILE',
                       help='Export to MIDI file')
    parser.add_argument('--tempo', type=int,
                       help='Override tempo (BPM)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Parse the partition file
    print(f"Reading partition file: {args.input_file}")
    print("=" * 60)
    
    try:
        partition_parser = PartitionParser()
        notes = partition_parser.parse_file(args.input_file)
        metadata = partition_parser.get_metadata()
        
        print(f"Title: {metadata['title']}")
        print(f"Tempo: {metadata['tempo']} BPM")
        print(f"Time Signature: {metadata['time_signature']}")
        print(f"Key: {metadata['key']}")
        print(f"Number of notes: {len(notes)}")
        print("=" * 60)
        
        if args.verbose:
            print("\nParsed notes:")
            for i, note in enumerate(notes, 1):
                print(f"  {i}. {note}")
            print()
        
        # Override tempo if specified
        tempo = args.tempo if args.tempo else metadata['tempo']
        
        # Play the music
        if args.play:
            print("\nPlaying music...")
            player = MusicPlayer(tempo=tempo)
            player.play_notes(notes)
            print()
        
        # Export to MIDI
        if args.midi:
            print(f"\nExporting to MIDI file: {args.midi}")
            player = MusicPlayer(tempo=tempo)
            player.save_to_midi_file(notes, args.midi)
            print()
        
        # Convert to LilyPond
        if args.latex:
            print(f"\nConverting to LilyPond format: {args.latex}")
            converter = LaTeXConverter(metadata)
            converter.save_to_file(notes, args.latex, full_document=False)
            print()
        
        # Convert to full LaTeX document
        if args.latex_doc:
            print(f"\nConverting to LaTeX document: {args.latex_doc}")
            converter = LaTeXConverter(metadata)
            converter.save_to_file(notes, args.latex_doc, full_document=True)
            print()
        
        # If no action specified, just show the info
        if not any([args.play, args.latex, args.latex_doc, args.midi]):
            print("\nNo action specified. Use --help to see available options.")
            print("Try --play to hear the music, or --latex to convert to LaTeX format.")
        
        print("Done!")
        return 0
        
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
