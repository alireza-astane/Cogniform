class CognitiveReflectionTest:
    def __init__(self):
        self.questions = [
            {
                "question": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?",
                "answer": 0.10
            },
            {
                "question": "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
                "answer": 5
            },
            {
                "question": "In a lake, there is a patch of water lilies. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long will it take for the patch to cover half of the lake?",
                "answer": 47
            }
        ]
        self.responses = []

    def get_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None

    def submit_response(self, index, user_answer):
        if 0 <= index < len(self.questions):
            correct_answer = self.questions[index]["answer"]
            is_correct = user_answer == correct_answer
            self.responses.append({
                "question": self.questions[index]["question"],
                "user_answer": user_answer,
                "is_correct": is_correct
            })
            return is_correct
        return None

    def get_results(self):
        return self.responses