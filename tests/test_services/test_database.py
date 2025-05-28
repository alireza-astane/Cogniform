import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cogniform.services.database import (
    Base,
    UserResponses,
    init_db,
    save_user_responses,
    fetch_all_responses,
)

# Set up an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    # Create the database schema
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_init_db():
    # Ensure the database schema is created without errors
    try:
        init_db()
    except Exception as e:
        pytest.fail(f"init_db() raised an exception: {e}")


import uuid


def test_save_user_responses(test_db):
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    responses = {
        "demographics": {
            "age": 25,
            "education": "bachelors",
            "familiarity": "intermediate",
        },
        "crt": [
            {"user_answer": 0.10, "is_correct": True, "response_time": 5.2},
            {"user_answer": 5, "is_correct": True, "response_time": 4.8},
            {"user_answer": 47, "is_correct": True, "response_time": 6.1},
        ],
        "delay_discounting": [
            {"user_answer": "larger", "response_time": 3.5},
        ],
    }

    # Save the responses
    saved_response = save_user_responses(test_db, session_id, responses)

    # Verify the saved data
    assert saved_response.session_id == session_id
    assert saved_response.age == 25
    assert saved_response.education == "bachelors"
    assert saved_response.familiarity == "intermediate"
    assert saved_response.crt_q1_answer == 0.10
    assert saved_response.crt_q1_correct is True
    assert saved_response.crt_q1_response_time == 5.2
    assert saved_response.crt_q2_answer == 5
    assert saved_response.crt_q2_correct is True
    assert saved_response.crt_q2_response_time == 4.8
    assert saved_response.crt_q3_answer == 47
    assert saved_response.crt_q3_correct is True
    assert saved_response.crt_q3_response_time == 6.1
    assert saved_response.delay_choice == "larger"
    assert saved_response.delay_response_time == 3.5


def test_fetch_all_responses(test_db):
    # Generate unique session IDs
    session_id_1 = str(uuid.uuid4())
    session_id_2 = str(uuid.uuid4())
    responses_1 = {
        "demographics": {
            "age": 30,
            "education": "masters",
            "familiarity": "advanced",
        },
        "crt": [
            {"user_answer": 0.10, "is_correct": True, "response_time": 5.0},
            {"user_answer": 5, "is_correct": True, "response_time": 4.5},
            {"user_answer": 47, "is_correct": True, "response_time": 6.0},
        ],
        "delay_discounting": [
            {"user_answer": "smaller", "response_time": 3.0},
        ],
    }
    responses_2 = {
        "demographics": {
            "age": 22,
            "education": "bachelors",
            "familiarity": "basic",
        },
        "crt": [
            {"user_answer": 0.15, "is_correct": False, "response_time": 7.0},
            {"user_answer": 6, "is_correct": False, "response_time": 6.5},
            {"user_answer": 48, "is_correct": False, "response_time": 8.0},
        ],
        "delay_discounting": [
            {"user_answer": "larger", "response_time": 4.0},
        ],
    }

    # Save the responses
    save_user_responses(test_db, session_id_1, responses_1)
    save_user_responses(test_db, session_id_2, responses_2)

    # Fetch all responses
    all_responses = fetch_all_responses(test_db)

    # Verify the fetched data
    assert len(all_responses) == 2

    response_1 = all_responses[0]
    assert response_1.session_id == session_id_1
    assert response_1.age == 30
    assert response_1.education == "masters"
    assert response_1.familiarity == "advanced"

    response_2 = all_responses[1]
    assert response_2.session_id == session_id_2
    assert response_2.age == 22
    assert response_2.education == "bachelors"
    assert response_2.familiarity == "basic"


#
