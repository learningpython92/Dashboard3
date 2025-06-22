# backend/llm_utils.py

import os
import json
from openai import OpenAI
from typing import List, Dict, Union

def get_insights_from_llm(analysis_text: str) -> Union[List[Dict[str, str]], Dict]:
    """
    Sends the data analysis text to an LLM and gets a structured JSON response
    containing three detailed insights, each with a title and description.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return [{"title": "Configuration Error", "description": "OPENAI_API_KEY not found. Please set it in the .env file."}]

    try:
        client = OpenAI(api_key=api_key)
        system_prompt = """
        You are an expert HR strategist and data analyst reviewing a hiring performance report. 
        Your task is to generate exactly three distinct and detailed insights from the provided data summary. Make sure to call out businesses and functions wherever appropriate for the insights. Please note that Energy, FMCG, Tech, Media are businesses.

        For each insight, you MUST provide:
        1. A "title": A short, catchy headline (3-5 words).
        2. A "description": A detailed explanation of 2-3 sentences that elaborates on the 'what', 'why', and potential 'so what' of the insight.

        You MUST format your entire response as a single, valid JSON array of objects, with no other text before or after the array.

        Example of required JSON structure:
        [
          {
            "title": "Insight Title 1",
            "description": "Detailed explanation for the first insight..."
          },
          {
            "title": "Insight Title 2",
            "description": "Detailed explanation for the second insight..."
          },
          {
            "title": "Insight Title 3",
            "description": "Detailed explanation for the third insight..."
          }
        ]
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": analysis_text}
            ],
            temperature=0.6,
            max_tokens=500,
        )
        
        raw_response_content = response.choices[0].message.content
        
        # --- DEBUGGING PRINT ---
        print("--- RAW LLM RESPONSE ---")
        print(raw_response_content)
        print("------------------------")
        
        return json.loads(raw_response_content)

    except Exception as e:
        print(f"❌ LLM API Error: {e}")
        return [{"title": "AI Error", "description": f"Error communicating with the AI model: {e}"}]