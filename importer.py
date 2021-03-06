import os
from vika import Vika
from jina import Flow
from docarray import Document, DocumentArray
from multiprocessing import freeze_support
from jina.logging.profile import ProgressBar

from model import Lipstick
from storage import lipstick_db
from executors.face_mesher import FaceMesher
from executors.lip_skin_color_embedder import LipSkinColorEmbedder
from executors.s3_downloader import S3Downloader

flow = Flow().add(uses=S3Downloader).add(uses=FaceMesher).add(uses=LipSkinColorEmbedder)

vika = Vika(os.environ.get('VIKA_API_KEY'))
lipstick_datasheet = vika.datasheet(os.environ.get('VIKA_DATASHEET_ID'), field_key="name")
lipstick_trials_datasheet = vika.datasheet(
    os.environ.get('VIKA_TRIAL_DATASHEET_ID'), field_key="name")

if __name__ == '__main__':
    freeze_support()
    with flow, lipstick_db:
        records = lipstick_datasheet.records.all(viewId=os.environ.get('VIKA_VIEW_ID'))
        with ProgressBar(
            description='Importing Lipsticks Data from Vika',
            total_length=len(records),
        ) as pb:
            for record in records:
                fields = record.json()
                product_images = fields.get('产品图', [])
                product_image = product_images[0]['url'] if len(
                    product_images) > 0 else None
                trials_records = fields.get('口红试色', [])
                trial_images = []
                for trial_record_id in trials_records:
                    trial_record = lipstick_trials_datasheet.records.get(
                        trial_record_id)
                    trial_images += [image['url']
                                    for image in trial_record.json().get('附件', [])]
                lipstick = Lipstick(
                    brand=fields.get('品牌'),
                    series=fields.get('系列'),
                    color=fields.get('色号'),
                    name=fields.get('官方名称'),
                    nickname=fields.get('昵称/中文名称', fields.get('官方名称')),
                    meta={
                        'type': fields.get('类型'),
                        'texture': fields.get('质地'),
                        'price': fields.get('官方参考价格'),
                    },
                    product_image=product_image,
                    trial_images=trial_images,
                )
                document = Document(lipstick)
                da: DocumentArray = flow.post(
                    on='/index',
                    inputs=document.chunks[7].chunks,
                    parameters={},
                )
                document.chunks[7].chunks = da
                lipstick_db.append(document)
                pb.update()
