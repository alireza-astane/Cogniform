import pytest
from app.tasks.crt import CognitiveReflectionTest
from app.tasks.stroop import StroopTask
from app.tasks.delay_discounting import DelayDiscountingTask

def test_crt_task():
    crt = CognitiveReflectionTest()
    questions = crt.get_questions()
    assert len(questions) == 3  # Assuming CRT has 3 questions

    response = crt.record_response(0, "Your answer")
    assert response['question_index'] == 0
    assert response['answer'] == "Your answer"

def test_stroop_task():
    stroop = StroopTask()
    color_word = stroop.get_color_word()
    assert color_word in stroop.color_words  # Assuming color_words is a list of valid words

    response = stroop.record_response(color_word, "Red")
    assert response['selected_color'] == "Red"

def test_delay_discounting_task():
    delay_discounting = DelayDiscountingTask()
    choices = delay_discounting.get_choices()
    assert len(choices) == 2  # Assuming two choices are presented

    response = delay_discounting.record_choice(choices[0])
    assert response['selected_choice'] == choices[0]