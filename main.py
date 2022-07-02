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
    asyncio=True,
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
async def get_lipsticks(client: JinaClient = Depends(get_jina_client)) -> List[LipstickModel]:
    lipsticks = []
    async for docs in client.post('/all'):
        for doc in docs:
            lipsticks.append(lipstick_doc_to_model(doc))
    return lipsticks


@app.get("/lipsticks/{id}")
async def get_lipstick(id: str, client: JinaClient = Depends(get_jina_client)) -> LipstickModel:
    async for db in client.post('/all', parameters={'slice': id}):
        doc = lipstick_doc_to_model(db[id], include_trial_images=True)
    return doc


@app.get("/lipsticks/{id}/trial_images/{trial_id}", response_model=List[LipstickTrialImageColors])
async def get_trial_image(id: str, trial_id: str, client: JinaClient = Depends(get_jina_client)) -> PydanticDocumentArray:
    async for db in client.post('/all', parameters={'slice': id}):
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
async def index_s3_file(
    filename: str,
    client: JinaClient = Depends(get_jina_client),
):
    document = Document(uri=filename)
    async for response in client.post(
        on='/s3_index',
        inputs=DocumentArray([document]),
    ):
        skin_colors: Document = response[0].chunks[1]
        lip_colors: Document = response[0].chunks[2]
    return DocumentArray([skin_colors, lip_colors]).to_pydantic_model()


@app.post("/search")
async def search(req: SearchRequest, client: JinaClient = Depends(get_jina_client)):
    docs = DocumentArray([Document(embedding=np.array(embedding, dtype=np.int32)) for embedding in req.embeddings])
    responses = []
    async for search_response in client.post(
        on=f'/{req.search_type}_search',
        inputs=docs,
    ):
        for doc in search_response:
            async for trial_image_lookup in client.post(
                on='/lookup',
                inputs = doc.matches,
                parameters={'type': 'trial_image'},
            ):
                async for lipstick_lookup in client.post(
                    on='/lookup',
                    inputs = doc.matches,
                    parameters={'type': 'lipstick'},
                ):
                    response = SearchResponse(
                        matches=[SearchMatch(
                            lipstick_id=lipstick_lookup[idx].id,
                            trial_image_id=trial_image_lookup[idx].id,
                            score=match.scores['cosine'].value,
                        ) for idx, match in enumerate(doc.matches)],
                    )
                    responses.append(response)
    return responses
