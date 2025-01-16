import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Data for campaigns
campaigns = [
    {
        "name": "Access Group",
        "weeklyTarget": 10,
        "cumulativeTarget": 100,
        "weeks": [
            {"week": 1, "focus": "Till 15th Jan", "target": 0, "actual": 64},
            {"week": 2, "focus": "3 emails/week + LinkedIn (13th - 17th Jan)", "target": 10, "actual": 4},
            {"week": 3, "focus": "3 emails/week + LinkedIn (20th - 24th Jan)", "target": 10, "actual": 0},
            {"week": 4, "focus": "3 emails/week + LinkedIn (27th - 31st Jan)", "target": 10, "actual": 0},
            {"week": 5, "focus": "3 emails/week + LinkedIn (3rd - 7th Feb)", "target": 10, "actual": 0},
            {"week": 6, "focus": "3 emails/week + LinkedIn (10th - 14th Feb)", "target": 10, "actual": 0},
            {"week": 7, "focus": "Analysis & refinement (17th - 21st Feb)", "target": 10, "actual": 0},
            {"week": 8, "focus": "Final push (24th - 28th Feb)", "target": 10, "actual": 0}
        ]
    },
    {
        "name": "HSBC",
        "weeklyTarget": 6,
        "cumulativeTarget": 36,
        "weeks": [
            {"week": 1, "focus": "Expand data pot", "target": 0, "actual": 0},
            {"week": 2, "focus": "LinkedIn outreach", "target": 0, "actual": 0},
            {"week": 3, "focus": "2-3 emails/week", "target": 6, "actual": 0},
            {"week": 4, "focus": "2-3 emails/week", "target": 6, "actual": 0},
            {"week": 5, "focus": "2-3 emails/week", "target": 6, "actual": 0},
            {"week": 6, "focus": "2-3 emails/week", "target": 6, "actual": 0},
            {"week": 7, "focus": "Analysis & refinement", "target": 6, "actual": 0},
            {"week": 8, "focus": "Final push", "target": 6, "actual": 0}
        ]
    },
    {
        "name": "Tieto",
        "weeklyTarget": 6,
        "cumulativeTarget": 36,
        "weeks": [
            {"week": 1, "focus": "Expand data pot", "target": 0, "actual": 0},
            {"week": 2, "focus": "LinkedIn outreach", "target": 0, "actual": 0},
            {"week": 3, "focus": "2-3 emails/week", "target": 6, "actual": 0},
            {"week": 4, "focus": "2-3 emails/week", "target": 6, "actual": 0},
            {"week": 5, "focus": "2-3 emails/week", "target": 6, "actual": 0},
            {"week": 6, "focus": "2-3 emails/week", "target": 6, "actual": 0},
            {"week": 7, "focus": "Analysis & refinement", "target": 6, "actual": 0},
            {"week": 8, "focus": "Final push", "target": 6, "actual": 0}
        ]
    }
    # Add other campaigns similarly
]

# Streamlit app
st.title("Campaign Progress Tracker (Jan 15 - Mar 15)")

# Sidebar for selecting campaigns
campaign_names = [campaign['name'] for campaign in campaigns]
selected_campaign_name = st.sidebar.selectbox("Select a campaign", campaign_names)

selected_campaign = next(campaign for campaign in campaigns if campaign["name"] == selected_campaign_name)

# Data preparation for charts
def calculate_progress(weeks):
    actual = sum(week["actual"] for week in weeks)
    target = sum(week["target"] for week in weeks)
    return actual, target

def create_date_range(week_number):
    start_date = datetime(2025, 1, 15) + timedelta(weeks=week_number - 1)
    end_date = start_date + timedelta(days=6)
    return start_date.strftime("%b %d"), end_date.strftime("%b %d")

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
week = campaigns[0]["weeks"][0]["focus"]
st.markdown(f"### {selected_campaign_name}")
st.write(f"Weekly Target: {selected_campaign['weeklyTarget']} |{week}:{actual}|Progress: {actual}/{target}")

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
