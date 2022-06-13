from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from docarray import DocumentArray

from model import Lipstick, LipstickModel, lipstick_doc_to_model
from storage import lipstick_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_docarray():
    yield lipstick_db

@app.get("/lipsticks")
def read_root(db: DocumentArray = Depends(get_docarray)) -> List[LipstickModel]:
    lipsticks = []
    for doc in db:
        lipsticks.append(lipstick_doc_to_model(doc))
    return lipsticks
