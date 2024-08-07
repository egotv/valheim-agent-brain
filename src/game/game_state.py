import json

class GameState:

    # Factory method from json
    @staticmethod
    def from_json(json_object: dict):
        return GameState(
            description=json.dumps(json_object)
        )
    
    def __init__(self, description: str) -> None:
        self.description = description

    def __repr__(self) -> str:
        return f"GameState(description={self.description})"
    
    def item_name_conversion(self, item_name):
        # Replace special characters and capitalize each word
        return ' '.join(word.capitalize() for word in item_name.replace('$item_', '').replace('_', ' ').split())

    def get_textual_description(self) -> str:
        description = self.description
        description = json.loads(description)
        print(description)
        
        health = description["Health"]
        stamina = description["Stamina"]
        
        inventory_items = description["Inventory"]
        inventory_description = ", ".join([f'{self.item_name_conversion(item["name"])} (x{item["amount"]})' for item in inventory_items])
        
        npc_mode = description["NPC_Mode"]
        alerted = "Yes" if description["Alerted"] else "No"
        is_cold = "Yes" if description["IsCold"] else "No"
        is_freezing = "Yes" if description["IsFreezing"] else "No"
        is_wet = "Yes" if description["IsWet"] else "No"
        
        current_time = description["currentTime"]
        current_weather = description["currentWeather"]
        current_biome = description["currentBiome"]
        
        nearby_items = json.loads(description["nearbyItems"])
        nearby_items_description = ", ".join([f'{self.item_name_conversion(item["name"])} (x{item["quantity"]}, nearest: {item["nearestDistance"]})' for item in nearby_items])
        
        nearby_enemies = json.loads(description["nearbyEnemies"])
        nearby_enemies_description = ", ".join([f'{enemy["name"]} (x{enemy["quantity"]}, nearest: {enemy["nearestDistance"]})' for enemy in nearby_enemies])
        
        result = (
            f"Health: {health}\n"
            f"Stamina: {stamina}\n"
            f"Inventory: {inventory_description}\n"
            f"NPC Mode: {npc_mode}\n"
            f"Alerted: {alerted}\n"
            f"Is Cold: {is_cold}\n"
            f"Is Freezing: {is_freezing}\n"
            f"Is Wet: {is_wet}\n"
            f"Current Time: {current_time}\n"
            f"Current Weather: {current_weather}\n"
            f"Current Biome: {current_biome}\n"
            f"Nearby Items: {nearby_items_description}\n"
            f"Nearby Enemies: {nearby_enemies_description}"
        )
        
        return result