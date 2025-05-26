class CognitiveTask:
    def __init__(self, task_id: str, task_name: str):
        self.task_id = task_id
        self.task_name = task_name
        self.responses = []

    def present_task(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def collect_response(self, response):
        self.responses.append(response)

    def get_results(self):
        return self.responses
