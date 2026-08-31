FROM python:3.12-slim

LABEL description="Aviz Academy GHA demo app"

# Don't buffer stdout/stderr, don't write .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Bind address for gunicorn. 127.0.0.1 keeps the app on the container's
# loopback only; override at runtime (-e BIND_ADDRESS=0.0.0.0:8000) to
# publish the port outside the container.
ENV BIND_ADDRESS=127.0.0.1:8000

WORKDIR /app

# Create a non-root user to run the application
RUN groupadd --system avizuser \
    && useradd --system --gid avizuser --create-home --home-dir /home/avizuser --shell /usr/sbin/nologin avizuser

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN chown -R avizuser:avizuser /app

# Drop privileges: everything below runs as avizuser
USER avizuser

EXPOSE 8000

CMD ["sh", "-c", "exec gunicorn --bind ${BIND_ADDRESS} --workers 2 --threads 4 --timeout 60 --access-logfile - --error-logfile - app:app"]
