# Complete Deployment Guide - All Platforms

Your repo is now fully configured for deployment on **Vercel** (frontend), **Render** (backend), and **MongoDB Atlas** (database).

## 🚀 Quick Deploy (15 minutes)

### 1. Frontend → Vercel (5 min)

```bash
# Already configured in VERCEL_DEPLOYMENT.md
git push origin main
# Go to https://vercel.com/new
# Select your repo → Deploy ✅
```

**Then add env var in Vercel:**
```
REACT_APP_BACKEND_URL=https://backend-url.onrender.com
```

See: **[VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)**

### 2. Backend → Render (5 min)

```bash
# render.yaml is already configured!
git push origin main
# Go to https://render.com/new
# Select repo (auto-loads render.yaml) → Deploy ✅
```

**Then add env vars in Render:**
```
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/
DB_NAME=keystroker_auth
CORS_ORIGINS=https://yourdomain.vercel.app
```

See: **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)**

### 3. Database → MongoDB Atlas (5 min)

1. Go to [mongodb.com/cloud](https://mongodb.com/cloud)
2. Create account → Free M0 cluster
3. Create user (keystroker_user, strong password)
4. Whitelist IP: `0.0.0.0/0`
5. Get connection string:
   ```
   mongodb+srv://keystroker_user:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
6. Add to `MONGO_URL` in Render

---

## 📊 Architecture

```
┌─────────────────────────────────────┐
│   Frontend (React)                  │
│   Deployed on Vercel                │
│   https://yourdomain.vercel.app     │
└──────────────┬──────────────────────┘
               │ REACT_APP_BACKEND_URL
               │ (env variable)
               ▼
┌─────────────────────────────────────┐
│   Backend (FastAPI + ML)            │
│   Deployed on Render                │
│   https://your-backend.onrender.com │
└──────────────┬──────────────────────┘
               │ MONGO_URL
               │ (env variable)
               ▼
┌─────────────────────────────────────┐
│   Database (MongoDB)                │
│   Hosted on MongoDB Atlas           │
│   mongodb+srv://...                 │
└─────────────────────────────────────┘
```

---

## 📋 Deployment Files

| File | Purpose | For Whom |
|------|---------|----------|
| **vercel.json** | Frontend config on Vercel | Frontend devs |
| **render.yaml** | Backend config on Render | Backend devs |
| **.env.example** | Environment template | Everyone |
| **backend/.env.example** | Backend env template | Backend devs |
| **docker-compose.yml** | Local Docker setup | Local development |

---

## 🔧 Config Checklists

### Vercel Frontend ✅

File: `vercel.json`
- ✅ Build command: `cd frontend && npm install && npm run build`
- ✅ Output: `frontend/build`
- ✅ Cache headers configured
- ✅ Routing rules for SPA

See: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

### Render Backend ✅

File: `render.yaml`
- ✅ Python 3.11
- ✅ Build: `pip install -r backend/requirements-prod.txt`
- ✅ Start: `cd backend && python server.py`
- ✅ Free tier on Oregon

See: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

### Environment Variables

**Render Backend** (Settings → Environment):
```
MONGO_URL           # From MongoDB Atlas
DB_NAME             # keystroker_auth
CORS_ORIGINS        # Your Vercel domain
ENVIRONMENT         # production
```

**Vercel Frontend** (Settings → Environment):
```
REACT_APP_BACKEND_URL   # Your Render URL
```

---

## 🌍 Free Tier Considerations

### Render Free Tier
- ✅ 750 hours/month (≈ always available)
- ⚠️ Spins down after 15 min inactivity
- ✅ Use UptimeRobot (free) to keep warm

→ See: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) section "Prevent Sleep"

### Vercel Free Tier
- ✅ Up to 100GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Automatic SSL

### MongoDB Atlas Free Tier
- ✅ 512MB storage
- ✅ Shared cluster
- ✅ 3 nodes for replication

---

## 🧪 Local Development

### Setup

```bash
# Clone and install dependencies
git clone <your-repo>
cd Keystroker-Auth-Numpad

# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set MONGO_URL to mongodb://localhost:27017

# Frontend
cd ../frontend
npm install
```

### Run Services

**Terminal 1: Start MongoDB**
```bash
docker run -p 27017:27017 --name mongodb mongo:latest
```

**Terminal 2: Start Backend**
```bash
cd backend
python server.py
# Runs on http://localhost:8000
```

**Terminal 3: Start Frontend**
```bash
cd frontend
npm start
# Runs on http://localhost:3000
```

Visit: http://localhost:3000

---

## ✅ Verification Checklist

### After Deploying Frontend to Vercel
- [ ] Visit Vercel URL in browser
- [ ] Page loads without errors
- [ ] No "Failed to compile" message
- [ ] CSS/styling looks good

### After Deploying Backend to Render
- [ ] Test health endpoint:
  ```bash
  curl https://you-backend.onrender.com/api/health
  ```
- [ ] Should return `{"status":"ok",...}`
- [ ] Render logs show "Starting Keystroker Auth API"

### End-to-End Test
- [ ] Visit Vercel frontend URL
- [ ] Open DevTools (F12) → Console
- [ ] No CORS errors
- [ ] Click "Register" → page works
- [ ] Fill form → submit
- [ ] Check backend logs for request
- [ ] Check MongoDB for new user

### Production Verification
- [ ] Backend URL responds in < 2s
- [ ] Frontend loads in < 3s
- [ ] Authentication works end-to-end
- [ ] No errors in browser console
- [ ] No errors in Render logs
- [ ] MongoDB has user data

---

## 🚨 Troubleshooting

### Frontend Shows "Cannot reach backend"

**Cause**: CORS or wrong backend URL

**Fix**:
1. Check `REACT_APP_BACKEND_URL` in Vercel settings
2. Make sure it matches your Render domain exactly
3. Add your Vercel domain to `CORS_ORIGINS` in Render
4. Redeploy Render: Dashboard → Manual Deploy

### Backend Returns 502

**Cause**: Service crashed on startup

**Fix**:
1. Check Render logs: Dashboard → Logs
2. Common issues:
   - Missing `MONGO_URL`
   - MongoDB connection string wrong
   - Models directory missing
3. Find and fix the error
4. Redeploy

### "MongoDB connection timeout"

**Cause**: IP not whitelisted or wrong credentials

**Fix**:
1. MongoDB Atlas → Network Access
2. Add `0.0.0.0/0` (allows all IPs)
3. Check username/password in connection string
4. Special chars in password? URL-encode them (`@` → `%40`)
5. Test locally with connection string

### Backend takes 30+ seconds to respond

**Cause**: Render free tier cold start

**Fix**:
1. This is normal for free tier
2. Set up UptimeRobot to ping every 5 minutes
3. See: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

---

## 📚 Deployment Guides

- **Frontend**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) - Complete Vercel guide
- **Backend**: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Complete Render guide
- **Comparison**: [RENDER_VS_RAILWAY.md](RENDER_VS_RAILWAY.md) - Render vs Railway
- **Quick Start**: [QUICK_START.md](QUICK_START.md) - 5-min quick reference
- **Changes**: [RENDER_CHANGES.md](RENDER_CHANGES.md) - What was configured
- **Checklist**: [VERCEL_CHECKLIST.md](VERCEL_CHECKLIST.md) - Pre-deployment checklist

---

## 🎯 Step-by-Step for First Deployment

### Week 1: Prepare

- [ ] Read [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
- [ ] Create MongoDB Atlas account and cluster
- [ ] Test backend locally with production MongoDB
- [ ] Push code to GitHub

### Week 2: Deploy Backend

- [ ] Go to render.com
- [ ] Create web service from repo
- [ ] Add environment variables
- [ ] Wait for deploy (3-5 min)
- [ ] Test `/api/health` endpoint
- [ ] Check logs for errors

### Week 3: Deploy Frontend

- [ ] Go to vercel.com
- [ ] Create web service from repo
- [ ] Add `REACT_APP_BACKEND_URL` env var
- [ ] Wait for deploy (1-3 min)
- [ ] Test frontend loads
- [ ] Test browser console has no errors

### Week 4: Verify & Optimize

- [ ] End-to-end test the full flow
- [ ] Check response times
- [ ] Set up UptimeRobot for backend
- [ ] Monitor logs for first week
- [ ] Share with users!

---

## 💰 Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| Vercel Frontend | Up to 100GB/mo | Free ✅ |
| Render Backend | 750 hrs/mo | Free ✅ |
| MongoDB Atlas | 512MB storage | Free ✅ |
| UptimeRobot | 50 monitors | Free ✅ |
| **Total** | - | **$0/month** 🎉 |

---

## 🔗 Useful Links

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- MongoDB Atlas: https://www.mongodb.com/cloud
- FastAPI: https://fastapi.tiangolo.com
- UptimeRobot: https://uptimerobot.com
- GitHub: https://github.com

---

## 🎓 Learning Resources

### YouTube Tutorials
- "Deploy FastAPI to Render" (2-3 min)
- "MongoDB Atlas Setup" (5 min)
- "Vercel + API Integration" (10 min)

### Documentation
- [Render Docker Guide](https://render.com/docs/docker)
- [MongoDB Connection String](https://docs.mongodb.com/manual/reference/connection-string/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/concepts/)

---

## ❓ FAQ

**Q: Can I use different database?**
A: Yes, update MONGO_URL to your database. Keep same env variable name.

**Q: Can I use Railway instead of Render?**
A: Yes! See [RENDER_VS_RAILWAY.md](RENDER_VS_RAILWAY.md) for setup.

**Q: What if I need to scale?**
A: Upgrade Render/Railway plan when needed. Code doesn't change.

**Q: How do I update after deploying?**
A: Just push to GitHub. Vercel/Render auto-redeploy!

**Q: Can I use my own domain?**
A: Yes, both Vercel and Render support custom domains.

**Q: What about security?**
A: Use strong MongoDB password, enable HTTPS (automatic), use env variables for secrets.

---

## 📞 Need Help?

1. Check relevant guide above (Render/Vercel/MongoDB)
2. Read troubleshooting section
3. Check service logs (Render/Vercel dashboard)
4. Search GitHub issues
5. Contact platform support

---

## ✨ You're All Set!

Your repo is fully configured for deployment. Choose your platform and deploy! 🚀

**Next Step**: Pick Render or Railway (or both!) and follow the 5-minute setup.

Questions? Check the guides above or open an issue! 🙌
