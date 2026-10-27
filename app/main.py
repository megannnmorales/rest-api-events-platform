from fastapi import FastAPI
from app.routes.events import events_router

app = FastAPI()

app.include_router(events_router)