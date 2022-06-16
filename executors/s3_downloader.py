import io
from jina import Executor, requests, DocumentArray
from docarray.document.mixins.image import _to_image_tensor

from s3 import BUCKET_NAME, s3_client


class S3Downloader(Executor):
    @requests(on='/s3_index')
    def download_from_s3(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            # get the file from s3
            s3_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=doc.uri)
            # get the file content
            content = s3_object['Body'].read()
            file_content = io.BytesIO(content)
            # index the file
            doc.tensor = _to_image_tensor(file_content)
        return docs