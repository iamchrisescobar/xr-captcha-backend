from flask import Flask, request, jsonify
from model_utils import get_highest_score, _expected_embeddings
import os 

app = Flask(__name__)

@app.route("/api/get_score", methods=["POST"])
def score():
    data = request.get_json()
    # Strict input validation
    if not data:
        return jsonify(error="Invalid JSON payload"), 400
    
    prompt_id = data.get("prompt_id")
    user_answer = data.get("user_answer", "")

    if not isinstance(prompt_id, str) or prompt_id not in _expected_embeddings:
        return jsonify(error="prompt_id is missing or unknown"), 400

    if not isinstance(user_answer, str) or not user_answer.strip():
        return jsonify(error="user_answer must be a non-empty string"), 400
    
    # Graceful failure fallback
    try:
        score = get_highest_score(prompt_id, user_answer)
    except Exception as e:
        # log.exception(e)  # optionally log full traceback
        return jsonify(error="Internal error during scoring"), 500

    return jsonify(prompt_id=prompt_id, score=score)

if __name__ == "__main__":
    # Listen on all interfaces so Docker can map ports
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port)
