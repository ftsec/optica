# Use an official Python runtime as a parent image, with a specific version tag
FROM python:3.11-alpine
WORKDIR /app

RUN adduser -D -u 1001 optica && chown -R optica:optica /app
USER 1001

COPY --chown=optica:optica requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=optica:optica src/ ./
