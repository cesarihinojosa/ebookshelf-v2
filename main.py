from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from goodreads_adapter import GoodreadsAdapter

app = FastAPI()
goodreads_adapter = GoodreadsAdapter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/api/get_books")
def read_root():
    return goodreads_adapter.get_books_read(144045223)

app.mount("/", StaticFiles(directory="static", html=True), name="static")