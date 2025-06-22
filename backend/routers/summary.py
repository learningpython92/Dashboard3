# backend/routers/summary.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/summaries",
    tags=["Summaries"]
)

@router.get("/", response_model=List[schemas.BusinessSummary])
def read_all_summaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all high-level business summary records.
    """
    summaries = crud.get_all_business_summaries(db, skip=skip, limit=limit)
    return summaries

@router.get("/{business_group}", response_model=List[schemas.BusinessSummary])
def read_summary_for_business_group(business_group: str, db: Session = Depends(get_db)):
    """
    Retrieve all summary records for a specific business group,
    including the 'Overall' and function-specific summaries.
    """
    summaries = crud.get_summary_by_business_group(db, business_group=business_group)
    return summaries