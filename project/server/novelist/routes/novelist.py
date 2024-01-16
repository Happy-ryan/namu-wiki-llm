from fastapi import APIRouter, Form
from pydantic import BaseModel

from typing import Annotated


from infra.librarian.client import LibrarianClient
from infra.wiseman.client import WisemanClient

librarianClient = LibrarianClient()
wisemanClient = WisemanClient()

novelist_router = APIRouter(tags=["Novelist"])

@novelist_router.post("/text")
async def get_resposne(text: Annotated[str, Form()]) -> dict:
    
    response_librarianClient = await librarianClient.search_document(text)
    
    document = response_librarianClient
    
    reponse_wisemanClient = await wisemanClient.get_GPT_answer(text, document)
    
    return {"text" : {text},
            "response (librarianClient)" : {response_librarianClient},
            "response (wisemanClient) - guide" : {reponse_wisemanClient[0]},
            "response (wisemanClient) - content" : {reponse_wisemanClient[1]},}