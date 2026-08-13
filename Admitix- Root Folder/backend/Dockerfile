# Base Image
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Working directory inside container
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]