from jina import Executor, requests, Document, DocumentArray

from storage import lipstick_db


class LipstickTrialImageMatcher(Executor):
    @requests(on='/all')
    def get_all_lipsticks(self, **kwargs):
        return lipstick_db

    @requests(on=['/lookup'])
    def lookup(self, docs: DocumentArray, **kwargs):
        da = DocumentArray()
        for doc in docs:
            parent_doc: Document = lipstick_db['@c[-1]c'][doc.parent_id]
            grandparent_doc: Document = lipstick_db['@c'][parent_doc.parent_id]
            great_grandparent_doc: Document = lipstick_db[grandparent_doc.parent_id]
            da.append(great_grandparent_doc)
        return da

    @requests(on='/lip_search')
    def lip_search(self, docs: DocumentArray, **kwargs):
        lip_colors: DocumentArray = lipstick_db['@c[-1]cc[2]']
        lip_color_query: DocumentArray = docs['@c[2]']
        lip_color_query.match(
            lip_colors,
            metric='cosine',
            limit=10,
        )
        docs['@c[2]'] = lip_color_query
        return docs

    @requests(on='/skin_search')
    def skin_search(self, docs: DocumentArray, **kwargs):
        skin_colors: DocumentArray = lipstick_db['@c[-1]cc[1]']
        skin_color_query: DocumentArray = docs['@c[1]']
        skin_color_query.match(
            skin_colors,
            metric='cosine',
            limit=10,
        )
        docs['@c[1]'] = skin_color_query
        return docs
