from sqlalchemy.orm import Session, Query
from sqlalchemy import func, cast, Float
from . import models

def _apply_filters(query: Query, model, business_group: str | None, function: str | None) -> Query:
    """Helper function to apply common filters (business_group and function)."""
    if business_group:
        query = query.filter(model.business_group == business_group)
    if function:
        query = query.filter(model.function == function)
    return query

def get_summary_data(db: Session, business_group: str | None, function: str | None):
    """Gets the headcount summary data for the provided filters."""
    query = db.query(models.BusinessSummary)
    if business_group:
        if function:
            query = query.filter(
                (models.BusinessSummary.business_group == business_group) &
                ((models.BusinessSummary.function == function) | (models.BusinessSummary.function == 'Overall'))
            )
        else:
            query = query.filter(models.BusinessSummary.business_group == business_group)
    elif function:
        query = query.filter(models.BusinessSummary.function == function)
    return query.all()

# --- EXPLICIT, HARDCODED FUNCTIONS FOR EACH KPI DRILL-DOWN ---

# --- Time to Fill ---
def get_time_to_fill_trend(db: Session, bg: str | None, fn: str | None):
    q = db.query(
        func.strftime("%Y-%m", models.Hiring.hire_date).label("label"),
        func.avg(models.Hiring.time_to_fill).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by("label").all()

def get_time_to_fill_breakdown(db: Session, bg: str | None, fn: str | None):
    breakdown_col = models.Hiring.business_group if fn else models.Hiring.function
    q = db.query(
        breakdown_col.label("label"),
        func.avg(models.Hiring.time_to_fill).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by(func.avg(models.Hiring.time_to_fill).desc()).all()

# --- Cost per Hire ---
def get_cost_per_hire_trend(db: Session, bg: str | None, fn: str | None):
    q = db.query(
        func.strftime("%Y-%m", models.Hiring.hire_date).label("label"),
        func.avg(models.Hiring.cost_per_hire).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by("label").all()

def get_cost_per_hire_breakdown(db: Session, bg: str | None, fn: str | None):
    q = db.query(
        models.Hiring.source.label("label"),
        func.avg(models.Hiring.cost_per_hire).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by(func.avg(models.Hiring.cost_per_hire).desc()).all()

# --- Diversity Rate ---
def get_diversity_rate_trend(db: Session, bg: str | None, fn: str | None):
    q = db.query(
        func.strftime("%Y-%m", models.Hiring.hire_date).label("label"),
        func.avg(cast(models.Hiring.diversity_ratio, Float)).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by("label").all()

def get_diversity_rate_breakdown(db: Session, bg: str | None, fn: str | None):
    breakdown_col = models.Hiring.business_group if fn else models.Hiring.function
    q = db.query(
        breakdown_col.label("label"),
        func.avg(cast(models.Hiring.diversity_ratio, Float)).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by(func.avg(cast(models.Hiring.diversity_ratio, Float)).desc()).all()

# --- IJP Adherence Rate ---
def get_ijp_adherence_rate_trend(db: Session, bg: str | None, fn: str | None):
    q = db.query(
        func.strftime("%Y-%m", models.Hiring.hire_date).label("label"),
        func.avg(cast(models.Hiring.ijp_adherence, Float)).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by("label").all()

def get_ijp_adherence_rate_breakdown(db: Session, bg: str | None, fn: str | None):
    breakdown_col = models.Hiring.business_group if fn else models.Hiring.function
    q = db.query(
        breakdown_col.label("label"),
        func.avg(cast(models.Hiring.ijp_adherence, Float)).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by(func.avg(cast(models.Hiring.ijp_adherence, Float)).desc()).all()

# --- Build Rate ---
def get_build_rate_trend(db: Session, bg: str | None, fn: str | None):
    q = db.query(
        func.strftime("%Y-%m", models.Hiring.hire_date).label("label"),
        func.avg(cast(models.Hiring.build_buy_ratio == 'Build', Float)).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by("label").all()

def get_build_rate_breakdown(db: Session, bg: str | None, fn: str | None):
    breakdown_col = models.Hiring.business_group if fn else models.Hiring.function
    q = db.query(
        breakdown_col.label("label"),
        func.avg(cast(models.Hiring.build_buy_ratio == 'Build', Float)).label("value")
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by(func.avg(cast(models.Hiring.build_buy_ratio == 'Build', Float)).desc()).all()

# --- Total Hires (The New KPI) ---
def get_total_hires_trend(db: Session, bg: str | None, fn: str | None):
    """Calculates the month-over-month trend for the COUNT of hires."""
    q = db.query(
        func.strftime("%Y-%m", models.Hiring.hire_date).label("label"),
        func.count(models.Hiring.id).label("value") # <-- Using COUNT instead of AVG
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by("label").all()

def get_total_hires_breakdown(db: Session, bg: str | None, fn: str | None):
    """Calculates the breakdown of the COUNT of hires by another category."""
    breakdown_col = models.Hiring.business_group if fn else models.Hiring.function
    q = db.query(
        breakdown_col.label("label"),
        func.count(models.Hiring.id).label("value") # <-- Using COUNT instead of AVG
    )
    return _apply_filters(q, models.Hiring, bg, fn).group_by("label").order_by(func.count(models.Hiring.id).desc()).all()