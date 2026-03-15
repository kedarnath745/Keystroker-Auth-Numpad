# Vercel Deployment Guide for Keystroker Auth Numpad

## Overview

This application consists of:
- **Frontend**: React application with Radix UI components
- **Backend**: FastAPI server with ML pipeline and MongoDB integration

## Deployment Strategy

You have two options for deploying to Vercel:

### Option 1: Frontend Only (Recommended)
Deploy the frontend React app to Vercel and keep the backend running separately.

**Pros:**
- Simple Vercel setup
- Backend can use resources like GPU for ML models
- Easy backend updates without redeployment

**Cons:**
- Need to manage backend separately

### Option 2: Full Stack with Vercel Serverless Functions
Deploy both frontend and API routes as Vercel serverless functions.

**Pros:**
- All in one place
- Easy management

**Cons:**
- Serverless functions have limitations (timeout, memory)
- ML models may not fit within constraints
- More expensive at scale

## Setup Instructions

### Prerequisites
- Vercel account (free at vercel.com)
- GitHub repository with your code
- MongoDB Atlas account (free tier available)

### Step 1: Prepare Environment Variables

1. Copy `.env.example` to create your production values
2. Set these environment variables in Vercel Dashboard:
   ```
   REACT_APP_BACKEND_URL=https://your-backend-domain.com
   ```

**For Option 2 (Serverless Backend) additionally set:**
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=keystroker_auth
```

### Step 2: Deploy Frontend to Vercel

#### Via Vercel CLI:
```bash
npm install -g vercel
vercel
```

#### Via GitHub Integration:
1. Push your repository to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Select your GitHub repository
5. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `./frontend`
   - **Build Command**: `npm install && npm run build`
   - **Output Directory**: `build`
6. Add environment variables in "Environment Variables"
7. Click "Deploy"

### Step 3: Deploy Backend (Choose One)

#### Option A: Use External Backend Service

For best performance with ML models, deploy to:
- **Railway.app** (recommended)
- **Render.com**
- **Heroku**
- **AWS/Google Cloud**

Create `.env` file with:
```
MONGO_URL=your_mongodb_url
DB_NAME=keystroker_auth
PYTHONUNBUFFERED=1
```

Then set `REACT_APP_BACKEND_URL` in Vercel to your backend URL.

#### Option B: Use Vercel Serverless Functions (Python)

Structure:
```
api/
  auth.py
  users.py
  keystroke.py
  utils/
    __init__.py
    models.py
```

Create `api/auth.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

# Import other routes...
```

Then in `vercel.json`:
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/build",
  "functions": {
    "api/**/*.py": {
      "memory": 3008,
      "maxDuration": 30
    }
  }
}
```

### Step 4: Update Frontend API Base URL

The frontend automatically uses the environment variable:
```javascript
const API_BASE_URL = 
  process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
```

Set `REACT_APP_BACKEND_URL` in Vercel project settings.

### Step 5: Configure CORS

Ensure your backend allows requests from your Vercel frontend domain:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.vercel.app",
        "https://yourdomain.com",
        "http://localhost:3000"  # for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Database Setup

### MongoDB Atlas (Recommended for Vercel)

1. Go to [mongodb.com/cloud](https://mongodb.com/cloud)
2. Create a free M0 cluster
3. Create a database user (credentials)
4. Whitelist your backend IP (or 0.0.0.0 for development)
5. Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/`

Add to environment variables:
- `MONGO_URL`: Your MongoDB connection string
- `DB_NAME`: `keystroker_auth`

## Vercel Project Settings

### Environment Variables
Go to Settings → Environment Variables and add:
```
REACT_APP_BACKEND_URL=https://your-backend-url.com
```

### Build Settings
- **Framework**: Other (since using Create React App)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/build`

### Root Directory
- Keep as root (`./`) or set to root if Vercel doesn't auto-detect

## Domains & Custom DNS

1. In Vercel Dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed by Vercel

## Monitoring & Logs

- View deployment logs: Vercel Dashboard → Deployments
- View runtime logs: Click on deployment, then "Runtime Logs"
- Monitor frontend performance: Analytics tab

## Troubleshooting

### Build Fails
- Check that `frontend/package.json` exists
- Ensure all dependencies are in `package.json`
- Check Node version compatibility (default: 18.x)

### API Calls Fail
- Verify `REACT_APP_BACKEND_URL` is set correctly
- Check CORS settings on backend
- Verify backend service is running

### Slow Performance
- Check backend service performance
- Monitor database query performance
- Use Connect/disconnect pools efficiently

### ML Model Issues
- Verify model files are in backend
- Check model file size (may exceed serverless limits)
- Consider using external ML service (Hugging Face, etc.)

## Production Checklist

- [ ] Backend deployed and running
- [ ] MongoDB Atlas cluster created and secured
- [ ] CORS configured for your domain
- [ ] Environment variables set in Vercel
- [ ] Custom domain configured (optional)
- [ ] SSL certificate enabled (automatic)
- [ ] Database backups configured
- [ ] Error monitoring setup (Sentry, LogRocket)
- [ ] Performance monitoring enabled

## Advanced: CI/CD Pipeline

Vercel automatically deploys on:
1. Push to main branch
2. Pull request (preview deployment)
3. Manual redeploy

Configure in `vercel.json`:
```json
{
  "github": {
    "enabled": false,
    "silent": false
  }
}
```

## Cost Estimates

**Vercel (Frontend)**
- Free tier: up to 100 GB bandwidth/month
- Pro: $20/month for more features

**Backend Service (e.g., Railway)**
- Free tier: $5 credit/month
- Pay-as-you-go after

**MongoDB Atlas**
- Free tier (M0): 512 MB storage
- Shared tier (M2): $9/month for 10 GB

## Support

- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- MongoDB Docs: https://docs.mongodb.com
