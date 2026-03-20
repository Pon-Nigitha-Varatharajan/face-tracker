from insightface.app import FaceAnalysis
import numpy as np

class FaceRecognizer:
    def __init__(self):
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0)  # CPU

        self.known_faces = {}   # face_id -> embedding
        self.face_count = 0

    def get_embedding(self, face):
        return face.embedding

    def recognize(self, embedding):
        for face_id, known_emb in self.known_faces.items():
            similarity = self.cosine_similarity(embedding, known_emb)

            if similarity > 0.6:
                return face_id

        # New face
        self.face_count += 1
        new_id = f"F{self.face_count}"
        self.known_faces[new_id] = embedding

        return new_id

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))