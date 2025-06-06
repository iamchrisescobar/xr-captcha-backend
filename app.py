from flask import Flask, request, jsonify
from model_utils import get_highest_score, _expected_embeddings
import os 

app = Flask(__name__)

@app.route("/api/get_score", methods=["POST"])
def score():
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="Invalid JSON payload"), 400

    # ——— Batch mode ———
    if "items" in data:
        items = data["items"]
        # Must be a list of 1–15 entries
        if not isinstance(items, list):
            return jsonify(error="`items` must be a list"), 400
        if not (1 <= len(items) <= 15):
            return jsonify(error="`items` length must be between 1 and 15"), 400

        results = []
        for idx, item in enumerate(items, start=1):
            pid = item.get("prompt_id")
            ans = item.get("user_answer")

            # Per-item validation
            if not isinstance(pid, str) or pid not in _expected_embeddings:
                return jsonify(error=f"item {idx}: prompt_id is missing or unknown"), 400
            if not isinstance(ans, str) or not ans.strip():
                return jsonify(error=f"item {idx}: user_answer must be a non-empty string"), 400

            try:
                sc = get_highest_score(pid, ans)
            except Exception:
                return jsonify(error="Internal error during scoring"), 500

            results.append({"prompt_id": pid, "score": sc})

        return jsonify(results=results)

    # ——— Single-question fallback ———
    prompt_id = data.get("prompt_id")
    user_answer = data.get("user_answer", "")

    if not isinstance(prompt_id, str) or prompt_id not in _expected_embeddings:
        return jsonify(error="prompt_id is missing or unknown"), 400
    if not isinstance(user_answer, str) or not user_answer.strip():
        return jsonify(error="user_answer must be a non-empty string"), 400

    try:
        score = get_highest_score(prompt_id, user_answer)
    except Exception:
        return jsonify(error="Internal error during scoring"), 500

    return jsonify(prompt_id=prompt_id, score=score)

if __name__ == "__main__":
    # Listen on all interfaces so Docker can map ports
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port)
