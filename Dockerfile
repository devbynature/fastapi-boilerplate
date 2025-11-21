FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml ./

RUN uv sync

COPY src/ .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]
