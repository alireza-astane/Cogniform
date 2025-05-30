# CogniForm

CogniForm is an interactive cognitive science survey platform designed to assess various cognitive traits through tasks such as the Cognitive Reflection Test (CRT) and Delay Discounting Task. The platform provides a user-friendly interface for participants to complete surveys and view their results, while also offering tools for researchers to analyze and visualize collected data.

---

## Features

- **Interactive Cognitive Tasks**: Includes tasks like CRT and Delay Discounting to assess cognitive traits.
- **Demographics Collection**: Collects participant demographics such as age, education, and familiarity with cognitive science.
- **Real-Time Results**: Displays individual results immediately after task completion.
- **Data Analysis and Visualization**: Provides aggregated analysis and visualizations of participant data.
- **Database Integration**: Stores participant responses in a database for further analysis.
- **Dockerized Deployment**: Easily deployable using Docker and Docker Compose.
- **Continuous Integration/Deployment**: Automated CI/CD pipelines using GitHub Actions.

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Project Structure](#project-structure)
4. [Development](#development)
5. [Testing](#testing)
6. [API Endpoints](#api-endpoints)
7. [Contributing](#contributing)
8. [License](#license)

---

## Installation

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose (optional for containerized deployment)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/CogniForm.git
   cd CogniForm
   ```

2. Install dependencies using Poetry:
   ```bash
   pip install poetry
   poetry install
   ```

3. Set up the database:
   ```bash
   python -m cogniform.services.database
   ```

4. Run the application:
   ```bash
   poetry run uvicorn cogniform.main:app --reload
   ```

5. Access the application at `http://127.0.0.1:8000`.

---

## Usage

### Running with Docker

1. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

2. Access the application at `http://127.0.0.1:8000`.

---

## Project Structure

```
CogniForm/
├── cogniform/                # Core application code
│   ├── api/                  # API routes
│   ├── core/                 # Configuration and initialization
│   ├── models/               # Data models
│   ├── services/             # Database and analysis services
│   ├── tasks/                # Cognitive tasks logic
│   └── main.py               # FastAPI application entry point
├── templates/                # HTML templates and static files
├── tests/                    # Unit and integration tests
├── .github/workflows/        # CI/CD workflows
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── pyproject.toml            # Poetry configuration
└── README.md                 # Project documentation
```

---

## Development

### Setting Up the Development Environment

1. Install development dependencies:
   ```bash
   poetry install --with dev
   ```

2. Run the application in development mode:
   ```bash
   poetry run uvicorn cogniform.main:app --reload
   ```

3. Access the application at `http://127.0.0.1:8000`.

---

## Testing

### Running Tests

1. Run all tests:
   ```bash
   poetry run pytest
   ```

2. Run specific tests:
   ```bash
   poetry run pytest tests/test_services/test_database.py
   ```

3. View test coverage:
   ```bash
   poetry run pytest --cov=cogniform
   ```

---

## API Endpoints

### Public Endpoints

- `GET /`: Home page.
- `GET /demographics`: Demographics form.
- `POST /demographics`: Submit demographics data.
- `GET /crt`: Cognitive Reflection Test.
- `POST /crt`: Submit CRT response.
- `GET /delay_discounting`: Delay Discounting Task.
- `POST /delay_discounting`: Submit Delay Discounting response.
- `GET /results`: View aggregated analysis results.

### Admin Endpoints

- `GET /responses`: Fetch all user responses (requires database access).

---

## Contributing

We welcome contributions from the community! Please follow the [contribution guidelines](CONTRIBUTING.md) to get started.

### Steps to Contribute

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
4. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

Special thanks to all contributors and the open-source community for their support in building CogniForm.  