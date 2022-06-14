import os
from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from docarray import DocumentArray, Document
from docarray.document.pydantic_model import PydanticDocumentArray

from model import LipstickModel, UploadLink, UploadRequest, convert_hsv_tensor_to_rgb, lipstick_doc_to_model, LipstickTrialImageColors
from storage import lipstick_db
from s3 import s3_client, s3_resource

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'lipstick-db')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_s3_client():
    return s3_client

def get_s3_resource():
    return s3_resource

def get_docarray():
    yield lipstick_db


@app.get("/lipsticks")
def get_lipsticks(db: DocumentArray = Depends(get_docarray)) -> List[LipstickModel]:
    lipsticks = []
    for doc in db:
        lipsticks.append(lipstick_doc_to_model(doc))
    return lipsticks


@app.get("/lipsticks/{id}")
def get_lipstick(id: str, db: DocumentArray = Depends(get_docarray)) -> LipstickModel:
    doc = lipstick_doc_to_model(db[id], include_trial_images=True)
    return doc


@app.get("/lipsticks/{id}/trial_images/{trial_id}", response_model=List[LipstickTrialImageColors])
def get_trial_image(id: str, trial_id: str, db: DocumentArray = Depends(get_docarray)) -> PydanticDocumentArray:
    trial_image: Document = db[id].chunks[5].chunks[trial_id]
    skin_colors: Document = trial_image.chunks[1]
    skin_colors.tensor = convert_hsv_tensor_to_rgb(skin_colors.tensor)
    lip_colors: Document = trial_image.chunks[2]
    lip_colors.tensor = convert_hsv_tensor_to_rgb(lip_colors.tensor)
    return DocumentArray([skin_colors, lip_colors]).to_pydantic_model()


@app.post("/upload")
def get_upload_link(req: UploadRequest, client = Depends(get_s3_client)) -> UploadLink:
    return client.generate_presigned_post(BUCKET_NAME, req.filename)


@app.post("/search")
def search():
    pass
