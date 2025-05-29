import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_missing_prompt_id(client):
    resp = client.post('/api/get_score', json={'user_answer': 'foo'})
    assert resp.status_code == 400

    data = resp.get_json()
    # Now checking the new error message
    assert data.get('error') == 'prompt_id is missing or unknown'

def test_valid_score_response(client):
    payload = {'prompt_id':'question_1',
               'user_answer':'That is a happy person'}
    resp = client.post('/api/get_score', json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['prompt_id'] == 'question_1'
    assert isinstance(data['score'], float)
    assert 0.0 <= data['score'] <= 1.0

def test_batch_scoring_multiple_questions(client):
    # Prepare a payload with two valid prompt/answer pairs
    payload = {
        "items": [
            {"prompt_id": "question_1", "user_answer": "That is a happy person"},
            {"prompt_id": "question_1", "user_answer": "That is a sad person"}
        ]
    }

    resp = client.post('/api/get_score', json=payload)
    assert resp.status_code == 200

    data = resp.get_json()
    # Should return a list called "results" with exactly two entries
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) == 2

    # Each result must have a prompt_id and a float score between 0 and 1
    for idx, result in enumerate(data["results"], start=1):
        assert "prompt_id" in result, f"missing prompt_id in result {idx}"
        assert "score" in result, f"missing score in result {idx}"
        assert isinstance(result["score"], float)
        assert 0.0 <= result["score"] <= 1.0