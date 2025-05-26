import pytest
from app.models.tasks import CRTTask, StroopTask, DelayDiscountingTask, ConsistencyCheck


def test_crt_task_initialization():
    crt_task = CRTTask(
        question="What is 2 + 2?", answer="4", response_time=1.5, edits=1
    )
    assert crt_task.question == "What is 2 + 2?"
    assert crt_task.answer == "4"
    assert crt_task.response_time == 1.5
    assert crt_task.edits == 1


def test_crt_task_optional_fields():
    crt_task = CRTTask(question="What is 2 + 2?")
    assert crt_task.answer is None
    assert crt_task.response_time is None
    assert crt_task.edits == 0


def test_stroop_task_initialization():
    stroop_task = StroopTask(
        color_word="RED",
        font_color="BLUE",
        selected_color="BLUE",
        response_time=2.0,
        correct=True,
    )
    assert stroop_task.color_word == "RED"
    assert stroop_task.font_color == "BLUE"
    assert stroop_task.selected_color == "BLUE"
    assert stroop_task.response_time == 2.0
    assert stroop_task.correct is True


def test_stroop_task_optional_fields():
    stroop_task = StroopTask(color_word="RED", font_color="BLUE")
    assert stroop_task.selected_color is None
    assert stroop_task.response_time is None
    assert stroop_task.correct is None


def test_delay_discounting_task_initialization():
    delay_task = DelayDiscountingTask(
        smaller_reward=10.0, larger_reward=20.0, choice="larger", response_time=3.5
    )
    assert delay_task.smaller_reward == 10.0
    assert delay_task.larger_reward == 20.0
    assert delay_task.choice == "larger"
    assert delay_task.response_time == 3.5


def test_delay_discounting_task_optional_fields():
    delay_task = DelayDiscountingTask(smaller_reward=10.0, larger_reward=20.0)
    assert delay_task.choice is None
    assert delay_task.response_time is None


def test_consistency_check_initialization():
    consistency_check = ConsistencyCheck(
        original_question="What is 2 + 2?",
        modified_question="What is 3 + 3?",
        original_answer="4",
        modified_answer="6",
        response_time=2.0,
        consistent=True,
    )
    assert consistency_check.original_question == "What is 2 + 2?"
    assert consistency_check.modified_question == "What is 3 + 3?"
    assert consistency_check.original_answer == "4"
    assert consistency_check.modified_answer == "6"
    assert consistency_check.response_time == 2.0
    assert consistency_check.consistent is True


def test_consistency_check_optional_fields():
    consistency_check = ConsistencyCheck(
        original_question="What is 2 + 2?", modified_question="What is 3 + 3?"
    )
    assert consistency_check.original_answer is None
    assert consistency_check.modified_answer is None
    assert consistency_check.response_time is None
    assert consistency_check.consistent is None
