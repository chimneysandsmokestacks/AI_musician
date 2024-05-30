import re

### converts MIDI notes to the ABC format and vice versa ###
def note_number_to_name(note_number):
    """ Convert MIDI note number to musical note name. """
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[note_number % 12] + str(note_number // 12 - 1)

def note_name_to_number(note_name):
    ### converts musical note names to MIDI note numbers. Only processes valid note names."""
    pattern = re.compile(r'^([A-G][#b]?)(\d)')
    match = pattern.match(note_name)
    if not match:
        print(f"Invalid note format: {note_name}")
        return None  

    note, octave = match.groups()
    octave = int(octave)

    notes = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'E#': 5, 'Fb': 4, 'F': 5, 
        'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }

    note = note.replace('♭', 'b').replace('♯', '#') 
    if note in notes:
        return notes[note] + (octave + 1) * 12
    else:
        print(f"Note name not recognized: {note}")
        return None
