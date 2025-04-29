FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap

RUN pip install uv

WORKDIR /app
COPY pyproject.toml README.md ./
COPY app/ app/
COPY tests/ tests/

RUN uv venv
ENV PATH="/app/.venv/bin:$PATH"

RUN uv pip install -e ".[dev]"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]w