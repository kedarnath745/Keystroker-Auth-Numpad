# Docker Setup Guide - Keystroke Auth Numpad

This guide explains how to run the Keystroke Authentication System using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (comes with Docker Desktop)
- At least 2GB of free disk space

## Quick Start

### 1. Build and Start All Services

```bash
cd Keystroker-Auth-Numpad
docker-compose up -d
```

This command will:
- Build the backend Docker image
- Build the frontend Docker image
- Download and start MongoDB
- Start all services in the background

### 2. Access the Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MongoDB**: mongodb://admin:keystroke_secure_password@localhost:27017

## Docker Services

### MongoDB (Database)
- **Container Name**: keystroke_mongodb
- **Port**: 27017
- **Username**: admin
- **Password**: keystroke_secure_password
- **Storage**: Persisted in `mongodb_data` volume

### Backend (FastAPI)
- **Container Name**: keystroke_backend
- **Port**: 8000
- **Technology**: Python 3.11 + FastAPI
- **Hot Reload**: Enabled (code changes auto-apply)

### Frontend (React)
- **Container Name**: keystroke_frontend
- **Port**: 80
- **Technology**: Node.js 20 + React + Nginx
- **Build**: Multi-stage build (production-optimized)

## Common Commands

### View Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Stop Services
```bash
docker-compose stop
```

### Stop and Remove Containers
```bash
docker-compose down
```

### Stop and Remove Everything (including volumes)
```bash
docker-compose down -v
```

### Rebuild Services
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Restart a Specific Service
```bash
docker-compose restart backend
```

## Development Workflow

### Making Code Changes

**Backend Python Changes:**
- Changes are automatically applied (hot reload enabled)
- Check logs with: `docker-compose logs -f backend`

**Frontend React Changes:**
- Rebuild the frontend: `docker-compose build frontend`
- Restart frontend: `docker-compose up -d frontend`
- Or do a full rebuild: `docker-compose down && docker-compose up -d`

### Accessing the Backend Interactive Shell
```bash
docker-compose exec backend bash
```

### Accessing MongoDB Shell
```bash
docker-compose exec mongodb mongosh -u admin -p keystroke_secure_password --authenticationDatabase admin keystroke_auth
```

## Environment Variables

The docker-compose.yml uses these environment variables:

**Backend:**
- `MONGO_URL`: MongoDB connection string
- `DB_NAME`: Database name
- `PYTHONUNBUFFERED`: Ensures Python output is logged immediately

**MongoDB:**
- `MONGO_INITDB_ROOT_USERNAME`: Admin username
- `MONGO_INITDB_ROOT_PASSWORD`: Admin password
- `MONGO_INITDB_DATABASE`: Initial database

To customize, edit `docker-compose.yml` or create a `.env` file with the variables.

## Troubleshooting

### Port Already in Use
If port 80, 8000, or 27017 is already in use:

```bash
# Change ports in docker-compose.yml:
# Change "80:80" to "8080:80" for frontend
# Change "8000:8000" to "8001:8000" for backend
# Change "27017:27017" to "27018:27017" for mongodb
```

### Container Won't Start
```bash
# Check logs for errors
docker-compose logs backend

# Rebuild without cache
docker-compose build --no-cache backend
docker-compose up -d
```

### MongoDB Connection Failed
```bash
# Verify MongoDB is running
docker-compose ps

# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

### Frontend Shows "Cannot reach backend"
1. Verify backend is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Verify network: `docker network ls`
4. Restart all services: `docker-compose restart`

## Production Deployment

For production deployment:

1. **Update Credentials**: Change MongoDB password in `docker-compose.yml`
2. **Use Environment File**: Create `.env` file with production values
3. **Configure CORS**: Update backend CORS settings for your domain
4. **Set up SSL/TLS**: Use a reverse proxy (Nginx) with SSL certificates
5. **Use Production Build**: Remove `--reload` flag from backend command
6. **Resource Limits**: Add `resources` section to docker-compose.yml services

Example resource limits for production:
```yaml
services:
  backend:
    # ... other config ...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## File Structure

```
Keystroker-Auth-Numpad/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py
│   └── ...
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── public/
│   └── src/
├── docker-compose.yml
├── .dockerignore
├── .env.docker
└── DOCKER_SETUP.md (this file)
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [React Docker Guide](https://create-react-app.dev/docs/deployment/)

## Support

For issues or questions:
1. Check the logs: `docker-compose logs`
2. Verify all services are healthy: `docker-compose ps`
3. Ensure ports are available and not in use
4. Try rebuilding: `docker-compose build --no-cache && docker-compose up -d`
