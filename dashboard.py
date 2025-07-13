import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import requests
import json
from typing import Dict, List, Optional, Tuple

# ========================================================================================
# APP CONFIGURATION
# ========================================================================================
st.set_page_config(
    page_title="🌳 ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================================
# ENHANCED CSS STYLING
# ========================================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=Kanit:wght@300;400;500;600&display=swap');

    /* Global Theme */
    .stApp {
        font-family: 'Prompt', 'Kanit', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #2c3e50;
    }
    
    /* Main Container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 1.5rem;
        margin: 1rem;
    }

    /* Header Styling */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .dashboard-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #f093fb 0%, #f5576c 100%);
    }
    
    .sidebar-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }

    /* Modern Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.3rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Chart Containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .chart-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
    }

    /* Employee Status Cards */
    .employee-status-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .status-summary-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .status-present { border-left-color: #10b981; background: linear-gradient(135deg, #ecfdf5, #f0fdf4); }
    .status-late { border-left-color: #f59e0b; background: linear-gradient(135deg, #fffbeb, #fefce8); }
    .status-leave { border-left-color: #8b5cf6; background: linear-gradient(135deg, #f5f3ff, #faf5ff); }
    .status-absent { border-left-color: #ef4444; background: linear-gradient(135deg, #fef2f2, #fefefe); }
    
    .status-number {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    
    .status-label {
        font-size: 0.8rem;
        font-weight: 500;
        opacity: 0.8;
    }

    .employee-item {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .employee-item:hover {
        transform: translateX(3px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .employee-name {
        font-weight: 600;
        font-size: 0.9rem;
        color: #2c3e50;
    }
    
    .employee-status {
        font-size: 0.8rem;
        opacity: 0.8;
        margin-top: 0.2rem;
    }

    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    /* Data Table Styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: none !important;
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        font-weight: 600;
        padding: 1rem !important;
        border: none !important;
    }
    
    .dataframe tbody td {
        padding: 0.8rem !important;
        border-bottom: 1px solid #e2e8f0 !important;
        color: #2c3e50 !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #f8fafc !important;
    }

    /* Form Elements */
    .stSelectbox label, .stTextInput label, .stDateInput label, .stMultiSelect label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stSelectbox > div > div > select,
    .stTextInput > div > div > input,
    .stDateInput > div > div > input {
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.6rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    .stSelectbox > div > div > select:focus,
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }

    /* Alert Messages */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }

    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        backdrop-filter: blur(10px);
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .empty-state h3 {
        color: #64748b;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .empty-state p {
        color: #94a3b8;
        font-size: 0.9rem;
    }

    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #e2e8f0;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .dashboard-title { font-size: 2rem; }
        .metric-card { height: 120px; padding: 1rem; }
        .metric-value { font-size: 1.5rem; }
        .chart-container { padding: 1rem; }
    }

    /* Hide Streamlit Elements */
    .viewerBadge_container__1QSob { display: none; }
    .stDeployButton { display: none; }
    footer { display: none; }
    .stDecoration { display: none; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #5a67d8, #6b46c1);
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# DATA LOADING FUNCTIONS
# ========================================================================================

@st.cache_data(ttl=300, show_spinner=False)
def load_rubber_data() -> pd.DataFrame:
    """Load rubber data from Google Sheets with enhanced error handling"""
    try:
        with st.spinner("🔄 กำลังโหลดข้อมูลยางพารา..."):
            url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
            df = pd.read_csv(url, header=None)
            
            # Set column names
            df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
            
            # Data cleaning and type conversion
            df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')
            df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            df['ราคา'] = pd.to_numeric(df['ราคา'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            df['จำนวนเงิน'] = pd.to_numeric(df['จำนวนเงิน'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            
            # Remove rows with invalid data
            df = df.dropna(subset=['วันที่'])
            df = df[df['จำนวนยาง'] > 0]
            
            return df
            
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดข้อมูลยางพาราได้: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60, show_spinner=False)
def load_employee_data() -> pd.DataFrame:
    """Load employee status from Google Apps Script API with timeout handling"""
    try:
        apps_script_url = 'https://script.google.com/macros/s/AKfycbwcURACTMc6xWy-0vPfxiuG4orie0Pp0UafiNIA57uebo33YRvDiUleqihfZ_rw3B1PKw/exec'
        
        response = requests.get(apps_script_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                employees = data['data']
                emp_df = pd.DataFrame(employees)
                emp_df = emp_df[['name', 'status', 'time']].rename(columns={
                    'name': 'ชื่อพนักงาน',
                    'status': 'สถานะ',
                    'time': 'เวลา'
                })
                return emp_df
                
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])
        
    except requests.exceptions.Timeout:
        st.sidebar.warning("⏰ การเชื่อมต่อข้อมูลพนักงานใช้เวลานานกว่าปกติ")
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])
    except Exception as e:
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])

# ========================================================================================
# UTILITY FUNCTIONS
# ========================================================================================

def format_number(value: float, decimal_places: int = 0) -> str:
    """Format number with Thai-style comma separation"""
    if decimal_places == 0:
        return f"{value:,.0f}"
    else:
        return f"{value:,.{decimal_places}f}"

def create_metric_card(icon: str, value: str, label: str, color: str = "#667eea") -> str:
    """Generate HTML for metric card"""
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value" style="color: {color};">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def filter_dataframe(df: pd.DataFrame, selected_date: date, branches: List[str], groups: List[str]) -> pd.DataFrame:
    """Filter dataframe based on selected criteria"""
    if df.empty:
        return df
        
    filtered_df = df[
        (df['วันที่'].dt.date == selected_date) &
        (df['สาขา'].isin(branches)) &
        (df['กอง'].isin(groups))
    ]
    
    return filtered_df

# ========================================================================================
# SESSION STATE INITIALIZATION
# ========================================================================================

def initialize_session_state():
    """Initialize session state variables"""
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = date.today()
    if 'selected_branches' not in st.session_state:
        st.session_state.selected_branches = []
    if 'selected_groups' not in st.session_state:
        st.session_state.selected_groups = []

initialize_session_state()

# ========================================================================================
# SIDEBAR COMPONENTS
# ========================================================================================

def render_sidebar():
    """Render enhanced sidebar with filters and employee status"""
    with st.sidebar:
        # Filters Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">🎛️ ตัวกรองข้อมูล</div>', unsafe_allow_html=True)
        
        # Date selector
        selected_date = st.date_input(
            "📅 เลือกวันที่",
            value=st.session_state.selected_date,
            max_value=date.today(),
            help="เลือกวันที่ที่ต้องการดูข้อมูล"
        )
        st.session_state.selected_date = selected_date

        # Load data for filter options
        df = load_rubber_data()
        
        if not df.empty:
            # Branch filter
            branches = sorted(df['สาขา'].dropna().unique().tolist())
            selected_branches = st.multiselect(
                "🏢 เลือกสาขา",
                options=branches,
                default=st.session_state.selected_branches or branches,
                help="เลือกสาขาที่ต้องการดูข้อมูล"
            )
            st.session_state.selected_branches = selected_branches

            # Group filter
            groups = sorted(df['กอง'].dropna().unique().tolist())
            selected_groups = st.multiselect(
                "📦 เลือกกอง",
                options=groups,
                default=st.session_state.selected_groups or groups,
                help="เลือกกองที่ต้องการดูข้อมูล"
            )
            st.session_state.selected_groups = selected_groups
        
        # Refresh button
        if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True, help="โหลดข้อมูลใหม่"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Employee Status Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">👨‍🌾 สถานะพนักงาน</div>', unsafe_allow_html=True)
        
        emp_df = load_employee_data()
        
        if not emp_df.empty:
            # Count status
            status_counts = {
                'มาทำงาน': len(emp_df[emp_df['สถานะ'] == 'มาทำงาน']),
                'มาสาย': len(emp_df[emp_df['สถานะ'] == 'มาสาย']),
                'ลา': len(emp_df[emp_df['สถานะ'] == 'ลา']),
                'ขาด': len(emp_df[emp_df['สถานะ'] == 'ขาด'])
            }
            
            # Status summary grid
            st.markdown('<div class="employee-status-grid">', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="status-summary-card status-present">
                <div class="status-number" style="color: #10b981;">{status_counts['มาทำงาน']}</div>
                <div class="status-label">มาทำงาน</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="status-summary-card status-late">
                <div class="status-number" style="color: #f59e0b;">{status_counts['มาสาย']}</div>
                <div class="status-label">มาสาย</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="status-summary-card status-leave">
                <div class="status-number" style="color: #8b5cf6;">{status_counts['ลา']}</div>
                <div class="status-label">ลางาน</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="status-summary-card status-absent">
                <div class="status-number" style="color: #ef4444;">{status_counts['ขาด']}</div>
                <div class="status-label">ขาดงาน</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Individual employee list
            st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
            for _, employee in emp_df.iterrows():
                name = employee['ชื่อพนักงาน']
                status = employee['สถานะ']
                time_str = employee.get('เวลา', '')
                
                # Determine status display and styling
                if status == 'มาทำงาน':
                    icon = "🟢"
                    status_text = f"มาทำงาน {time_str}"
                    border_color = "#10b981"
                elif status == 'มาสาย':
                    icon = "🟡"
                    status_text = f"มาสาย {time_str}"
                    border_color = "#f59e0b"
                elif status == 'ลา':
                    icon = "🟣"
                    status_text = "ลางาน"
                    border_color = "#8b5cf6"
                else:
                    icon = "🔴"
                    status_text = "ขาดงาน"
                    border_color = "#ef4444"
                
                st.markdown(f"""
                <div class="employee-item" style="border-left-color: {border_color};">
                    <div class="employee-name">{icon} {name}</div>
                    <div class="employee-status">{status_text}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="employee-item" style="border-left-color: #ef4444;">
                <div class="employee-name">⚠️ ไม่สามารถดึงข้อมูลได้</div>
                <div class="employee-status">กรุณาลองใหม่อีกครั้ง</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# CHART FUNCTIONS
# ========================================================================================

def create_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create enhanced bar chart"""
    fig = px.bar(
        data, 
        x=x_col, 
        y=y_col,
        text=y_col,
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c']
    )
    
    fig.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside',
        textfont=dict(size=12, color='#2c3e50', family='Prompt'),
        hovertemplate=f'<b>%{{x}}</b><br>{y_col}: %{{y:,.0f}}<extra></extra>'
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color='#2c3e50', family='Prompt'),
            x=0.5
        ),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(family="Prompt", color='#2c3e50'),
        showlegend=False,
        xaxis=dict(
            title="",
            showgrid=False,
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title="",
            showgrid=True,
            gridcolor='rgba(102, 126, 234, 0.1)',
            tickfont=dict(size=11)
        )
    )
    
    return fig

def create_pie_chart(data: pd.DataFrame, values_col: str, names_col: str, title: str) -> go.Figure:
    """Create enhanced pie chart"""
    fig = px.pie(
        data, 
        values=values_col, 
        names=names_col,
        hole=0.5,
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4ecdc4']
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=11, color='white', family='Prompt'),
        hovertemplate='<b>%{label}</b><br>จำนวน: %{value:,.0f}<br>สัดส่วน: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color='#2c3e50', family='Prompt'),
            x=0.5
        ),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(family="Prompt", color='#2c3e50'),
        showlegend=False
    )
    
    return fig

def create_line_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create enhanced line chart for trends"""
    fig = px.line(
        data,
        x=x_col,
        y=y_col,
        markers=True,
        color_discrete_sequence=['#667eea']
    )
    
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8, color='#764ba2'),
        hovertemplate=f'<b>%{{x}}</b><br>{y_col}: %{{y:,.0f}}<extra></extra>'
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color='#2c3e50', family='Prompt'),
            x=0.5
        ),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(family="Prompt", color='#2c3e50'),
        showlegend=False,
        xaxis=dict(
            title="",
            showgrid=False,
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title="",
            showgrid=True,
            gridcolor='rgba(102, 126, 234, 0.1)',
            tickfont=dict(size=11)
        )
    )
    
    return fig

# ========================================================================================
# MAIN CONTENT FUNCTIONS
# ========================================================================================

def render_empty_state(message: str = "ไม่มีข้อมูล", description: str = "ไม่มีข้อมูลในวันที่ สาขา หรือกองที่เลือก"):
    """Render beautiful empty state"""
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">📊</div>
        <h3>{message}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_overview_tab(df_filtered: pd.DataFrame):
    """Render enhanced overview tab"""
    if df_filtered.empty:
        render_empty_state()
        return
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_rubber = df_filtered['จำนวนยาง'].sum()
    total_revenue = df_filtered['จำนวนเงิน'].sum()
    total_customers = df_filtered['ชื่อลูกค้า'].count()
    avg_price = df_filtered['ราคา'].mean()
    
    with col1:
        st.markdown(create_metric_card("⚖️", format_number(total_rubber, 1), "กิโลกรัม", "#667eea"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card("💰", f"฿{format_number(total_revenue)}", "รายได้รวม", "#10b981"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card("👥", format_number(total_customers), "ลูกค้าทั้งหมด", "#f59e0b"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card("📊", f"฿{format_number(avg_price, 2)}", "ราคาเฉลี่ย", "#8b5cf6"), unsafe_allow_html=True)

    # Charts Row
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        bar_data = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
        if not bar_data.empty:
            fig_bar = create_bar_chart(bar_data, 'สาขา', 'จำนวนยาง', "📊 จำนวนยางตามสาขา (กก.)")
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_chart2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        pie_data = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
        if not pie_data.empty:
            fig_pie = create_pie_chart(pie_data, 'จำนวนเงิน', 'สาขา', "💰 สัดส่วนรายได้ตามสาขา")
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Additional insights
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🔍 ข้อมูลเชิงลึก</div>', unsafe_allow_html=True)
    
    col_insight1, col_insight2, col_insight3 = st.columns(3)
    
    with col_insight1:
        if not df_filtered.empty:
            top_customer = df_filtered.nlargest(1, 'จำนวนยาง')
            if not top_customer.empty:
                customer_name = top_customer.iloc[0]['ชื่อลูกค้า']
                customer_amount = top_customer.iloc[0]['จำนวนยาง']
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #10b981, #059669); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
                    <h4 style='margin: 0 0 0.5rem 0; color: white;'>🏆 ลูกค้ายอดสูงสุด</h4>
                    <p style='margin: 0; font-weight: 600; font-size: 1.1rem;'>{customer_name}</p>
                    <p style='margin: 0.3rem 0 0 0; opacity: 0.9;'>{format_number(customer_amount, 1)} กก.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col_insight2:
        price_range = df_filtered['ราคา'].max() - df_filtered['ราคา'].min()
        price_min = df_filtered['ราคา'].min()
        price_max = df_filtered['ราคา'].max()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
            <h4 style='margin: 0 0 0.5rem 0; color: white;'>📈 ช่วงราคา</h4>
            <p style='margin: 0; font-weight: 600; font-size: 1.1rem;'>฿{format_number(price_min, 2)} - ฿{format_number(price_max, 2)}</p>
            <p style='margin: 0.3rem 0 0 0; opacity: 0.9;'>ต่างกัน ฿{format_number(price_range, 2)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_insight3:
        total_branches = df_filtered['สาขา'].nunique()
        total_groups = df_filtered['กอง'].nunique()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb, #f5576c); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
            <h4 style='margin: 0 0 0.5rem 0; color: white;'>🏢 ความครอบคลุม</h4>
            <p style='margin: 0; font-weight: 600; font-size: 1.1rem;'>{total_branches} สาขา</p>
            <p style='margin: 0.3rem 0 0 0; opacity: 0.9;'>{total_groups} กอง</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_summary_tab(df_filtered: pd.DataFrame):
    """Render enhanced summary tab"""
    if df_filtered.empty:
        render_empty_state()
        return
    
    col_summary1, col_summary2 = st.columns(2)
    
    with col_summary1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📦 สรุปข้อมูลตามกอง</div>', unsafe_allow_html=True)
        
        by_group = df_filtered.groupby('กอง').agg({
            'จำนวนยาง': 'sum', 
            'จำนวนเงิน': 'sum', 
            'ชื่อลูกค้า': 'count',
            'ราคา': 'mean'
        }).reset_index()
        
        by_group = by_group.rename(columns={
            'ชื่อลูกค้า': 'จำนวนลูกค้า',
            'ราคา': 'ราคาเฉลี่ย'
        })
        
        # Format columns for display
        by_group['จำนวนยาง'] = by_group['จำนวนยาง'].apply(lambda x: f"{x:,.1f}")
        by_group['จำนวนเงิน'] = by_group['จำนวนเงิน'].apply(lambda x: f"฿{x:,.0f}")
        by_group['ราคาเฉลี่ย'] = by_group['ราคาเฉลี่ย'].apply(lambda x: f"฿{x:,.2f}")
        
        st.dataframe(by_group, use_container_width=True, height=300)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_summary2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏢 สรุปข้อมูลตามสาขา</div>', unsafe_allow_html=True)
        
        by_branch = df_filtered.groupby('สาขา').agg({
            'จำนวนยาง': 'sum', 
            'จำนวนเงิน': 'sum', 
            'ชื่อลูกค้า': 'count', 
            'ราคา': 'mean'
        }).reset_index()
        
        by_branch = by_branch.rename(columns={
            'ชื่อลูกค้า': 'จำนวนลูกค้า',
            'ราคา': 'ราคาเฉลี่ย'
        })
        
        # Format columns for display
        by_branch['จำนวนยาง'] = by_branch['จำนวนยาง'].apply(lambda x: f"{x:,.1f}")
        by_branch['จำนวนเงิน'] = by_branch['จำนวนเงิน'].apply(lambda x: f"฿{x:,.0f}")
        by_branch['ราคาเฉลี่ย'] = by_branch['ราคาเฉลี่ย'].apply(lambda x: f"฿{x:,.2f}")
        
        st.dataframe(by_branch, use_container_width=True, height=300)
        st.markdown('</div>', unsafe_allow_html=True)

    # Performance Analysis
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 การวิเคราะห์ประสิทธิภาพ</div>', unsafe_allow_html=True)
    
    # Top customers table
    st.subheader("🏆 ลูกค้าชั้นนำ (Top 10)")
    top_customers = df_filtered.nlargest(10, 'จำนวนยาง')[['ชื่อลูกค้า', 'สาขา', 'กอง', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']].copy()
    
    # Format for display
    top_customers['จำนวนยาง'] = top_customers['จำนวนยาง'].apply(lambda x: f"{x:,.1f}")
    top_customers['ราคา'] = top_customers['ราคา'].apply(lambda x: f"฿{x:,.2f}")
    top_customers['จำนวนเงิน'] = top_customers['จำนวนเงิน'].apply(lambda x: f"฿{x:,.0f}")
    
    st.dataframe(top_customers, use_container_width=True, height=300)
    st.markdown('</div>', unsafe_allow_html=True)

def render_details_tab(df_filtered: pd.DataFrame):
    """Render enhanced details tab with search and filtering"""
    if df_filtered.empty:
        render_empty_state()
        return
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📋 รายการลูกค้าทั้งหมด</div>', unsafe_allow_html=True)
    
    # Search and filter controls
    col_search1, col_search2, col_search3 = st.columns([2, 1, 1])
    
    with col_search1:
        search_keyword = st.text_input(
            "🔍 ค้นหาชื่อลูกค้า", 
            placeholder="กรอกชื่อลูกค้าที่ต้องการค้นหา...",
            help="ค้นหาจากชื่อลูกค้า"
        )
    
    with col_search2:
        sort_options = {
            "จำนวนยาง": "จำนวนยาง (มาก-น้อย)",
            "จำนวนเงิน": "จำนวนเงิน (มาก-น้อย)", 
            "ชื่อลูกค้า": "ชื่อลูกค้า (A-Z)",
            "ราคา": "ราคา (มาก-น้อย)"
        }
        sort_by = st.selectbox("📊 เรียงตาม", options=list(sort_options.keys()), format_func=lambda x: sort_options[x])
    
    with col_search3:
        min_amount = st.number_input(
            "จำนวนยางขั้นต่ำ (กก.)", 
            min_value=0.0, 
            value=0.0, 
            step=10.0,
            help="กรองข้อมูลตามจำนวนยางขั้นต่ำ"
        )
    
    # Filter data based on search criteria
    result_df = df_filtered.copy()
    
    if search_keyword:
        result_df = result_df[result_df['ชื่อลูกค้า'].str.contains(search_keyword, case=False, na=False)]
    
    if min_amount > 0:
        result_df = result_df[result_df['จำนวนยาง'] >= min_amount]
    
    # Sort data
    if sort_by in ["จำนวนยาง", "จำนวนเงิน", "ราคา"]:
        result_df = result_df.sort_values(sort_by, ascending=False)
    else:
        result_df = result_df.sort_values(sort_by)

    if result_df.empty:
        render_empty_state("🔍 ไม่พบข้อมูล", "ไม่พบข้อมูลลูกค้าตามเงื่อนไขที่ค้นหา")
    else:
        # Display summary stats
        total_found = len(result_df)
        total_rubber_found = result_df['จำนวนยาง'].sum()
        total_revenue_found = result_df['จำนวนเงิน'].sum()
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem;'>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; text-align: center;'>
                <div>
                    <div style='font-size: 1.5rem; font-weight: 700;'>{format_number(total_found)}</div>
                    <div style='opacity: 0.9;'>รายการ</div>
                </div>
                <div>
                    <div style='font-size: 1.5rem; font-weight: 700;'>{format_number(total_rubber_found, 1)}</div>
                    <div style='opacity: 0.9;'>กิโลกรัม</div>
                </div>
                <div>
                    <div style='font-size: 1.5rem; font-weight: 700;'>฿{format_number(total_revenue_found)}</div>
                    <div style='opacity: 0.9;'>รายได้รวม</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Prepare display dataframe
        display_df = result_df[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']].copy()
        
        # Format numbers for display
        display_df['จำนวนยาง'] = display_df['จำนวนยาง'].apply(lambda x: f"{x:,.1f}")
        display_df['ราคา'] = display_df['ราคา'].apply(lambda x: f"฿{x:,.2f}")
        display_df['จำนวนเงิน'] = display_df['จำนวนเงิน'].apply(lambda x: f"฿{x:,.0f}")
        
        # Display data table
        st.dataframe(
            display_df, 
            use_container_width=True, 
            height=500,
            column_config={
                "สาขา": st.column_config.TextColumn("🏢 สาขา", width="small"),
                "กอง": st.column_config.TextColumn("📦 กอง", width="small"),
                "ชื่อลูกค้า": st.column_config.TextColumn("👤 ชื่อลูกค้า", width="medium"),
                "จำนวนยาง": st.column_config.TextColumn("⚖️ จำนวนยาง (กก.)", width="small"),
                "ราคา": st.column_config.TextColumn("💰 ราคา", width="small"),
                "จำนวนเงิน": st.column_config.TextColumn("💵 จำนวนเงิน", width="small")
            }
        )

        # Download functionality
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            # CSV download
            csv_data = result_df[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่']].copy()
            csv_data['วันที่'] = csv_data['วันที่'].dt.strftime('%d/%m/%Y')
            csv = csv_data.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                "📥 ดาวน์โหลด CSV", 
                csv, 
                f"rubber_data_{st.session_state.selected_date.strftime('%Y%m%d')}.csv", 
                "text/csv",
                use_container_width=True,
                help="ดาวน์โหลดข้อมูลในรูปแบบ CSV"
            )
        
        with col_download2:
            # Excel download (if needed)
            import io
            from io import BytesIO
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                csv_data.to_excel(writer, sheet_name='RubberData', index=False)
            excel_data = output.getvalue()
            
            st.download_button(
                "📊 ดาวน์โหลด Excel",
                excel_data,
                f"rubber_data_{st.session_state.selected_date.strftime('%Y%m%d')}.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                help="ดาวน์โหลดข้อมูลในรูปแบบ Excel"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# MAIN APPLICATION
# ========================================================================================

def main():
    """Main application function"""
    
    # Render header
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">🌳 ลิตาการยาง Dashboard</h1>
        <p class="dashboard-subtitle">ระบบจัดการข้อมูลยางพาราแบบเรียลไทม์ | Real-time Rubber Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Load and filter data
    df = load_rubber_data()
    
    if not df.empty and st.session_state.selected_branches and st.session_state.selected_groups:
        df_filtered = filter_dataframe(
            df, 
            st.session_state.selected_date, 
            st.session_state.selected_branches, 
            st.session_state.selected_groups
        )
    else:
        df_filtered = pd.DataFrame()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "📋 สรุปข้อมูล", "📁 รายการละเอียด"])
    
    with tab1:
        render_overview_tab(df_filtered)
    
    with tab2:
        render_summary_tab(df_filtered)
    
    with tab3:
        render_details_tab(df_filtered)
    
    # Footer
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    '>
        <p style='margin: 0; font-weight: 500;'>
            🌳 ลิตาการยาง Dashboard © 2025 | 
            อัปเดตล่าสุด: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | 
            Built with ❤️ using Streamlit
        </p>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;'>
            Developed for Operational Excellence & Strategic Decision Making
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========================================================================================
# RUN APPLICATION
# ========================================================================================

if __name__ == "__main__":
    main()
