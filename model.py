from typing import Any, Dict, TypeVar, List
from docarray import dataclass, field, Document
from docarray.typing import Image, Text, JSON
from pydantic import BaseModel

TrialImages = TypeVar('TrialImages', bound=str)

def trial_images_setter(value: List[str]) -> Document:
    # TODO: this is still not a multi-modal document, but I think it is fine
    doc = Document(modality='trial_images')
    doc.chunks = [Document(uri=uri, modality='image').load_uri_to_image_tensor() for uri in value]
    return doc

def trial_images_getter(doc: Document) -> List[str]:
    return [d.uri for d in doc.chunks]

@dataclass
class Lipstick:
    brand: Text
    color: Text
    nickname: Text
    meta: JSON
    product_image: Image
    # nested document for embeddings of skin and lip colors from all the trials
    trial_images: TrialImages = field(setter=trial_images_setter, getter=trial_images_getter, default_factory=lambda: [])

class LipstickModel(BaseModel):
    id: str
    brand: str
    color: str
    nickname: str
    meta: Dict[str, Any]
    product_image: str

def lipstick_doc_to_model(doc: Document) -> LipstickModel:
    lipstick = Lipstick(doc)
    lipstick_model = LipstickModel(
        id=doc.id,
        brand=lipstick.brand,
        color=lipstick.color,
        nickname=lipstick.nickname,
        meta=lipstick.meta,
        product_image=lipstick.product_image,
    )
    return lipstick_model