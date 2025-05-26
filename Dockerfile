FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install the latest version of Poetry
RUN pip install --no-cache-dir poetry==1.6.1  # Replace with the latest stable version if newer

# Copy the requirements file
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi

# Copy the application code
COPY cogniform ./app
# Copy the templates directory (including static files)
COPY templates ./templates

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]