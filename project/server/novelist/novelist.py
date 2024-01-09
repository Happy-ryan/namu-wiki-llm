from fastapi import FastAPI
from routes.novelist import novelist_router

import uvicorn

app = FastAPI()

app.include_router(novelist_router, prefix="/novelist", tags=["Novelist"])

@app.get("/")
async def servercheck() -> dict:
    return {
        "message" : "novelist server is OK!"
    }
    

if __name__ == "__main__":
    uvicorn.run("novelist:app", port=8000, host="0.0.0.0", reload=True)