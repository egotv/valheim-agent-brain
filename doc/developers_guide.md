# System Architecture of Valheim Agent Brain

This is the service that enables the Valheim agent to think, taking in player commands, game states and deciding what the agent should do and say.

### How Valheim Agent Brain fits in the big picture

The entire Valheim agent mod is made up of two services - the client (Valheim mod) and the server (brain). There are multiple clients (each client is an instance of a player's Valheim game)
and only one server. The client sends requests to the server giving player instructions and game states to the brain, the brain processes it, and returns to the client a set of actions that the agent will take and the words that the agent will say to the player.

## Data Flow

The Data Flow describes how the server processes information given by the client in a linear way.

* The server receives the data from the client with `POST /instruct_agent`. This data includes player instruction (in audio form), game state (in JSON form) and other auxiliary information.
* The player instruction audio is decoded and transcribed into text.
* The memory of the agent w.r.t. to the current player is retrieved (currently it is simply a log of the conversation and the actions performed by the agent)
* The valheim-specific knowledge is retrieved from the valheim knowledge base (csv files under the folder `valheim_knowledge_base`)
* The player instruction text, memory, knowledge and game state are fed into the LLM to decide what the agent should say and do.
* Upon receiving the words of the agent, the words are then synthesized into audio and saved locally.
* The server returns to the client the list of actions that the agent will do, and an identifier to the audio file of what the agent says.
* The client calls `GET /get_audio_file` to download the audio file into their local devices.

## Components

### Brain

The Brain is the central component of this system. It takes input from the Input System, thinks through the Thinker, and outputs instructions through the Output System.

### Thinker (LLM Wrapper)

The Thinker defines an interface for the brain to use various LLMs to think.

### Memory System

The Input System receives input from the player and the game, such as player commands, game states etc. It then passes the input to the Brain.

### Web API

The API is made with Flask, which handles the communication between the outside world with the I/O systems.
