import mido
from threading import Thread, Timer
from queue import Queue
import time
from midi_input_handler import handle_midi_input, simulate_midi_input
from note_processor import process_note_queue

SIMULATE_NOTES = True
use_default_port = False  # or some condition that determines this

if use_default_port:
    keyboard_to_script_port = 'MPK249 Port A'
else:
    keyboard_to_script_port = 'IAC Driver Bus 1'

script_to_garageband_port = 'IAC Driver Bus 2'
note_queue = Queue()
mode = "sequence"  
midi_port = keyboard_to_script_port 

### opens port to listen to incoming notes. Sends notes to midi_input_handler. Also creates thread to send notes 
### in note_quee to note_processor.py/process_note_queue
def monitor_note_queue(note_queue):
    while True:
        note_data = note_queue.get()
        if note_data is None:
            break
       
       #  Timer(5.0, lambda data=note_data: print(f"New note data detected: {data}")).start()

def main(note_queue, mode, midi_port):
    with mido.open_output(script_to_garageband_port) as outport_gb:
        # Starting processing thread
        player_thread = Thread(target=process_note_queue, args=(note_queue, outport_gb))
        player_thread.start()

        # Starting monitoring thread
        monitor_thread = Thread(target=monitor_note_queue, args=(note_queue,))
        monitor_thread.start()

if __name__ == '__main__':
    with mido.open_output(script_to_garageband_port) as outport_gb:
        player_thread = Thread(target=process_note_queue, args=(note_queue, outport_gb))
        player_thread.start()

        if SIMULATE_NOTES:
            with mido.open_output(script_to_garageband_port) as outport:
                simulate_midi_input(outport, note_queue, mode)
        else:
            with mido.open_input(keyboard_to_script_port) as inport:
                print(f"Listening on {keyboard_to_script_port}...")
                handle_midi_input(inport, note_queue, mode)

        # print("Preparing to send termination signal...")
        # note_queue.put(None)  # Signal to stop the player thread
        player_thread.join()

main(note_queue, mode, midi_port)
