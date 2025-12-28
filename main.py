from fastapi import FastAPI
from database import engine, Base
import models
from routes.user_routes import router as user_router
from routes.note_routes import router as note_router
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(note_router)

@app.get("/")
def root():
    return {"msg": "Smart Notes API Running"}
