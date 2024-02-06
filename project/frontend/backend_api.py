import yaml, requests
import streamlit as st


class Novelist:
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.conf = yaml.safe_load(f)
        
        self.novelist_api = self.conf["novelist"]
    
    
    def get_response(self, query: str) -> str:
        form_data = {
            "query": query
        }
        response = requests.post(f"{self.novelist_api}/query", data=form_data)
        
        answer = response.json()['answer']
        
        print(answer)
        
        return answer
