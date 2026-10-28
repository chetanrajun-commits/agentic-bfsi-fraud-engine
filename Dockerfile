FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY examples ./examples

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["fraud-engine"]
CMD ["run", "--tx", "examples/transaction.json", "--workdir", "/tmp/out"]
