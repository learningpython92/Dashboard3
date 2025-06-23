# backend/routers/insights.py

import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import date

# CORRECTED: Changed relative 'from ..' imports to absolute imports
import schemas
import analysis
import llm_utils
from database import get_db

router = APIRouter(
    prefix="/insights",
    tags=["AI Insights"]
)

@router.get("inisights/deep-dive/", response_model=schemas.AI_Insight)
def get_ai_powered_insights(
    business_group: str | None = None,
    function: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    # Steps 1 & 2: Load and filter the data
    hirings_df = pd.read_sql_table("hirings", db.bind)
    summaries_df = pd.read_sql_table("business_summaries", db.bind)
    hirings_df["hire_date"] = pd.to_datetime(hirings_df["hire_date"])

    filtered_hirings = hirings_df.copy()
    if business_group:
        filtered_hirings = filtered_hirings[filtered_hirings["business_group"].str.lower() == business_group.lower()]
    if function:
        filtered_hirings = filtered_hirings[filtered_hirings["function"].str.lower() == function.lower()]
    if start_date:
        filtered_hirings = filtered_hirings[filtered_hirings["hire_date"].dt.date >= start_date]
    if end_date:
        filtered_hirings = filtered_hirings[filtered_hirings["hire_date"].dt.date <= end_date]
    
    # Step 3: Run the local Pandas analysis
    analysis_results = analysis.generate_deep_insights(filtered_hirings, summaries_df)
    
    if not analysis_results:
        return schemas.AI_Insight(insights=[{"title": "No Data Found", "description": "No hiring records match the specified filters."}])

    # Step 4: Format the analysis into a prompt
    prompt_text = "Here is the data summary:\n\n"
    for result in analysis_results:
        prompt_text += f"--- For {result['Business']} - {result['Function']} ---\n"
        prompt_text += f"KPIs:\n{result['Level_1_KPIs']}\n"
        prompt_text += f"Operational Data:\n{result['Level_2_Operational']}\n"
        prompt_text += f"Deeper Signals:\n{result['Level_3_Deep_Insights']}\n\n"

    # Step 5: Call the LLM
    llm_output = llm_utils.get_insights_from_llm(prompt_text)

    # This block robustly handles the LLM response.
    final_insights_list = []
    if isinstance(llm_output, dict) and 'insights' in llm_output:
        final_insights_list = llm_output['insights']
    elif isinstance(llm_output, list):
        final_insights_list = llm_output
    else:
        # Handle unexpected format
        final_insights_list = [{"title": "Formatting Error", "description": "The AI returned data in an unexpected format."}]

    # Step 6: Create the final response object and return it
    return schemas.AI_Insight(insights=final_insights_list)
