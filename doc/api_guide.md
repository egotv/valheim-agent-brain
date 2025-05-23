# API Documentation

This is the API documentation for the Valheim Agent Brain, which interfaces with the Valheim Mod Client.
The endpoint of this API is https://valheim-agent-brain.fly.dev/

## Endpoints that interface with Valheim Mod Client

### Player Instructs the Agent

`POST /instruct_agent`

JSON parameters:

```
{
    "player_id": str,
    "game_state": JSON object,
    "player_instruction_audio_file_base64": Base64-encoded wav file,
    "timestamp": float [optional],
    "personality": str [optional],
    "voice": str (find voices at https://developers.deepgram.com/docs/tts-models) [optional, defaults to "asteria"]
}
```

Example request in Python:

```
{
    "player_id": "player123",
    "game_state": {
        "location": "Salt Lake City",
        "weather": "sunny",
        "temperature": "35 C",
        "time": "12:00 PM",
        "hunger_level": "high",
        "nearby": 'Crops that are fully grown and ready to be harvested.'
    },
    "timestamp": 43453455334.534534
    "player_instruction_audio_file_base64": audio_base64,
    "personality": "feisty",
    "voice": "asteria"
}
```

Response example:

```
{
    'agent_commands': [
        {'action': 'EquipItem', 'category': 'Inventory', 'parameters': ['sword']}, 
        {'action': 'StartAttacking', 'category': 'Combat', 'parameters': ['wild boar', 'sword']}
    ]
    'agent_text_response': "Harvesting time, buttercup! Make hay while the sun shines! Don't forget - your tummy's rumbling!", 
    'agent_text_response_audio_file_id': '941b65c4-7142-4e9d-9c29-4430e1317171', 
    'player_id': 'player123', 
    'player_instruction_transcription': 'Greetings for Salt Lake City, the city of snow, sunshine and much more.', 
    'timestamp': 1718657404.9899921,
    'personality': "feisty",
    "voice": "asteria"
}
```

Notes:

* The `timestamp` is in seconds from epoch
* The `game_state` can be any json-like dictionary object
* The `player_instruction_audio_file_base64` is a `wav` file encoded in base64

The possible actions that the agent can take as as follows:
```
[Category: Follow]
- Follow_Start(target)
- Follow_Stop()

[Category: Combat]
- Combat_StartAttacking(target, weapon)
- Combat_StopAttacking()
- Combat_Sneak()
- Combat_Defend(target)

[Category: Inventory]
- Inventory_DropAll()
- Inventory_DropItem(item)
- Inventory_EquipItem(item)
- Inventory_PickupItem(item)

[Category: Harvesting]
- Harvesting_Start(item, quantity)
- Harvesting_Stop()
- Harvesting_Craft(item, quantity)

[Category: Patrol]
- Patrol_Start(target)
- Patrol_Stop()
```

Python example of encoding the audio file

```
audio_file = "audio_file.wav"
with open(audio_file, "rb") as file:
    audio_base64 = base64.b64encode(file.read()).decode("utf-8")
```

### Text-to-Speech

`GET /synthesize_audio`

GET Arguments:

`text`: The content to be spoken
`voice`: The person speaking the content

Response example:

```
{
    "text": "Hello",
    "voice": "asteria",
    "audio_file_id": "4tuj3904jv0wer"
}
```

Use the audio file ID to download the audio file with `GET /get_audio_file`

### Downloading Audio Files

`GET /get_audio_file`

GET Arguments:

`audio_file_id`: The `agent_text_response_audio_file_id` that has been received prior

The content of the response is the audio file that is requested




