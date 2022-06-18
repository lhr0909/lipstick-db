import cv2
import numpy as np
from jina import Executor, requests, Document, DocumentArray

class LipSkinColorEmbedder(Executor):
    @requests(on=['/s3_index', '/index'])
    def index(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            if len(doc.chunks) > 1:
                raise RuntimeError('chunks indices are off, please check pipeline')
            img_rgb: np.ndarray = doc.tensor
            mask: np.ndarray = doc.chunks[0].tensor
            img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
            skin_colors = self._get_colors_kmeans(img_hsv[mask == 255])
            skin_vector = self._get_histogram_vector(skin_colors)
            skin_colors_doc = Document(
                tensor=self._convert_hsv_tensor_to_rgb(skin_colors),
                embedding=skin_vector,
                modality='skin_colors',
            )
            doc.chunks.append(skin_colors_doc)
            lip_colors = self._get_colors_kmeans(img_hsv[mask == 128])
            lip_vector = self._get_histogram_vector(lip_colors)
            lip_colors_doc = Document(
                tensor=self._convert_hsv_tensor_to_rgb(lip_colors),
                embedding=lip_vector,
                modality='lip_colors',
            )
            doc.chunks.append(lip_colors_doc)
        return docs

    def _get_colors_kmeans(self, values, K=20):
        Z = np.float32(values)
        # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
        criteria = (cv2.TERM_CRITERIA_EPS, 100, 0.00001)
        compactness, labels, centers = cv2.kmeans(
            Z, K, None, criteria, 50, cv2.KMEANS_PP_CENTERS)
        colors = centers
        return colors

    def _get_palette(self, colors, size=100, K=10):
        palette = np.zeros((size, K * size, 3), dtype=np.uint8)
        for i in range(colors.shape[0]):
            palette[:, i * size: (i + 1) * size, :] = colors[i, :]
        return palette

    def _get_histogram_vector(self, hsv_colors, density=False, normalized=False):
        h_hist, h_hist_edges = np.histogram(
            hsv_colors[:, 0], bins=18, range=(0, 179), density=density)
        s_hist, h_hist_edges = np.histogram(
            hsv_colors[:, 1], bins=16, range=(0, 255), density=density)
        v_hist, h_hist_edges = np.histogram(
            hsv_colors[:, 2], bins=16, range=(0, 255), density=density)
        v = np.concatenate((h_hist, s_hist, v_hist), axis=None)
        if normalized:
            return v / np.sqrt(np.sum(v ** 2))
        else:
            return v

    def _convert_hsv_tensor_to_rgb(self, hsv: np.ndarray) -> np.ndarray:
        hsv_container = np.zeros((1, hsv.shape[0], hsv.shape[1]), dtype=np.uint8)
        hsv_sorted = hsv[np.lexsort((hsv[:, 0], hsv[:, 1], hsv[:, 2]))]
        hsv_container[0, :, :] = np.uint8(hsv_sorted)
        rgb_container = cv2.cvtColor(hsv_container, cv2.COLOR_HSV2RGB)
        return rgb_container[0, :, :]
