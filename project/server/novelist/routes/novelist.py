from fastapi import APIRouter, Form
from pydantic import BaseModel

from typing import Annotated


novelist_router = APIRouter(tags=["Novelist"])

@novelist_router.post("/text")
async def get_resposne(text: Annotated[str, Form()]) -> str:
    print("novelist 체크")
    return f"{text}를 입력하셨습니다."