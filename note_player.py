import mido
from threading import Timer
from notes_conversion import note_name_to_number, note_number_to_name

def play_note_groups(outport_gb, note_groups, timings):
    # print("Note groups received:", note_groups)
    if len(timings) < len(note_groups):
        last_timing = timings[-1] if timings else 0.5
        timings.extend([last_timing] * (len(note_groups) - len(timings)))

    for i, group in enumerate(note_groups):
        delay = sum(timings[:i + 1])
        
        note_names = '-'.join(note for note, _ in group)
        Timer(delay, lambda note_names=note_names, delay=delay: print(f"{note_names}")).start()
        
        for note_tuple in group:  
            if len(note_tuple) == 2:
                note, velocity = note_tuple
                note_number = note_name_to_number(note)
                if note_number is None:
                    print(f"Invalid note: {note} could not be converted to a MIDI number.")
                else:
                    #note_name = note_number_to_name(note)
                    # print(f"{note_name}(velocity {velocity})")
                    Timer(delay, lambda nn=note_number, v=velocity: play_single_note(outport_gb, nn, v)).start()
            else:
                print("Unexpected note format:", note_tuple))

def play_single_note(outport_gb, note_number, velocity):
    # print(f"Playing {note_number} with velocity {velocity}")
    outport_gb.send(mido.Message('note_on', note=note_number, velocity=velocity))
    Timer(0.8, lambda nn=note_number: note_off(outport_gb, nn)).start()

def note_off(outport_gb, note_number):
    # print(f"Stopping note {note_number}")
    outport_gb.send(mido.Message('note_off', note=note_number, velocity=0))
