from fastapi import APIRouter, Form

from typing import Annotated, Union

from infra.librarian.client import LibrarianClient
from infra.wiseman.client import WisemanClient

librarian_client = LibrarianClient("./config.yaml")
wiseman_client = WisemanClient("./config.yaml")

novelist_router = APIRouter(tags=["Novelist"])

@novelist_router.post("/query")
async def get_resposne(query: Annotated[str, Form()]) -> Union[dict, None]:
    # librarian client가 elsatic에서 document 추출
    response_librarian_client = await librarian_client.search_document_content(query)
    
    document = response_librarian_client
    # 해당 검색이 없는 경우.
    if document is None:
        document = ''
        
    reponse_wiseman_client = await wiseman_client.get_resposne(query, document)

    
    return {"answer": reponse_wiseman_client}