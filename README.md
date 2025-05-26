# CogniForm

CogniForm is an interactive cognitive science survey platform designed to deliver and collect cognitive task surveys via a web browser. This project emphasizes clean code, modularity, object-oriented design, and collaboration through Git, along with packaging and Dockerization.

## Project Overview

CogniForm serves various cognitive tasks, including:

1. **Cognitive Reflection Test (CRT)**: A test designed to measure cognitive reflection through open-ended questions.
2. **Stroop-like Task**: A task that assesses cognitive control by requiring users to identify the color of words that may conflict with their meaning.
3. **Delay Discounting Task**: A task that evaluates decision-making by offering choices between smaller-sooner and larger-later rewards.

The application is built using FastAPI, allowing for a RESTful API that serves randomized tasks, collects user responses, and provides feedback or visualizations as needed.

## Features

- Modular and object-oriented design for cognitive tasks.
- FastAPI server for handling requests and responses.
- Data validation and analysis using Pydantic and Python libraries.
- Visualization of results using Matplotlib or Seaborn.
- Containerization with Docker for easy deployment.
- Continuous Integration/Continuous Deployment (CI/CD) setup for testing and linting.
- Comprehensive documentation and contribution guidelines.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CogniForm.git
   cd CogniForm
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application using Docker:
   ```
   docker-compose up --build
   ```

### Usage

- Access the API at `http://localhost:8000`.
- Use the endpoints to retrieve tasks, submit responses, and view results.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- Thanks to the contributors and the cognitive science community for their insights and support in developing this platform.