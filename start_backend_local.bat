@echo off
REM Start MongoDB locally (requires Docker)
echo Starting MongoDB...
docker run -d -p 27017:27017 --name mongodb mongo:latest

REM Start Backend
echo Starting Backend...
cd backend
python server.py

REM In another terminal, run:
REM cd frontend
REM npm start
