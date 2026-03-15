#!/bin/bash
# Start MongoDB locally (requires Docker)
echo "Starting MongoDB..."
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Start Backend
echo "Starting Backend..."
cd backend
python server.py

# In another terminal, run:
# cd frontend
# npm start
