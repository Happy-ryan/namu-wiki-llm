from fastapi import APIRouter, Form
from pydantic import BaseModel

from typing import Annotated


from infra.librarian.client import LibrarianClient
from infra.wiseman.client import WisemanClient

librarian_client = LibrarianClient("./config.yaml")
wiseman_client = WisemanClient("./config.yaml")

novelist_router = APIRouter(tags=["Novelist"])

@novelist_router.post("/text")
async def get_resposne(text: Annotated[str, Form()]) -> dict:
    
    response_librarian_client = await librarian_client.search_document(text)
    
    document = response_librarian_client
    
    reponse_wiseman_client = await wiseman_client.get_resposne(text, document)
    
    return {"text_query" : {text},
            "response_librarianClient_document" : {response_librarian_client},
            "response_wisemanClient_guide" : {reponse_wiseman_client[0]},
            "response_wisemanClient_content" : {reponse_wiseman_client[1]},}