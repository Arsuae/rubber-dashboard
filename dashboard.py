import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ========================================================================================
# CONFIGURATION & BASIC MODERN STYLING
# ========================================================================================

st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal modern CSS
st.markdown("""
<style>
    body, .stApp { background: #f6f8fa !important; color: #222; }
    .main-header {
        background: #4472C4;
        padding: 2rem 1rem 1.5rem 1rem;
        border-radius: 14px;
        text-align: center;
        color: white !important;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(44,62,80,0.10);
    }
    .summary-row {
        display: flex;
        justify-content: center;
        gap: 2.5rem;
        margin: 0.5rem 0 1.5rem 0;
    }
    .summary-card {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(44,62,80,0.07);
        padding: 1.2rem 2rem;
        text-align: center;
        min-width: 170px;
    }
    .summary-label { font-size: 14px; color: #888; margin-bottom: 0.25rem; }
    .summary-value { font-size: 2rem; font-weight: 700; color: #4472C4; }
    .section-card {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(44,62,80,0.07);
        padding: 1.5rem;
        margin-bottom: 1.3rem;
    }
    .footer {
        text-align: center;
        color: #888;
        padding: 1rem 0 0.2rem 0;
        font-size: 13px;
    }
    .stDataFrame { background: #fff; border-radius: 10px; }
    .stTabs [role=tablist] { background: #f6f8fa; border-radius: 8px; }
    .stTabs [role=tab] { font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# DATA LOADING & PROCESSING
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
# HEADER
# ========================================================================================

st.markdown("""
<div class="main-header">
    <h1 style="margin-bottom: 0.1rem;">ลิตาการยาง</h1>
    <div style="font-size:1.2rem;font-weight:400;opacity:0.95;">แดชบอร์ดข้อมูลยางพารา</div>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# SIDEBAR CONTROLS
# ========================================================================================

with st.sidebar:
    st.header("🎛️ ตัวควบคุม")
    df = load_data()
    if df.empty:
        st.error("ไม่สามารถโหลดข้อมูลได้")
        st.stop()
    selected_date = st.date_input(
        "📅 เลือกวันที่", value=date.today(),
        help="เลือกวันที่ที่ต้องการดูข้อมูล"
    )
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect(
        "🏢 เลือกสาขา", options=branches, default=branches,
        help="เลือกสาขาที่ต้องการดูข้อมูล"
    )
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ========================================================================================
# DATA FILTERING
# ========================================================================================

df_filtered = df[
    (df['วันที่'].dt.date == selected_date) &
    (df['สาขา'].isin(selected_branches))
]

# ========================================================================================
# MAIN DASHBOARD
# ========================================================================================

if df_filtered.empty:
    st.markdown("""
    <div class="section-card" style="text-align:center;">
        <h4>⚠️ ไม่พบข้อมูล</h4>
        <div>ไม่มีข้อมูลสำหรับวันที่และสาขาที่เลือก</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Statistics
    total_rubber_today = df_filtered['จำนวนยาง'].sum()
    total_money_today = df_filtered['จำนวนเงิน'].sum()
    total_customers_today = df_filtered['ชื่อลูกค้า'].count()

    # Summary Row
    st.markdown("""
    <div class="summary-row">
        <div class="summary-card">
            <div class="summary-label">จำนวนยางรวม</div>
            <div class="summary-value">{:,.1f} กก.</div>
        </div>
        <div class="summary-card">
            <div class="summary-label">รายได้รวม</div>
            <div class="summary-value">฿{:,.0f}</div>
        </div>
        <div class="summary-card">
            <div class="summary-label">จำนวนลูกค้า</div>
            <div class="summary-value">{:,.0f} ราย</div>
        </div>
    </div>
    """.format(total_rubber_today, total_money_today, total_customers_today), unsafe_allow_html=True)

    # CHARTS
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("##### จำนวนยางตามสาขา")
        branch_summary = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
        if not branch_summary.empty:
            fig_branch = px.bar(
                branch_summary, x='สาขา', y='จำนวนยาง',
                color='จำนวนยาง', color_continuous_scale='Blues', text='จำนวนยาง',
                labels={'จำนวนยาง': 'จำนวนยาง (กก.)', 'สาขา': 'สาขา'}
            )
            fig_branch.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=30, b=10),
                font=dict(size=13)
            )
            fig_branch.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig_branch, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("##### สัดส่วนรายได้ตามสาขา")
        money_summary = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
        if not money_summary.empty:
            fig_money = px.pie(
                money_summary,
                values='จำนวนเงิน',
                names='สาขา',
                color_discrete_sequence=px.colors.sequential.Blues
            )
            fig_money.update_layout(
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=30, b=10),
                font=dict(size=13)
            )
            fig_money.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_money, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # DATA TABLES WITH TABS
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📋 รายการวันนี้", "📦 สรุปตามกอง", "🏢 สรุปตามสาขา"])

    with tab1:
        columns_to_show = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
        search_term = st.text_input("🔍 ค้นหาลูกค้า", placeholder="พิมพ์ชื่อลูกค้าเพื่อค้นหา...")
        if search_term:
            df_display = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(search_term, case=False, na=False)]
        else:
            df_display = df_filtered
        st.dataframe(
            df_display[columns_to_show],
            use_container_width=True,
            hide_index=True,
            column_config={
                'จำนวนยาง': st.column_config.NumberColumn('จำนวนยาง (กก.)', format='%.1f'),
                'ราคา': st.column_config.NumberColumn('ราคา (บาท/กก.)', format='%.2f'),
                'จำนวนเงิน': st.column_config.NumberColumn('จำนวนเงิน (บาท)', format='%.0f')
            }
        )

    with tab2:
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
                'จำนวนยาง': st.column_config.NumberColumn('จำนวนยาง (กก.)', format='%.1f'),
                'จำนวนเงิน': st.column_config.NumberColumn('จำนวนเงิน (บาท)', format='%.0f')
            }
        )

    with tab3:
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
                'จำนวนยาง': st.column_config.NumberColumn('จำนวนยาง (กก.)', format='%.1f'),
                'จำนวนเงิน': st.column_config.NumberColumn('จำนวนเงิน (บาท)', format='%.0f'),
                'ราคาเฉลี่ย': st.column_config.NumberColumn('ราคาเฉลี่ย (บาท/กก.)', format='%.2f')
            }
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# FOOTER
# ========================================================================================
st.markdown(
    f'<div class="footer">📊 ลิตาการยาง Dashboard | อัพเดทล่าสุด: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div>',
    unsafe_allow_html=True
)
