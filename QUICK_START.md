# Quick Start: Local Development & Vercel Deployment

## Local Development

### 1. Install Dependencies

```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

### 2. Environment Setup

Create `.env` in the root and `backend/.env`:

```env
# backend/.env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=keystroker_auth
```

For MongoDB locally via Docker:
```bash
docker run -d -p 27017:27017 mongo:latest
```

### 3. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
python server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Visit http://localhost:3000

## Vercel Deployment Quick Steps

### 1. Connect GitHub Repository
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin git@github.com:yourusername/repo.git
git push -u origin main
```

### 2. Import to Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Select your GitHub repository
3. Framework: **Create React App**
4. Root Directory: **./frontend**
5. Build Command: `npm install && npm run build`
6. Output: `build`

### 3. Add Environment Variables
In Vercel Dashboard → Settings → Environment Variables:
```
REACT_APP_BACKEND_URL=https://your-api.example.com
```

### 4. Deploy Backend (Option A: External Service)

**Using Railway (Recommended):**
```bash
# Install Railway CLI
curl -fsSL https://cli.new | sh

# Login and deploy
railway login
railway init
railway link # select your project
railway up
```

Then add the Railway URL to Vercel environment variables.

## Verification

### Frontend Works
- Visit your Vercel URL
- Should see the login/registration page
- Check browser console for errors (F12)

### Backend Connected
- Try registering a user
- Should create user in database
- Check backend logs for requests

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| CORS errors | Add your Vercel domain to backend CORS config |
| 404 on API calls | Verify `REACT_APP_BACKEND_URL` is set correctly |
| Database connection fails | Check MongoDB connection string and IP whitelist |
| Build fails on Vercel | Ensure `frontend/package.json` has all dependencies |

## Performance Tips

- Use Vercel Analytics to monitor performance
- Enable caching for static assets (done in vercel.json)
- Consider CDN for additional speed
- Monitor database query performance

## Next Steps

After successful deployment:
1. Configure custom domain (vercel.com/domains)
2. Set up SSL (automatic with custom domain)
3. Add environment monitoring (Sentry/DataDog)
4. Enable error tracking
5. Set up database backups
