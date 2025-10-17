﻿from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat, upload

app = FastAPI(title="Archon", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Archon API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
