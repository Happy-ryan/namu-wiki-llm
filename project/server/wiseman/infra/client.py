import httpx, yaml
from fastapi import HTTPException

class LLMClient:
    
    def __init__(self, config_path: str):
        
        with open(config_path) as f:
            self.conf = yaml.safe_load(f)

        self.OPENAI_API_URL = self.conf["openai_api"]["url"]
        self.OPENAI_API_KEY = self.conf["openai_api"]["key"]
        self.OPENAI_API_MODEL = self.conf["openai_api"]["model"]
    

    async def get_resposne(self, text: str):
        async with httpx.AsyncClient() as client:
            print("GPT Client ")
            response = await client.post(
                self.OPENAI_API_URL,
                headers={"Authorization": f"Bearer {self.OPENAI_API_KEY}"},
                json={"model": self.OPENAI_API_MODEL,
                    "messages": [
                        {"role": "user",
                        "content": text}
                    ]},
                timeout=None
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code,
                                    detail="[ERROR] LLMClient!")
                
            GPT_answer = response.json()['choices'][0]['message']['content']
            
            return GPT_answer
        