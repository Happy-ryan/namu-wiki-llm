from fastapi import FastAPI, Form

from routes.librarian import librarian_router

import uvicorn

app = FastAPI()

app.include_router(librarian_router,prefix="/librarian",tags=["Librarian"])

@app.get("/")
async def server_check() -> dict:
    return {
        "message" : "librarian is OK!"
        }

if __name__ == "__main__":
    uvicorn.run("librarian:app", port=8001, host="0.0.0.0", reload=True)