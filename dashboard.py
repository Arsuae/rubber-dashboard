import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import requests
import json

# ========================================================================================
# PAGE CONFIG
# ========================================================================================
st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================================
# MODERN CUSTOM CSS
# ========================================================================================
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');
    
    /* Variables */
    :root {
        --primary: #2E7D32;
        --primary-light: #4CAF50;
        --primary-dark: #1B5E20;
        --secondary: #FF6B35;
        --success: #4CAF50;
        --warning: #FF9800;
        --danger: #F44336;
        --info: #2196F3;
        --background: #F5F7FA;
        --surface: #FFFFFF;
        --text-primary: #1A202C;
        --text-secondary: #718096;
        --border: #E2E8F0;
        --shadow: 0 1px 3px rgba(0,0,0,0.1);
        --shadow-hover: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Global Styles */
    .stApp {
        font-family: 'Kanit', sans-serif;
        background: var(--background);
        color: var(--text-primary);
    }
    
    /* Container */
    .block-container {
        padding: 1rem;
        max-width: 1400px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }
    
    .sidebar-section {
        background: var(--background);
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border);
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2rem;
        font-weight: 600;
        margin: 0;
        color: white !important;
    }
    
    .main-header p {
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        color: white !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--primary);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Charts */
    .chart-container {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    /* Employee Status Cards */
    .employee-status-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .status-count {
        text-align: center;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .status-working {
        background: rgba(76, 175, 80, 0.1);
        color: var(--success);
    }
    
    .status-late {
        background: rgba(255, 152, 0, 0.1);
        color: var(--warning);
    }
    
    .status-leave {
        background: rgba(33, 150, 243, 0.1);
        color: var(--info);
    }
    
    .status-absent {
        background: rgba(244, 67, 54, 0.1);
        color: var(--danger);
    }
    
    /* Employee List */
    .employee-item {
        background: var(--background);
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }
    
    .employee-item:hover {
        transform: translateX(4px);
    }
    
    .employee-working {
        border-left-color: var(--success);
    }
    
    .employee-late {
        border-left-color: var(--warning);
    }
    
    .employee-leave {
        border-left-color: var(--info);
    }
    
    .employee-absent {
        border-left-color: var(--danger);
    }
    
    /* Table */
    .dataframe {
        border: none !important;
        font-size: 0.9rem;
    }
    
    .dataframe thead {
        background: var(--primary);
        color: white;
    }
    
    .dataframe tbody tr:hover {
        background: var(--background);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
    }
    
    .stDownloadButton > button {
        background: var(--success);
        color: white;
        width: 100%;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--surface);
        border-radius: 8px;
        padding: 0.25rem;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary);
        color: white;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 3rem;
        background: var(--surface);
        border-radius: 12px;
        border: 1px solid var(--border);
        color: var(--text-secondary);
    }
    
    .empty-state h3 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem;
        }
        .metric-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# DATA LOADING FUNCTIONS
# ========================================================================================
@st.cache_data(ttl=300)
def load_rubber_data():
    """โหลดข้อมูลยางพารา"""
    try:
        url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
        df = pd.read_csv(url, header=None)
        df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
        
        # Clean data
        df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')
        df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['ราคา'] = pd.to_numeric(df['ราคา'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['จำนวนเงิน'] = pd.to_numeric(df['จำนวนเงิน'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดข้อมูลได้: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def load_employee_status():
    """โหลดสถานะพนักงาน"""
    try:
        url = 'https://script.google.com/macros/s/AKfycbwcURACTMc6xWy-0vPfxiuG4orie0Pp0UafiNIA57uebo33YRvDiUleqihfZ_rw3B1PKw/exec'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return pd.DataFrame(data.get('data', []))
        
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# ========================================================================================
# HELPER FUNCTIONS
# ========================================================================================
def create_metric_card(icon, value, label):
    """สร้าง metric card"""
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def filter_data(df, date_filter, branches, groups):
    """กรองข้อมูลตามเงื่อนไข"""
    if df.empty:
        return pd.DataFrame()
    
    filtered = df[
        (df['วันที่'].dt.date == date_filter) &
        (df['สาขา'].isin(branches)) &
        (df['กอง'].isin(groups))
    ]
    return filtered

# ========================================================================================
# SIDEBAR
# ========================================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🎛️ ตัวกรองข้อมูล")
    
    # Date picker
    selected_date = st.date_input("📅 เลือกวันที่", value=date.today())
    
    # Load data
    df = load_rubber_data()
    
    # Branch and group filters
    branches = []
    groups = []
    
    if not df.empty:
        branches = df['สาขา'].dropna().unique().tolist()
        selected_branches = st.multiselect("🏢 เลือกสาขา", branches, default=branches)
        
        groups = df['กอง'].dropna().unique().tolist()
        selected_groups = st.multiselect("📦 เลือกกอง", groups, default=groups)
    else:
        selected_branches = []
        selected_groups = []
    
    # Refresh button
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Employee Status
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 👥 สถานะพนักงาน")
    
    emp_df = load_employee_status()
    
    if not emp_df.empty:
        # Count by status
        status_counts = emp_df['status'].value_counts().to_dict()
        
        # Display counts
        st.markdown('<div class="employee-status-grid">', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="status-count status-working">
                <div style="font-size: 1.5rem; font-weight: 600;">{status_counts.get('มาทำงาน', 0)}</div>
                <div style="font-size: 0.8rem;">มาทำงาน</div>
            </div>
            <div class="status-count status-late">
                <div style="font-size: 1.5rem; font-weight: 600;">{status_counts.get('มาสาย', 0)}</div>
                <div style="font-size: 0.8rem;">มาสาย</div>
            </div>
            <div class="status-count status-leave">
                <div style="font-size: 1.5rem; font-weight: 600;">{status_counts.get('ลา', 0)}</div>
                <div style="font-size: 0.8rem;">ลางาน</div>
            </div>
            <div class="status-count status-absent">
                <div style="font-size: 1.5rem; font-weight: 600;">{status_counts.get('ขาด', 0)}</div>
                <div style="font-size: 0.8rem;">ขาดงาน</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Employee list
        st.markdown("<hr style='margin: 1rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        
        for _, emp in emp_df.iterrows():
            status = emp['status']
            name = emp['name']
            time = emp.get('time', '')
            
            status_class = {
                'มาทำงาน': 'employee-working',
                'มาสาย': 'employee-late',
                'ลา': 'employee-leave',
                'ขาด': 'employee-absent'
            }.get(status, 'employee-absent')
            
            status_icon = {
                'มาทำงาน': '🟢',
                'มาสาย': '🟡',
                'ลา': '🟣',
                'ขาด': '🔴'
            }.get(status, '🔴')
            
            st.markdown(f'''
                <div class="employee-item {status_class}">
                    <strong>{name}</strong><br>
                    <small>{status_icon} {status} {time}</small>
                </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("ไม่สามารถโหลดข้อมูลพนักงานได้")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# MAIN CONTENT
# ========================================================================================

# Header
st.markdown("""
<div class="main-header">
    <h1>🌳 ลิตาการยาง Dashboard</h1>
    <p>ระบบจัดการข้อมูลยางพาราแบบเรียลไทม์</p>
</div>
""", unsafe_allow_html=True)

# Filter data
filtered_df = filter_data(df, selected_date, selected_branches, selected_groups)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "📈 วิเคราะห์", "📋 รายการ"])

# ========================================================================================
# TAB 1: Overview
# ========================================================================================
with tab1:
    if filtered_df.empty:
        st.markdown("""
        <div class="empty-state">
            <h3>⚠️ ไม่มีข้อมูล</h3>
            <p>ไม่พบข้อมูลตามเงื่อนไขที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_weight = filtered_df['จำนวนยาง'].sum()
            st.markdown(create_metric_card("⚖️", f"{total_weight:,.0f}", "กิโลกรัม"), unsafe_allow_html=True)
        
        with col2:
            total_revenue = filtered_df['จำนวนเงิน'].sum()
            st.markdown(create_metric_card("💰", f"฿{total_revenue:,.0f}", "รายได้รวม"), unsafe_allow_html=True)
        
        with col3:
            total_customers = filtered_df['ชื่อลูกค้า'].count()
            st.markdown(create_metric_card("👥", f"{total_customers:,}", "ลูกค้า"), unsafe_allow_html=True)
        
        with col4:
            avg_price = filtered_df['ราคา'].mean()
            st.markdown(create_metric_card("📊", f"฿{avg_price:.2f}", "ราคาเฉลี่ย"), unsafe_allow_html=True)
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">จำนวนยางตามสาขา</h3>', unsafe_allow_html=True)
            
            branch_data = filtered_df.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
            fig_bar = px.bar(
                branch_data, 
                x='สาขา', 
                y='จำนวนยาง',
                text='จำนวนยาง',
                color_discrete_sequence=['#2E7D32']
            )
            fig_bar.update_traces(texttemplate='%{text:.0f}', textposition='outside')
            fig_bar.update_layout(
                height=350,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="",
                yaxis_title="กิโลกรัม",
                font=dict(family="Kanit")
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_chart2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">สัดส่วนรายได้ตามสาขา</h3>', unsafe_allow_html=True)
            
            revenue_data = filtered_df.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
            fig_pie = px.pie(
                revenue_data, 
                values='จำนวนเงิน', 
                names='สาขา',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Greens
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                height=350,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                font=dict(family="Kanit")
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB 2: Analysis
# ========================================================================================
with tab2:
    if filtered_df.empty:
        st.markdown("""
        <div class="empty-state">
            <h3>⚠️ ไม่มีข้อมูล</h3>
            <p>ไม่พบข้อมูลตามเงื่อนไขที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary by group
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("### 📦 สรุปตามกอง")
            
            group_summary = filtered_df.groupby('กอง').agg({
                'จำนวนยาง': 'sum',
                'จำนวนเงิน': 'sum',
                'ชื่อลูกค้า': 'count'
            }).round(0).reset_index()
            group_summary.columns = ['กอง', 'น้ำหนัก (กก.)', 'รายได้ (บาท)', 'จำนวนลูกค้า']
            
            st.dataframe(group_summary, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("### 🏢 สรุปตามสาขา")
            
            branch_summary = filtered_df.groupby('สาขา').agg({
                'จำนวนยาง': 'sum',
                'จำนวนเงิน': 'sum',
                'ราคา': 'mean'
            }).round(2).reset_index()
            branch_summary.columns = ['สาขา', 'น้ำหนัก (กก.)', 'รายได้ (บาท)', 'ราคาเฉลี่ย']
            
            st.dataframe(branch_summary, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Top performers
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 🏆 ข้อมูลโดดเด่น")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_customer = filtered_df.nlargest(1, 'จำนวนยาง').iloc[0]
            st.info(f"**ลูกค้ายอดสูงสุด**\n\n{top_customer['ชื่อลูกค้า']}\n\n{top_customer['จำนวนยาง']:,.0f} กก.")
        
        with col2:
            price_range = filtered_df['ราคา'].max() - filtered_df['ราคา'].min()
            st.success(f"**ช่วงราคา**\n\n฿{filtered_df['ราคา'].min():.2f} - ฿{filtered_df['ราคา'].max():.2f}\n\nต่างกัน ฿{price_range:.2f}")
        
        with col3:
            branches_count = filtered_df['สาขา'].nunique()
            groups_count = filtered_df['กอง'].nunique()
            st.warning(f"**ความครอบคลุม**\n\n{branches_count} สาขา\n\n{groups_count} กอง")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# TAB 3: Details
# ========================================================================================
with tab3:
    if filtered_df.empty:
        st.markdown("""
        <div class="empty-state">
            <h3>⚠️ ไม่มีข้อมูล</h3>
            <p>ไม่พบข้อมูลตามเงื่อนไขที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Search and sort
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            search = st.text_input("🔍 ค้นหาชื่อลูกค้า", placeholder="พิมพ์ชื่อลูกค้า...")
        
        with col2:
            sort_by = st.selectbox("📊 เรียงตาม", ["จำนวนยาง", "จำนวนเงิน", "ชื่อลูกค้า"])
        
        with col3:
            sort_order = st.selectbox("📈 ลำดับ", ["มาก→น้อย", "น้อย→มาก"])
        
        # Filter and sort
        display_df = filtered_df.copy()
        
        if search:
            display_df = display_df[display_df['ชื่อลูกค้า'].str.contains(search, case=False, na=False)]
        
        ascending = sort_order == "น้อย→มาก"
        display_df = display_df.sort_values(sort_by, ascending=ascending)
        
        # Summary
        st.info(f"📊 พบ **{len(display_df)}** รายการ | น้ำหนักรวม **{display_df['จำนวนยาง'].sum():,.0f}** กก. | รายได้รวม **฿{display_df['จำนวนเงิน'].sum():,.0f}**")
        
        # Display table
        show_df = display_df[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']].reset_index(drop=True)
        st.dataframe(
            show_df.style.format({
                'จำนวนยาง': '{:,.1f}',
                'ราคา': '฿{:,.2f}',
                'จำนวนเงิน': '฿{:,.0f}'
            }),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = show_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            "📥 ดาวน์โหลด CSV",
            csv,
            f"rubber_data_{selected_date.strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )

# ========================================================================================
# FOOTER
# ========================================================================================
st.markdown(f"""
<div style="text-align: center; padding: 2rem 0; color: var(--text-secondary); border-top: 1px solid var(--border); margin-top: 2rem;">
    <p>🌳 ลิตาการยาง Dashboard © 2025 | อัปเดตล่าสุด: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
</div>
""", unsafe_allow_html=True)
