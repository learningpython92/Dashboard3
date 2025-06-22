# backend/routers/summary.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# CORRECTED: Using absolute imports instead of relative ones.
import crud
import schemas
from database import get_db

router = APIRouter()

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
    # Note: The original file called a function `get_summary_by_business_group`.
    # Based on your `crud.py` file, the correct function name is `get_summaries_by_business_group`.
    # I am assuming this is a typo in the provided file and using the name from your crud.py.
    # If a different function is intended, please provide the `crud.py` content.
    summaries = crud.get_summaries_by_business_group(db, business_group=business_group)
    return summaries
