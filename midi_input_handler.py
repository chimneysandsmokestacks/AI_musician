import mido
from mido import Message
from threading import Timer
import time
from notes_conversion import note_number_to_name, note_name_to_number

### handle_midi_input receives notes from the inport (MIDI). It appends them them to a buffer, and sends that buffer 
### to enqueue_notes, which adds the notes to a note queue. The note_queue is then available in main.py to send to the processor.

api_delay = 2.0

def handle_midi_input(inport, note_queue, mode):
    notes_buffer = []
    timings = []
    last_time = None
    timer = None
    def send_notes():
        if notes_buffer:
            enqueue_notes(note_queue, notes_buffer.copy(), timings.copy(), mode)
            notes_buffer.clear()
            timings.clear()
        reset_last_time()
    def reset_last_time():
        nonlocal last_time
        last_time = None
    for message in inport:
        if message.type == 'note_on' and message.velocity > 0:
            current_time = time.time()
            note_name = note_number_to_name(message.note)
            print(f"{note_name}")
            notes_buffer.append(note_name)
            if last_time is not None:
                timings.append(current_time - last_time)
            else:
                timings.append(0)
            last_time = current_time

            if timer:
                timer.cancel()
            timer = Timer(api_delay, send_notes)
            timer.start()

def simulate_midi_input(outport, note_queue, mode):
    simulated_notes = ['E3', 'C3', 'D3', 'G2']
    simulated_timings = [0.5, 0.5, 0.5, 0.5]
    notes_buffer = []
    timings_buffer = []

    print("Simulating MIDI notes.")
    for note, timing in zip(simulated_notes, simulated_timings):
        time.sleep(timing) 
        note_number = note_name_to_number(note) 
        outport.send(mido.Message('note_on', note=note_number, velocity=64)) 
        print(f"{note}")
        
   
        notes_buffer.append(note)
        timings_buffer.append(timing)

    # Queue the note data for processing after a delay
    Timer(api_delay, lambda: enqueue_notes(note_queue, notes_buffer, timings_buffer, mode)).start()
    # print("Notes queued for processing after delay.")

def enqueue_notes(note_queue, notes, timings, mode):
    # print(f"Enqueuing {notes} with timings {timings} for mode: {mode}")
    note_queue.put({'notes': notes, 'timings': timings, 'mode': mode})

