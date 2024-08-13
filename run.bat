@echo off
copy /y .env.example .env
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
docker-compose up