import httpx, yaml
from fastapi import HTTPException, status

class LibrarianClient:
    
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.conf = yaml.safe_load(f)
    
        self.API_URL = self.conf['librarian_server_api']

    async def search_document(self, text: str):
        async with httpx.AsyncClient() as client:
            print("Librarian client 작동 확인")
            response = await client.post(
                f"{self.API_URL}/search",
                data={
                    "text": text,
                },
                timeout=None
                )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="[ERROR] LibrarianClient!"
                )
                
        result = response.json()["text"]
        
        return result