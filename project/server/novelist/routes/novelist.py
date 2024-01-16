from fastapi import APIRouter, Form
from pydantic import BaseModel

from typing import Annotated


from infra.librarian.client import LibrarianClient
from infra.wiseman.client import WisemanClient

librarianClient = LibrarianClient("./config.yaml")
wisemanClient = WisemanClient("./config.yaml")

novelist_router = APIRouter(tags=["Novelist"])

@novelist_router.post("/text")
async def get_resposne(text: Annotated[str, Form()]) -> dict:
    
    response_librarianClient = await librarianClient.search_document(text)
    
    document = response_librarianClient
    
    reponse_wisemanClient = await wisemanClient.get_GPT_answer(text, document)
    
    return {"text_query" : {text},
            "response_librarianClient_document" : {response_librarianClient},
            "response_wisemanClient_guide" : {reponse_wisemanClient[0]},
            "response_wisemanClient_content" : {reponse_wisemanClient[1]},}