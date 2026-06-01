from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analyze import router as analyze
from app.routes.chat import router as chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze)
app.include_router(chat)

@app.get("/")
def root():
    return {"message": "Welcome to the RAG Video Analyzer API!"}