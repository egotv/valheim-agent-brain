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

The Brain is the central component of this system. It takes input from the Input System, thinks through the Thinker, and outputs what the agent does and says through the Output System.

#### brain.py

The central class containing the thinker, memory manager and Valheim knowledge base.

Function `def generate_agent_output(self, player_instruction: str, game_state: GameState, personality: str, player_memory: PlayerMemory) -> OutputObject`

This function is where the agent output is generated, in an `OutputObject` which contains what the agent will say and do. It takes the arguments passed in, retrieves
additional information from the knowledge base, and pass all these through the thinker.

#### knowledge_base_archived.py

This is a currently unused module which attemps to search for relevant information in the knowledge base through vector embeddings.

#### knowledge_base.py

This is the module to manage the Valheim knowledge base. You can retrieve the list of all items, list of monsters and lookup relevant items from a player instruction through string matching.

Function `def lookup_knowledge_base(self, query: str, number_of_rows: int=5) -> List[Dict[str, str]]`

This function does a search whereby all the words in the query are matched against all the words in the item name, and matches are returned, limited to the `number_of_rows`

#### personality_examples.py

This module contains a few examples to guide the thinker on how it should respond given its personality.

### Game

The Game module defines classes that represent information related to the game, such as agent commands and game states.

### I/O System

The I/O System module defines classes that represent how the input to the thinker and the output from the thinker should be structured.

### Memory System

The Memory System represents what the agent remembers between itself and a particular player.

#### memory_manager.py

`MemoryManager` class

This class manages the memories for all players.

`PlayerMemory` class

This class represents the memory of a specific player. Conversation, game states, agent actions and reflections are stored in this class.

#### log_components.py

This module has classes which represent abstractly each of the memory elements, like conversation, agent actions etc.

### Speech

The speech module converts speech to text (using Whisper) and text to speech (using Deepgram).

### Thinker (LLM Wrapper)

#### thinker.py

`Thinker` is an abstract class that has one abstract method `think(input: InputObject) -> OutputObject`. All child classes of `Thinker` need to implement
`think`.

There are other helper static methods for parsing, such as those to validate the format of the output given by the LLMs, and those that can retrieve the ACTIONS and the TEXT_RESPONSE from the LLM output.

#### claude_wrapper.py

This module defines a function `run(prompt, model, temperature)` that runs a prompt through the LLM model provided by Claude. 

#### openai_wrapper.py

This module defines two functions
* `run(prompt, model, temperature)` that runs a prompt through the LLM model provided by OpenAI. 
* `transcribe(file_path, prompt)` that transcribes audio using the Whisper model provided by OpenAI.

#### claude_thinker.py

This module is a `ClaudeThinker` class which inherits the `Thinker` abstract class.

`def think(self, input: InputObject) -> OutputObject`

The `think` function takes the `InputObject`, generate the prompt through `generate_prompt`, and runs the prompt through the LLM.
The result of that is then parsed and the actions and text response from the agent is returned through the `OutputObject`.

`def generate_prompt(self, input: InputObject) -> str`

This is the function where the prompt to feed into the LLM is generated. The prompt includes several things
* Context (game state, player instruction, player memory etc.) expressed in textual form.
* The list of actions that the player can take, including examples of what is considered valid and what is not.
* The prompt for the text response according to the context and the list of actions.
* Out examples with formatting.

#### openai_thinker.py

Currently, this module works in the same way as the `claude_thinker.py` module.

### Web API

This is the flask app that enables the Brain to interface with the outside world. Refer to the `api_guide.md` to find out more about the design of the Web API.

## Deployment and Testing

### Remote Deployment

The Brain is deployed with fly.io under the name `valheim-agent-brain` in the Ego organization. Simply run `fly deploy` to deploy the application to the remote fly server.

### Local Testing

To test locally, you should
* Install the necessary dependencies `pip3 install -r requirements.txt`
* Run the program with `python3 src/app.py`
