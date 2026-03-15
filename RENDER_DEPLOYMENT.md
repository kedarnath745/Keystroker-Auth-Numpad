# Deploy to Render - Step by Step Guide

## What We've Changed

Your repo has been optimized for Render with:
- ✅ `requirements-prod.txt` - Production-only dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `server.py` - Updated to use PORT env variable
- ✅ `Dockerfile` - Updated for Render deployment
- ✅ `.env.example` - Environment template

## Deploy Backend to Render (5 minutes)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Authorize GitHub access

### Step 2: Deploy Backend on Render
1. Go to [render.com/dashboard](https://render.com/dashboard)
2. Click **"New +"** → **"Web Service"**
3. Select your GitHub repository
4. Fill in the form:

   | Setting | Value |
   |---------|-------|
   | **Name** | keystroker-auth-backend |
   | **Environment** | Docker |
   | **Region** | Oregon (Free tier available) |
   | **Plan** | Free |

5. Click **"Create Web Service"**

### Step 3: ADD ENVIRONMENT VARIABLES

While the service is deploying, go to **Settings** → **Environment**:

```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=keystroker_auth
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.vercel.app
```

For local dev + production, use:
```
CORS_ORIGINS=http://localhost:3000,https://yourdomain.vercel.app
```

### Step 4: Get Your Backend URL

After deployment completes:
1. Copy the service URL (e.g., `https://keystroker-auth-backend.onrender.com`)
2. Test it: Visit `https://keystroker-auth-backend.onrender.com/api/health`
3. Should see: `{"status":"ok","timestamp":"...","service":"keystroker-auth-vercel"}`

### Step 5: Connect Frontend (Vercel)

Update Vercel environment variable:

In Vercel Dashboard → Settings → Environment Variables:
```
REACT_APP_BACKEND_URL=https://keystroker-auth-backend.onrender.com
```

Then trigger a redeploy by pushing to GitHub.

---

## MongoDB Setup (if not done)

### Option A: MongoDB Atlas (Recommended & Free)

1. Go to [mongodb.com/cloud](https://mongodb.com/cloud)
2. Create free account
3. Create M0 (free) cluster
4. Create database user:
   - Username: `keystroker_user`
   - Password: Generate strong password
5. Whitelist IP: **`0.0.0.0/0`** (allows all IPs)
6. Get connection string:
   ```
   mongodb+srv://keystroker_user:YOUR_PASSWORD@cluster0.mongodb.net/?retryWrites=true&w=majority
   ```

Add this as `MONGO_URL` in Render environment variables.

### Option B: Self-Hosted MongoDB

Skip this if using MongoDB Atlas. Only if you have your own MongoDB server:
- Ensure it's publicly accessible
- Update connection string in Render

---

## Frontend Deployment (Vercel)

Your frontend is already configured for Vercel. Just ensure:

1. Frontend is deployed: [vercel.com/new](https://vercel.com/new)
2. Root directory: `./frontend`
3. Build: `npm install && npm run build`
4. Add env var: `REACT_APP_BACKEND_URL=https://keystroker-auth-backend.onrender.com`

---

## Prevent Render Free Tier Sleep

🚨 **Important**: Render free tier spins down after 15 minutes of inactivity

### Option 1: Use UptimeRobot (Free)

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Sign up (free account)
3. Create Monitor:
   - **Friendly Name**: Keystroker API
   - **URL**: `https://keystroker-auth-backend.onrender.com/api/health`
   - **Check Interval**: 5 minutes
4. Service will stay awake!

### Option 2: Upgrade to Paid Plan

- Paid plans on Render don't have sleep/spin-down
- Starts at ~$7/month

### Option 3: Use Railway Instead

Railway has better free tier:
- $5/month credits
- No cold starts
- See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

---

## Verify Deployment

### 1. Test Backend API
```bash
# Health check
curl https://keystroker-auth-backend.onrender.com/api/health

# Should return:
# {"status":"ok","timestamp":"2026-03-15T...","service":"keystroker-auth-vercel"}
```

### 2. Test Frontend → Backend Connection
1. Visit your Vercel URL: `https://yourdomain.vercel.app`
2. Open DevTools (F12) → Console
3. No CORS errors = ✅ Success
4. Try registering a user
5. Check that user is created in MongoDB Atlas

### 3. Check Logs

**Render Backend Logs:**
- Render Dashboard → Your service → Logs
- Should see: "Starting Keystroker Auth API..."

**Frontend Network Logs:**
- Open DevTools → Network
- Try authentication request
- Should show 200/201 responses from backend

---

## Troubleshooting

### CORS Errors
**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Fix**:
1. Add your Vercel domain to Render `CORS_ORIGINS`
2. Redeploy Render service: Dashboard → Manual Deploy

```
CORS_ORIGINS=https://yourdomain.vercel.app
```

### 502 Bad Gateway
**Error**: Service returns 502

**Cause**: Backend crashed during deploy

**Fix**:
1. Check Render logs: Dashboard → Logs
2. Common issues:
   - Missing `MONGO_URL` env var
   - MongoDB connection string has special chars not URL-encoded
   - Models directory missing

### Service Sleeping
**Error**: First request takes 30+ seconds

**Cause**: Free tier spins down

**Fix**: Set up UptimeRobot to ping every 5 minutes

### MongoDB Connection Timeout
**Error**: `Unable to connect to MongoDB`

**Fix**:
1. Test connection string locally:
   ```bash
   python -c "from pymongo import MongoClient; MongoClient('YOUR_CONNECTION_STRING')"
   ```
2. Verify IP whitelist in MongoDB Atlas is `0.0.0.0/0`
3. Check password doesn't have special chars (URL encode: `@` → `%40`)

---

## Production Checklist

- [ ] Backend deployed on Render
- [ ] `MONGO_URL` set correctly in Render
- [ ] `CORS_ORIGINS` includes your Vercel domain
- [ ] UptimeRobot monitoring Render (to prevent sleep)
- [ ] Frontend deployed on Vercel
- [ ] `REACT_APP_BACKEND_URL` set to Render URL
- [ ] End-to-end test: register → enroll → authenticate works
- [ ] No CORS errors in browser console
- [ ] Health check responds: `/api/health`
- [ ] Database shows created users
- [ ] Error logs reviewed for issues

---

## Cost Summary

**Free Deployment:**
- Vercel Frontend: Free ✅
- Render Backend: Free (with 750 hrs/month) ✅
- MongoDB Atlas: Free 512MB tier ✅
- UptimeRobot: Free ✅

**Total: $0/month** 🎉

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Set environment variables
3. ✅ Test `/api/health` endpoint
4. ✅ Update Vercel environment variables
5. ✅ Verify end-to-end functionality
6. ✅ Set up UptimeRobot monitoring
7. ✅ Share with users!

---

## Support & References

- 📖 Render Docs: https://render.com/docs
- 📖 MongoDB Atlas: https://docs.mongodb.com/manual/reference/connection-string/
- 📖 FastAPI: https://fastapi.tiangolo.com/
- 🔗 UptimeRobot: https://uptimerobot.com

