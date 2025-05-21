import json
from sentence_transformers import SentenceTransformer, util

# 1. Load model once
MODEL_NAME = "sentence-transformers/all-roberta-large-v1"
model = SentenceTransformer(MODEL_NAME)

# 2. Load expected answers
with open("expected_answers.json") as f:
    EXPECTED = json.load(f)

def get_highest_score(prompt_id: str, user_answer: str) -> float:
    # Embed user answer
    user_emb = model.encode(user_answer, convert_to_tensor=True)
    
    best_score = 0.0
    for ans in EXPECTED.get(prompt_id, []):
        ans_emb = model.encode(ans, convert_to_tensor=True)
        # cosine similarity in [–1,1], we want [0,1]
        score = util.pytorch_cos_sim(user_emb, ans_emb).item()
        best_score = max(best_score, score)
    return best_score
