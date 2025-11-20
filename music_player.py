"""
Music Player Module
Plays music from parsed partition data using MIDI
"""

import time
import mido
from typing import List
from partition_parser import Note


class MusicPlayer:
    """Plays music from Note objects using MIDI"""
    
    def __init__(self, tempo: int = 120):
        self.tempo = tempo
        self.beat_duration = 60.0 / tempo  # Duration of one quarter note in seconds
        
    def play_notes(self, notes: List[Note], output_port_name: str = None):
        """
        Play a list of notes using MIDI
        If output_port_name is None, uses virtual MIDI port
        """
        try:
            # Try to open a MIDI output port
            if output_port_name:
                outport = mido.open_output(output_port_name)
            else:
                # Get available output ports
                outputs = mido.get_output_names()
                if outputs:
                    outport = mido.open_output(outputs[0])
                    print(f"Using MIDI output: {outputs[0]}")
                else:
                    # Create virtual port if no physical port available
                    try:
                        outport = mido.open_output('PartitionReader Virtual Port', virtual=True)
                        print("Created virtual MIDI port: PartitionReader Virtual Port")
                    except:
                        print("Warning: Could not open MIDI port. Simulating playback...")
                        self._simulate_playback(notes)
                        return
            
            print(f"Playing {len(notes)} notes at tempo {self.tempo} BPM...")
            
            for i, note in enumerate(notes):
                midi_note = note.to_midi()
                velocity = 64  # Medium velocity
                
                # Note on
                msg_on = mido.Message('note_on', note=midi_note, velocity=velocity)
                outport.send(msg_on)
                
                # Calculate duration in seconds
                duration = note.duration * self.beat_duration
                time.sleep(duration)
                
                # Note off
                msg_off = mido.Message('note_off', note=midi_note, velocity=velocity)
                outport.send(msg_off)
                
                print(f"Played note {i+1}/{len(notes)}: {note}")
            
            outport.close()
            print("Playback complete!")
            
        except Exception as e:
            print(f"Error during MIDI playback: {e}")
            print("Simulating playback instead...")
            self._simulate_playback(notes)
    
    def _simulate_playback(self, notes: List[Note]):
        """Simulate playback without MIDI (for systems without MIDI support)"""
        print(f"\nSimulating playback of {len(notes)} notes at tempo {self.tempo} BPM...")
        print("=" * 60)
        
        for i, note in enumerate(notes):
            midi_note = note.to_midi()
            duration = note.duration * self.beat_duration
            
            print(f"Note {i+1}/{len(notes)}: {note.name}{note.accidental} "
                  f"(Octave {note.octave}, MIDI {midi_note}, "
                  f"Duration {note.duration} beats = {duration:.2f}s)")
            
            time.sleep(duration)
        
        print("=" * 60)
        print("Simulated playback complete!")
    
    def save_to_midi_file(self, notes: List[Note], filename: str):
        """Save notes to a MIDI file"""
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)
        
        # Set tempo
        tempo_microseconds = mido.bpm2tempo(self.tempo)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo_microseconds))
        
        # Add notes
        for note in notes:
            midi_note = note.to_midi()
            velocity = 64
            
            # Calculate duration in ticks (480 ticks per beat is standard)
            ticks_per_beat = mid.ticks_per_beat
            duration_ticks = int(note.duration * ticks_per_beat)
            
            # Note on
            track.append(mido.Message('note_on', note=midi_note, velocity=velocity, time=0))
            
            # Note off (with duration)
            track.append(mido.Message('note_off', note=midi_note, velocity=velocity, time=duration_ticks))
        
        mid.save(filename)
        print(f"MIDI file saved to: {filename}")
