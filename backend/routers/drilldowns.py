from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import drilldown_crud as crud
from .. import drilldown_schemas as schemas
from ..drilldown_llm_utils import get_kpi_specific_insights

router = APIRouter()

@router.get("/{kpi_name}", response_model=schemas.KpiDrilldownResponse)
def get_kpi_drilldown(
    kpi_name: str,
    business_group: str | None = None,
    function: str | None = None,
    db: Session = Depends(get_db)
):
    summary_data = crud.get_summary_data(db, business_group, function)
    # The total_hires count is now part of the main response, not fetched separately here.
    kpi_title = kpi_name.replace('_', ' ').title()
    
    # The logic now correctly calls the right function for each KPI
    if kpi_name == "time_to_fill":
        trend_data_raw = crud.get_time_to_fill_trend(db, business_group, function)
        breakdown_data_raw = crud.get_time_to_fill_breakdown(db, business_group, function)
        breakdown_title = "Function" if not function else "Business Group"
        unit = "days"
    elif kpi_name == "cost_per_hire":
        trend_data_raw = crud.get_cost_per_hire_trend(db, business_group, function)
        breakdown_data_raw = crud.get_cost_per_hire_breakdown(db, business_group, function)
        breakdown_title = "Source"
        unit = "cost"
    elif kpi_name == "diversity_rate":
        trend_data_raw = crud.get_diversity_rate_trend(db, business_group, function)
        breakdown_data_raw = crud.get_diversity_rate_breakdown(db, business_group, function)
        breakdown_title = "Function" if not function else "Business Group"
        unit = "%"
    elif kpi_name == "ijp_adherence_rate":
        trend_data_raw = crud.get_ijp_adherence_rate_trend(db, business_group, function)
        breakdown_data_raw = crud.get_ijp_adherence_rate_breakdown(db, business_group, function)
        breakdown_title = "Function" if not function else "Business Group"
        unit = "%"
    elif kpi_name == "build_rate":
        trend_data_raw = crud.get_build_rate_trend(db, business_group, function)
        breakdown_data_raw = crud.get_build_rate_breakdown(db, business_group, function)
        breakdown_title = "Function" if not function else "Business Group"
        unit = "%"
    # --- THIS IS THE NEW LOGIC FOR THE TOTAL HIRES KPI ---
    elif kpi_name == "total_hires":
        trend_data_raw = crud.get_total_hires_trend(db, business_group, function)
        breakdown_data_raw = crud.get_total_hires_breakdown(db, business_group, function)
        breakdown_title = "Function" if not function else "Business Group"
        unit = "hires" # A new unit for formatting
    else:
        raise HTTPException(status_code=404, detail=f"KPI '{kpi_name}' not found.")

    # We get the overall total hires count to display on the page
    total_hires_for_selection = sum(row.value for row in breakdown_data_raw if row.value)

    trend_data = [row for row in trend_data_raw if row.value is not None]
    breakdown_data = [row for row in breakdown_data_raw if row.value is not None]

    prompt_text = (
        f"Data for '{kpi_title}' KPI on a selection of {total_hires_for_selection} hires.\n\n"
        f"Monthly Trend:\n{', '.join([f'{row.label}: {row.value:.2f}' for row in trend_data])}\n\n"
        f"Breakdown by {breakdown_title}:\n{', '.join([f'{row.label}: {row.value:.2f}' for row in breakdown_data])}"
    )

    llm_response = get_kpi_specific_insights(prompt_text, kpi_title)

    # The formatting logic now handles the new 'hires' unit
    formatted_trend = [{"label": row.label, "value": round(row.value * 100) if unit == "%" else round(row.value)} for row in trend_data]
    formatted_breakdown = [{"label": row.label, "value": round(row.value * 100) if unit == "%" else round(row.value)} for row in breakdown_data]
    
    return {
        "summary_data": summary_data,
        "total_hires": total_hires_for_selection, # Use the calculated total for the filtered view
        "trend_chart_data": formatted_trend,
        "breakdown_chart_data": formatted_breakdown,
        "ai_insights": {"insights": llm_response}
    }