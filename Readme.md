# XR-CAPTCHA Backend Documentation

This repository provides a lightweight Flask-based API for scoring user responses in a VR CAPTCHA system using a pretrained RoBERTa model via the [sentence-transformers](https://github.com/UKPLab/sentence-transformers) library. It can be run locally or containerized with Docker.

---

## Project Structure

```
xr-captcha-backend/
├── app.py                  # Flask application entrypoint
├── model_utils.py          # Model loading, warm-up, and scoring logic
├── expected_answers.json   # Predefined human answers per prompt
├── requirements.txt        # Python dependencies
├── Dockerfile              # Containerization instructions
├── pytest.ini              # Pytest config (adds project root to path)
├── tests/                  # Unit tests (pytest)
│   ├── test_api.py
│   └── test_model_utils.py
└── README.md               # This documentation file
```

---

## Prerequisites

* Python 3.8+ (3.9 recommended)
* [pip](https://pip.pypa.io/) or [conda](https://docs.conda.io/)
* (Optional) Docker & Docker Desktop

---

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/iamchrisescobar/xr-captcha-backend.git xr-captcha-backend
   cd xr-captcha-backend
   ```

2. **Create a virtual environment**

   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows PowerShell

   # Or using conda
   conda create -n captcha-backend python=3.9
   conda activate captcha-backend
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify imports**

   ```bash
   python - <<EOF
   ```

import flask, torch, sentence\_transformers print("Dependencies loaded successfully!") EOF

---

## Running the API Locally

Start the Flask server on port 5000:

```bash
python app.py
````

By default it listens on `http://0.0.0.0:5000`. You can change the port via the `PORT` environment variable:

```bash
export PORT=8080       # macOS/Linux
set PORT=8080          # Windows
python app.py
```

### Example Request

```bash
curl -X POST "http://localhost:5000/api/get_score" -H "Content-Type: application/json" -d '{"prompt_id":"question_1","user_answer":"That is a happy person aint it"}' 
```

**Response**

```json
{
  "prompt_id": "question_1",
  "score": 0.92
}
```

---

## Docker Usage

1. **Build the container**

   ```bash
   docker build -t xr-captcha-backend .
   ```

2. **Run the container with defaults (HOST=0.0.0.0, PORT=5000 baked in via Dockerfile ENV):**

   ```bash
   docker run --rm -p 5000:5000 xr-captcha-backend
   ```

3. **Override HOST/PORT at runtime using -e flags and matching port mapping:**
```bash
    # Example: expose container port 9000 on host port 9000
    docker run --rm \
    -e HOST=0.0.0.0 \
    -e PORT=9000 \
    -p 9000:9000 \
    xr-captcha-backend
   ```
---

## Model Warm-up & Performance

* On import, the model is "warmed up" with a dummy encode to minimize latency on the first real request.
* All expected answers are pre-encoded to speed up each scoring call.
* For a smaller footprint, you can switch in `model_utils.py` to a lighter model such as `sentence-transformers/all-MiniLM-L6-v2`.

---

## Input Validation & Error Handling

* **400 Bad Request** if:

  * JSON payload is invalid
  * `prompt_id` is missing or unknown
  * `user_answer` is empty or not a string
* **500 Internal Server Error** if an exception occurs during scoring

Example error response:

```json
{ "error": "prompt_id is missing or unknown" }
```

---

## Testing

Run unit tests with pytest (no Docker required):

```bash
pytest -q
```

Tests cover:

* API endpoint validation and responses
* Scoring logic accuracy for known answers

---

## Environment Variables

* `PORT` — Port for Flask server (default `5000`)
* `HF_HUB_DISABLE_SYMLINKS_WARNING=1` — Disable symlink warnings on Windows

