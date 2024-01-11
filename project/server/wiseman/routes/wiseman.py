from fastapi import APIRouter, Form
from pydantic import BaseModel

from typing import Annotated

wiseman_router = APIRouter(tags=["Wiseman"])


class Question(BaseModel):
    text: str
    document: dict
    
    
@wiseman_router.post("/ask")
async def get_LLM_answer(question: Question):
    gpt_query = f'''[{question.document}] []안의 내용을 3줄로 요약해줘!
                '''
    # content - gpt api의 결과물을 의미
    return {
        "guide" : f'|{question.text}|에 대한 답변은 GPT-4 기반 AI로 작성되었습니다.',
        "content" : gpt_query
    }
    

# @wiseman_router.post("/ask1")
# async def get_LLM_answer(text: Annotated[str, Form()], document: Annotated[dict, Form()]):
#     gpt_query = f'''[{document}] 
#                 \n
#                 위의 []안의 내용을 3줄로 요약해줘!
#                 '''
#     # content - gpt api의 결과물을 의미
#     return {
#         "guide" : f'|{text}| 에 대한 답변은 GPT-4 기반 AI로 작성되었습니다.',
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
    
    


