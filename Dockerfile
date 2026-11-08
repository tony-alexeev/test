FROM python:3.12-slim

ARG APP_VERSION
RUN test -n "$APP_VERSION"
ENV APP_VERSION=$APP_VERSION
LABEL org.opencontainers.image.revision=$APP_VERSION

WORKDIR /app
COPY access.py server.py ./
USER 65532:65532
EXPOSE 8000
CMD ["python3", "server.py"]
