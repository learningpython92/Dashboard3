# backend/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import List

class BusinessSummary(BaseModel):
    id: int
    business_group: str
    function: str
    total_headcount: int
    available_headcount: int
    gap: int
    class Config:
        from_attributes = True

class Hiring(BaseModel):
    id: int
    business_group: str
    function: str
    role_title: str
    hire_date: date
    cost_per_hire: int
    time_to_fill: int
    ijp_adherence: bool
    build_buy_ratio: str
    diversity_ratio: bool
    source: str
    class Config:
        from_attributes = True

class KpiAverages(BaseModel):
    avg_time_to_fill: int
    avg_cost_per_hire: int
    ijp_adherence_rate: int
    build_buy_rate: int
    diversity_hire_rate: int
    total_hires: int
    class Config:
        from_attributes = True

class InsightCard(BaseModel):
    title: str
    description: str

class AI_Insight(BaseModel):
    insights: List[InsightCard]