import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ========================================================================================
# 📊 CONFIGURATION & STYLING
# ========================================================================================

st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;600;700&display=swap');

    body {
        font-family: 'Noto Sans Thai', sans-serif;
        background-color: #f4f7fa;
    }

    .main-header {
        background: linear-gradient(135deg, #2a4d69 0%, #4b86b4 100%);
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }

    .branch-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #6ab04c 0%, #55efc4 100%);
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4b86b4;
        margin: 1rem 0;
        transition: box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .info-card {
        background: linear-gradient(135deg, #4834d4 0%, #686de0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: #ffffff;
        border-right: 1px solid #e9ecef;
        padding: 1rem;
    }
    
    .stMetric {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-3px);
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .company-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #2a4d69;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }
    
    .total-summary {
        background: linear-gradient(135deg, #1dd1a1 0%, #00b894 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stButton>button {
        background: #4b86b4;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: background 0.3s ease;
    }
    
    .stButton>button:hover {
        background: #2a4d69;
    }
    
    .stTextInput>div>input {
        border-radius: 8px;
        border: 1px solid #e9ecef;
        padding: 0.5rem;
    }
    
    h3, h4, h5 {
        color: #2a4d69;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# 🗂️ DATA LOADING & PROCESSING
# ========================================================================================

@st.cache_data(ttl=300)
def load_data():
    """Load data from Google Sheets with caching"""
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
        df = pd.read_csv(sheet_url, header=None)
        
        df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
        df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')
        df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['ราคา'] = pd.to_numeric(df['ราคา'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['จำนวนเงิน'] = pd.to_numeric(df['จำนวนเงิน'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดข้อมูลได้: {str(e)}")
        return pd.DataFrame()

# ========================================================================================
# 🎨 HEADER SECTION
# ========================================================================================

st.markdown("""
<div class="main-header">
    <h1>ลิตาการยาง</h1>
    <p>แดชบอร์ดข้อมูลยางพาราแบบเรียลไทม์</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# 📊 SIDEBAR CONTROLS
# ========================================================================================

with st.sidebar:
    st.markdown("### ⚙️ การควบคุม")
    
    df = load_data()
    
    if df.empty:
        st.error("ไม่สามารถโหลดข้อมูลได้")
        st.stop()
    
    st.markdown("#### 📅 ตัวเลือกวันที่")
    selected_date = st.date_input(
        "เลือกวันที่",
        value=date.today(),
        help="เลือกวันที่ที่ต้องการดูข้อมูล"
    )
    
    st.markdown("#### 🏢 ตัวเลือกสาขา")
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect(
        "เลือกสาขา",
        options=branches,
        default=branches,
        help="เลือกสาขาที่ต้องการดูข้อมูล"
    )
    
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ========================================================================================
# 📈 DATA FILTERING & PROCESSING
# ========================================================================================

df_filtered = df[
    (df['วันที่'].dt.date == selected_date) &
    (df['สาขา'].isin(selected_branches))
]

# ========================================================================================
# 📊 MAIN DASHBOARD
# ========================================================================================

if df_filtered.empty:
    st.markdown("""
    <div class="info-card">
        <h3>⚠️ ไม่มีข้อมูล</h3>
        <p>ไม่พบข้อมูลสำหรับวันที่และสาขาที่เลือก กรุณาเลือกวันที่หรือสาขาอื่น</p>
    </div>
    """, unsafe_allow_html=True)
else:
    branch_stats = df_filtered.groupby('สาขา').agg({
        'จำนวนยาง': 'sum',
        'จำนวนเงิน': 'sum',
        'ชื่อลูกค้า': 'count'
    }).reset_index()
    
    total_rubber_today = df_filtered['จำนวนยาง'].sum()
    total_money_today = df_filtered['จำนวนเงิน'].sum()
    total_customers_today = df_filtered['ชื่อลูกค้า'].count()
    
    # ========================================================================================
    # 📊 TOTAL SUMMARY SECTION
    # ========================================================================================
    
    st.markdown(f"""
    <div class="total-summary">
        <h2>📊 สรุปข้อมูลวันนี้</h2>
        <div style="display: flex; justify-content: center; gap: 2.5rem; margin-top: 1.5rem;">
            <div class="stats-card">
                <div style="font-size: 1rem; font-weight: 400;">จำนวนยางรวม</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{total_rubber_today:,.1f} กก.</div>
            </div>
            <div class="stats-card">
                <div style="font-size: 1rem; font-weight: 400;">จำนวนเงิน</div>
                <div style="font-size: 1.8rem; font-weight: 700;">฿{total_money_today:,.0f}</div>
            </div>
            <div class="stats-card">
                <div style="font-size: 1rem; font-weight: 400;">จำนวนลูกค้า</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{total_customers_today:,.0f} ราย</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================================================
    # 📊 CHARTS SECTION
    # ========================================================================================
    
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.markdown("#### 📊 จำนวนยางตามสาขา")
        branch_summary = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
        
        if not branch_summary.empty:
            fig_branch = px.bar(
                branch_summary,
                x='สาขา',
                y='จำนวนยาง',
                title="จำนวนยางแยกตามสาขา",
                color='จำนวนยาง',
                color_continuous_scale='teal',
                text='จำนวนยาง'
            )
            fig_branch.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, family='Noto Sans Thai'),
                title_font=dict(size=16, family='Noto Sans Thai', weight='bold'),
                margin=dict(t=50, b=50)
            )
            fig_branch.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig_branch, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 สัดส่วนรายได้ตามสาขา")
        money_summary = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
        
        if not money_summary.empty:
            fig_money = px.pie(
                money_summary,
                values='จำนวนเงิน',
                names='สาขา',
                title="สัดส่วนรายได้ตามสาขา",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_money.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, family='Noto Sans Thai'),
                title_font=dict(size=16, family='Noto Sans Thai', weight='bold'),
                margin=dict(t=50, b=50)
            )
            fig_money.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_money, use_container_width=True)

    # ========================================================================================
    # BRANCH STATISTICS SECTION
    # ========================================================================================

    st.markdown("#### 🏢 สถิติแยกตามสาขา")
    
    for i, row in branch_stats.iterrows():
        st.markdown(f"##### สาขา {row['สาขา']}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card" style="background: linear-gradient(135deg, #6ab04c 0%, #55efc4 100%);">
                <div style="font-size: 1rem;">จำนวนยาง</div>
                <div style="font-size: 1.6rem; font-weight: 700;">{row['จำนวนยาง']:,.1f} กก.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card" style="background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);">
                <div style="font-size: 1rem;">จำนวนเงิน</div>
                <div style="font-size: 1.6rem; font-weight: 700;">฿{row['จำนวนเงิน']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card" style="background: linear-gradient(135deg, #fdcb6e 0%, #ffeaa7 100%);">
                <div style="font-size: 1rem;">จำนวนลูกค้า</div>
                <div style="font-size: 1.6rem; font-weight: 700;">{row['ชื่อลูกค้า']:,.0f} ราย</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
    # ========================================================================================
    # 📋 DATA TABLES SECTION
    # ========================================================================================
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📋 ข้อมูลทั้งหมด", "📦 สรุปตามกอง", "🏢 สรุปตามสาขา"])
    
    with tab1:
        st.markdown("#### 📋 รายละเอียดข้อมูล")
        columns_to_show = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
        
        search_term = st.text_input("🔍 ค้นหาลูกค้า", placeholder="พิมพ์ชื่อลูกค้าที่ต้องการค้นหา...")
        
        if search_term:
            df_display = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(search_term, case=False, na=False)]
        else:
            df_display = df_filtered
        
        st.dataframe(
            df_display[columns_to_show],
            use_container_width=True,
            hide_index=True,
            column_config={
                'จำนวนยาง': st.column_config.NumberColumn(
                    'จำนวนยาง (กก.)',
                    help='จำนวนยาง (กิโลกรัม)',
                    format='%.1f'
                ),
                'ราคา': st.column_config.NumberColumn(
                    'ราคา (บาท/กก.)',
                    help='ราคาต่อหน่วย (บาท)',
                    format='%.2f'
                ),
                'จำนวนเงิน': st.column_config.NumberColumn(
                    'จำนวนเงิน (บาท)',
                    help='จำนวนเงิน (บาท)',
                    format='%.0f'
                )
            }
        )
    
    with tab2:
        st.markdown("#### 📦 สรุปข้อมูลตามกอง")
        grouped_by_gong = df_filtered.groupby('กอง').agg({
            'จำนวนยาง': 'sum',
            'จำนวนเงิน': 'sum',
            'ชื่อลูกค้า': 'count'
        }).reset_index()
        grouped_by_gong.columns = ['กอง', 'จำนวนยาง', 'จำนวนเงิน', 'จำนวนลูกค้า']
        
        st.dataframe(
            grouped_by_gong,
            use_container_width=True,
            hide_index=True,
            column_config={
                'จำนวนยาง': st.column_config.NumberColumn(
                    'จำนวนยาง (กก.)',
                    format='%.1f'
                ),
                'จำนวนเงิน': st.column_config.NumberColumn(
                    'จำนวนเงิน (บาท)',
                    format='%.0f'
                )
            }
        )
    
    with tab3:
        st.markdown("#### 🏢 สรุปข้อมูลตามสาขา")
        grouped_by_branch = df_filtered.groupby('สาขา').agg({
            'จำนวนยาง': 'sum',
            'จำนวนเงิน': 'sum',
            'ชื่อลูกค้า': 'count',
            'ราคา': 'mean'
        }).reset_index()
        grouped_by_branch.columns = ['สาขา', 'จำนวนยาง', 'จำนวนเงิน', 'จำนวนลูกค้า', 'ราคาเฉลี่ย']
        
        st.dataframe(
            grouped_by_branch,
            use_container_width=True,
            hide_index=True,
            column_config={
                'จำนวนยาง': st.column_config.NumberColumn(
                    'จำนวนยาง (กก.)',
                    format='%.1f'
                ),
                'จำนวนเงิน': st.column_config.NumberColumn(
                    'จำนวนเงิน (บาท)',
                    format='%.0f'
                ),
                'ราคาเฉลี่ย': st.column_config.NumberColumn(
                    'ราคาเฉลี่ย (บาท/กก.)',
                    format='%.2f'
                )
            }
        )

# ========================================================================================
# 📊 FOOTER
# ========================================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #2a4d69; padding: 1.5rem; font-size: 1rem;">
    <p>📊 ลิตาการยาง Dashboard | อัพเดทล่าสุด: {}</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
