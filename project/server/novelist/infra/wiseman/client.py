import httpx
from fastapi import HTTPException, status

class WisemanClient:
    
    API_URL = "http://localhost:8002/wiseman"
    
    async def get_GPT_answer(self, text: str, document: str) -> tuple:
        async with httpx.AsyncClient() as client:
            print("Wiseman Client 작동 확인")
            response = await client.post(
                f"{self.API_URL}/ask",
                
                data= {"text" : text, "document": document},
                
                timeout=None
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code= response.status_code,
                    detail= "[ERROR] Wiseman-GPT error"
                )
            
        guide = response.json()['guide']
        content = response.json()['content']
        
        return (guide, content)