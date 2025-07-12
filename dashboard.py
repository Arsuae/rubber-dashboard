import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, time
import io
import requests
import json

# ========================================================================================
# CONFIG
# ========================================================================================
st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================================
# CUSTOM CSS - Pastel Minimal Style
# ========================================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500&display=swap');

    body, .stApp {
        font-family: 'Prompt', sans-serif;
        background-color: #f9f9f9;
        color: #333;
    }

    .header-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .header-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #4a4a4a;
    }

    .header-subtitle {
        font-size: 1rem;
        color: #999;
        margin-top: 0.3rem;
    }

    .sidebar-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 1.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #eee;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .sidebar-title {
        color: #333;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }

    .employee-card {
        background: #f2f6ff;
        padding: 0.8rem 1rem;
        border-radius: 0.8rem;
        margin-bottom: 0.6rem;
        border-left: 6px solid #a3c4f3;
    }

    .employee-offline { border-left-color: #f8b6b8; background: #fff2f2; }
    .employee-done    { border-left-color: #a3f7bf; background: #f2fff7; }
    .employee-late    { border-left-color: #ffe28a; background: #fffbee; }
    .employee-leave   { border-left-color: #c4b5fd; background: #f8f6ff; }

    .metric-card {
        background: #ffffff;
        border-radius: 1.2rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #4a4a4a;
    }

    .metric-label {
        font-size: 0.95rem;
        color: #888;
    }

    .chart-container {
        background: #ffffff;
        border-radius: 1.2rem;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .chart-title {
        font-size: 1.25rem;
        font-weight: 500;
        color: #444;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .search-container, .footer {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #aaa;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# จากตรงนี้ไป (streamlit logic) ไม่ต้องเปลี่ยน UI
# เพราะ CSS ถูกแก้แล้วทั้งหมดด้านบน
