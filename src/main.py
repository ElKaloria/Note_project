from fastapi import FastAPI
from src.note_app.routers import router as note_app_router

app = FastAPI()

app.include_router(note_app_router)

