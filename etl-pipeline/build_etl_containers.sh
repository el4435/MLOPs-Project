#!/bin/bash

set -e

echo "Building Docker images for ETL services..."

# Build each Docker image that requires building from the current context
docker compose -f docker-compose.yml -p taxi-only-etl build process-taxi
docker compose -f docker-compose.yml -p taxi-only-etl build download-events-monthly
docker compose -f docker-compose.yml -p taxi-only-etl build process-events-monthly
docker compose -f docker-compose.yml -p taxi-only-etl build download-events-test
docker compose -f docker-compose.yml -p taxi-only-etl build split-datasets

echo "Build completed for all services."
