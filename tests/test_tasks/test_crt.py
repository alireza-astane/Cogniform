import pytest
from cogniform.tasks.crt import CognitiveReflectionTest


@pytest.fixture
def crt_instance():
    return CognitiveReflectionTest()


def test_get_question_valid_index(crt_instance):
    question = crt_instance.get_question(0)
    assert question is not None
    assert (
        question["question"]
        == "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?"
    )
    assert question["answer"] == 0.10


def test_get_question_invalid_index(crt_instance):
    question = crt_instance.get_question(-1)
    assert question is None
    question = crt_instance.get_question(100)
    assert question is None


def test_submit_response_correct_answer(crt_instance):
    is_correct = crt_instance.submit_response(0, 0.10)
    assert is_correct is True
    results = crt_instance.get_results()
    assert len(results) == 1
    assert results[0]["is_correct"] is True


def test_submit_response_incorrect_answer(crt_instance):
    is_correct = crt_instance.submit_response(0, 0.20)
    assert is_correct is False
    results = crt_instance.get_results()
    assert len(results) == 1
    assert results[0]["is_correct"] is False


def test_submit_response_invalid_index(crt_instance):
    is_correct = crt_instance.submit_response(-1, 0.10)
    assert is_correct is None
    is_correct = crt_instance.submit_response(100, 0.10)
    assert is_correct is None
    results = crt_instance.get_results()
    assert len(results) == 0


def test_get_results_empty(crt_instance):
    results = crt_instance.get_results()
    assert results == []


def test_get_results_after_responses(crt_instance):
    crt_instance.submit_response(0, 0.10)
    crt_instance.submit_response(1, 10)  # Incorrect answer
    results = crt_instance.get_results()
    assert len(results) == 2
    assert results[0]["is_correct"] is True
    assert results[1]["is_correct"] is False
