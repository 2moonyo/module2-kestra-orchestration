FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /code

# Copy dependency files
COPY pyproject.toml .python-version uv.lock ./

# Install dependencies
RUN uv sync --locked

# Copy application files
COPY Ingest_script.py ./

# Set PATH to include virtual environment
ENV PATH="/code/.venv/bin:$PATH"

ENTRYPOINT ["/bin/bash"]