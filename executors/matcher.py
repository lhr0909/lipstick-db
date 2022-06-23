import os
from jina import Executor, requests, Document, DocumentArray

from storage import lipstick_db

if os.environ.get('WIFE_MODE') is None:
    db = lipstick_db
else:
    print('\n\n===================')
    print('Wife Mode Activated')
    print('===================\n\n')
    db = DocumentArray()
    subdocs: DocumentArray = lipstick_db['@.[meta]']
    filtered_subdocs: DocumentArray = subdocs.find({
        'tags__price': {
            '$lt': 100,
        },
    })
    for doc in filtered_subdocs:
        db.append(lipstick_db[doc.parent_id])

class LipstickTrialImageMatcher(Executor):
    @requests(on='/all')
    def get_all_lipsticks(self, parameters, **kwargs):
        if parameters.get('slice'):
            d = db[parameters.get('slice')]
            if isinstance(d, Document):
                return DocumentArray([d])
            else:
                return d
        return db

    @requests(on=['/lookup'])
    def lookup(self, docs: DocumentArray, parameters, **kwargs):
        da = DocumentArray()
        for doc in docs:
            parent_doc: Document = db['@c[7]c'][doc.parent_id]
            if parameters.get('type') == 'trial_image':
                da.append(parent_doc)
                continue
            grandparent_doc: Document = db['@c'][parent_doc.parent_id]
            great_grandparent_doc: Document = db[grandparent_doc.parent_id]
            da.append(great_grandparent_doc)
        return da

    @requests(on='/lip_search')
    def lip_search(self, docs: DocumentArray, **kwargs):
        lip_colors: DocumentArray = db['@c[7]cc[2]']
        docs.match(
            lip_colors,
            metric='cosine',
            limit=5,
        )
        return docs

    @requests(on='/skin_search')
    def skin_search(self, docs: DocumentArray, **kwargs):
        skin_colors: DocumentArray = db['@c[7]cc[1]']
        docs.match(
            skin_colors,
            metric='cosine',
            limit=5,
        )
        return docs
