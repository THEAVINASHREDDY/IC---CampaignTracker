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
            {"week": 1, "focus": "Till 10th Jan", "target": 55, "actual": 60},
            {"week": 2, "focus": "3 emails/week + LinkedIn (13th - 17th Jan)", "target": 9, "actual": 4},
            {"week": 3, "focus": "3 emails/week + LinkedIn (20th - 24th Jan)", "target": 9, "actual": 0},
            {"week": 4, "focus": "3 emails/week + LinkedIn (27th - 31st Jan)", "target": 9, "actual": 0},
            {"week": 5, "focus": "Analysis & refinement (3rd - 7th Feb)", "target": 9, "actual": 0},
            {"week": 6, "focus": "Final push (10th - 14th Feb)", "target": 9, "actual": 0},
        ]
    },
    # Add other campaigns as needed
]

# Streamlit app
st.title("Campaign Progress Tracker (Jan 15 - Mar 15)")

# Sidebar for selecting campaigns
campaign_names = [campaign["name"] for campaign in campaigns]
selected_campaign_name = st.sidebar.selectbox("Select a campaign", campaign_names)
selected_campaign = next(campaign for campaign in campaigns if campaign["name"] == selected_campaign_name)

# Function to calculate progress
def calculate_progress(weeks):
    actual = sum(week["actual"] for week in weeks)
    target = sum(week["target"] for week in weeks)
    return actual, target

# Function to create date ranges based on custom logic
def create_date_range(week_number):
    if week_number == 1:
        start_date = datetime(2025, 1, 1)  # Start of January
        end_date = datetime(2025, 1, 10)  # Till 10th January
    else:
        # Calculate Monday and Friday for subsequent weeks
        days_offset = 10 + (week_number - 2) * 7  # Offset from 10th January
        start_date = datetime(2025, 1, 10) + timedelta(days=days_offset)  # Monday of the week
        end_date = start_date + timedelta(days=4)  # Friday of the week
    return start_date.strftime("%b %d"), end_date.strftime("%b %d")

# Data preparation for charts
data = []
for week in selected_campaign["weeks"]:
    start_date, end_date = create_date_range(week["week"])
    data.append({
        "Week": week["week"],
        "Date Range": f"{start_date} - {end_date}",
        "Focus": week["focus"],
        "Target": week["target"],
        "Actual": week["actual"],
        "Progress": f"{(week['actual'] / week['target'] * 100):.2f}%" if week["target"] > 0 else "N/A"
    })

df = pd.DataFrame(data)

# Display summary
actual, target = calculate_progress(selected_campaign["weeks"])
st.markdown(f"### {selected_campaign_name}")
st.write(f"Weekly Target: {selected_campaign['weeklyTarget']} | Progress: {actual}/{target}")

# Line chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Week"], y=df["Target"], mode='lines+markers', name="Target", line=dict(color="blue")
))
fig.add_trace(go.Scatter(
    x=df["Week"], y=df["Actual"], mode='lines+markers', name="Actual", line=dict(color="green")
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
