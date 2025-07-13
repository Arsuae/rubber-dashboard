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
# CUSTOM CSS - Professional & Elegant Design
# ========================================================================================
st.markdown("""
<style>
  /* Import Google Fonts */
  @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=Kanit:wght@300;400;500;600&display=swap');

  /* Global Styles */
  .stApp {
    font-family: 'Prompt', 'Kanit', sans-serif;
    background: linear-gradient(to bottom, #FFF9F3 0%, #F5F3FF 100%);
    min-height: 100vh;
    color: #2C3E50;
  }
  
  .block-container {
    padding: 1.5rem;
    max-width: 1400px;
    margin: auto;
  }

  /* Sidebar Styling */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFE5EC 0%, #E8E5FF 100%);
    border-right: 2px solid #FFD6E0;
  }
  
  .sidebar-section {
    background: rgba(255, 255, 255, 0.95);
    padding: 1rem;
    margin-bottom: 0.8rem;
    border-radius: 12px;
    border: 1px solid #FFE0EC;
    box-shadow: 0 2px 8px rgba(255, 182, 193, 0.1);
  }
  
  .sidebar-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #2C3E50;
    margin-bottom: 0.6rem;
    text-align: center;
  }

  /* Compact Header */
  .header-container {
    background: linear-gradient(135deg, #FFE5E5 0%, #E8E5FF 50%, #E5F3FF 100%);
    padding: 1rem 1.5rem;
    border-radius: 16px;
    border: 1px solid #FFD6E0;
    margin-bottom: 1rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(255, 182, 193, 0.15);
  }
  
  .header-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #2C3E50;
    margin: 0;
  }
  
  .header-subtitle {
    font-size: 0.9rem;
    color: #34495E;
    margin-top: 0.3rem;
    font-weight: 500;
  }

  /* Tabs Styling */
  .stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 12px;
    padding: 0.4rem;
    margin-bottom: 1rem;
    border: 1px solid #FFE0EC;
  }
  
  .stTabs [data-baseweb="tab"] {
    background: linear-gradient(135deg, #FFF5F5 0%, #F5F3FF 100%);
    border: 1px solid #FFE0EC;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    color: #2C3E50;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
  }
  
  .stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(255, 182, 193, 0.2);
  }
  
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FFB6C1 0%, #DDA0DD 100%);
    border-color: #FF69B4;
    color: #FFFFFF;
    box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);
  }

  /* Compact Metric Cards */
.metric-card-compact {
  background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 100%);
  border: 1px solid #FFE0EC;
  border-radius: 12px;
  padding: 0.8rem;
  text-align: center;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(255, 182, 193, 0.1);
  height: auto;
  max-width: 100%;
  overflow-wrap: break-word;
  word-break: break-word;
}

  .metric-card-compact:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 182, 193, 0.2);
  }

  .metric-icon-small {
    font-size: 1.5rem;
    margin-bottom: 0.2rem;
  }

  .metric-value-small {
    font-size: 1.3rem;
    font-weight: 700;
    color: #E91E63;
    line-height: 1.2;
  }

  .metric-label-small {
    font-size: 0.75rem;
    color: #2C3E50;
    font-weight: 500;
    margin-top: 0.2rem;
  }

  /* Compact Chart Container */
  .chart-container-compact {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF9FC 100%);
    border: 1px solid #FFE0EC;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(255, 182, 193, 0.1);
  }

  /* Employee Cards */
  .employee-card {
    background: linear-gradient(135deg, #FFEAA7 0%, #FFF3E0 100%);
    padding: 0.6rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    border-left: 3px solid #FFD93D;
    transition: all 0.3s ease;
    font-size: 0.85rem;
    color: #2C3E50;
  }
  
  .employee-card b {
    color: #1A252F;
    font-weight: 600;
  }
  
  .employee-card small {
    color: #34495E;
    font-size: 0.75rem;
  }
  
  .employee-card:hover {
    transform: translateX(3px);
    box-shadow: 0 2px 8px rgba(255, 217, 61, 0.2);
  }
  
  .employee-offline {
    background: linear-gradient(135deg, #FFB6C1 0%, #FFE0EC 100%);
    border-left-color: #FF69B4;
  }
  
  .employee-done {
    background: linear-gradient(135deg, #B2DFDB 0%, #E0F2F1 100%);
    border-left-color: #4DB6AC;
  }
  
  .employee-late {
    background: linear-gradient(135deg, #FFE0B2 0%, #FFF3E0 100%);
    border-left-color: #FFB74D;
  }
  
  .employee-leave {
    background: linear-gradient(135deg, #E1BEE7 0%, #F3E5F5 100%);
    border-left-color: #BA68C8;
  }

  /* Data Table Styling */
  .dataframe {
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #FFE0EC !important;
    background: white;
    color: #2C3E50;
    font-size: 0.9rem;
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
    color: #2C3E50 !important;
    font-weight: 500;
    padding: 0.5rem !important;
  }

  /* Search Container */
  .search-container {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 100%);
    border: 1px solid #FFE0EC;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(255, 182, 193, 0.1);
  }
  
  .search-container h3 {
    color: #2C3E50 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    margin-bottom: 0.8rem !important;
  }

  /* Input Fields */
  .stTextInput > div > div > input,
  .stSelectbox > div > div > select,
  .stMultiSelect > div > div > div,
  .stDateInput > div > div > input {
    border: 1px solid #FFE0EC !important;
    border-radius: 8px !important;
    background: #FFF9FC !important;
    padding: 0.5rem !important;
    color: #2C3E50 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
  }
  
  .stTextInput > div > div > input:focus,
  .stSelectbox > div > div > select:focus,
  .stDateInput > div > div > input:focus {
    border-color: #FF69B4 !important;
    box-shadow: 0 0 0 2px rgba(255, 105, 180, 0.2) !important;
  }
  
  /* Labels */
  .stTextInput label, .stSelectbox label, .stMultiSelect label, .stDateInput label {
    color: #2C3E50 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
  }

  /* Buttons */
  .stButton > button {
    background: linear-gradient(135deg, #FFB6C1 0%, #DDA0DD 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(255, 105, 180, 0.3);
  }
  
  .stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(255, 105, 180, 0.4);
  }
  
  .stDownloadButton > button {
    background: linear-gradient(135deg, #98FB98 0%, #90EE90 100%);
    color: #1B5E20;
    border: 1px solid #90EE90;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
  }
  
  .stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(144, 238, 144, 0.4);
  }

  /* Footer */
  .footer {
    background: linear-gradient(135deg, #FFE5E5 0%, #E8E5FF 100%);
    border: 1px solid #FFE0EC;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    color: #2C3E50;
    font-size: 0.85rem;
    margin-top: 1.5rem;
    box-shadow: 0 2px 8px rgba(255, 182, 193, 0.1);
  }
  
  .footer p {
    color: #2C3E50 !important;
    font-weight: 500;
    margin: 0.3rem 0;
  }

  /* Alerts & Messages */
  .stAlert {
    border-radius: 8px;
    border: 1px solid #FFE0EC;
    background: linear-gradient(135deg, #FFF5F5 0%, #FFE0EC 100%);
    color: #2C3E50 !important;
    font-size: 0.9rem;
  }
  
  .stAlert > div {
    color: #2C3E50 !important;
    font-weight: 500;
  }

  /* Empty State */
  .empty-state {
    text-align: center;
    padding: 2rem;
    background: rgba(255,255,255,0.9);
    border-radius: 16px;
    margin: 1rem 0;
    border: 1px solid #FFE0EC;
  }
  
  .empty-state h3 {
    color: #2C3E50;
    margin-bottom: 0.5rem;
  }
  
  .empty-state p {
    color: #34495E;
  }

  /* All text elements */
  p, span, div, label {
    color: #2C3E50;
  }
  
  /* Headings */
  h1, h2, h3, h4, h5, h6 {
    color: #2C3E50 !important;
    font-weight: 600 !important;
  }

  /* Hide Plotly Toolbar */
  .modebar {
    display: none !important;
  }

  /* Scrollbar */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  
  ::-webkit-scrollbar-track {
    background: #FFF5F8;
    border-radius: 8px;
  }
  
  ::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #FFB6C1, #DDA0DD);
    border-radius: 8px;
  }
  
  ::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #FF69B4, #BA68C8);
  }

  /* Loading Spinner */
  .stSpinner > div {
    border-color: #FFB6C1 !important;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .header-title {
      font-size: 1.5rem;
    }
    
    .metric-card-compact {
      height: 80px;
      padding: 0.6rem;
    }
    
    .metric-value-small {
      font-size: 1.1rem;
    }
    
    .metric-label-small {
      font-size: 0.7rem;
    }
  }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# LOAD DATA FUNCTIONS
# ========================================================================================
@st.cache_data(ttl=300)
def load_data():
    """Load rubber data from Google Sheets with error handling"""
    try:
        url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
        df = pd.read_csv(url, header=None)
        df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
        
        # Data cleaning and type conversion
        df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')
        df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['ราคา'] = pd.to_numeric(df['ราคา'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['จำนวนเงิน'] = pd.to_numeric(df['จำนวนเงิน'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดข้อมูลได้: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def load_employee_status_from_apps_script():
    """Load employee status from Google Apps Script API"""
    try:
        apps_script_url = 'https://script.google.com/macros/s/AKfycbwcURACTMc6xWy-0vPfxiuG4orie0Pp0UafiNIA57uebo33YRvDiUleqihfZ_rw3B1PKw/exec'
        response = requests.get(apps_script_url, timeout=(5, 30))

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                employees = data.get('data', [])
                emp_df = pd.DataFrame(employees)
                if not emp_df.empty:
                    emp_df = emp_df[['name', 'status', 'time']].rename(columns={
                        'name': 'ชื่อพนักงาน',
                        'status': 'สถานะ',
                        'time': 'เวลา'
                    })
                    return emp_df
        
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])
        
    except Exception as e:
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])

# ========================================================================================
# SESSION STATE INITIALIZATION
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
# SIDEBAR
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
    st.markdown('<h3 class="sidebar-title">👨‍🌾 สถานะพนักงาน</h3>', unsafe_allow_html=True)
    
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
        
        # Display summary in 2x2 grid
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div style='text-align: center; padding: 0.5rem; background: rgba(76,175,80,0.1); border-radius: 8px; margin-bottom: 0.5rem;'><b style='color: #4CAF50; font-size: 1.2rem;'>{status_counts['มาทำงาน']}</b><br><small style='color: #2C3E50;'>มาทำงาน</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; padding: 0.5rem; background: rgba(242,153,74,0.1); border-radius: 8px;'><b style='color: #f2994a; font-size: 1.2rem;'>{status_counts['มาสาย']}</b><br><small style='color: #2C3E50;'>มาสาย</small></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='text-align: center; padding: 0.5rem; background: rgba(102,126,234,0.1); border-radius: 8px; margin-bottom: 0.5rem;'><b style='color: #667eea; font-size: 1.2rem;'>{status_counts['ลา']}</b><br><small style='color: #2C3E50;'>ลางาน</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; padding: 0.5rem; background: rgba(244,67,54,0.1); border-radius: 8px;'><b style='color: #f44336; font-size: 1.2rem;'>{status_counts['ขาด']}</b><br><small style='color: #2C3E50;'>ขาดงาน</small></div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 0.8rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        
        # Display individual employees
        for _, row in emp_df.iterrows():
            name = row['ชื่อพนักงาน']
            status = row['สถานะ']
            time_str = row.get('เวลา', '')
            
            if status == 'มาทำงาน':
                status_text = f"🟢 มาทำงาน {time_str}"
                card_class = "employee-card employee-done"
            elif status == 'มาสาย':
                status_text = f"🟡 มาสาย {time_str}"
                card_class = "employee-card employee-late"
            elif status == 'ลา':
                status_text = "🟣 ลางาน"
                card_class = "employee-card employee-leave"
            else:
                status_text = "🔴 ขาดงาน"
                card_class = "employee-card employee-offline"
            
            st.markdown(f'<div class="{card_class}"><b>{name}</b><br><small>{status_text}</small></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="employee-card employee-offline">ไม่สามารถดึงข้อมูลพนักงานได้</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# FILTER DATA
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
    <h1 class="header-title">🌳 ลิตาการยาง Dashboard</h1>
    <p class="header-subtitle">ระบบจัดการข้อมูลยางพาราแบบเรียลไทม์</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# MAIN TABS
# ========================================================================================
tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "📋 สรุปข้อมูล", "📁 รายการ"])

# ========================================================================================
# TAB 1: Overview Dashboard
# ========================================================================================
with tab1:
    if df_filtered.empty:
        st.markdown("""
        <div class="empty-state">
            <h3>⚠️ ไม่มีข้อมูล</h3>
            <p>ไม่มีข้อมูลในวันที่ สาขา หรือกองที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Compact Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card-compact">
                <div class="metric-icon-small">⚖️</div>
                <div class="metric-value-small">{df_filtered['จำนวนยาง'].sum():,.0f}</div>
                <div class="metric-label-small">กิโลกรัม</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card-compact">
                <div class="metric-icon-small">💰</div>
                <div class="metric-value-small">฿{df_filtered['จำนวนเงิน'].sum():,.0f}</div>
                <div class="metric-label-small">รายได้รวม</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card-compact">
                <div class="metric-icon-small">👥</div>
                <div class="metric-value-small">{df_filtered['ชื่อลูกค้า'].count():,.0f}</div>
                <div class="metric-label-small">ลูกค้าทั้งหมด</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            avg_price = df_filtered['ราคา'].mean()
            st.markdown(f"""
            <div class="metric-card-compact">
                <div class="metric-icon-small">📊</div>
                <div class="metric-value-small">฿{avg_price:,.1f}</div>
                <div class="metric-label-small">ราคาเฉลี่ย</div>
            </div>
            """, unsafe_allow_html=True)

        # Charts in same row
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown('<div class="chart-container-compact">', unsafe_allow_html=True)
            bar_data = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
            if not bar_data.empty:
                fig_bar = px.bar(
                    bar_data, 
                    x='สาขา', 
                    y='จำนวนยาง',
                    text='จำนวนยาง',
                    color_discrete_sequence=['#FFB6C1', '#DDA0DD', '#E1BEE7', '#F8BBD0']
                )
                fig_bar.update_traces(
                    texttemplate='%{text:.0f}',
                    textposition='outside',
                    textfont_size=11
                )
                fig_bar.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0),
                    title="จำนวนยางตามสาขา (กก.)",
                    title_font_size=14,
                    title_font_color='#2C3E50',
                    font_family="Prompt",
                    plot_bgcolor='rgba(255,255,255,0)',
                    paper_bgcolor='rgba(255,255,255,0)',
                    font_color='#2C3E50',
                    showlegend=False,
                    xaxis_title="",
                    yaxis_title=""
                )
                fig_bar.update_xaxes(showgrid=False)
                fig_bar.update_yaxes(showgrid=True, gridcolor='rgba(255,224,236,0.5)')
                st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_chart2:
            st.markdown('<div class="chart-container-compact">', unsafe_allow_html=True)
            pie_data = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
            if not pie_data.empty:
                fig_pie = px.pie(
                    pie_data, 
                    values='จำนวนเงิน', 
                    names='สาขา', 
                    hole=0.5,
                    color_discrete_sequence=['#FFB6C1', '#DDA0DD', '#E1BEE7', '#F8BBD0', '#FCE4EC']
                )
                fig_pie.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    textfont_size=11
                )
                fig_pie.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0),
                    title="สัดส่วนรายได้ตามสาขา",
                    title_font_size=14,
                    title_font_color='#2C3E50',
                    font_family="Prompt",
                    plot_bgcolor='rgba(255,255,255,0)',
                    paper_bgcolor='rgba(255,255,255,0)',
                    font_color='#2C3E50',
                    showlegend=False
                )
                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB 2: Summary
# ========================================================================================
with tab2:
    if df_filtered.empty:
        st.markdown("""
        <div class="empty-state">
            <h3>⚠️ ไม่มีข้อมูล</h3>
            <p>ไม่มีข้อมูลในวันที่ สาขา หรือกองที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_summary1, col_summary2 = st.columns(2)
        
        with col_summary1:
            st.markdown('<div class="chart-container-compact">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #2C3E50; font-size: 1.1rem; margin-bottom: 1rem;">📦 สรุปข้อมูลตามกอง</h3>', unsafe_allow_html=True)
            by_gong = df_filtered.groupby('กอง').agg({
                'จำนวนยาง': 'sum', 
                'จำนวนเงิน': 'sum', 
                'ชื่อลูกค้า': 'count'
            }).reset_index()
            by_gong = by_gong.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า'})
            by_gong['จำนวนยาง'] = by_gong['จำนวนยาง'].round(1)
            by_gong['จำนวนเงิน'] = by_gong['จำนวนเงิน'].round(0)
            st.dataframe(by_gong, use_container_width=True, height=200)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_summary2:
            st.markdown('<div class="chart-container-compact">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #2C3E50; font-size: 1.1rem; margin-bottom: 1rem;">🏢 สรุปข้อมูลตามสาขา</h3>', unsafe_allow_html=True)
            by_branch = df_filtered.groupby('สาขา').agg({
                'จำนวนยาง': 'sum', 
                'จำนวนเงิน': 'sum', 
                'ชื่อลูกค้า': 'count', 
                'ราคา': 'mean'
            }).reset_index()
            by_branch = by_branch.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า', 'ราคา': 'ราคาเฉลี่ย'})
            by_branch['จำนวนยาง'] = by_branch['จำนวนยาง'].round(1)
            by_branch['จำนวนเงิน'] = by_branch['จำนวนเงิน'].round(0)
            by_branch['ราคาเฉลี่ย'] = by_branch['ราคาเฉลี่ย'].round(2)
            st.dataframe(by_branch, use_container_width=True, height=200)
            st.markdown('</div>', unsafe_allow_html=True)

        # Additional Analysis
        st.markdown('<div class="chart-container-compact">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #2C3E50; font-size: 1.1rem; margin-bottom: 1rem;">📈 การวิเคราะห์เพิ่มเติม</h3>', unsafe_allow_html=True)
        
        col_analysis1, col_analysis2, col_analysis3 = st.columns(3)
        
        with col_analysis1:
            top_customer = df_filtered.nlargest(1, 'จำนวนยาง')
            if not top_customer.empty:
                st.markdown(f"""
                <div style='background: #E8F5E9; padding: 1rem; border-radius: 8px; border: 1px solid #C8E6C9;'>
                    <h4 style='color: #2E7D32; margin: 0; font-size: 0.9rem;'>🏆 ลูกค้ายอดสูงสุด</h4>
                    <p style='margin: 0.5rem 0 0 0; font-weight: 600; color: #1B5E20;'>{top_customer.iloc[0]['ชื่อลูกค้า']}</p>
                    <p style='margin: 0; color: #388E3C; font-size: 0.85rem;'>{top_customer.iloc[0]['จำนวนยาง']:,.1f} กก.</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_analysis2:
            price_range = df_filtered['ราคา'].max() - df_filtered['ราคา'].min()
            st.markdown(f"""
            <div style='background: #E3F2FD; padding: 1rem; border-radius: 8px; border: 1px solid #BBDEFB;'>
                <h4 style='color: #1565C0; margin: 0; font-size: 0.9rem;'>📊 ช่วงราคา</h4>
                <p style='margin: 0.5rem 0 0 0; font-weight: 600; color: #0D47A1;'>฿{df_filtered['ราคา'].min():.2f} - ฿{df_filtered['ราคา'].max():.2f}</p>
                <p style='margin: 0; color: #1976D2; font-size: 0.85rem;'>ต่างกัน ฿{price_range:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_analysis3:
            total_branches = df_filtered['สาขา'].nunique()
            total_groups = df_filtered['กอง'].nunique()
            st.markdown(f"""
            <div style='background: #F3E5F5; padding: 1rem; border-radius: 8px; border: 1px solid #E1BEE7;'>
                <h4 style='color: #6A1B9A; margin: 0; font-size: 0.9rem;'>🏢 ความครอบคลุม</h4>
                <p style='margin: 0.5rem 0 0 0; font-weight: 600; color: #4A148C;'>{total_branches} สาขา</p>
                <p style='margin: 0; color: #7B1FA2; font-size: 0.85rem;'>{total_groups} กอง</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB 3: Detailed List
# ========================================================================================
with tab3:
    if df_filtered.empty:
        st.markdown("""
        <div class="empty-state">
            <h3>⚠️ ไม่มีข้อมูล</h3>
            <p>ไม่มีข้อมูลในวันที่ สาขา หรือกองที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        st.markdown('<h3>📋 รายการลูกค้าทั้งหมด</h3>', unsafe_allow_html=True)
        
        col_search1, col_search2 = st.columns([3, 1])
        with col_search1:
            keyword = st.text_input("🔍 ค้นหาชื่อลูกค้า", placeholder="กรอกชื่อลูกค้าที่ต้องการค้นหา...", label_visibility="collapsed")
        with col_search2:
            sort_by = st.selectbox("เรียงตาม", ["จำนวนยาง", "จำนวนเงิน", "ชื่อลูกค้า"], label_visibility="collapsed")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filter and sort data
        if keyword:
            result_df = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(keyword, case=False, na=False)]
        else:
            result_df = df_filtered
        
        # Sort data
        if sort_by == "จำนวนยาง":
            result_df = result_df.sort_values('จำนวนยาง', ascending=False)
        elif sort_by == "จำนวนเงิน":
            result_df = result_df.sort_values('จำนวนเงิน', ascending=False)
        else:
            result_df = result_df.sort_values('ชื่อลูกค้า')

        if result_df.empty:
            st.markdown("""
            <div class="empty-state">
                <h4>🔍 ไม่พบข้อมูล</h4>
                <p>ไม่พบข้อมูลลูกค้าที่ค้นหา</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display summary
            st.markdown(f"""
            <div style='background: #F5F5F5; padding: 0.8rem; border-radius: 8px; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #2C3E50; font-weight: 500;'>พบข้อมูล {len(result_df)} รายการ</span>
                <span style='color: #666; font-size: 0.9rem;'>รวม {result_df['จำนวนยาง'].sum():,.1f} กก. | ฿{result_df['จำนวนเงิน'].sum():,.0f}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Prepare display dataframe
            result_df = result_df.reset_index(drop=True)
            display_df = result_df[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']].copy()
            
            # Format numbers
            display_df['จำนวนยาง'] = display_df['จำนวนยาง'].apply(lambda x: f"{x:,.1f}")
            display_df['ราคา'] = display_df['ราคา'].apply(lambda x: f"{x:,.2f}")
            display_df['จำนวนเงิน'] = display_df['จำนวนเงิน'].apply(lambda x: f"{x:,.0f}")
            
            st.markdown('<div class="chart-container-compact">', unsafe_allow_html=True)
            st.dataframe(display_df, use_container_width=True, height=400)
            st.markdown('</div>', unsafe_allow_html=True)

            # Download button
            csv = result_df[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']].to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "📥 ดาวน์โหลดข้อมูล (CSV)", 
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
    <p>Developed with Strategic Excellence for Operational Efficiency</p>
</div>
""", unsafe_allow_html=True)
