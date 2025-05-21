import json
from sentence_transformers import SentenceTransformer, util

# 1. Load model once
MODEL_NAME = "sentence-transformers/all-roberta-large-v1"
model = SentenceTransformer(MODEL_NAME)

# ──────────────────────────────────────────────────────────────────────
# Warm up the model on import so first real request is fast
# (this runs one dummy encode at startup)
_ = model.encode("warm up", convert_to_tensor=True)
# ──────────────────────────────────────────────────────────────────────

# 2. Load and pre-encode all expected-answer embeddings:
with open("expected_answers.json") as f:
    _raw = json.load(f)

_expected_embeddings = {}
for prompt_id, answers in _raw.items():
    # Batch-encode list of strings into a tensor
    embs = model.encode(answers, convert_to_tensor=True)
    _expected_embeddings[prompt_id] = embs

def get_highest_score(prompt_id: str, user_answer: str) -> float:
    user_emb = model.encode(user_answer, convert_to_tensor=True)
    # Compare user_emb against the precomputed embeddings tensor:
    scores = util.cos_sim(user_emb, _expected_embeddings.get(prompt_id, []))
    return float(scores.max())
