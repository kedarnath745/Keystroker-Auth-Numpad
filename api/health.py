from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "keystroker-auth-vercel"
    }

@app.get("/")
async def root():
    """Root API endpoint"""
    return {
        "message": "Keystroker Auth API",
        "version": "1.0.0",
        "docs": "/docs"
    }
