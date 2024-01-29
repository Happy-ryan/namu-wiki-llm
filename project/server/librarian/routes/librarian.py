from fastapi import APIRouter, Form

from typing import Union

# python warning 방지용
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

librarian_router = APIRouter(tags=["Librarian"])

from infra.model import ElasticClient
elsaticsearch_client = ElasticClient("korean_analyzer", "./config.yaml", "./config.json")

def elastic_explorer_filed(query: str) -> Union[list[str], None]:
    response = elsaticsearch_client.search_by_field(query)
    
    documents = []
    
    if len(response['hits']['hits']) == 0:
        return None
    
    for idx, result in enumerate(response['hits']['hits']):
            pretty_out = f"{idx} - ID: {result['_id']}\nScore: {result['_score']}\nTitle: {result['_source']['title']}\n=Content=\n {result['_source']['content']}"
            documents.append(pretty_out)
            
    return documents


def elastic_explorer_id(title_query: str) -> Union[str, None]:
    res = elsaticsearch_client.search_by_id(title_query)
    
    if len(res['hits']['hits']) == 0:
        return None
    
    for result in res['hits']['hits']:
            pretty_out = f"ID: {result['_id']}\nScore: {result['_score']}\nTitle: {result['_source']['title']}\n=Content=\n {result['_source']['content']}"
            
    return pretty_out


@librarian_router.get("/search-content/{query}")
async def get_documents(query: str) -> dict:
    documents = elastic_explorer_filed(query)
    
    if documents is None:
        return {
            f"{query}": "해당 내용을 가진 문서를 찾지 못했어요. 다시 검색해주세요."
        }

    return {
            "찾은 문서 중 가장 score가 높은 문서" : documents[0]
            }
    
@librarian_router.get("/search-title/{query}")
async def get_documents(query: str) -> dict:
    document = elastic_explorer_id(query)
    
    if document is None:
        return {
            f"title이 {query}인 해당 문서": "없는 문서입니다. 다시 입력해주세요."
        }
        
    return {
        f"title이 {query}인 해당 문서": document 
    }