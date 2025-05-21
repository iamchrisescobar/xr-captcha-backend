from flask import Flask, request, jsonify
from model_utils import get_highest_score

app = Flask(__name__)

@app.route("/api/get_score", methods=["POST"])
def score():
    data = request.get_json()
    prompt_id = data.get("prompt_id")
    user_answer = data.get("user_answer", "")
    if not prompt_id:
        return jsonify({"error": "prompt_id is required"}), 400

    score = get_highest_score(prompt_id, user_answer)
    return jsonify({"prompt_id": prompt_id, "score": score})

if __name__ == "__main__":
    # Listen on all interfaces so Docker can map ports
    app.run(host="0.0.0.0", port=5000)
