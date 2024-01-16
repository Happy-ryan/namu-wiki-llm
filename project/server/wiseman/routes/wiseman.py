from fastapi import APIRouter, Form
from pydantic import BaseModel

from typing import Annotated

from infra.client import WisemanClient

wiseman_router = APIRouter(tags=["Wiseman"])

wiseman_client = WisemanClient("./config.yaml")


@wiseman_router.post("/ask")
async def get_LLM_answer(text: Annotated[str, Form()], document: Annotated[str, Form()]) -> dict:
    gpt_query = f'''
                query:
                - [{text}]
                
                reference:
                - [{document}]
                '''
    # content - gpt api의 결과물을 의미
    content = await wiseman_client.get_GPT_answer(gpt_query)
    
    return {
        "guide" : f'|{text}| 에 대한 답변은 GPT-4 기반 AI로 작성되었습니다.',
        "content" : content
    }
    
    
# class Question(BaseModel):
#     text: str
#     document: str
    
    
# @wiseman_router.post("/ask")
# async def get_LLM_answer(question: Question):
#     gpt_query = f'''[{question.document}] []안의 내용을 3줄로 요약해줘!
#                 '''
#     # content - gpt api의 결과물을 의미
#     return {
#         "guide" : f'|{question.text}|에 대한 답변은 GPT-4 기반 AI로 작성되었습니다.',
#         "content" : gpt_query
#     }    
    
# class ValinaQuestion:
#         def __init__(self, text: str, document: dict):
#             self.text = text
#             self.document = document
            
#         def get_text(self):
#             return self.text
        
#         def get_documents(self):
#             return self.document
            

# @wiseman_router.post("/ask2")
# async def get_LLM_answer(question: ValinaQuestion):
#     gpt_query = f'''[{question.get_documents()}] 
#                 \n
#                 위의 []안의 내용을 3줄로 요약해줘!
#                 '''
#     # content - gpt api의 결과물을 의미
#     return {
#         "guide" : f"질문: {question.get_text()} \n 에 대한 답변은 GPT-4 기반 AI로 작성되었습니다.",
#         "content" : gpt_query
#     }



