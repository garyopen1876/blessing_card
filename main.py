from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 允許跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE = "messages.txt"

class Message(BaseModel):
    message: str


@app.post("/add")
def add_message(msg: Message):

    with open(FILE, "a", encoding="utf-8") as f:
        f.write(msg.message + "\\n")

    return {"status": "ok"}


@app.get("/list")
def list_message():

    if not os.path.exists(FILE):
        return []

    with open(FILE, encoding="utf-8") as f:
        content = f.read() 
        lines = [line.strip() for line in content.split("\\n") if line.strip()]

    return lines


app.mount("/", StaticFiles(directory="static", html=True), name="static")