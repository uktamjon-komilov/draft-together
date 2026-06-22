FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# build deps for psycopg2; libpq is the runtime shared lib
RUN apk add --no-cache gcc musl-dev libpq-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]
