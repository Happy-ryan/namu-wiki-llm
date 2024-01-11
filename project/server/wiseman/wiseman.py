from fastapi import FastAPI
from routes.wiseman import wiseman_router

import uvicorn

app = FastAPI()

app.include_router(wiseman_router, tags=["Wiseame"], prefix="/wiseman")

@app.get("/")
async def server_check() -> dict:
    return {
        "message" : "wiseman server is OK!"
    }


if __name__ == "__main__":
    uvicorn.run("wiseman:app", port = 8002, host="0.0.0.0", reload=True)