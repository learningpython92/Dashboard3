from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, cast, Float, case
from datetime import date
import models
import schemas

# === BusinessSummary CRUD Functions ===

def get_all_business_summaries(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all business summary records with pagination.
    """
    return db.query(models.BusinessSummary).offset(skip).limit(limit).all()

def get_summaries_by_business_group(db: Session, business_group: str):
    """
    Retrieve all summary records for a specific business group.
    Note: The original file had a different function name here, this one aligns with the router.
    """
    return db.query(models.BusinessSummary).filter(models.BusinessSummary.business_group == business_group).all()


# === Hiring CRUD Functions ===

def get_filtered_hirings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    business_group: str | None = None,
    function: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    """
    Retrieve hiring records with dynamic filters and pagination.
    """
    query = db.query(models.Hiring)

    if business_group:
        query = query.filter(models.Hiring.business_group == business_group)
    if function:
        query = query.filter(models.Hiring.function == function)
    if start_date:
        query = query.filter(models.Hiring.hire_date >= start_date)
    if end_date:
        query = query.filter(models.Hiring.hire_date <= end_date)

    return query.offset(skip).limit(limit).all()


# === Functions for UI Filters ===

def get_unique_business_groups(db: Session):
    """
    Get a list of unique business groups to populate UI filters.
    """
    results = db.query(distinct(models.Hiring.business_group)).all()
    return [result[0] for result in results]

def get_unique_functions(db: Session):
    """
    Get a list of unique functions to populate UI filters.
    """
    results = db.query(distinct(models.Hiring.function)).all()
    return [result[0] for result in results]


# === KPI Aggregation Function ===

def get_kpi_aggregates(
    db: Session,
    business_group: str | None = None,
    function: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    """
    Calculates and formats aggregate KPIs based on the provided filters.
    """
    query = db.query(
        func.avg(models.Hiring.time_to_fill).label("avg_time_to_fill"),
        func.avg(models.Hiring.cost_per_hire).label("avg_cost_per_hire"),
        func.avg(cast(models.Hiring.ijp_adherence, Float)).label("ijp_adherence_rate"),
        func.avg(
            case(
                (models.Hiring.build_buy_ratio == 'Build', 1),
                else_=0
            )
        ).label("build_buy_rate"),
        func.avg(
            case(
                (models.Hiring.diversity_ratio == True, 1),
                else_=0
            )
        ).label("diversity_hire_rate"),
        func.count(models.Hiring.id).label("total_hires")
    )

    if business_group:
        query = query.filter(models.Hiring.business_group == business_group)
    if function:
        query = query.filter(models.Hiring.function == function)
    if start_date:
        query = query.filter(models.Hiring.hire_date >= start_date)
    if end_date:
        query = query.filter(models.Hiring.hire_date <= end_date)

    raw_results = query.first()

    if raw_results and raw_results.total_hires > 0:
        # We have valid results, so we format them into a clean dictionary.
        return {
            "avg_time_to_fill": round(raw_results.avg_time_to_fill or 0),
            "avg_cost_per_hire": round(raw_results.avg_cost_per_hire or 0),
            "ijp_adherence_rate": round((raw_results.ijp_adherence_rate or 0) * 100),
            "build_buy_rate": round((raw_results.build_buy_rate or 0) * 100),
            "diversity_hire_rate": round((raw_results.diversity_hire_rate or 0) * 100),
            "total_hires": raw_results.total_hires,
        }
    else:
        # No results found, return a default dictionary of clean integers.
        return {
            "avg_time_to_fill": 0,
            "avg_cost_per_hire": 0,
            "ijp_adherence_rate": 0,
            "build_buy_rate": 0,
            "diversity_hire_rate": 0,
            "total_hires": 0,
        }
