from insightface.app import FaceAnalysis
import numpy as np

class FaceRecognizer:
    def __init__(self, threshold=0.6):
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=-1)  # CPU mode

        self.known_faces = {}   # face_id -> embedding
        self.face_count = 0
        self.threshold = threshold

    # ---------------- NORMALIZE ----------------
    def normalize(self, emb):
        norm = np.linalg.norm(emb)

        # ❗ Prevent division by zero
        if norm == 0:
            return emb

        return emb / norm

    # ---------------- SIMILARITY ----------------
    def cosine_similarity(self, a, b):
        return np.dot(a, b)

    # ---------------- MAIN RECOGNITION ----------------
    def recognize(self, frame_crop):

        # ❗ 1. Safety check for empty crop
        if frame_crop is None or frame_crop.size == 0:
            return None

        h, w = frame_crop.shape[:2]

        # ❗ 2. Skip very small images
        if h < 20 or w < 20:
            return None

        # ❗ 3. Safe InsightFace call
        try:
            faces = self.app.get(frame_crop)
        except:
            return None

        # ❗ 4. No face detected
        if len(faces) == 0:
            return None

        # ---------------- GET BEST FACE ----------------
        face = faces[0]

        emb = self.normalize(face.embedding)

        # ❗ Extra safety
        if emb is None or emb.shape[0] == 0:
            return None

        # ---------------- MATCHING ----------------
        best_match = None
        best_score = 0

        for fid, known_emb in self.known_faces.items():
            score = self.cosine_similarity(emb, known_emb)

            if score > best_score:
                best_score = score
                best_match = fid

        # ---------------- EXISTING FACE ----------------
        if best_score > self.threshold:
            return best_match

        # ---------------- NEW FACE ----------------
        self.face_count += 1
        new_id = f"F{self.face_count}"

        self.known_faces[new_id] = emb

        return new_id