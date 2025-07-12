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
    initial_sidebar_state="collapsed"  # Collapsed by default for mobile
)

# ========================================================================================
# MOBILE-OPTIMIZED CSS
# ========================================================================================
st.markdown("""
<style>
  /* Import Google Fonts */
  @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=Kanit:wght@300;400;500;600&display=swap');

  /* Global Styles */
  * {
    box-sizing: border-box;
  }
  
  .stApp {
    font-family: 'Prompt', 'Kanit', sans-serif;
    background: linear-gradient(to bottom, #FFF9F3 0%, #F5F3FF 100%);
    min-height: 100vh;
    color: #2C3E50;
  }
  
  .block-container {
    padding: 0.5rem;
    max-width: 100%;
    margin: auto;
  }



  /* Mobile-First Header */
  .header-container {
    background: linear-gradient(135deg, #FFE5E5 0%, #E8E5FF 50%, #E5F3FF 100%);
    padding: 0.8rem;
    border-radius: 12px;
    border: 1px solid #FFD6E0;
    margin-bottom: 0.8rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(255, 182, 193, 0.15);
  }
  
  .header-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #2C3E50;
    margin: 0;
    word-wrap: break-word;
  }
  
  .header-subtitle {
    font-size: 0.8rem;
    color: #34495E;
    margin-top: 0.2rem;
    font-weight: 500;
    word-wrap: break-word;
  }

  /* Mobile-Optimized Sidebar */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFE5EC 0%, #E8E5FF 100%);
    border-right: 2px solid #FFD6E0;
    width: 280px !important;
  }
  
section[data-testid="stSidebar"] {
    background: #F5F5F5 !important; /* Light gray instead of gradient */
    border-right: 1px solid #E0E0E0;
}

.sidebar-section {
    background: #FFFFFF !important; /* Pure white background */
    padding: 1rem;
    margin-bottom: 0.8rem;
    border-radius: 10px;
    border: 1px solid #E0E0E0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
  
  .sidebar-title {
    font-size: 1rem;
    font-weight: 600;
    color: #2C3E50;
    margin-bottom: 0.5rem;
    text-align: center;
    word-wrap: break-word;
  }

  /* Mobile Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 0.3rem;
    margin-bottom: 0.8rem;
    border: 1px solid #FFE0EC;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
/* Fix tab text that might be cut off */
.stTabs [data-baseweb="tab"] {
    padding: 0.5rem 1rem !important;
    min-width: auto !important;
    font-size: 0.85rem !important;
}
  
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FFB6C1 0%, #DDA0DD 100%);
    border-color: #FF69B4;
    color: #FFFFFF;
    box-shadow: 0 2px 8px rgba(255, 105, 180, 0.3);
  }

  /* Mobile Metric Cards */
  .metric-card-mobile {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 100%);
    border: 1px solid #FFE0EC;
    border-radius: 10px;
    padding: 0.6rem;
    text-align: center;
    margin-bottom: 0.4rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 6px rgba(255, 182, 193, 0.1);
    min-height: 75px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .metric-icon-mobile {
    font-size: 1.2rem;
    margin-bottom: 0.1rem;
  }

  .metric-value-mobile {
    font-size: 1.1rem;
    font-weight: 700;
    color: #E91E63;
    line-height: 1.1;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }

  .metric-label-mobile {
    font-size: 0.7rem;
    color: #2C3E50;
    font-weight: 500;
    margin-top: 0.1rem;
    word-wrap: break-word;
  }

/* Fix chart containers */
.chart-container-mobile, .chart-container-compact {
    background: #FFFFFF !important;
    border: 1px solid #E0E0E0;
}

/* Employee status cards - High contrast */
.employee-card {
    background: #FFFFFF !important;
    padding: 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.3rem;
    border-left: 3px solid #333;
    color: #000000 !important; /* Black text */
    font-size: 0.85rem;
}

.employee-card b {
    color: #000000 !important;
    font-weight: 700;
    font-size: 0.9rem;
}

.employee-card small {
    color: #333333 !important;
    font-size: 0.75rem;
    display: block;
    margin-top: 0.1rem;
}

/* Fix specific employee card backgrounds */
.employee-done {
    background: #E8F5E9 !important;
    border-left-color: #4CAF50;
}

.employee-late {
    background: #FFF3E0 !important;
    border-left-color: #FF9800;
}

.employee-leave {
    background: #F3E5F5 !important;
    border-left-color: #9C27B0;
}

.employee-offline {
    background: #FFEBEE !important;
    border-left-color: #F44336;
}


  /* Mobile Data Table */
/* Fix table text overflow */
.dataframe {
    table-layout: fixed !important;
    width: 100% !important;
}

.dataframe th, .dataframe td {
    color: #000000 !important;
    background-color: #FFFFFF !important;
    padding: 0.5rem !important;
    font-size: 0.85rem !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 120px;
}

.dataframe thead th {
    background-color: #333333 !important;
    color: #FFFFFF !important;
    font-weight: 600;
    position: sticky;
    top: 0;
    z-index: 10;
}

.dataframe tbody tr:nth-child(even) {
    background-color: #F5F5F5 !important;
}

.dataframe tbody tr:hover {
    background-color: #E0E0E0 !important;
}

  /* Mobile Search Container */
/* Fix search container */
.search-container {
    background: #FFFFFF !important;
    border: 1px solid #E0E0E0;
}

.search-container h3 {
    color: #000000 !important;
}

/* Fix input fields text visibility */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stMultiSelect > div > div > div,
.stDateInput > div > div > input {
    background: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #CCCCCC !important;
    font-weight: 500 !important;
}

/* Fix all labels */
.stTextInput label, 
.stSelectbox label, 
.stMultiSelect label, 
.stDateInput label,
label {
    color: #000000 !important;
    font-weight: 600 !important;
}

  /* Mobile Buttons */
  .stButton > button {
    background: linear-gradient(135deg, #FFB6C1 0%, #DDA0DD 100%);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 6px rgba(255, 105, 180, 0.3);
    width: 100%;
  }
  
  .stDownloadButton > button {
    background: linear-gradient(135deg, #98FB98 0%, #90EE90 100%);
    color: #1B5E20;
    border: 1px solid #90EE90;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.3s ease;
    width: 100%;
  }

  /* Mobile Footer */
  .footer {
    background: linear-gradient(135deg, #FFE5E5 0%, #E8E5FF 100%);
    border: 1px solid #FFE0EC;
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
    color: #2C3E50;
    font-size: 0.75rem;
    margin-top: 1rem;
    box-shadow: 0 2px 6px rgba(255, 182, 193, 0.1);
  }
  
  .footer p {
    color: #2C3E50 !important;
    font-weight: 500;
    margin: 0.2rem 0;
    word-wrap: break-word;
  }

/* Fix empty state messages */
.empty-state {
    background: #FFFFFF !important;
    border: 1px solid #E0E0E0;
}
  
.empty-state h3, .empty-state p {
    color: #000000 !important;
}

  /* Hide Plotly Toolbar on Mobile */
  .modebar {
    display: none !important;
  }

/* Responsive text sizing */
@media (max-width: 768px) {
    .header-title {
        font-size: 1.2rem !important;
        padding: 0 0.5rem;
    }
    
    .header-subtitle {
        font-size: 0.75rem !important;
        padding: 0 0.5rem;
    }
    
    .dataframe th, .dataframe td {
        font-size: 0.75rem !important;
        padding: 0.3rem !important;
        max-width: 100px;
    }
    
    /* Prevent horizontal scroll */
    * {
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }
}
    
* Fix metric cards text */
.metric-card-mobile, .metric-card-compact {
    background: #FFFFFF !important;
    border: 1px solid #E0E0E0;
    color: #000000 !important;
}

.metric-value-mobile, .metric-value-small {
    color: #000000 !important;
    font-weight: 700;
}

.metric-label-mobile, .metric-label-small {
    color: #333333 !important;
    font-weight: 600;
}
    
    .dataframe {
      font-size: 0.85rem !important;
    }
    
    .dataframe td, .dataframe th {
      max-width: 150px;
      padding: 0.4rem !important;
    }
  }

  @media (min-width: 1024px) {
    .block-container {
      padding: 1.5rem;
      max-width: 1400px;
    }
    
    .header-title {
      font-size: 1.8rem;
    }
    
    .header-subtitle {
      font-size: 1rem;
    }
    
    .metric-card-mobile {
      min-height: 90px;
    }
    
    .dataframe th, .dataframe td {
        font-size: 0.75rem !important;
        padding: 0.3rem !important;
        max-width: 100px;
    }
  }

  @media (prefers-contrast: high) {
    * {
        color: #000000 !important;
    }
    
    .stApp {
        background: #FFFFFF !important;
    }
}

  /* Prevent horizontal scroll */
  html, body {
    overflow-x: hidden;
    width: 100%;
  }
  
  /* Ensure all content fits within viewport */
  .main > div {
    max-width: 100%;
    overflow-x: hidden;
  }
  
  /* Fix Streamlit default margins on mobile */
  @media (max-width: 768px) {
    .main > div {
      padding: 0 !important;
    }
    
    section.main > div {
      padding: 0 0.5rem !important;
    }
  }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# DETECT MOBILE DEVICE
# ========================================================================================
def is_mobile():
    """Simple mobile detection based on viewport width"""
    return st.session_state.get('viewport_width', 768) < 768

# ========================================================================================
# LOAD DATA FUNCTIONS (Same as before)
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
            st.markdown(f"<div style='text-align: center; padding: 0.4rem; background: rgba(76,175,80,0.1); border-radius: 6px; margin-bottom: 0.4rem;'><b style='color: #4CAF50; font-size: 1rem;'>{status_counts['มาทำงาน']}</b><br><small style='color: #2C3E50; font-size: 0.7rem;'>มาทำงาน</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; padding: 0.4rem; background: rgba(242,153,74,0.1); border-radius: 6px;'><b style='color: #f2994a; font-size: 1rem;'>{status_counts['มาสาย']}</b><br><small style='color: #2C3E50; font-size: 0.7rem;'>มาสาย</small></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='text-align: center; padding: 0.4rem; background: rgba(102,126,234,0.1); border-radius: 6px; margin-bottom: 0.4rem;'><b style='color: #667eea; font-size: 1rem;'>{status_counts['ลา']}</b><br><small style='color: #2C3E50; font-size: 0.7rem;'>ลางาน</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; padding: 0.4rem; background: rgba(244,67,54,0.1); border-radius: 6px;'><b style='color: #f44336; font-size: 1rem;'>{status_counts['ขาด']}</b><br><small style='color: #2C3E50; font-size: 0.7rem;'>ขาดงาน</small></div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 0.6rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        
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
            
            st.markdown(f'<div class="{card_class}"><b>{name}</b><small>{status_text}</small></div>', unsafe_allow_html=True)
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
# TAB 1: Overview Dashboard (Mobile Optimized)
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
        # Mobile-optimized metrics - 2x2 grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card-mobile">
                <div class="metric-icon-mobile">⚖️</div>
                <div class="metric-value-mobile">{df_filtered['จำนวนยาง'].sum():,.0f}</div>
                <div class="metric-label-mobile">กิโลกรัม</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card-mobile">
                <div class="metric-icon-mobile">👥</div>
                <div class="metric-value-mobile">{df_filtered['ชื่อลูกค้า'].count():,.0f}</div>
                <div class="metric-label-mobile">ลูกค้าทั้งหมด</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card-mobile">
                <div class="metric-icon-mobile">💰</div>
                <div class="metric-value-mobile">฿{df_filtered['จำนวนเงิน'].sum()/1000:.1f}K</div>
                <div class="metric-label-mobile">รายได้รวม</div>
            </div>
            """, unsafe_allow_html=True)
            
            avg_price = df_filtered['ราคา'].mean()
            st.markdown(f"""
            <div class="metric-card-mobile">
                <div class="metric-icon-mobile">📊</div>
                <div class="metric-value-mobile">฿{avg_price:,.1f}</div>
                <div class="metric-label-mobile">ราคาเฉลี่ย</div>
            </div>
            """, unsafe_allow_html=True)

        # Charts - Stack vertically on mobile
        st.markdown('<div class="chart-container-mobile">', unsafe_allow_html=True)
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
                textfont_size=10
            )
            fig_bar.update_layout(
                height=250,
                margin=dict(l=0, r=0, t=30, b=0),
                title="จำนวนยางตามสาขา (กก.)",
                title_font_size=12,
                title_font_color='#2C3E50',
                font_family="Prompt",
                plot_bgcolor='rgba(255,255,255,0)',
                paper_bgcolor='rgba(255,255,255,0)',
                font_color='#2C3E50',
                showlegend=False,
                xaxis_title="",
                yaxis_title="",
                xaxis_tickfont_size=10,
                yaxis_tickfont_size=10
            )
            fig_bar.update_xaxes(showgrid=False)
            fig_bar.update_yaxes(showgrid=True, gridcolor='rgba(255,224,236,0.5)')
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container-mobile">', unsafe_allow_html=True)
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
                textfont_size=10
            )
            fig_pie.update_layout(
                height=250,
                margin=dict(l=0, r=0, t=30, b=0),
                title="สัดส่วนรายได้ตามสาขา",
                title_font_size=12,
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
# TAB 2: Summary (Mobile Optimized)
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
        # Stack tables vertically on mobile
        st.markdown('<div class="chart-container-mobile">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #2C3E50; font-size: 1rem; margin-bottom: 0.8rem;">📦 สรุปข้อมูลตามกอง</h3>', unsafe_allow_html=True)
        by_gong = df_filtered.groupby('กอง').agg({
            'จำนวนยาง': 'sum', 
            'จำนวนเงิน': 'sum', 
            'ชื่อลูกค้า': 'count'
        }).reset_index()
        by_gong = by_gong.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า'})
        by_gong['จำนวนยาง'] = by_gong['จำนวนยาง'].round(1)
        by_gong['จำนวนเงิน'] = by_gong['จำนวนเงิน'].round(0)
        st.dataframe(by_gong, use_container_width=True, height=150)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-container-mobile">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #2C3E50; font-size: 1rem; margin-bottom: 0.8rem;">🏢 สรุปข้อมูลตามสาขา</h3>', unsafe_allow_html=True)
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
        st.dataframe(by_branch, use_container_width=True, height=150)
        st.markdown('</div>', unsafe_allow_html=True)

        # Mobile-optimized analysis cards
        st.markdown('<div class="chart-container-mobile">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #2C3E50; font-size: 1rem; margin-bottom: 0.8rem;">📈 การวิเคราะห์เพิ่มเติม</h3>', unsafe_allow_html=True)
        
        # Stack analysis cards vertically on mobile
        top_customer = df_filtered.nlargest(1, 'จำนวนยาง')
        if not top_customer.empty:
            st.markdown(f"""
            <div style='background: #E8F5E9; padding: 0.8rem; border-radius: 6px; border: 1px solid #C8E6C9; margin-bottom: 0.5rem;'>
                <h4 style='color: #2E7D32; margin: 0; font-size: 0.85rem;'>🏆 ลูกค้ายอดสูงสุด</h4>
                <p style='margin: 0.3rem 0 0 0; font-weight: 600; color: #1B5E20; font-size: 0.9rem; word-wrap: break-word;'>{top_customer.iloc[0]['ชื่อลูกค้า']}</p>
                <p style='margin: 0; color: #388E3C; font-size: 0.8rem;'>{top_customer.iloc[0]['จำนวนยาง']:,.1f} กก.</p>
            </div>
            """, unsafe_allow_html=True)
        
        price_range = df_filtered['ราคา'].max() - df_filtered['ราคา'].min()
        st.markdown(f"""
        <div style='background: #E3F2FD; padding: 0.8rem; border-radius: 6px; border: 1px solid #BBDEFB; margin-bottom: 0.5rem;'>
            <h4 style='color: #1565C0; margin: 0; font-size: 0.85rem;'>📊 ช่วงราคา</h4>
            <p style='margin: 0.3rem 0 0 0; font-weight: 600; color: #0D47A1; font-size: 0.9rem;'>฿{df_filtered['ราคา'].min():.2f} - ฿{df_filtered['ราคา'].max():.2f}</p>
            <p style='margin: 0; color: #1976D2; font-size: 0.8rem;'>ต่างกัน ฿{price_range:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        total_branches = df_filtered['สาขา'].nunique()
        total_groups = df_filtered['กอง'].nunique()
        st.markdown(f"""
        <div style='background: #F3E5F5; padding: 0.8rem; border-radius: 6px; border: 1px solid #E1BEE7;'>
            <h4 style='color: #6A1B9A; margin: 0; font-size: 0.85rem;'>🏢 ความครอบคลุม</h4>
            <p style='margin: 0.3rem 0 0 0; font-weight: 600; color: #4A148C; font-size: 0.9rem;'>{total_branches} สาขา, {total_groups} กอง</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB 3: Detailed List (Mobile Optimized)
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
        
        # Stack search inputs vertically on mobile
        keyword = st.text_input("🔍 ค้นหาชื่อลูกค้า", placeholder="กรอกชื่อลูกค้า...", label_visibility="collapsed")
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
            <div style='background: #F5F5F5; padding: 0.6rem; border-radius: 6px; margin-bottom: 0.8rem;'>
                <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
                    <span style='color: #2C3E50; font-weight: 500; font-size: 0.85rem;'>พบ {len(result_df)} รายการ</span>
                    <span style='color: #666; font-size: 0.8rem;'>{result_df['จำนวนยาง'].sum():,.0f} กก. | ฿{result_df['จำนวนเงิน'].sum():,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Prepare display dataframe with mobile-friendly columns
            result_df = result_df.reset_index(drop=True)
            # Show only essential columns on mobile
            display_df = result_df[['ชื่อลูกค้า', 'จำนวนยาง', 'จำนวนเงิน', 'สาขา']].copy()
            
            # Format numbers
            display_df['จำนวนยาง'] = display_df['จำนวนยาง'].apply(lambda x: f"{x:,.0f}")
            display_df['จำนวนเงิน'] = display_df['จำนวนเงิน'].apply(lambda x: f"฿{x:,.0f}")
            
            st.markdown('<div class="chart-container-mobile">', unsafe_allow_html=True)
            st.dataframe(display_df, use_container_width=True, height=300)
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
    <p>🌳 ลิตาการยาง Dashboard © 2025</p>
    <p>อัปเดต: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
</div>
""", unsafe_allow_html=True)
