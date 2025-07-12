import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, time
import io
import requests
import json

# ========================================================================================
# PAGE CONFIG
# การตั้งค่าหน้าเว็บหลัก
# ========================================================================================
st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================================
# CUSTOM CSS (Minimal Pastel Theme)
# CSS สำหรับปรับแต่งหน้าตาให้เป็นสไตล์มินิมอล พาสเทล
# ========================================================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    :root {
        --primary-color: #A7C7E7; /* Baby Blue */
        --secondary-color: #B2D3C2; /* Sage Green */
        --background-color: #F8F9FA;
        --card-bg-color: #FFFFFF;
        --text-color: #495057;
        --light-text-color: #6C757D;
        --border-color: #DEE2E6;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        --border-radius: 12px;
    }

    .stApp {
        font-family: 'Noto Sans Thai', sans-serif;
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Header Styles */
    .header-container {
        background-color: var(--card-bg-color);
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
        border-left: 8px solid var(--primary-color);
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-color);
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: var(--light-text-color);
        margin: 0.25rem 0 0 0;
        font-weight: 400;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background-color: var(--card-bg-color);
        border-right: 1px solid var(--border-color);
    }
    
    .sidebar-section {
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 1.5rem;
        background-color: #F8F9FA;
    }
    
    .sidebar-title {
        color: var(--text-color);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: left;
    }
    
    .employee-card {
        background: var(--card-bg-color);
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.6rem;
        border-left: 5px solid;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .employee-card:hover {
        transform: translateX(3px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.07);
    }
    
    .employee-card[data-status="มาทำงาน"] { border-left-color: #A8D8B9; } /* Pastel Green */
    .employee-card[data-status="มาสาย"] { border-left-color: #FDDDA0; } /* Pastel Yellow */
    .employee-card[data-status="ลา"] { border-left-color: #D1C4E9; } /* Pastel Purple */
    .employee-card[data-status="ขาด"] { border-left-color: #F8BBD0; } /* Pastel Pink */
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: transparent;
        border-bottom: 2px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        padding: 0.8rem 1.5rem;
        border: none;
        font-weight: 500;
        color: var(--light-text-color);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E9ECEF;
        color: var(--text-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--card-bg-color);
        color: var(--primary-color);
        font-weight: 600;
        border-bottom: 2px solid var(--primary-color);
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: var(--card-bg-color);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.07);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--light-text-color);
        font-weight: 500;
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        line-height: 1;
    }
    
    /* Chart & Data Container */
    .content-container {
        background-color: var(--card-bg-color);
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
    }
    
    .content-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 1.5rem;
        text-align: left;
    }
    
    /* Data Table */
    .stDataFrame {
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        filter: brightness(105%);
        box-shadow: 0 2px 8px rgba(167, 199, 231, 0.5);
    }

    .stDownloadButton button {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.8rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton button:hover {
        filter: brightness(105%);
        box-shadow: 0 2px 8px rgba(178, 211, 194, 0.5);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: var(--light-text-color);
        margin-top: 3rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# LOAD DATA
# ฟังก์ชันสำหรับโหลดข้อมูล
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

@st.cache_data(ttl=60)
def load_employee_status_from_apps_script():
    try:
        apps_script_url = 'https://script.google.com/macros/s/AKfycbwcURACTMc6xWy-0vPfxiuG4orie0Pp0UafiNIA57uebo33YRvDiUleqihfZ_rw3B1PKw/exec'
        response = requests.get(apps_script_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('success'):
            emp_df = pd.DataFrame(data.get('data', []))
            if not emp_df.empty:
                return emp_df.rename(columns={'name': 'ชื่อพนักงาน', 'status': 'สถานะ', 'time': 'เวลา'})
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])
    except requests.exceptions.RequestException as e:
        st.warning(f"ไม่สามารถเชื่อมต่อ API พนักงานได้: {e}")
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูลพนักงาน: {str(e)}")
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ", "เวลา"])

# ========================================================================================
# STATE HANDLING
# การจัดการสถานะของแอปพลิเคชัน
# ========================================================================================
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = date.today()
if 'selected_branches' not in st.session_state:
    st.session_state.selected_branches = []
if 'selected_groups' not in st.session_state:
    st.session_state.selected_groups = []

# ========================================================================================
# SIDEBAR CONTROLS
# ส่วนควบคุมในแถบด้านข้าง
# ========================================================================================
with st.sidebar:
    st.markdown('<h1 style="font-weight: 700; font-size: 1.8rem;">ลิตาการยาง</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6C757D; margin-top: -10px;">เมนูควบคุม</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">🎛️ ตัวกรองข้อมูล</h3>', unsafe_allow_html=True)
    
    selected_date = st.date_input("📅 เลือกวันที่", value=st.session_state.selected_date)
    st.session_state.selected_date = selected_date

    df = load_data()
    
    if not df.empty:
        branches = sorted(df['สาขา'].dropna().unique().tolist())
        selected_branches = st.multiselect("🏢 เลือกสาขา", options=branches, default=st.session_state.selected_branches or branches)
        st.session_state.selected_branches = selected_branches

        groups = sorted(df['กอง'].dropna().unique().tolist())
        selected_groups = st.multiselect("📦 เลือกกอง", options=groups, default=st.session_state.selected_groups or groups)
        st.session_state.selected_groups = selected_groups
    else:
        st.warning("ไม่พบข้อมูลหลัก")
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
        status_counts = emp_df['สถานะ'].value_counts().to_dict()
        
        def status_display(label, count, color):
            st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                <span style='color: {color}; font-weight: 500;'>{label}</span>
                <span style='font-weight: 600; background-color: #E9ECEF; padding: 2px 8px; border-radius: 6px;'>{count}</span>
            </div>
            """, unsafe_allow_html=True)

        status_display("มาทำงาน", status_counts.get('มาทำงาน', 0), "#28A745")
        status_display("มาสาย", status_counts.get('มาสาย', 0), "#FFC107")
        status_display("ลางาน", status_counts.get('ลา', 0), "#6F42C1")
        status_display("ขาดงาน", status_counts.get('ขาด', 0), "#DC3545")
        
        st.markdown("<hr style='margin: 1rem 0; border-color: var(--border-color);'>", unsafe_allow_html=True)
        
        with st.expander("ดูรายชื่อพนักงาน"):
            for _, row in emp_df.iterrows():
                name = row['ชื่อพนักงาน']
                status = row['สถานะ']
                time_str = row.get('เวลา', '')
                
                status_text = f"{status} {time_str}".strip()
                
                st.markdown(f"""
                <div class="employee-card" data-status="{status}">
                    <b>{name}</b><br><small>{status_text}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("ไม่พบข้อมูลสถานะพนักงาน")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# FILTERED DATA
# การกรองข้อมูลตามที่ผู้ใช้เลือก
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
# ส่วนหัวของหน้าเว็บ
# ========================================================================================
st.markdown(f"""
<div class="header-container">
    <p class="header-subtitle">แดชบอร์ดข้อมูลยางพารา | {st.session_state.selected_date.strftime("%d %B %Y")}</p>
    <h1 class="header-title">🌿 ภาพรวมข้อมูล</h1>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# TABS
# แท็บสำหรับแสดงข้อมูลในมุมมองต่างๆ
# ========================================================================================
tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "📋 สรุปข้อมูล", "📁 รายการทั้งหมด"])

def display_no_data_message():
    st.info("ไม่พบข้อมูลสำหรับวันที่และตัวกรองที่เลือก กรุณาเลือกวันที่หรือตัวกรองอื่น", icon="⚠️")

# ========================================================================================
# TAB: ภาพรวม
# ========================================================================================
with tab1:
    if df_filtered.empty:
        display_no_data_message()
    else:
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">⚖️</div>
                <div class="metric-value">{df_filtered['จำนวนยาง'].sum():,.1f}</div>
                <div class="metric-label">น้ำหนักรวม (กก.)</div>
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
                <div class="metric-value">{df_filtered['ชื่อลูกค้า'].nunique():,.0f}</div>
                <div class="metric-label">จำนวนลูกค้า</div>
            </div>
            """, unsafe_allow_html=True)

        # Charts
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="content-title">🏢 น้ำหนักรวมตามสาขา</h3>', unsafe_allow_html=True)
            bar_data = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index().sort_values('จำนวนยาง', ascending=False)
            if not bar_data.empty:
                fig_bar = px.bar(bar_data, x='สาขา', y='จำนวนยาง', text='จำนวนยาง', color_discrete_sequence=[px.colors.qualitative.Pastel[0]])
                fig_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                fig_bar.update_layout(font_family="Noto Sans Thai", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='var(--text-color)', yaxis_title="น้ำหนัก (กก.)", xaxis_title=None)
                st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart2:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="content-title">💰 สัดส่วนรายได้ตามสาขา</h3>', unsafe_allow_html=True)
            pie_data = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
            if not pie_data.empty and pie_data['จำนวนเงิน'].sum() > 0:
                fig_pie = px.pie(pie_data, values='จำนวนเงิน', names='สาขา', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_pie.update_traces(textinfo='percent+label', textfont_size=14)
                fig_pie.update_layout(font_family="Noto Sans Thai", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
                st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB: สรุปข้อมูล
# ========================================================================================
with tab2:
    if df_filtered.empty:
        display_no_data_message()
    else:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="content-title">📦 สรุปข้อมูลตามกอง</h3>', unsafe_allow_html=True)
        by_gong = df_filtered.groupby('กอง').agg(
            จำนวนยาง=('จำนวนยาง', 'sum'),
            จำนวนเงิน=('จำนวนเงิน', 'sum'),
            จำนวนลูกค้า=('ชื่อลูกค้า', 'nunique')
        ).reset_index()
        st.dataframe(by_gong, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="content-title">🏢 สรุปข้อมูลตามสาขา</h3>', unsafe_allow_html=True)
        by_branch = df_filtered.groupby('สาขา').agg(
            จำนวนยาง=('จำนวนยาง', 'sum'),
            จำนวนเงิน=('จำนวนเงิน', 'sum'),
            จำนวนลูกค้า=('ชื่อลูกค้า', 'nunique'),
            ราคาเฉลี่ย=('ราคา', 'mean')
        ).reset_index()
        st.dataframe(by_branch, use_container_width=True,
            column_config={"ราคาเฉลี่ย": st.column_config.NumberColumn(format="%.2f")})
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB: รายการทั้งหมด
# ========================================================================================
with tab3:
    if df_filtered.empty:
        display_no_data_message()
    else:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="content-title">📋 รายการข้อมูลทั้งหมด</h3>', unsafe_allow_html=True)
        keyword = st.text_input("🔍 ค้นหาชื่อลูกค้า", placeholder="กรอกชื่อลูกค้า...")
        
        if keyword:
            result_df = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(keyword, case=False, na=False)]
        else:
            result_df = df_filtered

        if result_df.empty:
            st.warning("ไม่พบข้อมูลลูกค้าที่ค้นหา")
        else:
            display_df = result_df[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']].reset_index(drop=True)
            st.dataframe(display_df, use_container_width=True, height=500)
            
            csv = display_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "📥 ดาวน์โหลดข้อมูล (CSV)", 
                csv, 
                f"LitaKarnYang_data_{st.session_state.selected_date.strftime('%Y%m%d')}.csv", 
                "text/csv", 
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# FOOTER
# ส่วนท้ายของหน้าเว็บ
# ========================================================================================
st.markdown(f"""
<div class="footer">
    <p>Lita Karn Yang Dashboard © {datetime.now().year} | Last updated: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
</div>
""", unsafe_allow_html=True)
