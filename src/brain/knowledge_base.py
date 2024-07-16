import os
import pandas as pd
from typing import List, Dict
import json

BASE_DIR_PATH = 'valheim_knowledge_base'

PRIMARY_KEYS = {
    "armor.csv": "Armor",
    "crafting_system.csv": "Upgrade",
    "material_food.csv": "Item",
    "structure.csv": "Structure",
    "tool.csv": "Tool",
    "weapon.csv": "Weapon",
    "ammunition.csv": "Ammunition"
}

class KnowledgeBaseSystem:

    @staticmethod
    def get_all_csv_files_in_knowledge_base() -> List[str]:

        if not os.path.exists(BASE_DIR_PATH):
            raise FileNotFoundError(f"Directory not found: {BASE_DIR_PATH}")

        all_files = [file_name for file_name in os.listdir(BASE_DIR_PATH) if file_name.endswith(".csv")]
        return all_files

    @staticmethod
    def csv_loader(file_path: str) -> pd.DataFrame:

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.endswith(".csv"):
            raise ValueError(f"File is not a CSV file: {file_path}")

        return pd.read_csv(file_path)
    
    @staticmethod
    def json_loader(file_path: str) -> Dict:

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.endswith(".json"):
            raise ValueError(f"File is not a JSON file: {file_path}")

        with open(file_path, 'r') as f:
            return json.load(f)

    def __init__(self) -> None:
        self.knowledge_base = self.load_knowledge_base()
        self.all_items_list = self.load_all_items()
        self.monsters_list = self.load_monsters()

    def load_knowledge_base(self) -> Dict[str, Dict[str, dict]]:
            
        knowledge_base = {}

        for file_name in self.get_all_csv_files_in_knowledge_base():

            file_path = os.path.join(BASE_DIR_PATH, file_name)
            
            # Load the csv
            df = self.csv_loader(file_path)
            df.dropna(how='all', inplace=True)
            primary_key = PRIMARY_KEYS[file_name]
            this_file_knowledge = df.set_index(primary_key).to_dict(orient='index')

            # Add the knowledge to the knowledge base
            knowledge_base[file_name] = this_file_knowledge

        return knowledge_base
    
    def load_all_items(self) -> List[dict]:
        loaded_json = self.json_loader(f"{BASE_DIR_PATH}/all_items_list.json")
        return list(map(lambda x: x['name'], loaded_json))
    
    def load_monsters(self) -> List[dict]:
        loaded_json = self.json_loader(f"{BASE_DIR_PATH}/monsters.json")
        return list(map(lambda x: x['name'], loaded_json))
    
    def get_all_items(self) -> List[dict]:
        return self.all_items_list
    
    def get_monsters(self) -> List[dict]:
        return self.monsters_list
    
    '''
    The knowledge base is a collection of CSV files, which contain information on topics in Valheim gameplay.
    For example, the "crafting system" csv has headers: [Crafting Station,Upgrade,Crafting Station Level,Materials Required,Description]
    
    The player says something to the agent (the query), and the agent needs to find the most relevant information
    in the knowledge base to augment the prompt to call the LLM-based thinker.

    To find the relevant information, the agent should find words in the query that matches the keys in the dataframe.
    The matching is done by string matching.
    The agent should return the top N most relevant rows from the dataframe.
    '''
    def lookup_knowledge_base(self, query: str, number_of_rows: int=5) -> List[Dict[str, str]]:

        query_lower = query.lower()
        relevant_knowledge = []

        for file_name, knowledge in self.knowledge_base.items():
            for item_name, value in knowledge.items():
                
                item_name_lower = item_name.lower()

                # Break query into words
                query_words = query_lower.split()

                # Break item name into words
                item_name_words = item_name_lower.split()

                # Check if any of the words in the query are in the item name
                if any([word in item_name_words for word in query_words]):
                    relevant_knowledge.append({ **value, 'Name': item_name })

                # Check if any of the words in the item name are in the query
                elif any([word in query_words for word in item_name_words]):
                    relevant_knowledge.append({ **value, 'Name': item_name })

        return relevant_knowledge[:number_of_rows]

# if __name__ == "__main__":

#     kbs = KnowledgeBaseSystem()
#     #print(json.dumps(kbs.knowledge_base, sort_keys=True, indent=2))
#     print(json.dumps(kbs.lookup_knowledge_base("I want to eat mushroom"), sort_keys=True, indent=2))



    