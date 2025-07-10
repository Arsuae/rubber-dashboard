import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ========================================================================================
# CONFIGURATION & LIGHT MODERN STYLING
# ========================================================================================

st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LIGHT THEME CSS (inspired by the white dashboard sample) ---
st.markdown("""
<style>
body, .stApp { background: #f7fafd !important; color: #1a1a1a;}
.main-header {
    background: #fff;
    padding: 2rem 1rem 1.5rem 1rem;
    border-radius: 16px;
    text-align: center;
    color: #324177 !important;
    margin-bottom: 2rem;
    box-shadow: 0 4px 22px rgba(45,56,100,0.10);
    font-family: 'Inter', 'Sarabun', sans-serif;
}
.total-summary {
    background: #fff;
    padding: 1.5rem;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(44,62,80,0.08);
    text-align: center;
    color: #222;
    margin: 1.5rem 0 2rem 0;
}
.total-summary h2 { color: #324177; font-size: 1.45rem; font-weight: 700;}
.summary-row {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin: 1rem 0 0 0;
}
.summary-box {
    min-width: 160px;
    background: #f7fafd;
    border-radius: 9px;
    box-shadow: 0 1px 3px rgba(44,62,80,0.04);
    padding: 0.7rem 1.3rem;
    text-align: center;
}
.summary-label {
    font-size: 14px; color: #8fa0bf; margin-bottom: 0.1rem;
}
.summary-value {
    font-size: 1.7rem; font-weight: 700; color: #324177;
}
.section-card {
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(44,62,80,0.08);
    padding: 1.3rem 1.2rem 1.5rem 1.2rem;
    margin-bottom: 1.8rem;
}
.metric-card {
    background: #f4f6fb;
    border-radius: 9px;
    padding: 1.1rem 1rem;
    text-align: center;
    color: #222;
    box-shadow: 0 1px 3px rgba(44,62,80,0.03);
}
.metric-title { font-size: 1rem; color: #626fa1; margin-bottom: 0.3rem;}
.metric-value { font-size: 1.5rem; font-weight: bold; color: #324177;}
.metric-value2 { color: #27b0e6;}
.metric-value3 { color: #f2b900;}
.metric-label { font-size: 0.95rem; color: #9db0ce; font-weight: 400;}
.stTabs [role=tablist] { background: #e3eaf8; border-radius: 9px; }
.stTabs [role=tab] { font-weight: 500; color: #324177; }
.stTabs [aria-selected="true"] { color: #1976d2 !important; }
.stDataFrame { background: #fff; border-radius: 12px; }
.branch-section {
    background: #f7fafd;
    border-radius: 12px;
    padding: 1rem 0.5rem 1rem 0.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(44,62,80,0.04);
}
.stat-card {
    background: #e7f7e1;
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    color: #135908;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 500;
}
.stat-card2 { background: #ecf7fd; color: #236db1;}
.stat-card3 { background: #fff8e1; color: #e2a800;}
.footer-modern {
    text-align: center;
    color: #9db0ce;
    padding: 1.2rem 0 0.5rem 0;
    font-size: 13px;
}
::-webkit-scrollbar-thumb { background: #e3eaf8 !important;}
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
    <p>ข้อมูลยางพาราวันนี้</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# 📊 SIDEBAR CONTROLS
# ========================================================================================

with st.sidebar:
    st.markdown("### 🎛️ ตัวควบคุม")
    df = load_data()
    if df.empty:
        st.error("ไม่สามารถโหลดข้อมูลได้")
        st.stop()
    st.markdown("#### 📅 เลือกวันที่")
    selected_date = st.date_input(
        "วันที่",
        value=date.today(),
        help="เลือกวันที่ที่ต้องการดูข้อมูล"
    )
    st.markdown("#### 🏢 เลือกสาขา")
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect(
        "สาขา",
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
    <div class="section-card" style="background:linear-gradient(90deg,#f7b8b8 0%, #e9e9e9 100%);">
        <h3 style="color:#c10000;">⚠️ ไม่มีข้อมูล</h3>
        <p>ไม่พบข้อมูลตามวันที่และสาขาที่เลือก กรุณาเลือกวันที่หรือสาขาอื่น</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Calculate statistics for each branch
    branch_stats = df_filtered.groupby('สาขา').agg({
        'จำนวนยาง': 'sum',
        'จำนวนเงิน': 'sum',
        'ชื่อลูกค้า': 'count'
    }).reset_index()
    
    # Calculate totals for today
    total_rubber_today = df_filtered['จำนวนยาง'].sum()
    total_money_today = df_filtered['จำนวนเงิน'].sum()
    total_customers_today = df_filtered['ชื่อลูกค้า'].count()

    # ========================================================================================
    # 📊 TOTAL SUMMARY SECTION (CARD + FLEX)
    # ========================================================================================
    st.markdown("""
    <div class="total-summary">
        <h2>📊 สรุปรวมวันนี้</h2>
        <div class="summary-row">
            <div class="summary-box">
                <div class="summary-label">จำนวนยางรวม</div>
                <div class="summary-value">{:,.1f} กก.</div>
            </div>
            <div class="summary-box">
                <div class="summary-label">รายได้รวม</div>
                <div class="summary-value">฿{:,.0f}</div>
            </div>
            <div class="summary-box">
                <div class="summary-label">จำนวนลูกค้า</div>
                <div class="summary-value">{:,.0f} ราย</div>
            </div>
        </div>
    </div>
    """.format(total_rubber_today, total_money_today, total_customers_today), unsafe_allow_html=True)

    # ========================================================================================
    # 📊 CHARTS SECTION (CARD)
    # ========================================================================================
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 จำนวนยางตามสาขา")
        branch_summary = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
        if not branch_summary.empty:
            fig_branch = px.bar(
                branch_summary,
                x='สาขา',
                y='จำนวนยาง',
                color='จำนวนยาง',
                color_continuous_scale='Blues',
                text='จำนวนยาง',
                height=350,
            )
            fig_branch.update_layout(
                showlegend=False,
                plot_bgcolor='#fff',
                paper_bgcolor='#fff',
                font=dict(size=13, family="Sarabun,sans-serif"),
                margin=dict(l=12, r=12, t=30, b=10)
            )
            fig_branch.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig_branch, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 💰 สัดส่วนรายได้แต่ละสาขา")
        money_summary = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
        if not money_summary.empty:
            fig_money = px.pie(
                money_summary,
                values='จำนวนเงิน',
                names='สาขา',
                hole=0.55,
                color_discrete_sequence=px.colors.sequential.Blues_r,
                height=350,
            )
            fig_money.update_layout(
                plot_bgcolor='#fff',
                paper_bgcolor='#fff',
                font=dict(size=13, family="Sarabun,sans-serif"),
                margin=dict(l=12, r=12, t=30, b=10)
            )
            fig_money.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_money, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================================
    # BRANCH STATISTICS SECTION (CARD)
    # ========================================================================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### 🏢 สถิติแยกตามสาขา")
    for i, row in branch_stats.iterrows():
        st.markdown(f"##### สาขา {row['สาขา']}")
        col1_, col2_, col3_ = st.columns(3)
        with col1_:
            st.markdown(f"""
            <div class="stat-card">
                <div>จำนวนยาง</div>
                <div style="font-size:1.5rem;font-weight:700;">{row['จำนวนยาง']:,.1f} กก.</div>
            </div>
            """, unsafe_allow_html=True)
        with col2_:
            st.markdown(f"""
            <div class="stat-card stat-card2">
                <div>จำนวนเงิน</div>
                <div style="font-size:1.5rem;font-weight:700;">฿{row['จำนวนเงิน']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3_:
            st.markdown(f"""
            <div class="stat-card stat-card3">
                <div>จำนวนรายการ</div>
                <div style="font-size:1.5rem;font-weight:700;">{row['ชื่อลูกค้า']:,.0f} ราย</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================================
    # 📋 DATA TABLES SECTION (CARD + TABS)
    # ========================================================================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📋 ข้อมูลทั้งหมด", "📦 สรุปตามกอง", "🏢 สรุปตามสาขา"])
    with tab1:
        st.markdown("#### 📋 ข้อมูลรายละเอียด")
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
                    help='รายได้รวม (บาท)',
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
        grouped_by_gong.columns = ['กอง', 'จำนวนยาง', 'จำนวนเงิน', 'จำนวนรายการ']
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
        grouped_by_branch.columns = ['สาขา', 'จำนวนยาง', 'จำนวนเงิน', 'จำนวนรายการ', 'ราคาเฉลี่ย']
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
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# 📊 FOOTER
# ========================================================================================
st.markdown(
    f'<div class="footer-modern">📊 ลิตาการยาง Dashboard | อัพเดทล่าสุด: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div>',
    unsafe_allow_html=True
)
