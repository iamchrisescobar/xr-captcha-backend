import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_missing_prompt_id(client):
    resp = client.post('/api/get_score', json={'user_answer':'foo'})
    assert resp.status_code == 400
    assert b'prompt_id is required' in resp.data

def test_valid_score_response(client):
    payload = {'prompt_id':'question_1',
               'user_answer':'That is a happy person'}
    resp = client.post('/api/get_score', json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['prompt_id'] == 'question_1'
    assert isinstance(data['score'], float)
    assert 0.0 <= data['score'] <= 1.0
