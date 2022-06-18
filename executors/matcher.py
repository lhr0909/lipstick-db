from jina import Executor, requests, Document, DocumentArray

from storage import lipstick_db


class LipstickTrialImageMatcher(Executor):
    @requests(on='/all')
    def get_all_lipsticks(self, parameters, **kwargs):
        if parameters.get('slice'):
            d = lipstick_db[parameters.get('slice')]
            if isinstance(d, Document):
                return DocumentArray([d])
            else:
                return d
        return lipstick_db

    @requests(on=['/lookup'])
    def lookup(self, docs: DocumentArray, parameters, **kwargs):
        da = DocumentArray()
        for doc in docs:
            parent_doc: Document = lipstick_db['@c[7]c'][doc.parent_id]
            if parameters.get('type') == 'trial_image':
                da.append(parent_doc)
                continue
            grandparent_doc: Document = lipstick_db['@c'][parent_doc.parent_id]
            great_grandparent_doc: Document = lipstick_db[grandparent_doc.parent_id]
            da.append(great_grandparent_doc)
        return da

    @requests(on='/lip_search')
    def lip_search(self, docs: DocumentArray, **kwargs):
        lip_colors: DocumentArray = lipstick_db['@c[7]cc[2]']
        docs.match(
            lip_colors,
            metric='cosine',
            limit=5,
        )
        return docs

    @requests(on='/skin_search')
    def skin_search(self, docs: DocumentArray, **kwargs):
        skin_colors: DocumentArray = lipstick_db['@c[7]cc[1]']
        docs.match(
            skin_colors,
            metric='cosine',
            limit=5,
        )
        return docs
