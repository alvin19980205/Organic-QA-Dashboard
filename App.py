import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta

st.set_page_config(layout="wide", page_title="Data QA Dashboard", page_icon="📊")

# --- 1. MOCK DATA GENERATOR (Replaces Snowflake) ---
# This ensures recruiters can run your app locally without needing database credentials.
@st.cache_data
def generate_mock_data():
    today = date.today()
    data = {
        "client": ["Brand A", "Brand A", "Brand A", "Brand B", "Brand B"],
        "platform": ["Instagram", "TikTok", "Instagram", "Facebook", "TikTok"],
        "post_date": [today, today - timedelta(days=2), today, today - timedelta(days=1), None],
        "api_feed_date": [today, today, None, today - timedelta(days=1), today],
        "asset_name": ["Summer Promo Vol 1", "Influencer Collab", "Story Update", "Ad Campaign B", "UGC Video"],
        "pm_tool_link": ["https://pm-tool.com/task/1", "https://pm-tool.com/task/2", "https://pm-tool.com/task/3", "https://pm-tool.com/task/4", None],
        "api_link": ["https://social.com/p/1", "https://social.com/p/2", None, "https://social.com/p/4", "https://social.com/p/5"],
        "null_fields": [None, None, "Campaign Name", None, None]
    }
    df = pd.DataFrame(data)
    
    # Simulate the SQL status logic
    conditions = [
        (df['post_date'].notna()) & (df['api_feed_date'].notna()) & (df['post_date'] != df['api_feed_date']),
        (df['post_date'].notna()) & (df['api_feed_date'].isna()),
        (df['post_date'].isna()) & (df['api_feed_date'].notna()),
        (df['null_fields'].notna())
    ]
    choices = ['Inconsistent Dates', 'Missing from API Feed', 'Missing from PM Tool', 'Field Error']
    df['Error Type'] = np.select(conditions, choices, default=None)
    
    return df

# --- 2. CUSTOM UI CSS (Retained from your original code) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background: #F7F6F3 !important;
}
.kpi-row { display: flex; gap: 12px; margin-bottom: 0.25rem; }
.kpi {
    flex: 1; background: #fff; border-radius: 10px;
    padding: 16px 20px; border: 1px solid #E5E2DC;
    border-top: 3px solid var(--c);
}
.kpi .lbl {
    font-size: 10px; font-weight: 600; letter-spacing: .08em;
    text-transform: uppercase; color: #999; margin-bottom: 6px;
}
.kpi .num {
    font-family: 'DM Mono', monospace; font-size: 28px;
    font-weight: 500; color: #1A1917; line-height: 1;
}
.kpi .sub { font-size: 11px; color: #BBB; margin-top: 5px; }
.section-title { font-size: 15px; font-weight: 600; color: #1A1917; margin-bottom: 0.75rem; }
</style>
""", unsafe_allow_html=True)

# --- 3. ERROR STYLING DICTIONARY ---
ERROR_STYLES = {
    "Missing from API Feed": {"color": "#EA4335", "bg": "#FEF2F2"},
    "Missing from PM Tool":   {"color": "#F97316", "bg": "#FFF7ED"},
    "Inconsistent Dates":     {"color": "#8B5CF6", "bg": "#F5F3FF"},
    "Field Error":            {"color": "#EC4899", "bg": "#FDF2F8"},
}

# --- 4. APP LOGIC ---
st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 0; margin-bottom: 20px;">
        <div style="width:32px;height:32px;background:#1A1917;border-radius:6px;
                    display:flex;align-items:center;justify-content:center">
            <span style="color:#fff;font-size:14px;font-weight:700">QA</span>
        </div>
        <div>
            <div style="font-size:16px;font-weight:700;color:#1A1917">Data Pipeline QA Dashboard</div>
            <div style="font-size:11px;color:#999">Project Management vs API Data Feed</div>
        </div>
    </div>
""", unsafe_allow_html=True)

df = generate_mock_data()

# Sidebar Filters
selected_client = st.sidebar.selectbox("Select Brand", df['client'].unique())
filtered_df = df[df['client'] == selected_client]

st.markdown('<div class="section-title">Data Discrepancy Overview</div>', unsafe_allow_html=True)

# Calculate KPIs
missing_api = len(filtered_df[filtered_df['Error Type'] == 'Missing from API Feed'])
missing_pm = len(filtered_df[filtered_df['Error Type'] == 'Missing from PM Tool'])
total_issues = missing_api + missing_pm + len(filtered_df[filtered_df['Error Type'].isin(['Inconsistent Dates', 'Field Error'])])

# KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
        <div class="kpi-row"><div class="kpi" style="--c:#4285F4">
            <div class="lbl">PM Tool Total</div>
            <div class="num">{len(filtered_df[filtered_df['post_date'].notna()])}</div>
            <div class="sub">{missing_api} Missing from API</div>
        </div></div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="kpi-row"><div class="kpi" style="--c:#34A853">
            <div class="lbl">API Feed Total</div>
            <div class="num">{len(filtered_df[filtered_df['api_feed_date'].notna()])}</div>
            <div class="sub">{missing_pm} Missing from PM Tool</div>
        </div></div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="kpi-row"><div class="kpi" style="--c:#EA4335">
            <div class="lbl">Total Issues</div>
            <div class="num">{total_issues}</div>
            <div class="sub">Requires review</div>
        </div></div>
    """, unsafe_allow_html=True)

st.markdown('<hr style="margin: 1.5rem 0; border: none; border-bottom: 1px solid #E5E2DC;">', unsafe_allow_html=True)

# Data Table Display
if total_issues > 0:
    st.markdown('<div class="section-title">Problematic Assets</div>', unsafe_allow_html=True)
    err_df = filtered_df[filtered_df['Error Type'].notnull()]
    
    # Streamlit native dataframe formatting
    st.dataframe(
        err_df[['Error Type', 'platform', 'asset_name', 'post_date', 'api_feed_date']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("✓ All data points match perfectly. No issues found.")