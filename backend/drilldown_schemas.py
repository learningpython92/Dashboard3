# backend/drilldown_schemas.py

from pydantic import BaseModel
from typing import List

# CORRECTED: Changed the relative import 'from .schemas' to an absolute import 'from schemas'.
# This allows the server to correctly locate the file during deployment.
from schemas import AI_Insight, BusinessSummary

class DrilldownChartDataPoint(BaseModel):
    # This is a generic structure for our chart data.
    # 'label' can be a month ("2025-01") or a category ("Tech").
    # 'value' is the calculated number for that label.
    label: str
    value: float # We keep it as float here for precision; rounding happens in the router.

# This is the main response model that defines the entire package of data
# for any KPI drill-down page.
class KpiDrilldownResponse(BaseModel):
    summary_data: List[BusinessSummary]
    trend_chart_data: List[DrilldownChartDataPoint]
    breakdown_chart_data: List[DrilldownChartDataPoint]
    ai_insights: AI_Insight
    # Added total_hires to the schema to match the data being returned by the router.
    total_hires: int
