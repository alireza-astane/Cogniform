class User:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.demographics = {}
        self.crt_responses = []
        self.delay_discounting_response = {}

    def add_demographics(self, age, education, familiarity):
        self.demographics = {
            "age": age,
            "education": education,
            "familiarity": familiarity,
        }

    def add_crt_response(self, question, user_answer, is_correct, response_time):
        self.crt_responses.append(
            {
                "question": question,
                "user_answer": user_answer,
                "is_correct": is_correct,
                "response_time": response_time,
            }
        )

    def add_delay_discounting_response(self, choice, response_time):
        self.delay_discounting_response = {
            "user_answer": choice,
            "response_time": response_time,
        }

    def get_results(self):
        return {
            "demographics": self.demographics,
            "crt": self.crt_responses,
            "delay_discounting": [self.delay_discounting_response],
        }
