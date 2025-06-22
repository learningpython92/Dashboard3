import os
import json
from openai import OpenAI
from typing import List, Dict, Union

def get_kpi_specific_insights(analysis_text: str, kpi_name: str) -> Union[List[Dict[str, str]], Dict]:
    """
    Sends KPI-specific data to an LLM and gets a structured JSON response
    containing two detailed, actionable insights for two cards.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return [{"title": "Configuration Error", "description": "OPENAI_API_KEY not found."}]

    try:
        client = OpenAI(api_key=api_key)
        
        # This prompt is now specialized for generating two "critical action" cards.
        system_prompt = f"""
        You are an expert HR strategist analyzing data for a specific KPI: '{kpi_name}'.
        Your task is to generate exactly two distinct and meaningful insights based on the provided data summary.
        These insights will be displayed on two separate cards in an executive dashboard.

        For each insight, you MUST provide:
        1. A "title": A short, impactful headline (3-5 words) that summarizes the core finding.
        2. A "description": A detailed explanation of 2-3 sentences that analyzes the data and suggests a critical, actionable recommendation for business leaders.

        You MUST explicitly mention the KPI '{kpi_name}' in your descriptions to keep the insights focused. Also, call out the business and function wherever appropriate. 
        You MUST format your entire response as a single, valid JSON array containing exactly two objects.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": analysis_text}
            ],
            temperature=0.7, # Slightly higher for more creative action-oriented text
            max_tokens=1000,
        )
        
        raw_response_content = response.choices[0].message.content
        
        # This robustly handles the case where the AI might wrap the list in a key
        parsed_json = json.loads(raw_response_content)
        if isinstance(parsed_json, dict) and len(parsed_json.keys()) == 1:
            return list(parsed_json.values())[0]
        
        return parsed_json

    except Exception as e:
        print(f"❌ Drilldown LLM Error: {e}")
        return [{"title": "AI Communication Error", "description": "There was an issue generating insights."}]