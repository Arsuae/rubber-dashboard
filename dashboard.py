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
# CUSTOM CSS (Improved Visibility & Professional Design)
# ========================================================================================
st.markdown("""
<style>
  /* Import Google Fonts */
  @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=Kanit:wght@300;400;500;600&display=swap');

  /* Global */
  .stApp {
    font-family: 'Prompt', 'Kanit', sans-serif;
    background: linear-gradient(to bottom, #FFF9F3 0%, #F5F3FF 100%);
    min-height: 100vh;
    color: #2C3E50; /* Darker base text color for better readability */
  }
  
  .block-container {
    padding: 1.5rem;
    max-width: 1200px;
    margin: auto;
  }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFE5EC 0%, #E8E5FF 100%);
    border-right: 2px solid #FFD6E0;
  }
  
  .sidebar-section {
    background: rgba(255, 255, 255, 0.95);
    padding: 1.2rem;
    margin-bottom: 1rem;
    border-radius: 16px;
    border: 2px solid #FFE0EC;
    box-shadow: 0 4px 12px rgba(255, 182, 193, 0.15);
  }
  
  .sidebar-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2C3E50; /* Dark color for better visibility */
    margin-bottom: 0.8rem;
    text-align: center;
  }

  /* Employee Cards */
  .employee-card {
    background: linear-gradient(135deg, #FFEAA7 0%, #FFF3E0 100%);
    padding: 0.8rem;
    border-radius: 12px;
    margin-bottom: 0.5rem;
    border: 2px solid #FFD93D;
    transition: all 0.3s ease;
    font-size: 0.9rem;
    color: #2C3E50; /* Dark text */
  }
  
  .employee-card b {
    color: #1A252F; /* Even darker for names */
    font-weight: 600;
  }
  
  .employee-card small {
    color: #34495E; /* Readable secondary text */
  }
  
  .employee-card:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 6px 16px rgba(255, 217, 61, 0.2);
  }
  
  .employee-offline {
    background: linear-gradient(135deg, #FFB6C1 0%, #FFE0EC 100%);
    border-color: #FF69B4;
  }
  
  .employee-done {
    background: linear-gradient(135deg, #B2DFDB 0%, #E0F2F1 100%);
    border-color: #4DB6AC;
  }
  
  .employee-late {
    background: linear-gradient(135deg, #FFE0B2 0%, #FFF3E0 100%);
    border-color: #FFB74D;
  }
  
  .employee-leave {
    background: linear-gradient(135deg, #E1BEE7 0%, #F3E5F5 100%);
    border-color: #BA68C8;
  }

  /* Header */
  .header-container {
    background: linear-gradient(135deg, #FFE5E5 0%, #E8E5FF 50%, #E5F3FF 100%);
    padding: 2rem;
    border-radius: 24px;
    border: 2px solid #FFD6E0;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 24px rgba(255, 182, 193, 0.2);
    position: relative;
    overflow: hidden;
  }
  
  .header-container::before {
    content: "✨";
    position: absolute;
    top: 10px;
    left: 20px;
    font-size: 2rem;
    animation: sparkle 2s infinite;
  }
  
  .header-container::after {
    content: "🌸";
    position: absolute;
    bottom: 10px;
    right: 20px;
    font-size: 2rem;
    animation: float 3s ease-in-out infinite;
  }
  
  @keyframes sparkle {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
  }
  
  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }
  
  .header-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #2C3E50; /* Dark color for main title */
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
  }
  
  .header-subtitle {
    font-size: 1.1rem;
    color: #34495E; /* Darker subtitle */
    margin-top: 0.5rem;
    font-weight: 500;
  }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    padding: 0.5rem;
    margin-bottom: 1.5rem;
    border: 2px solid #FFE0EC;
  }
  
  .stTabs [data-baseweb="tab"] {
    background: linear-gradient(135deg, #FFF5F5 0%, #F5F3FF 100%);
    border: 2px solid #FFE0EC;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    color: #2C3E50; /* Dark text for tabs */
    font-weight: 600;
    transition: all 0.3s ease;
  }
  
  .stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 182, 193, 0.2);
  }
  
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FFB6C1 0%, #DDA0DD 100%);
    border-color: #FF69B4;
    color: #FFFFFF; /* White text on active tab */
    box-shadow: 0 6px 16px rgba(255, 105, 180, 0.3);
  }

  /* Metric Cards */
  .metric-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 100%);
    border: 2px solid #FFE0EC;
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 6px 20px rgba(255, 182, 193, 0.15);
  }
  
  .metric-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 10px 30px rgba(255, 182, 193, 0.25);
  }
  
  .metric-icon {
    font-size: 3rem;
    margin-bottom: 0.8rem;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));
  }
  
  .metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #E91E63; /* Strong pink color for values */
    margin-bottom: 0.3rem;
  }
  
  .metric-label {
    font-size: 1rem;
    color: #2C3E50; /* Dark label text */
    font-weight: 600;
  }

  /* Chart Container */
  .chart-container {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF9FC 100%);
    border: 2px solid #FFE0EC;
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 6px 20px rgba(255, 182, 193, 0.15);
  }
  
  .chart-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #2C3E50; /* Dark chart titles */
    margin-bottom: 1.2rem;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  /* Dataframe/Table */
  .dataframe {
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #FFE0EC !important;
    background: white;
    color: #2C3E50; /* Dark table text */
  }
  
  .dataframe thead {
    background: linear-gradient(90deg, #FFB6C1, #DDA0DD);
    color: white;
    font-weight: 600;
  }
  
  .dataframe tbody tr:nth-child(even) {
    background: #FFF5F8;
  }
  
  .dataframe tbody tr:hover {
    background: #FFE0EC;
  }
  
  .dataframe td, .dataframe th {
    color: #2C3E50 !important; /* Ensure table text is dark */
    font-weight: 500;
  }

  /* Search Container */
  .search-container {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 100%);
    border: 2px solid #FFE0EC;
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(255, 182, 193, 0.15);
  }
  
  .search-container h3 {
    color: #2C3E50 !important; /* Dark search title */
    font-weight: 600 !important;
  }

  /* Input Fields */
  .stTextInput > div > div > input,
  .stSelectbox > div > div > select,
  .stMultiSelect > div > div > div {
    border: 2px solid #FFE0EC !important;
    border-radius: 12px !important;
    background: #FFF9FC !important;
    padding: 0.6rem !important;
    color: #2C3E50 !important; /* Dark input text */
    font-weight: 500 !important;
  }
  
  .stTextInput > div > div > input:focus,
  .stSelectbox > div > div > select:focus {
    border-color: #FF69B4 !important;
    box-shadow: 0 0 0 3px rgba(255, 105, 180, 0.2) !important;
  }
  
  /* Labels for inputs */
  .stTextInput label, .stSelectbox label, .stMultiSelect label {
    color: #2C3E50 !important;
    font-weight: 600 !important;
  }

  /* Buttons */
  .stButton > button {
    background: linear-gradient(135deg, #FFB6C1 0%, #DDA0DD 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);
  }
  
  .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 105, 180, 0.4);
  }
  
  .stDownloadButton > button {
    background: linear-gradient(135deg, #98FB98 0%, #90EE90 100%);
    color: #1B5E20; /* Dark green text */
    border: 2px solid #90EE90;
    border-radius: 12px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
  }
  
  .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(144, 238, 144, 0.4);
  }

  /* Footer */
  .footer {
    background: linear-gradient(135deg, #FFE5E5 0%, #E8E5FF 100%);
    border: 2px solid #FFE0EC;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    color: #2C3E50; /* Dark footer text */
    font-size: 0.9rem;
    margin-top: 2rem;
    box-shadow: 0 4px 12px rgba(255, 182, 193, 0.15);
  }
  
  .footer p {
    color: #2C3E50 !important;
    font-weight: 500;
  }

  /* Alerts & Messages */
  .stAlert {
    border-radius: 12px;
    border: 2px solid #FFE0EC;
    background: linear-gradient(135deg, #FFF5F5 0%, #FFE0EC 100%);
    color: #2C3E50 !important;
  }
  
  /* Warning/Error messages */
  .stAlert > div {
    color: #2C3E50 !important;
    font-weight: 500;
  }

  /* All text elements */
  p, span, div, label {
    color: #2C3E50;
  }
  
  /* Ensure all headings are visible */
  h1, h2, h3, h4, h5, h6 {
    color: #2C3E50 !important;
    font-weight: 600 !important;
  }

  /* Scrollbar */
  ::-webkit-scrollbar {
    width: 10px;
    height: 10px;
  }
  
  ::-webkit-scrollbar-track {
    background: #FFF5F8;
    border-radius: 10px;
  }
  
  ::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #FFB6C1, #DDA0DD);
    border-radius: 10px;
  }
  
  ::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #FF69B4, #BA68C8);
  }

  /* Loading Spinner */
  .stSpinner > div {
    border-color: #FFB6C1 !important;
  }
</style>
""", unsafe_allow_html=True)
# ========================================================================================
# LOAD DATA
# ========================================================================================
@st.cache_data(ttl=300)
def load_data():
    try:
        url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
        df = pd.read_csv(url, header=None)
        df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
        df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')
        df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['ราคา'] = pd.to_numeric(df['ราคา'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['จำนวนเงิน'] = pd.to_numeric(df['จำนวนเงิน'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดข้อมูลได้: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60)  # Cache for 1 minute since employee status changes frequently
def load_employee_status_from_apps_script():
    """Load employee status from Google Apps Script API"""
    try:
        # Google Apps Script Web App URL
        apps_script_url = 'https://script.google.com/macros/s/AKfycbwcURACTMc6xWy-0vPfxiuG4orie0Pp0UafiNIA57uebo33YRvDiUleqihfZ_rw3B1PKw/exec'
        
        response = requests.get(apps_script_url, timeout=(5, 30))

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                employees = data.get('data', [])
                # Convert to DataFrame
                emp_df = pd.DataFrame(employees)
                if not emp_df.empty:
                    emp_df = emp_df[['name', 'status', 'time']].rename(columns={
                        'name': 'ชื่อพนักงาน',
                        'status': 'สถานะ',
                        'time': 'เวลา'
                    })
                    return emp_df
        
        # Return empty DataFrame if failed
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])
        
    except Exception as e:
        st.error(f"ไม่สามารถโหลดข้อมูลพนักงานได้: {str(e)}")
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])

# ========================================================================================
# STATE HANDLING
# ========================================================================================
if 'tab' not in st.session_state:
    st.session_state.tab = "📁 รายการ"
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = date.today()
if 'selected_branches' not in st.session_state:
    st.session_state.selected_branches = []
if 'selected_groups' not in st.session_state:
    st.session_state.selected_groups = []

# ========================================================================================
# SIDEBAR CONTROLS
# ========================================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">🎛️ ตัวกรองข้อมูล</h3>', unsafe_allow_html=True)
    
    selected_date = st.date_input("📅 เลือกวันที่", value=st.session_state.selected_date)
    st.session_state.selected_date = selected_date

    df = load_data()
    
    if not df.empty:
        branches = df['สาขา'].dropna().unique().tolist()
        selected_branches = st.multiselect("🏢 เลือกสาขา", options=branches, default=st.session_state.selected_branches or branches)
        st.session_state.selected_branches = selected_branches

        groups = df['กอง'].dropna().unique().tolist()
        if "กอง3" not in groups:
            groups.append("กอง3")
        selected_groups = st.multiselect("📦 เลือกกอง", options=groups, default=st.session_state.selected_groups or groups)
        st.session_state.selected_groups = selected_groups
    else:
        st.error("ไม่มีข้อมูลให้แสดง")
        st.session_state.selected_branches = []
        st.session_state.selected_groups = []

    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Employee Status Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">👨‍🌾 พนักงาน</h3>', unsafe_allow_html=True)
    
    # Load employee data from Google Apps Script
    emp_df = load_employee_status_from_apps_script()
    
    if not emp_df.empty:
        # Count status
        status_counts = {
            'มาทำงาน': 0,
            'มาสาย': 0,
            'ลา': 0,
            'ขาด': 0
        }
        
        for _, row in emp_df.iterrows():
            status = row['สถานะ']
            if status in status_counts:
                status_counts[status] += 1
        
        # Display summary
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div style='text-align: center; color: #4CAF50;'><b>{status_counts['มาทำงาน']}</b><br>มาทำงาน</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; color: #f2994a;'><b>{status_counts['มาสาย']}</b><br>มาสาย</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='text-align: center; color: #667eea;'><b>{status_counts['ลา']}</b><br>ลางาน</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; color: #f44336;'><b>{status_counts['ขาด']}</b><br>ขาดงาน</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 1rem 0; opacity: 0.3;'>", unsafe_allow_html=True)
        
        # Display individual employees
        for _, row in emp_df.iterrows():
            name = row['ชื่อพนักงาน']
            status = row['สถานะ']
            time_str = row.get('เวลา', '')
            
            # Determine card class and status text based on status
            if status == 'มาทำงาน':
                status_text = f"🟢 มาทำงาน {time_str}"
                card_class = "employee-card"
            elif status == 'มาสาย':
                status_text = f"🟡 มาสาย {time_str}"
                card_class = "employee-card employee-late"
            elif status == 'ลา':
                status_text = "🟣 ลางาน"
                card_class = "employee-card employee-leave"
            else:  # ขาด
                status_text = "🔴 ขาดงาน"
                card_class = "employee-card employee-offline"
            
            st.markdown(f'<div class="{card_class}"><b>{name}</b><br><small>{status_text}</small></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="employee-card employee-offline">ไม่สามารถดึงข้อมูลพนักงานได้</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# FILTERED DATA
# ========================================================================================
if not df.empty and st.session_state.selected_branches and st.session_state.selected_groups:
    df_filtered = df[
        (df['วันที่'].dt.date == st.session_state.selected_date) &
        (df['สาขา'].isin(st.session_state.selected_branches)) &
        (df['กอง'].isin(st.session_state.selected_groups))
    ]
else:
    df_filtered = pd.DataFrame()

# ========================================================================================
# HEADER
# ========================================================================================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🌳 ลิตาการยาง</h1>
    <p class="header-subtitle">แดชบอร์ดข้อมูลยางพาราแบบเรียลไทม์</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# TABS
# ========================================================================================
tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "📋 สรุป", "📁 รายการ"])

# ========================================================================================
# TAB: ภาพรวม
# ========================================================================================
with tab1:
    if df_filtered.empty:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(255,255,255,0.1); border-radius: 20px; margin: 2rem 0;">
            <h3 style="color: white; margin-bottom: 1rem;">⚠️ ไม่มีข้อมูล</h3>
            <p style="color: rgba(255,255,255,0.8);">ไม่มีข้อมูลในวันที่ สาขา หรือกองที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">⚖️</div>
                <div class="metric-value">{df_filtered['จำนวนยาง'].sum():,.1f}</div>
                <div class="metric-label">กิโลกรัม</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-value">฿{df_filtered['จำนวนเงิน'].sum():,.0f}</div>
                <div class="metric-label">รายได้รวม</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">👥</div>
                <div class="metric-value">{df_filtered['ชื่อลูกค้า'].count():,.0f}</div>
                <div class="metric-label">ลูกค้าทั้งหมด</div>
            </div>
            """, unsafe_allow_html=True)

        # Charts
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">🏢 จำนวนยางตามสาขา</h3>', unsafe_allow_html=True)
        bar_data = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
        if not bar_data.empty:
            fig_bar = px.bar(
                bar_data, 
                x='สาขา', 
                y='จำนวนยาง', 
                text='จำนวนยาง',
                color='จำนวนยาง',
                color_continuous_scale='Viridis'
            )
            fig_bar.update_traces(texttemplate='%{text:.1f} กก.', textposition='outside')
            fig_bar.update_layout(
                font_family="Noto Sans Thai",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#2a4d69'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">💰 สัดส่วนรายได้</h3>', unsafe_allow_html=True)
        pie_data = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
        if not pie_data.empty:
            fig_pie = px.pie(
                pie_data, 
                values='จำนวนเงิน', 
                names='สาขา', 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textinfo='percent+label')
            fig_pie.update_layout(
                font_family="Noto Sans Thai",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#2a4d69'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB: สรุป
# ========================================================================================
with tab2:
    if df_filtered.empty:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(255,255,255,0.1); border-radius: 20px; margin: 2rem 0;">
            <h3 style="color: white; margin-bottom: 1rem;">⚠️ ไม่มีข้อมูล</h3>
            <p style="color: rgba(255,255,255,0.8);">ไม่มีข้อมูลในวันที่ สาขา หรือกองที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">📦 สรุปข้อมูลตามกอง</h3>', unsafe_allow_html=True)
        by_gong = df_filtered.groupby('กอง').agg({'จำนวนยาง': 'sum', 'จำนวนเงิน': 'sum', 'ชื่อลูกค้า': 'count'}).reset_index()
        st.dataframe(by_gong.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า'}), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">🏢 สรุปข้อมูลตามสาขา</h3>', unsafe_allow_html=True)
        by_branch = df_filtered.groupby('สาขา').agg({'จำนวนยาง': 'sum', 'จำนวนเงิน': 'sum', 'ชื่อลูกค้า': 'count', 'ราคา': 'mean'}).reset_index()
        by_branch = by_branch.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า', 'ราคา': 'ราคาเฉลี่ย'})
        st.dataframe(by_branch, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB: รายการ
# ========================================================================================
with tab3:
    if df_filtered.empty:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(255,255,255,0.1); border-radius: 20px; margin: 2rem 0;">
            <h3 style="color: white; margin-bottom: 1rem;">⚠️ ไม่มีข้อมูล</h3>
            <p style="color: rgba(255,255,255,0.8);">ไม่มีข้อมูลในวันที่ สาขา หรือกองที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #2a4d69; margin-bottom: 1rem;">📋 รายการลูกค้าทั้งหมด</h3>', unsafe_allow_html=True)
        keyword = st.text_input("🔍 ค้นหาชื่อลูกค้า", placeholder="กรอกชื่อลูกค้าที่ต้องการค้นหา...")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if keyword:
            result_df = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(keyword, case=False, na=False)]
        else:
            result_df = df_filtered

        if result_df.empty:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin: 1rem 0;">
                <h4 style="color: white;">🔍 ไม่พบข้อมูล</h4>
                <p style="color: rgba(255,255,255,0.8);">ไม่พบข้อมูลลูกค้าที่ค้นหา</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            result_df = result_df.reset_index(drop=True)
            display_df = result_df[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']]
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(display_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            csv = display_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "📥 ดาวน์โหลดข้อมูล", 
                csv, 
                f"rubber_data_{st.session_state.selected_date.strftime('%Y%m%d')}.csv", 
                "text/csv", 
                use_container_width=True
            )

# ========================================================================================
# FOOTER
# ========================================================================================
st.markdown(f"""
<div class="footer">
    <p>🌳 ลิตาการยาง Dashboard © 2025 | อัปเดตล่าสุด: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
    <p>พัฒนาด้วย ❤️ สำหรับการจัดการข้อมูลยางพาราแบบเรียลไทม์</p>
</div>
""", unsafe_allow_html=True)
