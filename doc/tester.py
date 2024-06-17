import requests
import json
import base64
import re

# Base URL of the API
base_url = "http://localhost:5000"

# Test the /hello_world endpoint
def test_hello_world():
    response = requests.get(f"{base_url}/hello_world")
    print("Response from /hello_world:", response.text)

# Test the /instruct_agent endpoint
def test_instruct_agent():

    # Express the audio file in a format that can be sent in a JSON payload
    audio_file = "salt_lake_city.wav"
    with open(audio_file, "rb") as file:
        audio_base64 = base64.b64encode(file.read()).decode("utf-8")

    # Prepare the data for the POST request
    data = {
        "player_id": "player123",
        "game_state": {
            "location": "Salt Lake City",
            "weather": "sunny",
            "temperature": "35 C",
            "time": "12:00 PM",
            "hunger_level": "high",
            "nearby": 'Crops that are fully grown and ready to be harvested.'
        },
        "player_instruction_audio_file_base64": audio_base64
    }
    
    # Send the POST request
    response = requests.post(f"{base_url}/instruct_agent", json=data)
    
    # Print the response
    print("Response from /instruct_agent:", response.json())

    # Audio file ID
    audio_file_id = response.json()["agent_text_response_audio_file_id"]
    response = requests.get(f"{base_url}/get_audio_file?audio_file_id={audio_file_id}")

    # If 404, the audio file does not exist
    if response.status_code == 404:
        print("Audio file does not exist.")
        return
    
    with open("audio.wav", "wb") as file:
        file.write(response.content)
    print("Audio file downloaded to:", "audio.wav")

# Run the tests
if __name__ == "__main__":
    test_hello_world()
    test_instruct_agent()