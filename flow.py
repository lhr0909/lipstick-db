from multiprocessing import freeze_support
from jina import Flow

from executors.s3_downloader import S3Downloader
from executors.face_mesher import FaceMesher
from executors.lip_skin_color_embedder import LipSkinColorEmbedder
from executors.matcher import LipstickTrialImageMatcher

flow = Flow(
    port=8888,
    protocol='grpc',
    compression='Gzip',
    prefetch=2,
).add(
    uses=S3Downloader,
).add(
    uses=FaceMesher,
).add(
    uses=LipSkinColorEmbedder,
).add(
    uses=LipstickTrialImageMatcher,
)

if __name__ == '__main__':
    freeze_support()
    with flow:
        flow.block()
