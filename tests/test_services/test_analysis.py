import pytest
import pandas as pd
from unittest.mock import MagicMock
from cogniform.services.analysis import (
    analyze_responses,
    visualize_results,
    plot_accuracy,
    analyze_data,
)
from sqlalchemy.orm import Session
from cogniform.services.database import UserResponses


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {"response_time": [1.2, 2.3, 3.1, 4.5, 2.2], "accuracy": [1, 0, 1, 1, 0]}
    )


def test_analyze_responses(sample_data):
    summary = analyze_responses(sample_data)
    assert "response_time" in summary.columns
    assert "accuracy" in summary.columns
    assert summary.loc["mean", "response_time"] == pytest.approx(2.66, 0.01)


def test_visualize_results(sample_data, mocker):
    mocker.patch("matplotlib.pyplot.show")  # Prevent plots from displaying during tests
    visualize_results(sample_data, "Sample Task")
    # No assertions needed; ensure no exceptions are raised


def test_plot_accuracy(sample_data, mocker):
    mocker.patch("matplotlib.pyplot.show")  # Prevent plots from displaying during tests
    plot_accuracy(sample_data, "Sample Task")
    # No assertions needed; ensure no exceptions are raised


@pytest.fixture
def mock_db_session():
    session = MagicMock(spec=Session)
    session.query.return_value.all.return_value = [
        UserResponses(
            age=25,
            education="bachelors",
            familiarity="intermediate",
            crt_q1_response_time=1.5,
            crt_q1_correct=True,
            crt_q2_response_time=2.0,
            crt_q2_correct=False,
            crt_q3_response_time=1.8,
            crt_q3_correct=True,
            delay_response_time=3.2,
            delay_choice="smaller",
        ),
        UserResponses(
            age=30,
            education="masters",
            familiarity="advanced",
            crt_q1_response_time=1.2,
            crt_q1_correct=True,
            crt_q2_response_time=2.5,
            crt_q2_correct=True,
            crt_q3_response_time=2.0,
            crt_q3_correct=False,
            delay_response_time=2.8,
            delay_choice="larger",
        ),
    ]
    return session


def test_analyze_data(mock_db_session):
    results = analyze_data(mock_db_session)
    assert "demographics" in results
    assert "crt" in results
    assert "delay_discounting" in results

    # Demographics assertions
    assert results["demographics"]["average_age"] == 27.5
    assert results["demographics"]["education_distribution"]["bachelors"] == 1
    assert results["demographics"]["education_distribution"]["masters"] == 1
    assert results["demographics"]["familiarity_distribution"]["intermediate"] == 1
    assert results["demographics"]["familiarity_distribution"]["advanced"] == 1

    # CRT assertions
    assert results["crt"]["average_response_time"] == pytest.approx(1.83, 0.01)
    assert results["crt"]["accuracy"] == pytest.approx(0.67, 0.01)

    # Delay Discounting assertions
    assert results["delay_discounting"]["average_response_time"] == pytest.approx(
        3.0, 0.01
    )
    assert results["delay_discounting"]["choice_distribution"]["smaller"] == 1
    assert results["delay_discounting"]["choice_distribution"]["larger"] == 1
