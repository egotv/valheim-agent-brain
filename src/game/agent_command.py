class AgentCommand:
    
    def __init__(self, action_code: int, action_str: str):
        self.action_code = action_code
        self.action_str = action_str

    def __repr__(self) -> str:
        return f"[{self.action_code}] {self.action_str}"
    
    def to_json(self) -> dict:
        return {
            "action_code": self.action_code,
            "action_str": self.action_str
        }
    
    @staticmethod
    def get_action_str_from_code(action_code: int) -> str:
        return {
            1: "StartFollowingPlayer",
            2: "StartAttacking",
            3: "StartHarvesting",
            4: "StartPatrolling"
        }.get(action_code, "Invalid action code")