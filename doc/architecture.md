# System Architecture of Valheim Agent Brain

This is the service that enables the Valheim agent to think and translate its thoughts into actions.

## Components

### Brain

The Brain is the central component of this system. It takes input from the Input System, thinks through the Thinker, and outputs instructions through the Output System.

### Thinker (LLM Wrapper)

The Thinker defines an interface for the brain to use various LLMs to think.

### Input System

The Input System receives input from the player and the game, such as player commands, game states etc. It then passes the input to the Brain.

### Output System

The Output System receives commands from the Brain, which is then returned to the user making the API call.

### Web API

The API is made with Flask, which handles the communication between the outside world with the I/O systems.

## Flow
