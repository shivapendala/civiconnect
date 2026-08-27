#!/usr/bin/env bash

# Entry point for the CivicConnect stack
# -------------------------------------------------
# 1. Build Docker containers (if not already built)
# 2. Start the Docker compose stack
# 3. Tail logs for convenience

set -e

echo "Building Docker images..."
 docker compose build

echo "Starting services..."
 docker compose up -d

echo "All services are up."
 echo "Backend API: http://localhost:8000/api/"
 echo "Flutter web: http://localhost"

# Keep the container running to see logs (optional)
# docker compose logs -f
