# Vercel Deployment Checklist

Use this checklist to ensure everything is properly configured for Vercel deployment.

## Pre-Deployment

- [ ] Code pushed to GitHub repository
- [ ] All environment variables documented in `.env.example`
- [ ] Frontend builds successfully locally (`npm run build` in frontend folder)
- [ ] No hardcoded URLs or credentials in code
- [ ] `.gitignore` includes `.env` files
- [ ] `vercel.json` configuration is present

## Vercel Setup

- [ ] Vercel account created at vercel.com
- [ ] GitHub connected to Vercel
- [ ] Project imported from GitHub
- [ ] Build settings configured:
  - [ ] Framework: Create React App (or None)
  - [ ] Build Command: `cd frontend && npm install && npm run build`
  - [ ] Output Directory: `frontend/build`
  - [ ] Root Directory: `./` (root of monorepo)

## Environment Variables (Vercel Dashboard)

- [ ] `REACT_APP_BACKEND_URL` set to your backend URL
- [ ] All environment variables are Production safe (no dev secrets)
- [ ] Variables are set for all environments (Production, Staging, Preview if applicable)

## Backend Setup

Choose One:

### Option A: External Backend Service (Recommended)
- [ ] Backend deployed to Railway/Render/AWS/Google Cloud
- [ ] MongoDB Atlas cluster created
- [ ] Database connection string secured (IP whitelist configured)
- [ ] Backend API is accessible from your Vercel domain
- [ ] CORS configured to allow your Vercel domain
- [ ] SSL certificate enabled on backend (if custom domain)

### Option B: Vercel Serverless Functions
- [ ] Python API routes created in `api/` folder
- [ ] `vercel.json` includes functions configuration
- [ ] `requirements.txt` in root (if using Python)
- [ ] All dependencies fit within 3008 MB limit
- [ ] Functions have timeout configured (max 30s)

## Database

- [ ] MongoDB Atlas (or self-hosted MongoDB)
  - [ ] User created with strong password
  - [ ] Database created (`keystroker_auth`)
  - [ ] IP whitelist configured (or 0.0.0.0 for flexibility)
  - [ ] Connection string format: `mongodb+srv://user:pass@cluster.mongodb.net/`
- [ ] Backup strategy configured
- [ ] Monitoring enabled

## Frontend Configuration

- [ ] All API endpoints use `REACT_APP_BACKEND_URL` environment variable
- [ ] No hardcoded `localhost:8000` URLs in code
- [ ] Error handling for offline/unavailable backend
- [ ] Loading states implemented
- [ ] CORS headers expected from backend

## Security

- [ ] No sensitive data in version control
- [ ] Environment variables properly isolated per environment
- [ ] HTTPS enforced (automatic with Vercel)
- [ ] CORS properly configured (not `*` for production)
- [ ] JWT/Auth tokens handled securely
- [ ] Database credentials never exposed in frontend

## Testing

- [ ] Frontend builds without errors: `npm run build` in frontend
- [ ] Frontend loads locally: `npm start` in frontend
- [ ] API endpoints respond correctly
- [ ] CORS requests work from frontend to backend
- [ ] User registration works end-to-end
- [ ] Authentication/keystroke capture works
- [ ] Error cases handled gracefully

## Post-Deployment Verification

- [ ] Visit Vercel deployment URL
- [ ] Frontend loads without errors (F12 → Console)
- [ ] No CORS errors in browser console
- [ ] API calls succeed to backend
- [ ] User can register/login/authenticate
- [ ] All features work end-to-end

## Monitoring & Maintenance

- [ ] Vercel Analytics enabled (optional but recommended)
- [ ] Error tracking enabled (Sentry/DataDog/etc.)
- [ ] Database monitoring enabled
- [ ] Backend service monitoring enabled
- [ ] Daily backup schedule for database configured
- [ ] Alerts configured for:
  - [ ] High error rates
  - [ ] Deployment failures
  - [ ] Database connection issues

## Custom Domain (Optional)

- [ ] Domain registered
- [ ] DNS records updated per Vercel instructions
- [ ] SSL certificate auto-generated
- [ ] Redirect from non-www to www (or vice versa)
- [ ] Email forwarding configured (if needed)

## Performance Optimization

- [ ] Static assets cached with long-lived headers (done in vercel.json)
- [ ] Images optimized
- [ ] Code splitting enabled (CRA default)
- [ ] Lazy loading for routes implemented
- [ ] Database queries optimized
- [ ] No blocking operations in critical path

## Documentation

- [ ] `VERCEL_DEPLOYMENT.md` committed to repo
- [ ] `QUICK_START.md` has deployment steps
- [ ] Environment variables documented
- [ ] API endpoints documented
- [ ] Backend setup guide included
- [ ] Troubleshooting guide written

## Final Checks

- [ ] All team members have access to Vercel project
- [ ] Rollback procedure documented
- [ ] Emergency contacts identified
- [ ] Support channels established
- [ ] DNS propagation verified (for custom domain)
- [ ] Performance baseline established

---

**Deployment Status**: ✅ Ready / ⏳ In Progress / ❌ Blocked

**Deployed on**: ___________

**Notes**: 
```
[Add any additional notes or blockers here]
```
