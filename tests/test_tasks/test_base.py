import pytest
from app.tasks.base import CognitiveTask


class TestCognitiveTask:
    def test_initialization(self):
        task = CognitiveTask(task_id="1", task_name="Sample Task")
        assert task.task_id == "1"
        assert task.task_name == "Sample Task"
        assert task.responses == []

    def test_collect_response(self):
        task = CognitiveTask(task_id="1", task_name="Sample Task")
        task.collect_response("Response 1")
        assert task.responses == ["Response 1"]

    def test_get_results(self):
        task = CognitiveTask(task_id="1", task_name="Sample Task")
        task.collect_response("Response 1")
        task.collect_response("Response 2")
        assert task.get_results() == ["Response 1", "Response 2"]

    def test_present_task_not_implemented(self):
        task = CognitiveTask(task_id="1", task_name="Sample Task")
        with pytest.raises(NotImplementedError):
            task.present_task()
