import pytest
from app.services.database import DatabaseService
from app.services.analysis import AnalysisService

@pytest.fixture
def db_service():
    return DatabaseService()

@pytest.fixture
def analysis_service():
    return AnalysisService()

def test_database_connection(db_service):
    assert db_service.connect() is True

def test_save_response(db_service):
    response_data = {'task_id': 1, 'user_id': 123, 'response': 'A'}
    db_service.save_response(response_data)
    assert db_service.get_response(123, 1) == response_data

def test_analyze_data(analysis_service):
    sample_data = [{'response': 'A', 'time': 2}, {'response': 'B', 'time': 3}]
    analysis_results = analysis_service.analyze(sample_data)
    assert isinstance(analysis_results, dict)
    assert 'average_time' in analysis_results

def test_visualize_data(analysis_service):
    sample_data = [{'response': 'A', 'time': 2}, {'response': 'B', 'time': 3}]
    plot = analysis_service.visualize(sample_data)
    assert plot is not None  # Assuming the visualize method returns a plot object