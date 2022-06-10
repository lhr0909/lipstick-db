from docarray import Document, DocumentArray
from jina import Flow

from indexer import LipstickTrialImageIndexer
from matcher import LipstickTrialImageMatcher


flow = Flow(
    port=8888,
).add(
    uses=LipstickTrialImageIndexer,
).add(
    uses=LipstickTrialImageMatcher,
)

with flow:
    # flow.block()
    query_doc = Document(uri='test_image1.jpeg').load_uri_to_image_tensor()
    lip_results = flow.post(on='/lip_search', inputs=DocumentArray([Document(query_doc, copy=True)]))
    for doc in lip_results:
        doc.summary()
    skin_results = flow.post(on='/skin_search', inputs=DocumentArray([Document(query_doc, copy=True)]))
    for doc in skin_results:
        doc.summary()
    # lip_lookup = flow.post(on='/lookup', inputs=lip_results['@c[2]m'])
    # for doc in lip_lookup:
    #     doc.summary()
    # skin_lookup = flow.post(on='/lookup', inputs=skin_results['@c[1]m'])
    # for doc in skin_lookup:
    #     doc.summary()