# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
from .routers import summary, hiring, insights,drilldowns  # <-- 1. ADD 'insights' TO THIS IMPORT
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

app = FastAPI(
    title="Hiring Dashboard API",
    description="The API for the Svelte hiring dashboard.",
    version="1.0.0",
)

# --- Middleware ---
# This is crucial. CORS allows your Svelte frontend (running on a different port)
# to make requests to this backend.
origins = [
    "http://localhost",
    "http://localhost:5173",  # Default SvelteKit dev port
    "http://localhost:3000",  # Default Svelte/Vite dev port
    "https://dashboard2-sdeh-git-main-ashwinrajaram11-gmailcoms-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routers ---
# Include the API endpoints from our router files with a global prefix.
app.include_router(summary.router, prefix="/api/v1")
app.include_router(hiring.router, prefix="/api/v1")
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
app.include_router(insights.router, prefix="/api/v1") # <-- 2. ADD THIS LINE TO INCLUDE THE AI ROUTER
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app.include_router(drilldowns.router, prefix="/api/v1/kpis/drilldown", tags=["KPI Drilldowns"]) # <-- 2. Add this line


# --- Root Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Hiring Dashboard API"}
