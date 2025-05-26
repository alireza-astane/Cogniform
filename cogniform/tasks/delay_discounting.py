from datetime import datetime
from typing import List, Dict, Any
import random

class DelayDiscountingTask:
    def __init__(self):
        self.trials = self.generate_trials()
        self.responses = []

    def generate_trials(self) -> List[Dict[str, Any]]:
        trials = []
        for _ in range(10):  # Generate 10 trials
            smaller_reward = random.randint(1, 10)  # Smaller-sooner reward
            larger_reward = random.randint(11, 20)  # Larger-later reward
            delay = random.randint(1, 30)  # Delay in days
            trials.append({
                "smaller_reward": smaller_reward,
                "larger_reward": larger_reward,
                "delay": delay
            })
        return trials

    def present_trial(self, trial: Dict[str, Any]) -> str:
        return (f"Choose between:\n"
                f"1. ${trial['smaller_reward']} now\n"
                f"2. ${trial['larger_reward']} in {trial['delay']} days")

    def collect_response(self, trial: Dict[str, Any], choice: int, response_time: float):
        self.responses.append({
            "trial": trial,
            "choice": choice,
            "response_time": response_time,
            "timestamp": datetime.now()
        })

    def analyze_responses(self) -> Dict[str, Any]:
        # Placeholder for analysis logic
        return {
            "total_trials": len(self.responses),
            "responses": self.responses
        }