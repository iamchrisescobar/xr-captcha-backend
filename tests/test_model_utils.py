from model_utils import get_highest_score

def test_exact_match_high_score():
    # one of the expected answers for question_1 is "It's sunny today."
    score = get_highest_score('question_1', "That is a happy person")
    assert score > 0.9

def test_unrelated_low_score():
    score = get_highest_score('question_1', "I enjoy quantum physics.")
    assert score < 0.5
