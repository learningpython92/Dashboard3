# FILE: backend/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Using absolute imports
import models
from database import engine
from routers import summary, hiring, insights, drilldowns

# This creates the database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Talent Dashboard API",
    description="API for the Talent Dashboard.",
    version="1.0.0",
)

# --- CORS Configuration ---
# This allows your frontend to communicate with your backend
origins = [
    "http://localhost:5173", # For local SvelteKit dev
    # CORRECTED: Added your live frontend URL to allow requests
    "https://frontend-44a0.onrender.com"
]

# Allows adding another production URL via an environment variable for flexibility
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in origins:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Routers ---
# Each router is included with its specific prefix based on the API design.
# This prevents path conflicts and organizes the API correctly.
app.include_router(summary.router, prefix="/api/v1", tags=["Summaries"])
app.include_router(hiring.router, prefix="/api/v1", tags=["Hiring Data & KPIs"])
app.include_router(insights.router, prefix="/api/v1", tags=["AI Insights"])
app.include_router(drilldowns.router, prefix="/api/v1/kpis/drilldown", tags=["KPI Drilldowns"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Talent Dashboard API"}

# FILE: backend/routers/summary.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# CORRECTED: Removed the leading dots from imports
import crud
import schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.BusinessSummary])
def read_summaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    summaries = crud.get_all_business_summaries(db, skip=skip, limit=limit)
    return summaries

@router.get("/{business_group}", response_model=List[schemas.BusinessSummary])
def read_summaries_by_business_group(business_group: str, db: Session = Depends(get_db)):
    summaries = crud.get_summaries_by_business_group(db, business_group=business_group)
    return summaries

# FILE: backend/routers/hiring.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

# CORRECTED: Removed the leading dots from imports
import crud
import schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Hiring])
def read_hiring_data(
    skip: int = 0,
    limit: int = 100,
    business_group: Optional[str] = None,
    function: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    hiring_data = crud.get_hiring_data(
        db,
        skip=skip,
        limit=limit,
        business_group=business_group,
        function=function,
        start_date=start_date,
        end_date=end_date
    )
    return hiring_data

@router.get("/filters/business-groups", response_model=List[str])
def get_business_groups(db: Session = Depends(get_db)):
    return crud.get_unique_business_groups(db)

@router.get("/filters/functions", response_model=List[str])
def get_functions(db: Session = Depends(get_db)):
    return crud.get_unique_functions(db)

@router.get("/kpis/averages/", response_model=schemas.KpiAverages)
def get_kpi_averages(
    business_group: Optional[str] = None,
    function: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return crud.get_kpi_aggregates(
        db,
        business_group=business_group,
        function=function,
        start_date=start_date,
        end_date=end_date
    )

# FILE: backend/routers/insights.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

# CORRECTED: Removed the leading dots from imports
import analysis
import schemas
from database import get_db

router = APIRouter()

@router.get("/deep-dive/", response_model=schemas.AI_Insight)
def get_deep_dive_insights(
    business_group: Optional[str] = None,
    function: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    insights = analysis.generate_deep_dive_insights(
        db=db,
        business_group=business_group,
        function=function,
        start_date=start_date,
        end_date=end_date
    )
    return {"insights": insights}

# FILE: backend/routers/drilldowns.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

# CORRECTED: Removed the leading dots from imports
import drilldown_crud as crud
import drilldown_schemas as schemas
from database import get_db

router = APIRouter()

SUPPORTED_KPIS = [
    "time_to_fill", "cost_per_hire", "diversity_rate",
    "ijp_adherence_rate", "build_rate", "total_hires"
]

@router.get("/{kpi_name}", response_model=schemas.KpiDrilldownResponse)
def get_kpi_drilldown(
    kpi_name: str,
    business_group: Optional[str] = None,
    function: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if kpi_name not in SUPPORTED_KPIS:
        raise HTTPException(status_code=404, detail="KPI not supported")

    response = crud.get_drilldown_data(
        db=db,
        kpi_name=kpi_name,
        business_group=business_group,
        function=function
    )
    return response
