import os
from vika import Vika
from jina import Flow
from jina.logging.profile import ProgressBar
from docarray import Document

from executor import LipstickTrialImageExecutor
from model import Lipstick
from storage import lipstick_db

flow = Flow(
    port=8888,
).add(
    uses=LipstickTrialImageExecutor,
    name='lipstickTrialImageExecutor',
)

vika = Vika(os.environ.get('VIKA_API_KEY'))
lipstick_datasheet = vika.datasheet("dstHNrtRuqeMGdpqji", field_key="name")
lipstick_trials_datasheet = vika.datasheet("dst6uTXHrt2SXHTaix", field_key="name")

with flow, lipstick_db:
    records = lipstick_datasheet.records.all(viewId="viwXrKXF2XXol")
    with ProgressBar(
        description='Importing Lipsticks Data from Vika',
        total_length=len(records),
    ) as pb:
        for record in records:
            fields = record.json()
            product_images = fields.get('产品图', [])
            product_image = product_images[0]['url'] if len(product_images) > 0 else None
            trials_records = fields.get('口红试色', [])
            trial_images = []
            for trial_record_id in trials_records:
                trial_record = lipstick_trials_datasheet.records.get(trial_record_id)
                trial_images += [image['url'] for image in trial_record.json().get('附件', [])]
            lipstick = Lipstick(
                brand=fields.get('品牌'),
                color=fields.get('色号'),
                nickname=fields.get('昵称'),
                meta={
                    'type': fields.get('类型'),
                },
                product_image=product_image,
                trial_images=trial_images,
            )
            document = Document(lipstick)
            da = flow.post(
                on='/index',
                inputs=document.chunks[5].chunks,
            )
            document.chunks[5].chunks = da
            lipstick_db.append(document)
            pb.update()
