# backend/routers/hiring.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    tags=["Hiring Data & KPIs"]
)

@router.get("/hirings/", response_model=List[schemas.Hiring])
def read_filtered_hirings(
    skip: int = 0,
    limit: int = 100,
    business_group: str | None = None,
    function: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve detailed hiring records with optional filters.
    """
    hirings = crud.get_filtered_hirings(db, skip=skip, limit=limit, business_group=business_group, function=function, start_date=start_date, end_date=end_date)
    return hirings

@router.get("/filters/business-groups", response_model=List[str])
def get_business_groups(db: Session = Depends(get_db)):
    """
    Get a unique list of all business groups to populate UI filters.
    """
    return crud.get_unique_business_groups(db)

@router.get("/filters/functions", response_model=List[str])
def get_functions(db: Session = Depends(get_db)):
    """
    Get a unique list of all functions to populate UI filters.
    """
    return crud.get_unique_functions(db)

@router.get("/kpis/averages/", response_model=schemas.KpiAverages)
def get_average_kpis(
    business_group: str | None = None,
    function: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    """
    Get aggregated KPIs, such as averages for cost and time, and rates for others.
    """
    aggregates = crud.get_kpi_aggregates(
        db,
        business_group=business_group,
        function=function,
        start_date=start_date,
        end_date=end_date
    )
    return aggregates