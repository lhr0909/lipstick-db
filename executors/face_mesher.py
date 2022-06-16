import cv2
import numpy as np
import mediapipe as mp
from jina import Executor, requests, Document, DocumentArray

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

FACE_MESH_OUTER_LIP = [
    (61, 146), (146, 91), (91, 181), (181, 84), (84, 17), (17, 314), (314, 405),
    (405, 321), (321, 375), (375, 291), (291, 409), (409, 270), (270, 269),
    (269, 267), (267, 0), (0, 37), (37, 39), (39, 40), (40, 185), (185, 61),
]

FACE_MESH_INNER_LIP = [
    (78, 95), (95, 88), (88, 178), (178, 87), (87, 14), (14, 317), (317, 402),
    (402, 318), (318, 324), (324, 308), (308, 415), (415, 310), (310, 311),
    (311, 312), (312, 13), (13, 82), (82, 81), (81, 80), (80, 191), (191, 78),
]

FACE_MESH_LEFT_CHEEK = [
    (451, 450), (450, 449), (449, 448), (448, 261), (261, 265),
    (265, 372), (372, 345), (345, 352), (352, 376), (376, 433),
    (433, 416), (416, 434), (434, 432), (432, 436), (436, 426),
    (426, 266), (266, 329), (329, 349), (349, 451)
]

FACE_MESH_RIGHT_CHEEK = [
    (231, 230), (230, 229), (229, 228), (228, 31), (31, 35),
    (35, 143), (143, 116), (116, 123), (123, 147), (147, 213),
    (213, 192), (192, 214), (214, 212), (212, 216), (216, 206),
    (206, 36), (36, 100), (100, 120), (120, 231)
]

FACE_MESH_CHIN = [
    (43, 106), (106, 182), (182, 83), (83, 18), (18, 313),
    (313, 406), (406, 335), (335, 273), (273, 422), (422, 430),
    (430, 394), (394, 395), (395, 369), (369, 396), (396, 175),
    (175, 171), (171, 140), (140, 170), (170, 169), (169, 210),
    (210, 202), (202, 43)
]


class FaceMesher(Executor):
    @requests(on=['/s3_index', '/index', '/lip_search', '/skin_search'])
    def face_mesh_mask(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            if len(doc.chunks) >= 1:
                raise RuntimeError('chunks indices are off, please check pipeline')
            img_rgb = doc.tensor
            face_mesh = self._get_face_mesh(img_rgb)
            mask = self._get_skin_mask(img_rgb.shape, face_mesh)
            mask_doc = Document(tensor=mask, modality='mask')
            doc.chunks.append(mask_doc)
        return docs

    def _get_face_mesh(self, img_rgb: np.ndarray):
        # Run MediaPipe Face Mesh.
        with mp_face_mesh.FaceMesh(
                static_image_mode=True,
                refine_landmarks=True,
                max_num_faces=2,
                min_detection_confidence=0.7) as face_mesh:
            results = face_mesh.process(img_rgb)
            return results.multi_face_landmarks

    def _get_skin_mask(self, image_shape, landmark_list):
        if landmark_list is None:
            return None
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        for face_landmarks in landmark_list:
            landmarks = face_landmarks.landmark
            # fill chin
            chin_polygon = []
            for chin_point in FACE_MESH_CHIN:
                chin_point_px = mp_drawing._normalized_to_pixel_coordinates(
                    landmarks[chin_point[1]].x,
                    landmarks[chin_point[1]].y,
                    image_shape[1],
                    image_shape[0]
                )
                chin_polygon.append(chin_point_px)
            cv2.fillPoly(
                mask, pts=[np.array(chin_polygon, dtype=np.int32)], color=255)
            # fill left cheek
            left_cheek_polygon = []
            for left_cheek_point in FACE_MESH_LEFT_CHEEK:
                left_cheek_point_px = mp_drawing._normalized_to_pixel_coordinates(
                    landmarks[left_cheek_point[1]].x,
                    landmarks[left_cheek_point[1]].y,
                    image_shape[1],
                    image_shape[0]
                )
                left_cheek_polygon.append(left_cheek_point_px)
            cv2.fillPoly(
                mask, pts=[np.array(left_cheek_polygon, dtype=np.int32)], color=255)
            # fill right cheek
            right_cheek_polygon = []
            for right_cheek_point in FACE_MESH_RIGHT_CHEEK:
                right_cheek_point_px = mp_drawing._normalized_to_pixel_coordinates(
                    landmarks[right_cheek_point[1]].x,
                    landmarks[right_cheek_point[1]].y,
                    image_shape[1],
                    image_shape[0]
                )
                right_cheek_polygon.append(right_cheek_point_px)
            cv2.fillPoly(
                mask, pts=[np.array(right_cheek_polygon, dtype=np.int32)], color=255)
            # fill outer lip
            outer_lip_polygon = []
            for outer_lip_point in FACE_MESH_OUTER_LIP:
                outer_lip_point_px = mp_drawing._normalized_to_pixel_coordinates(
                    landmarks[outer_lip_point[1]].x,
                    landmarks[outer_lip_point[1]].y,
                    image_shape[1],
                    image_shape[0]
                )
                outer_lip_polygon.append(outer_lip_point_px)
            cv2.fillPoly(
                mask, pts=[np.array(outer_lip_polygon, dtype=np.int32)], color=128)
            # fill inner lip
            inner_lip_polygon = []
            for inner_lip_point in FACE_MESH_INNER_LIP:
                inner_lip_point_px = mp_drawing._normalized_to_pixel_coordinates(
                    landmarks[inner_lip_point[1]].x,
                    landmarks[inner_lip_point[1]].y,
                    image_shape[1],
                    image_shape[0]
                )
                inner_lip_polygon.append(inner_lip_point_px)
            cv2.fillPoly(
                mask, pts=[np.array(inner_lip_polygon, dtype=np.int32)], color=0)
        return mask
