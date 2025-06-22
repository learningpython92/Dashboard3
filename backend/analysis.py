# backend/analysis.py

import pandas as pd
import numpy as np
from scipy.stats import linregress, zscore
from datetime import datetime

def generate_deep_insights(hirings_df: pd.DataFrame, summaries_df: pd.DataFrame) -> list:
    """
    Takes pre-filtered DataFrames and performs the deep analysis,
    returning a list of insight dictionaries.
    """
    # This function contains the exact analysis logic from your script,
    # but it operates on the DataFrames passed to it as arguments.

    if hirings_df.empty:
        return []

    results = []
    
    # Loop over the pre-filtered data
    for (biz, func), df in hirings_df.groupby(["business_group", "function"]):
        try:
            df = df.copy()
            summary = summaries_df[(summaries_df["business_group"] == biz) & (summaries_df["function"] == func)]

            # ---------------- LEVEL 1 ----------------
            level1 = {
                "Total Hires": len(df),
                "Avg Time to Fill": round(df["time_to_fill"].mean(), 1),
                "Avg Cost/Hire": round(df["cost_per_hire"].mean(), 1),
                "Build %": f"{(df['build_buy_ratio'] == 'Build').mean():.1%}",
                "IJP %": f"{df['ijp_adherence'].mean():.1%}",
                "Diversity %": f"{df['diversity_ratio'].mean():.1%}",
                "Top Sources": ", ".join(df["source"].value_counts().head(2).index.tolist())
            }

            # ---------------- LEVEL 2 ----------------
            hires = len(df)
            gap = summary["gap"].values[0] if not summary.empty else None
            coverage = hires / (gap + 1) if gap is not None and (gap + 1) != 0 else None
            monthly_hires = df["hire_date"].dt.month.value_counts().sort_index()
            stagnant_months = 12 - monthly_hires.count()
            avg_cost_by_source = df.groupby("source")["cost_per_hire"].mean()
            top_source = df["source"].value_counts().idxmax()
            cost_efficiency = (
                "⚠️ Top source has high cost"
                if avg_cost_by_source[top_source] > df["cost_per_hire"].mean()
                else "✅ Top source is cost-efficient"
            )
            level2 = {
                "Headcount Gap": gap if gap is not None else "N/A",
                "Coverage %": round(coverage * 100, 1) if coverage is not None else "N/A",
                "Hiring Months": monthly_hires.count(),
                "Stagnant Months": stagnant_months,
                "Top Source Cost-Efficiency": cost_efficiency,
            }

            # ---------------- LEVEL 3 ----------------
            level3 = []
            df["days"] = (df["hire_date"] - df["hire_date"].min()).dt.days
            if df["days"].nunique() > 10 and df['time_to_fill'].nunique() > 1:
                slope, _, _, p, _ = linregress(df["days"], df["time_to_fill"])
                if p < 0.05 and slope > 0:
                    level3.append(f"📈 Time to Fill rising by {round(slope, 2)} days/month (p={round(p, 4)})")
            if not df.empty:
                roi = df.groupby("source").agg({ "cost_per_hire": "mean", "time_to_fill": "mean", "diversity_ratio": "mean" }).sort_values(by="cost_per_hire", ascending=False)
                worst = roi.head(1)
                if not worst.empty:
                    level3.append(f"💸 Source '{worst.index[0]}' has high cost (₹{int(worst['cost_per_hire'].values[0])}) and diversity: {worst['diversity_ratio'].values[0]:.1%}")
            if len(df) > 10 and df['cost_per_hire'].nunique() > 1:
                df["cost_z"] = zscore(df["cost_per_hire"])
                extreme = df[df["cost_z"] > 2]
                if not extreme.empty:
                    level3.append(f"💣 {len(extreme)} cost outlier(s) detected (Z > 2)")
            build_ratio = (df["build_buy_ratio"] == "Build").mean()
            if build_ratio < 0.25 or build_ratio > 0.75:
                level3.append(f"🔀 Build/Buy imbalance: {build_ratio:.1%}")
            div_ratio = df["diversity_ratio"].mean()
            if div_ratio < 0.15 or div_ratio > 0.85:
                level3.append(f"🧬 Diversity outlier: {div_ratio:.1%}")

            results.append({
                "Business": biz, "Function": func,
                "Level_1_KPIs": "\n".join([f"{k}: {v}" for k, v in level1.items()]),
                "Level_2_Operational": "\n".join([f"{k}: {v}" for k, v in level2.items()]),
                "Level_3_Deep_Insights": "\n".join(level3) if level3 else "No deep signals"
            })
        except Exception as e:
            # If a group fails, we can add a record to show the error
            results.append({
                "Business": biz, "Function": func,
                "Level_1_KPIs": "Error during analysis.",
                "Level_2_Operational": f"Error: {e}",
                "Level_3_Deep_Insights": "Skipping due to error."
            })

    return results