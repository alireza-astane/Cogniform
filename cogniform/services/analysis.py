from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_responses(data: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze user responses and return a summary DataFrame.

    Parameters:
    - data: A DataFrame containing user responses.

    Returns:
    - A DataFrame summarizing the analysis.
    """
    summary = data.describe()
    return summary


def visualize_results(data: pd.DataFrame, task_name: str) -> None:
    """
    Visualize the results of a cognitive task.

    Parameters:
    - data: A DataFrame containing user responses for the task.
    - task_name: The name of the cognitive task being visualized.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data["response_time"], bins=30, kde=True)
    plt.title(f"Response Time Distribution for {task_name}")
    plt.xlabel("Response Time (seconds)")
    plt.ylabel("Frequency")
    plt.grid()
    plt.show()


def plot_accuracy(data: pd.DataFrame, task_name: str) -> None:
    """
    Plot accuracy of responses for a cognitive task.

    Parameters:
    - data: A DataFrame containing user responses for the task.
    - task_name: The name of the cognitive task being visualized.
    """
    accuracy = data["accuracy"].value_counts(normalize=True) * 100
    plt.figure(figsize=(8, 5))
    sns.barplot(x=accuracy.index, y=accuracy.values)
    plt.title(f"Accuracy Distribution for {task_name}")
    plt.xlabel("Accuracy")
    plt.ylabel("Percentage")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()


from typing import Dict, List
from sqlalchemy.orm import Session
from cogniform.services.database import fetch_all_responses
import statistics


# def analyze_data(db: Session) -> Dict[str, Dict]:
#     responses = fetch_all_responses(db)
#     analysis_results = {
#         "demographics": {
#             "average_age": None,
#             "education_distribution": {},
#             "familiarity_distribution": {},
#         },
#         "crt": {
#             "average_response_time": None,
#             "accuracy": None,
#         },
#         "delay_discounting": {
#             "average_response_time": None,
#             "choice_distribution": {},
#         },
#     }

#     # Analyze demographics
#     ages = [response.age for response in responses if response.age is not None]
#     if ages:
#         analysis_results["demographics"]["average_age"] = statistics.mean(ages)

#     education_levels = [
#         response.education for response in responses if response.education
#     ]
#     for level in education_levels:
#         analysis_results["demographics"]["education_distribution"][level] = (
#             analysis_results["demographics"]["education_distribution"].get(level, 0) + 1
#         )

#     familiarity_levels = [
#         response.familiarity for response in responses if response.familiarity
#     ]
#     for level in familiarity_levels:
#         analysis_results["demographics"]["familiarity_distribution"][level] = (
#             analysis_results["demographics"]["familiarity_distribution"].get(level, 0)
#             + 1
#         )

#     # Analyze CRT
#     crt_response_times = []
#     crt_correct_answers = 0
#     crt_total_questions = 0
#     for response in responses:
#         for i in range(1, 4):  # Assuming 3 CRT questions
#             crt_total_questions += 1
#             crt_response_time = getattr(response, f"crt_q{i}_response_time", None)
#             crt_correct = getattr(response, f"crt_q{i}_correct", None)
#             if crt_response_time is not None:
#                 crt_response_times.append(crt_response_time)
#             if crt_correct:
#                 crt_correct_answers += 1

#     if crt_response_times:
#         analysis_results["crt"]["average_response_time"] = statistics.mean(
#             crt_response_times
#         )
#     if crt_total_questions > 0:
#         analysis_results["crt"]["accuracy"] = crt_correct_answers / crt_total_questions

#     # Analyze Delay Discounting
#     delay_response_times = [
#         response.delay_response_time
#         for response in responses
#         if response.delay_response_time
#     ]
#     delay_choices = [
#         response.delay_choice for response in responses if response.delay_choice
#     ]
#     if delay_response_times:
#         analysis_results["delay_discounting"]["average_response_time"] = (
#             statistics.mean(delay_response_times)
#         )
#     for choice in delay_choices:
#         analysis_results["delay_discounting"]["choice_distribution"][choice] = (
#             analysis_results["delay_discounting"]["choice_distribution"].get(choice, 0)
#             + 1
#         )

#     return analysis_results


import matplotlib.pyplot as plt
import os

PLOTS_DIR = "templates/static/plots"


def analyze_data(db: Session) -> Dict[str, Dict]:
    responses = fetch_all_responses(db)
    analysis_results = {
        "demographics": {
            "average_age": None,
            "education_distribution": {},
            "familiarity_distribution": {},
        },
        "crt": {
            "average_response_time": None,
            "accuracy": None,
        },
        "delay_discounting": {
            "average_response_time": None,
            "choice_distribution": {},
        },
    }

    # Ensure the plots directory exists
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # Analyze demographics
    ages = [response.age for response in responses if isinstance(response.age, int)]
    if ages:
        analysis_results["demographics"]["average_age"] = statistics.mean(ages)
        # Plot age distribution
        plt.figure()
        plt.hist(ages, bins=10, color="blue", alpha=0.7)
        plt.title("Age Distribution")
        plt.xlabel("Age")
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(PLOTS_DIR, "age_distribution.png"))
        plt.close()

    education_levels = [
        response.education for response in responses if response.education
    ]
    for level in education_levels:
        analysis_results["demographics"]["education_distribution"][level] = (
            analysis_results["demographics"]["education_distribution"].get(level, 0) + 1
        )
    # Plot education distribution
    if education_levels:
        plt.figure()
        plt.bar(
            analysis_results["demographics"]["education_distribution"].keys(),
            analysis_results["demographics"]["education_distribution"].values(),
            color="green",
            alpha=0.7,
        )
        plt.title("Education Distribution")
        plt.xlabel("Education Level")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(PLOTS_DIR, "education_distribution.png"))
        plt.close()

    familiarity_levels = [
        response.familiarity for response in responses if response.familiarity
    ]
    for level in familiarity_levels:
        analysis_results["demographics"]["familiarity_distribution"][level] = (
            analysis_results["demographics"]["familiarity_distribution"].get(level, 0)
            + 1
        )
    # Plot familiarity distribution
    if familiarity_levels:
        plt.figure()
        plt.bar(
            analysis_results["demographics"]["familiarity_distribution"].keys(),
            analysis_results["demographics"]["familiarity_distribution"].values(),
            color="orange",
            alpha=0.7,
        )
        plt.title("Familiarity Distribution")
        plt.xlabel("Familiarity Level")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(PLOTS_DIR, "familiarity_distribution.png"))
        plt.close()

    # Analyze CRT
    crt_response_times = []
    crt_correct_answers = 0
    crt_total_questions = 0
    for response in responses:
        for i in range(1, 4):  # Assuming 3 CRT questions
            crt_total_questions += 1
            crt_response_time = getattr(response, f"crt_q{i}_response_time", None)
            crt_correct = getattr(response, f"crt_q{i}_correct", None)
            if crt_response_time is not None:
                crt_response_times.append(crt_response_time)
            if crt_correct:
                crt_correct_answers += 1

    if crt_response_times:
        analysis_results["crt"]["average_response_time"] = statistics.mean(
            crt_response_times
        )
        # Plot CRT response times
        plt.figure()
        plt.hist(crt_response_times, bins=10, color="purple", alpha=0.7)
        plt.title("CRT Response Times")
        plt.xlabel("Response Time (s)")
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(PLOTS_DIR, "crt_response_times.png"))
        plt.close()

    if crt_total_questions > 0:
        analysis_results["crt"]["accuracy"] = crt_correct_answers / crt_total_questions

    # Analyze Delay Discounting
    delay_response_times = [
        response.delay_response_time
        for response in responses
        if response.delay_response_time
    ]
    delay_choices = [
        response.delay_choice for response in responses if response.delay_choice
    ]
    if delay_response_times:
        analysis_results["delay_discounting"]["average_response_time"] = (
            statistics.mean(delay_response_times)
        )
        # Plot delay discounting response times
        plt.figure()
        plt.hist(delay_response_times, bins=10, color="red", alpha=0.7)
        plt.title("Delay Discounting Response Times")
        plt.xlabel("Response Time (s)")
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(PLOTS_DIR, "delay_response_times.png"))
        plt.close()

    for choice in delay_choices:
        analysis_results["delay_discounting"]["choice_distribution"][choice] = (
            analysis_results["delay_discounting"]["choice_distribution"].get(choice, 0)
            + 1
        )
    # Plot delay discounting choices
    if delay_choices:
        plt.figure()
        plt.bar(
            analysis_results["delay_discounting"]["choice_distribution"].keys(),
            analysis_results["delay_discounting"]["choice_distribution"].values(),
            color="cyan",
            alpha=0.7,
        )
        plt.title("Delay Discounting Choices")
        plt.xlabel("Choice")
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(PLOTS_DIR, "delay_choices.png"))
        plt.close()

    return analysis_results
