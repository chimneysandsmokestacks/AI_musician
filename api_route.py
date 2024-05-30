import requests
import os
import re
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
API_URL = 'https://api.openai.com/v1/chat/completions'
ORGANIZATION = os.getenv('ORGANIZATION_ID')
DEBUG_MODE = False
print(f"API Key: {API_KEY}")
print(f"Organization: {ORGANIZATION}")

def send_to_openai(notes, mode):
    if DEBUG_MODE:
        return get_debug_response(mode)

    print(f"Sending notes to model: {str(notes)}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'OpenAI-Organization': ORGANIZATION
    }

    prompt = generate_prompt(notes, mode)
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1
    }

    response = requests.post(API_URL, headers=headers, json=data)
    response_data = response.json()
    print(f"printing response data: {response_data}")
    return parse_response(response_data, mode)

def generate_prompt(notes, mode):
    if mode == "sequence":
        return (
                "Here is a melody: {}. Create a continuation that contains at least twice as many chords as the number of notes in my melody.\n"
                "Always follow these rules:\n"
                "- Determine the key of the melody I provided. Then, in your creation, "
                " attach to the last note I provided and end in the key's tonal ""home""."
                # " Include enough chords to end the progression in a harmonically stable place.\n"
                # "- The chord progression should be in the style of JS Bach.\n "
                "- Your melody should have up to 4 concurrent voices, but each chord cannot include more than three of the same notes (across octaves).\n "
                "- Put the root of each chord as the lowest note. This note needs to be voiced at least an octave lower than the next-lowest note.\n "
                # "- Two third intervals cannot appear in a row, and never create a major or minor second.\n "
                "- Come up with intonation/velocity for each note with a pair. The intonation should be very dynamic (use the full spectrum of available velocity between 50 and 80)\n"
                ### do not change the below ###
                "- Format your response as 'Key: [assumed key], (note[with register]-velocity[a value between 50 and 80],note-velocity,note-velocity,note-velocity), [next pair...] END. Chord progression: [chord progression in roman numerals]'\n"
                "- Do not include anything else in the response."
                ).format(', '.join(notes))

    elif mode == "duet":
        return ("Let's make music. I will give you a note and you will return a harmonious note. "
                "To determine harmony, use the average of the last 5 notes to assess which key we are likely to be in. "
                "Only output a single note, alongside the likely key without any other context: " + notes[0])




def parse_response(response_data, mode):
    content = response_data['choices'][0]['message']['content']
    # print(f"API response: {content}")

    try:

        note_parts, chord_progression = content.split(" END.")
    
        key, note_parts = note_parts.split(", ", 1)  # First split after key
        key = key.split("Key: ")[1].strip() 
        note_groups = []
        raw_note_groups = re.findall(r"\(([^)]+)\)", note_parts)
        for group in raw_note_groups:
            pairs = re.findall(r"(\w+\d+)-(\d+)", group)
            notes_and_velocities = [(note, int(velocity)) for note, velocity in pairs]
            note_groups.append(notes_and_velocities)

        return note_groups  # Only return note_groups here without the key
    except Exception as e:
        print("Failed to split or parse response correctly:", str(e))
        return None, None

def get_debug_response(mode):
    if mode == "sequence":
        return "C Major", [("E3", "E4", "95"), ("C3", "C4", "85"), ("D3", "D4", "95"), ("G2", "G3", "85")]
    elif mode == "duet":
        return "C4"
