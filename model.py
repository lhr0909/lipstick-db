from typing import Any, Dict, TypeVar, List, Optional
from docarray import dataclass, field, Document
from docarray.typing import Text, JSON
from pydantic import BaseModel

TrialImages = TypeVar('TrialImages', bound=str)


def trial_images_setter(value: List[str]) -> Document:
    # TODO: this is still not a multi-modal document, but I think it is fine
    doc = Document(modality='trial_images')
    doc.chunks = [Document(
        uri=uri, modality='image').load_uri_to_image_tensor() for uri in value]
    return doc


def trial_images_getter(doc: Document) -> List[Dict[str, str]]:
    return [{'uri': d.uri, 'id': d.id} for d in doc.chunks]


@dataclass
class Lipstick:
    brand: Text
    series: Text
    color: Text
    name: Text
    nickname: Text
    meta: JSON
    product_image: Text
    # nested document for embeddings of skin and lip colors from all the trials
    trial_images: TrialImages = field(
        setter=trial_images_setter, getter=trial_images_getter, default_factory=lambda: [])


class LipstickModel(BaseModel):
    id: str
    brand: str
    series: str
    color: str
    name: str
    nickname: str
    meta: Dict[str, Any]
    product_image: str
    trial_images: Optional[List[Dict[str, str]]] = None


class LipstickTrialImageColors(BaseModel):
    id: str
    parent_id: str
    modality: str
    scores: Optional[Dict[str, Any]] = None
    tensor: List[List[int]]
    embedding: List[int]


class UploadRequest(BaseModel):
    filename: str
    fields: Optional[Dict[str, str]] = None

class UploadLink(BaseModel):
    url: str
    fields: Dict[str, str]


class SearchRequest(BaseModel):
    embeddings: List[List[int]]
    search_type: str = 'skin'

class SearchMatch(BaseModel):
    lipstick_id: str
    trial_image_id: str
    score: float

class SearchResponse(BaseModel):
    matches: List[SearchMatch]

def lipstick_doc_to_model(doc: Document, include_trial_images=False) -> LipstickModel:
    lipstick = Lipstick(doc)
    lipstick_model = LipstickModel(
        id=doc.id,
        brand=lipstick.brand,
        series=lipstick.series,
        color=lipstick.color,
        name=lipstick.name,
        nickname=lipstick.nickname,
        meta=lipstick.meta,
        product_image=lipstick.product_image,
        trial_images=lipstick.trial_images if include_trial_images else None
    )
    return lipstick_model
