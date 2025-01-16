import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Data for campaigns
campaigns = [
    {
        "name": "Access Group",
        "weeklyTarget": 9,
        "cumulativeTarget": 100,
        "Till 10th Jan": 60,
        "weeks": [
            {"week": 1, "focus": "3 emails/week + LinkedIn", "target": 55, "actual": 60},
            {"week": 2, "focus": "3 emails/week + LinkedIn", "target": 9, "actual": 4},
            {"week": 3, "focus": "3 emails/week + LinkedIn", "target": 9, "actual": 0},
            {"week": 4, "focus": "3 emails/week + LinkedIn", "target": 9, "actual": 0},
            {"week": 5, "focus": "Analysis & refinement", "target": 9, "actual": 0},
            {"week": 6, "focus": "Final push", "target": 9, "actual": 0},
        ]
    },
    {
        "name": "HSBC",
        "weeklyTarget": 7,
        "cumulativeTarget": 45,
        "Till 10th Jan": 18,
        "weeks": [
            {"week": 1, "focus": "3 emails/week + LinkedIn", "target": 10, "actual": 18},
            {"week": 2, "focus": "3 emails/week + LinkedIn", "target": 7, "actual": 7},
            {"week": 3, "focus": "3 emails/week + LinkedIn", "target": 7, "actual": 0},
            {"week": 4, "focus": "3 emails/week + LinkedIn", "target": 7, "actual": 0},
            {"week": 5, "focus": "Analysis & refinement", "target": 7, "actual": 0},
            {"week": 6, "focus": "Final push", "target": 7, "actual": 0},
        ]
    },
     {
        "name": "Quickbooks",
        "weeklyTarget": 7,
        "cumulativeTarget": 100,
        "Till 10th Jan": 44,
        "weeks": [
            {"week": 1, "focus": "3 emails/week + LinkedIn", "target": 55, "actual": 44},
            {"week": 2, "focus": "3 emails/week + LinkedIn", "target": 9, "actual": 7},
            {"week": 3, "focus": "3 emails/week + LinkedIn", "target": 9, "actual": 0},
            {"week": 4, "focus": "3 emails/week + LinkedIn", "target": 9, "actual": 0},
            {"week": 5, "focus": "Analysis & refinement", "target": 9, "actual": 0},
            {"week": 6, "focus": "Final push", "target": 9, "actual": 0},
        ]
    },
]

# Streamlit app
st.title("Campaign Progress Tracker (Jan 15 - Mar 15)")

# Sidebar for selecting campaigns
campaign_names = [campaign['name'] for campaign in campaigns]
selected_campaign_name = st.sidebar.selectbox("Select a campaign", campaign_names)

selected_campaign = next(campaign for campaign in campaigns if campaign["name"] == selected_campaign_name)

# Date range calculation
def create_date_range(week_number):
    if week_number == 1:
        return "Till 10th Jan"  # Fixed focus for Week 1
    else:
        # Calculate Monday and Friday for subsequent weeks
        offset_days = (week_number - 2) * 7
        start_date = datetime(2025, 1, 13) + timedelta(days=offset_days)  # Monday of the week
        end_date = start_date + timedelta(days=4)  # Friday of the week
        return f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}"

# Data preparation for charts
data = []
for week in selected_campaign["weeks"]:
    date_range = create_date_range(week["week"])
    data.append({
        "Week": week["week"],
        "Date Range": date_range,
        "Focus": week["focus"],
        "Target": week["target"],
        "Actual": week["actual"],
        "Progress": f"{(week['actual'] / week['target'] * 100):.2f}%" if week["target"] > 0 else "N/A"
    })

df = pd.DataFrame(data)

# Display summary
def calculate_progress(weeks):
    actual = sum(week["actual"] for week in weeks)
    target = sum(week["target"] for week in weeks)
    return actual, target

actual, target = calculate_progress(selected_campaign["weeks"])
st.markdown(f"### {selected_campaign_name}")
st.write(f"Weekly Target: {selected_campaign['weeklyTarget']} | Progress: {actual}/{target}")

# Line chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Week"], y=df["Target"], mode='lines+markers', name='Target', line=dict(color='blue')
))
fig.add_trace(go.Scatter(
    x=df["Week"], y=df["Actual"], mode='lines+markers', name='Actual', line=dict(color='green')
))
fig.update_layout(
    title="Campaign Progress",
    xaxis_title="Week",
    yaxis_title="Value",
    legend_title="Legend",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# Table of details
st.markdown("#### Weekly Details")
st.dataframe(df)

# Additional information
st.info("Weekly actions: Stand-ups (Mon, Wed, Fri), Email outreach, LinkedIn engagement, Apollo lead scraping. Review metrics every Friday (RAG Review).")
