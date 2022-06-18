import os
from typing import List
from jina import Client as JinaClient
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from docarray import DocumentArray, Document
from docarray.document.pydantic_model import PydanticDocumentArray
import numpy as np


from model import LipstickModel, SearchMatch, SearchRequest, SearchResponse, UploadLink, UploadRequest, lipstick_doc_to_model, LipstickTrialImageColors
from s3 import BUCKET_NAME, s3_client, s3_resource


jina_client = JinaClient(
    host=os.environ.get('JINA_HOST', 'grpc://0.0.0.0:8888'),
)

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

def get_jina_client():
    yield jina_client


@app.get("/lipsticks")
def get_lipsticks(client: JinaClient = Depends(get_jina_client)) -> List[LipstickModel]:
    db = client.post('/all')
    lipsticks = []
    for doc in db:
        lipsticks.append(lipstick_doc_to_model(doc))
    return lipsticks


@app.get("/lipsticks/{id}")
def get_lipstick(id: str, client: JinaClient = Depends(get_jina_client)) -> LipstickModel:
    db = client.post('/all', parameters={'slice': id})
    doc = lipstick_doc_to_model(db[id], include_trial_images=True)
    return doc


@app.get("/lipsticks/{id}/trial_images/{trial_id}", response_model=List[LipstickTrialImageColors])
def get_trial_image(id: str, trial_id: str, client: JinaClient = Depends(get_jina_client)) -> PydanticDocumentArray:
    db: DocumentArray = client.post('/all', parameters={'slice': id})
    trial_image: Document = db[id].chunks[-1].chunks[trial_id]
    skin_colors: Document = trial_image.chunks[1]
    lip_colors: Document = trial_image.chunks[2]
    return DocumentArray([skin_colors, lip_colors]).to_pydantic_model()


@app.post("/upload")
def get_upload_link(req: UploadRequest, client = Depends(get_s3_client)) -> UploadLink:
    response = client.generate_presigned_post(BUCKET_NAME, req.filename, Fields=req.fields)
    response['filename'] = req.filename
    return response

@app.get("/upload/{filename}")
def get_upload_file_url(filename: str, client = Depends(get_s3_client)) -> str:
    url = client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': filename},
        ExpiresIn=1800,
    )
    return url

@app.get("/index/{filename}", response_model=List[LipstickTrialImageColors])
def index_s3_file(
    filename: str,
    client: JinaClient = Depends(get_jina_client),
):
    document = Document(uri=filename)
    response: DocumentArray = client.post(
        on='/s3_index',
        inputs=DocumentArray([document]),
    )
    skin_colors: Document = response[0].chunks[1]
    lip_colors: Document = response[0].chunks[2]
    return DocumentArray([skin_colors, lip_colors]).to_pydantic_model()


@app.post("/search")
def search(req: SearchRequest, client: JinaClient = Depends(get_jina_client)):
    docs = DocumentArray([Document(embedding=np.array(embedding, dtype=np.int32)) for embedding in req.embeddings])
    search_response: DocumentArray = client.post(
        on=f'/{req.search_type}_search',
        inputs=docs,
    )
    responses = []
    for doc in search_response:
        trial_image_lookup: DocumentArray = client.post(
            on='/lookup',
            inputs = doc.matches,
            parameters={'type': 'trial_image'},
        )
        lipstick_lookup: DocumentArray = client.post(
            on='/lookup',
            inputs = doc.matches,
            parameters={'type': 'lipstick'},
        )
        response = SearchResponse(
            matches=[SearchMatch(
                lipstick_id=lipstick_lookup[idx].id,
                trial_image_id=trial_image_lookup[idx].id,
                score=match.scores['cosine'].value,
            ) for idx, match in enumerate(doc.matches)],
        )
        responses.append(response)

    return responses
