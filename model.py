from typing import Any, Dict, TypeVar, List, Optional
from docarray import dataclass, field, Document
from docarray.typing import Image, Text, JSON
from pydantic import BaseModel
import numpy as np
import cv2

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
    color: Text
    nickname: Text
    meta: JSON
    product_image: Image
    # nested document for embeddings of skin and lip colors from all the trials
    trial_images: TrialImages = field(
        setter=trial_images_setter, getter=trial_images_getter, default_factory=lambda: [])


class LipstickModel(BaseModel):
    id: str
    brand: str
    color: str
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

class UploadLink(BaseModel):
    url: str
    fields: Dict[str, str]


def lipstick_doc_to_model(doc: Document, include_trial_images=False) -> LipstickModel:
    lipstick = Lipstick(doc)
    lipstick_model = LipstickModel(
        id=doc.id,
        brand=lipstick.brand,
        color=lipstick.color,
        nickname=lipstick.nickname,
        meta=lipstick.meta,
        product_image=lipstick.product_image,
        trial_images=lipstick.trial_images if include_trial_images else None
    )
    return lipstick_model


def convert_hsv_tensor_to_rgb(hsv: np.ndarray) -> np.ndarray:
    hsv_container = np.zeros((1, hsv.shape[0], hsv.shape[1]), dtype=np.uint8)
    hsv_sorted = hsv[np.lexsort((hsv[:, 0], hsv[:, 1], hsv[:, 2]))]
    hsv_container[0, :, :] = np.uint8(hsv_sorted)
    rgb_container = cv2.cvtColor(hsv_container, cv2.COLOR_HSV2RGB)
    return rgb_container[0, :, :]
