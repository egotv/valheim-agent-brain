import os
import pandas as pd
from typing import List, Dict
import json
from transformers import AutoTokenizer, AutoModel
import torch
import time

BASE_DIR_PATH = 'valheim_knowledge_base'

PRIMARY_KEYS = {
    "armor.csv": "Item",
    "crafting_system.csv": "Upgrade",
    "material_food.csv": "Item",
    "structure.csv": "Structure",
    "tool.csv": "Tool",
    "weapon.csv": "Weapon"
}

class KnowledgeBaseSystem:

    @staticmethod
    def get_all_files_in_knowledge_base() -> List[str]:

        if not os.path.exists(BASE_DIR_PATH):
            raise FileNotFoundError(f"Directory not found: {BASE_DIR_PATH}")

        return [file_name for file_name in os.listdir(BASE_DIR_PATH)]

    @staticmethod
    def csv_loader(file_path: str) -> pd.DataFrame:

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.endswith(".csv"):
            raise ValueError(f"File is not a CSV file: {file_path}")

        return pd.read_csv(file_path)

    def __init__(self) -> None:

        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

        self.knowledge_base = self.load_knowledge_base()

    def encode_sentence(self, sentence: str) -> torch.Tensor:

        inputs = self.tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)
    
    def compute_similarity(self, embedding0: torch.Tensor, embedding1: torch.Tensor) -> float:
            
        return torch.nn.functional.cosine_similarity(embedding0, embedding1).item()

    def load_knowledge_base(self) -> Dict[str, Dict[str, dict]]:
            
        knowledge_base = {}

        for file_name in self.get_all_files_in_knowledge_base():

            file_path = os.path.join(BASE_DIR_PATH, file_name)
            
            # Load the csv
            df = self.csv_loader(file_path)
            df = df.dropna()
            primary_key = PRIMARY_KEYS[file_name]
            this_file_knowledge = df.set_index(primary_key).to_dict(orient='index')

            # Embed the knowledge
            for key, value in this_file_knowledge.items():
                value_with_key = { **value, primary_key: key }
                value['embedding'] = self.encode_sentence(json.dumps(value_with_key))

            # Add the knowledge to the knowledge base
            knowledge_base[file_name] = this_file_knowledge

        return knowledge_base
    
    '''
    The knowledge base is a collection of CSV files, which contain information on topics in Valheim gameplay.
    For example, the "crafting system" csv has headers: [Crafting Station,Upgrade,Crafting Station Level,Materials Required,Description]
    
    The player says something to the agent (the query), and the agent needs to find the most relevant information
    in the knowledge base to augment the prompt to call the LLM-based thinker.

    To find the relevant information, the agent should find words in the query that matches the keys in the dataframe.
    The matching is done by semantic similarity.
    The agent should return the top N most relevant rows from the dataframe.
    The depth parameter specifies the number of layers of the recursive search in the knowledge base.
    The number_of_rows parameter specifies the number of rows to return from the dataframe per layer of the recursive search.
    '''
    def lookup_knowledge_base(self, query: str, number_of_rows: int=5) -> List[Dict[str, str]]:

        # Encode the query
        query_embedding = self.encode_sentence(query)

        # Compute the similarity between the query and each row in the knowledge base
        similarity_scores = {}
        for file_name, file_knowledge in self.knowledge_base.items():
            for key, value in file_knowledge.items():
                similarity_scores[(file_name, key)] = self.compute_similarity(query_embedding, value['embedding'])

        # Sort the similarity scores
        sorted_similarity_scores = {k: v for k, v in sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)}

        # Get the top N rows from the knowledge base
        top_rows = []
        for i, (file_name_primary_key_pair, value) in enumerate(sorted_similarity_scores.items()):

            if i >= number_of_rows:
                break

            file_name, key = file_name_primary_key_pair
            value_without_embedding = self.knowledge_base[file_name][key].copy()
            del value_without_embedding['embedding']
            top_rows.append({ **value_without_embedding, 'key': key })

        return top_rows
    
# if __name__ == '__main__':

#     knowledge_base_system = KnowledgeBaseSystem()

#     query = "Kill monsters! I need to upgrade my weapon!"

#     print(time.time())
#     result = knowledge_base_system.lookup_knowledge_base(query)
#     print(time.time())

#     for row in result:
#         del row['embedding']
#         print(row)




    