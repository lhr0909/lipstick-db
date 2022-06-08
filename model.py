from typing import TypeVar, List
from docarray import dataclass, field, Document
from docarray.typing import Image, Text, JSON

TrialImages = TypeVar('TrialImages', bound=str)

def trial_images_setter(value: List[str]) -> Document:
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
    trial_images: TrialImages = field(setter=trial_images_setter, getter=trial_images_getter, default_factory=[])
