import pytest
from fastapi.testclient import TestClient
from cogniform.main import app

client = TestClient(app)


# def test_home():
#     response = client.get("/")
#     assert response.status_code == 200


@pytest.fixture(scope="function")
def test_submission():
    # Initialize session
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to CogniForm" in response.text

    # Extract session_id from Set-Cookie header
    print(response.headers)  # Debugging line to see headers
    session_id = response.headers.get("set-cookie").split(";")[0].split("=")[1]

    # Submit demographics
    response = client.post(
        "/demographics",
        data={
            "age": 25,
            "education": "bachelors",
            "familiarity": "intermediate",
        },
        cookies={"session_id": session_id},
    )
    assert response.status_code == 303  # Redirect to the next page

    # Start CRT task
    response = client.get("/crt", cookies={"session_id": session_id})
    assert response.status_code == 200

    # Submit CRT response
    response = client.post(
        "/crt",
        data={
            "index": 0,
            "answer": 0.10,
            "response_time": 2.5,
        },
        cookies={"session_id": session_id},
    )
    assert response.status_code == 303  # Redirect to the next question or results

    response = client.get("/delay_discounting")
    assert response.status_code == 200
    assert "Delay Discounting Task" in response.text

    # Start delay discounting task
    response = client.get("/delay_discounting", cookies={"session_id": session_id})
    assert response.status_code == 200

    # Submit delay discounting response
    response = client.post(
        "/delay_discounting",
        data={
            "choice": "larger",
            "response_time": 3.5,
        },
        cookies={"session_id": session_id},
    )
    assert response.status_code == 303  # Redirect to the results page

    response = client.get("/results")
    assert response.status_code == 200
    assert "Analysis Results" in response.text

    response = client.get("/logout")
    assert response.status_code == 200 or response.status_code == 303
