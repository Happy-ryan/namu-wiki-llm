import httpx
from fastapi import HTTPException, status

class LibrarianClient:
    
    API_URL = "http://localhost:8001/librarian"

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