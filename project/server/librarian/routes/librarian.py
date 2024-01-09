from fastapi import APIRouter, Form

from typing import Annotated

librarian_router = APIRouter(tags=["Librarian"])

@librarian_router.post("/search")
async def get_documents(text: Annotated[str, Form()]) -> dict:    
    return {
            "text" : text + " 관련 문서 검색 결과 출력"
            }
    