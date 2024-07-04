class AgentCommand:
    
    def __init__(self, category: str, action: str, parameters: dict) -> None:
        self.category = category
        self.action = action
        self.parameters = parameters

    def __repr__(self) -> str:
        return f"{self.category} - {self.action} - {self.parameters}"
    
    def to_json(self) -> dict:
        return {
            "category": self.category,
            "action": self.action,
            "parameters": self.parameters
        }
