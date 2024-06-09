class GameState:

    # Factory method from json
    @staticmethod
    def from_json(json: dict):
        return GameState(
            description=json['description']
        )
    
    def __init__(self, description: str) -> None:
        self.description = description

    def __repr__(self) -> str:
        return f"GameState(description={self.description})"
    
    def get_textual_description(self) -> str:
        return self.description