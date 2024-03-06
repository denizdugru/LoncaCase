#!/bin/bash

# Build and run MongoDB container
docker build -t my-mongo -f dockerfiles/Dockerfile.mongo .
docker run -d --name mongo_container my-mongo

# Build and run FastAPI app container
docker build -t app -f dockerfiles/Dockerfile.app .
docker run -d --name app_container -p 8000:8000 --env-file .env --link mongo_container app
