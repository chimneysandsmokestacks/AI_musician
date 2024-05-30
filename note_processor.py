from api_route import send_to_openai
from note_player import play_note_groups

### Receives notes from main.py and sends them to the API route. Sends returned notes to note_player.py ###
def process_note_queue(note_queue, outport_gb):
    while True:
        note_data = note_queue.get()
        
        if note_data is None:
            print("Terminating")
            break 

        notes, timings, mode = note_data['notes'], note_data['timings'], note_data['mode']
        print(f"Sending to API Route: {notes}")

        result = send_to_openai(notes, mode)

        if result:
            note_groups = result
            # print(f"API response: {note_groups}")
            play_note_groups(outport_gb, note_groups, timings)
        else:
            print("Invalid response from OpenAI.")
