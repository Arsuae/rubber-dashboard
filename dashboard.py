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
# CUSTOM CSS
# ========================================================================================
# ========================================================================================
# CUSTOM CSS (Minimal + Pastel)
# ========================================================================================
st.markdown("""
<style>
  /* Import Google Font */
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

  /* Global */
  .stApp {
    font-family: 'Poppins', sans-serif;
    background-color: #FDFDFD;
    color: #333333;
  }
  .block-container {
    padding: 2rem 1rem;
    max-width: 1200px;
    margin: auto;
  }

  /* Sidebar */
  .css-1d391kg {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E0E0E0;
  }
  .sidebar-section {
    background-color: #FAFAFA;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 8px;
    border: 1px solid #E0E0E0;
  }
  .sidebar-title {
    font-size: 1.1rem;
    font-weight: 500;
    color: #555;
    margin-bottom: 0.75rem;
  }

  /* Header */
  .header-container {
    background-color: #FFF5E6;
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid #FFE0B2;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  .header-title {
    font-size: 2rem;
    font-weight: 600;
    color: #333;
    margin: 0;
  }
  .header-subtitle {
    font-size: 1rem;
    color: #666;
    margin-top: 0.5rem;
  }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background-color: transparent;
    margin-bottom: 1rem;
  }
  .stTabs [data-baseweb="tab"] {
    background-color: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    color: #555;
  }
  .stTabs [aria-selected="true"] {
    background-color: #FFE0B2;
    border-color: #FFCC80;
    color: #333;
  }

  /* Metric Cards */
  .metric-card {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
    margin-bottom: 1rem;
  }
  .metric-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }
  .metric-value {
    font-size: 1.75rem;
    font-weight: 600;
    color: #333;
  }
  .metric-label {
    font-size: 0.9rem;
    color: #777;
  }

  /* Chart Container */
  .chart-container {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
  }
  .chart-title {
    font-size: 1.1rem;
    font-weight: 500;
    color: #333;
    margin-bottom: 1rem;
    text-align: center;
  }

  /* Dataframe/Table */
  .dataframe {
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #E0E0E0;
  }

  /* Search Container */
  .search-container {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
  }

  /* Buttons */
  .stButton>button, .stDownloadButton>button {
    background-color: #FFCC80;
    color: #333;
    border: 1px solid #FFB74D;
    border-radius: 6px;
    padding: 0.5rem 1rem;
  }
  .stButton>button:hover, .stDownloadButton>button:hover {
    background-color: #FFB74D;
    border-color: #FFA726;
  }

  /* Footer */
  .footer {
    text-align: center;
    color: #777;
    font-size: 0.85rem;
    margin-top: 2rem;
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
