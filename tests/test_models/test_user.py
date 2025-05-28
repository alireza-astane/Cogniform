import pytest
from cogniform.models.user import User


@pytest.fixture
def user():
    return User(session_id="test_session")


def test_add_demographics(user):
    user.add_demographics(age=25, education="bachelors", familiarity="intermediate")
    assert user.demographics == {
        "age": 25,
        "education": "bachelors",
        "familiarity": "intermediate",
    }


def test_add_crt_response(user):
    user.add_crt_response(
        question="What is 2 + 2?",
        user_answer=4,
        is_correct=True,
        response_time=1.5,
    )
    assert len(user.crt_responses) == 1
    assert user.crt_responses[0] == {
        "question": "What is 2 + 2?",
        "user_answer": 4,
        "is_correct": True,
        "response_time": 1.5,
    }


def test_add_delay_discounting_response(user):
    user.add_delay_discounting_response(choice="smaller", response_time=2.3)
    assert user.delay_discounting_response == {
        "user_answer": "smaller",
        "response_time": 2.3,
    }


def test_get_results(user):
    user.add_demographics(age=30, education="masters", familiarity="advanced")
    user.add_crt_response(
        question="What is 5 + 5?",
        user_answer=10,
        is_correct=True,
        response_time=1.2,
    )
    user.add_delay_discounting_response(choice="larger", response_time=3.4)
    results = user.get_results()
    assert results["demographics"] == {
        "age": 30,
        "education": "masters",
        "familiarity": "advanced",
    }
    assert len(results["crt"]) == 1
    assert results["crt"][0] == {
        "question": "What is 5 + 5?",
        "user_answer": 10,
        "is_correct": True,
        "response_time": 1.2,
    }
    assert len(results["delay_discounting"]) == 1
    assert results["delay_discounting"][0] == {
        "user_answer": "larger",
        "response_time": 3.4,
    }
