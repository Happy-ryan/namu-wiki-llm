import httpx, yaml
from fastapi import HTTPException, status

class WisemanClient:
    
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.conf = yaml.safe_load(f)
    
        self.API_URL = self.conf['wisemane_server_api']
    
    async def get_resposne(self, text: str, document: str):
        async with httpx.AsyncClient() as client:
            print("Wiseman Client 작동 확인")
            response = await client.post(
                f"{self.API_URL}/ask",
                
                data= {"text" : text, "document": document},
                
                timeout=None
            )
            
            print("document: ", document)

            if response.status_code != 200:
                raise HTTPException(
                    status_code= response.status_code,
                    detail= "[ERROR] Wiseman-GPT error"
                )
        
        answer = response.json()['answer']
        
        return answer