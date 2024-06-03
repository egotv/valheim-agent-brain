class InputObject:
    
    def __init__(self, player_instruction, game_state, agent_commands=None):

        self.player_instruction = player_instruction
        self.game_state = game_state
        self.agent_commands = agent_commands

    