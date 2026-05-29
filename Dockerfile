FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --upgrade pip
COPY . .
RUN pip install --no-cache-dir .

CMD ["python", "-m", "refvault.main"]
