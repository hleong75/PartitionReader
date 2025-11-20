#!/usr/bin/env python3
"""
Test suite for PartitionReader
Tests the parser, player, and LaTeX converter
"""

import os
import sys
import tempfile
from partition_parser import PartitionParser, Note
from music_player import MusicPlayer
from latex_converter import LaTeXConverter


def test_note_class():
    """Test the Note class"""
    print("Testing Note class...")
    
    # Test MIDI conversion
    note_c4 = Note('C', 4, 1.0)
    assert note_c4.to_midi() == 60, "C4 should be MIDI 60"
    
    note_a4 = Note('A', 4, 1.0)
    assert note_a4.to_midi() == 69, "A4 should be MIDI 69"
    
    note_c5 = Note('C', 5, 1.0)
    assert note_c5.to_midi() == 72, "C5 should be MIDI 72"
    
    # Test with sharps and flats
    note_csharp = Note('C', 4, 1.0, '#')
    assert note_csharp.to_midi() == 61, "C#4 should be MIDI 61"
    
    note_bflat = Note('B', 4, 1.0, 'b')
    assert note_bflat.to_midi() == 70, "Bb4 should be MIDI 70"
    
    # Test LaTeX conversion
    assert 'c4' in note_c4.to_latex(), "C4 should convert to c4 in LaTeX"
    assert "c'4" in note_c5.to_latex(), "C5 should have octave marker"
    
    print("✓ Note class tests passed")


def test_parser():
    """Test the ABC notation parser"""
    print("\nTesting ABC notation parser...")
    
    # Test simple ABC content
    abc_content = """X:1
T:Test Scale
Q:120
M:4/4
K:C
C D E F G A B c
"""
    
    parser = PartitionParser()
    notes = parser.parse_abc(abc_content)
    
    assert len(notes) == 8, f"Should parse 8 notes, got {len(notes)}"
    assert parser.title == "Test Scale", f"Title should be 'Test Scale', got '{parser.title}'"
    assert parser.tempo == 120, f"Tempo should be 120, got {parser.tempo}"
    assert parser.time_signature == "4/4", f"Time signature should be 4/4, got {parser.time_signature}"
    
    # Check note names
    expected_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
    for i, note in enumerate(notes):
        assert note.name == expected_names[i], f"Note {i} should be {expected_names[i]}, got {note.name}"
    
    print("✓ Parser tests passed")


def test_parser_with_file():
    """Test parser with actual example file"""
    print("\nTesting parser with example file...")
    
    parser = PartitionParser()
    notes = parser.parse_file('examples/simple_scale.abc')
    
    assert len(notes) > 0, "Should parse notes from file"
    assert parser.title == "Simple C Major Scale", "Should parse title correctly"
    
    print("✓ File parsing tests passed")


def test_midi_export():
    """Test MIDI file export"""
    print("\nTesting MIDI export...")
    
    parser = PartitionParser()
    notes = parser.parse_file('examples/simple_scale.abc')
    
    with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_file:
        tmp_filename = tmp_file.name
    
    try:
        player = MusicPlayer(tempo=120)
        player.save_to_midi_file(notes, tmp_filename)
        
        assert os.path.exists(tmp_filename), "MIDI file should be created"
        assert os.path.getsize(tmp_filename) > 0, "MIDI file should not be empty"
        
        print(f"✓ MIDI export tests passed (file size: {os.path.getsize(tmp_filename)} bytes)")
    finally:
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_latex_converter():
    """Test LaTeX/LilyPond converter"""
    print("\nTesting LaTeX converter...")
    
    parser = PartitionParser()
    notes = parser.parse_file('examples/simple_scale.abc')
    metadata = parser.get_metadata()
    
    converter = LaTeXConverter(metadata)
    
    # Test LilyPond conversion
    lilypond_output = converter.convert_to_lilypond(notes)
    assert '\\version' in lilypond_output, "Should contain version directive"
    assert '\\score' in lilypond_output, "Should contain score block"
    assert '\\tempo' in lilypond_output, "Should contain tempo marking"
    assert 'Simple C Major Scale' in lilypond_output, "Should contain title"
    
    # Test LaTeX document conversion
    latex_doc = converter.convert_to_latex_document(notes)
    assert '\\documentclass' in latex_doc, "Should contain documentclass"
    assert '\\begin{lilypond}' in latex_doc, "Should contain lilypond environment"
    assert 'PartitionReader' in latex_doc, "Should mention PartitionReader"
    
    print("✓ LaTeX converter tests passed")


def test_latex_file_export():
    """Test LaTeX file export"""
    print("\nTesting LaTeX file export...")
    
    parser = PartitionParser()
    notes = parser.parse_file('examples/simple_scale.abc')
    metadata = parser.get_metadata()
    
    converter = LaTeXConverter(metadata)
    
    with tempfile.NamedTemporaryFile(suffix='.ly', delete=False, mode='w') as tmp_file:
        tmp_filename = tmp_file.name
    
    try:
        converter.save_to_file(notes, tmp_filename, full_document=False)
        
        assert os.path.exists(tmp_filename), "LaTeX file should be created"
        
        with open(tmp_filename, 'r') as f:
            content = f.read()
            assert '\\version' in content, "File should contain LilyPond code"
        
        print("✓ LaTeX file export tests passed")
    finally:
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_all_examples():
    """Test all example files can be parsed"""
    print("\nTesting all example files...")
    
    example_files = [
        'examples/simple_scale.abc',
        'examples/twinkle_twinkle.abc',
        'examples/melody.abc'
    ]
    
    for example_file in example_files:
        parser = PartitionParser()
        notes = parser.parse_file(example_file)
        assert len(notes) > 0, f"Should parse notes from {example_file}"
        print(f"  ✓ {example_file}: {len(notes)} notes parsed")
    
    print("✓ All example files parsed successfully")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running PartitionReader Test Suite")
    print("=" * 60)
    
    try:
        test_note_class()
        test_parser()
        test_parser_with_file()
        test_midi_export()
        test_latex_converter()
        test_latex_file_export()
        test_all_examples()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
