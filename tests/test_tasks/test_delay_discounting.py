import pytest
from datetime import datetime
from cogniform.tasks.delay_discounting import DelayDiscountingTask


@pytest.fixture
def delay_discounting_task():
    return DelayDiscountingTask()


def test_generate_trials(delay_discounting_task):
    trials = delay_discounting_task.generate_trials()
    assert len(trials) == 10  # Ensure 10 trials are generated
    for trial in trials:
        assert 1 <= trial["smaller_reward"] <= 10
        assert 11 <= trial["larger_reward"] <= 20
        assert 1 <= trial["delay"] <= 30


def test_present_trial(delay_discounting_task):
    trial = {"smaller_reward": 5, "larger_reward": 15, "delay": 10}
    presentation = delay_discounting_task.present_trial(trial)
    assert "Choose between:" in presentation
    assert "$5 now" in presentation
    assert "$15 in 10 days" in presentation


def test_collect_response(delay_discounting_task):
    trial = {"smaller_reward": 5, "larger_reward": 15, "delay": 10}
    choice = 1
    response_time = 2.5
    delay_discounting_task.collect_response(trial, choice, response_time)
    assert len(delay_discounting_task.responses) == 1
    response = delay_discounting_task.responses[0]
    assert response["trial"] == trial
    assert response["choice"] == choice
    assert response["response_time"] == response_time
    assert isinstance(response["timestamp"], datetime)


def test_analyze_responses(delay_discounting_task):
    trial = {"smaller_reward": 5, "larger_reward": 15, "delay": 10}
    delay_discounting_task.collect_response(trial, 1, 2.5)
    delay_discounting_task.collect_response(trial, 2, 3.0)
    analysis = delay_discounting_task.analyze_responses()
    assert analysis["total_trials"] == 2
    assert len(analysis["responses"]) == 2
    assert analysis["responses"][0]["choice"] == 1
    assert analysis["responses"][1]["choice"] == 2
