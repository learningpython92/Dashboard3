from pydantic import BaseModel
from typing import List

# We import the schemas we want to reuse from our core schemas file.
# This avoids code duplication and keeps our data structures consistent.
from .schemas import AI_Insight, BusinessSummary

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