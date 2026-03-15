# Optional: Vercel Serverless Functions

This directory contains optional API routes for Vercel deployment.

**NOTE**: The main backend should be deployed to an external service (Railway, Render, etc.) because:
1. Vercel functions have 30-second timeout limits
2. ML models are too large for serverless constraints
3. Background tasks can't run on serverless

Only use these if you want to serve simple health checks or middleware.

## Files in this directory (Optional)

- `health.py` - Health check endpoint
- `middleware.py` - CORS and common middleware

## To Enable Serverless Functions:

1. Ensure `vercel.json` has:
```json
{
  "functions": {
    "api/**/*.py": {
      "memory": 3008,
      "maxDuration": 30
    }
  }
}
```

2. Deploy and functions will be available at `/api/*`

## Recommended Approach:

Keep backend on external service (Railway/Render) pointing to MongoDB Atlas, and Vercel only hosts the frontend React app.
