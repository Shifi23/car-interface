# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN curl -sSL https://install.python-poetry.org | python3 -


# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN pip install poetry

WORKDIR /app
COPY . /app

COPY poetry.lock pyproject.toml /app/

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-root && \
    poetry build
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["poetry", "run", "start"]
