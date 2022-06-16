import os
from typing import List
from jina import Client as JinaClient
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from docarray import DocumentArray, Document
from docarray.document.pydantic_model import PydanticDocumentArray


from model import LipstickModel, UploadLink, UploadRequest, convert_hsv_tensor_to_rgb, lipstick_doc_to_model, LipstickTrialImageColors
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
    db = client.post('/all', parameters={'slice': id})
    trial_image: Document = db[id].chunks[-1].chunks[trial_id]
    skin_colors: Document = trial_image.chunks[1]
    skin_colors.tensor = convert_hsv_tensor_to_rgb(skin_colors.tensor)
    lip_colors: Document = trial_image.chunks[2]
    lip_colors.tensor = convert_hsv_tensor_to_rgb(lip_colors.tensor)
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
) -> str:
    document = Document(uri=filename)
    response: DocumentArray = client.post(
        on='/s3_index',
        inputs=DocumentArray([document]),
    )
    response.summary()
    response[0].summary()
    skin_colors: Document = response[0].chunks[1]
    skin_colors.tensor = convert_hsv_tensor_to_rgb(skin_colors.tensor)
    lip_colors: Document = response[0].chunks[2]
    lip_colors.tensor = convert_hsv_tensor_to_rgb(lip_colors.tensor)
    return DocumentArray([skin_colors, lip_colors]).to_pydantic_model()


@app.post("/search")
def search():
    pass
