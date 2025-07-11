import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, time
import io
import requests

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
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Noto Sans Thai', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header Styles */
    .header-container {
        background: linear-gradient(135deg, #2a4d69 0%, #1e3a5f 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #2a4d69 0%, #1e3a5f 100%);
    }
    
    .sidebar-section {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .sidebar-title {
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .employee-card {
        background: rgba(255,255,255,0.15);
        padding: 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #4CAF50;
        transition: all 0.3s ease;
    }
    
    .employee-card:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(5px);
    }
    
    .employee-offline {
        border-left-color: #f44336;
    }
    
    .employee-done {
        border-left-color: #2196F3;
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.1);
        padding: 0.5rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        box-shadow: 0 5px 15px rgba(76,175,80,0.3);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.8);
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2a4d69;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1.1rem;
        color: #666;
        font-weight: 500;
    }
    
    .metric-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.8);
    }
    
    .chart-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2a4d69;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Data Table */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Search Box */
    .search-container {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Footer */
    .footer {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: rgba(255,255,255,0.8);
        margin-top: 2rem;
        backdrop-filter: blur(10px);
    }
    
    /* Warning and Info Boxes */
    .stAlert {
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 500;
        padding: 0.8rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #45a049 0%, #4CAF50 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(76,175,80,0.3);
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

@st.cache_data(ttl=300)
def load_employee_status():
    url_attendance = "https://docs.google.com/spreadsheets/d/1ZDyYQWvPrxFEv7JzcWsVrn24w6iToFxbX0J0oup9DPo/export?format=csv&gid=1837491789"
    url_employees = "https://docs.google.com/spreadsheets/d/1ZDyYQWvPrxFEv7JzcWsVrn24w6iToFxbX0J0oup9DPo/export?format=csv&gid=1803808434"

    headers = {"User-Agent": "Mozilla/5.0"}
    att_resp = requests.get(url_attendance, headers=headers)
    emp_resp = requests.get(url_employees, headers=headers)

    if att_resp.status_code != 200 or emp_resp.status_code != 200:
        st.warning("ไม่สามารถดึงข้อมูลพนักงานได้")
        return pd.DataFrame(columns=["ชื่อพนักงาน", "สถานะ"])

    attendance_df = pd.read_csv(io.StringIO(att_resp.content.decode('utf-8')))
    employees_df = pd.read_csv(io.StringIO(emp_resp.content.decode('utf-8')), header=1)  # ✅ header แถวที่ 2

    employees_df.columns = employees_df.columns.str.strip()
    attendance_df.columns = attendance_df.columns.str.strip()

    today_str = date.today().strftime("%Y-%m-%d")
    today_df = attendance_df[attendance_df["Date"] == today_str]
    today_df = today_df[today_df["Punch"] == 0]

    present_ids = today_df["User ID"].dropna().astype(str).unique()
    employees_df = employees_df.dropna(subset=['User ID', 'Name'])
    employees_df["User ID"] = employees_df["User ID"].astype(str)

    employees_df["สถานะ"] = employees_df["User ID"].apply(
        lambda x: "ทำงาน" if x in present_ids else "ไม่มาทำงาน"
    )

    return employees_df[["Name", "สถานะ"]].rename(columns={"Name": "ชื่อพนักงาน"})

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

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">👨‍🌾 พนักงาน</h3>', unsafe_allow_html=True)
    
    emp_df = load_employee_status()
    
    if not emp_df.empty:
        current_time = datetime.now().time()
        for i, row in emp_df.iterrows():
            name = row['ชื่อพนักงาน']
            status = row['สถานะ']
            
            if status == "ทำงาน" and current_time >= time(16, 0):
                status_text = "✅ ออกงาน"
                card_class = "employee-card employee-done"
            elif status == "ไม่มาทำงาน":
                status_text = "❌ ไม่มาทำงาน"
                card_class = "employee-card employee-offline"
            else:
                status_text = "🟢 ทำงาน"
                card_class = "employee-card"
            
            st.markdown(f'<div class="{card_class}">{name}<br><small>{status_text}</small></div>', unsafe_allow_html=True)
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
