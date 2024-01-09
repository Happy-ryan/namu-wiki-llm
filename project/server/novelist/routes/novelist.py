from fastapi import APIRouter, Form
from pydantic import BaseModel

from typing import Annotated


from infra.client import LibrarianClient

librarianClient = LibrarianClient()

novelist_router = APIRouter(tags=["Novelist"])

@novelist_router.post("/text")
async def get_resposne(text: Annotated[str, Form()]) -> dict:
    response_librarianClient = await librarianClient.search_document(text)
    
    return {"text" : {text},
            "response (librarianClient)" : {response_librarianClient}}