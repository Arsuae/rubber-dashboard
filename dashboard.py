import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ========================================================================================
# CONFIG & MODERN CSS
# ========================================================================================

st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dashboard CSS (inspired by image1)
st.markdown("""
<style>
    body, .stApp { background: #f4f7fa !important; color: #222; }
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #6ed0fa 100%);
        padding: 2rem 1rem 1.2rem 1rem;
        border-radius: 18px;
        text-align: left;
        color: white !important;
        margin-bottom: 1.8rem;
        box-shadow: 0 3px 12px rgba(44,62,80,0.10);
        font-family: 'Inter', sans-serif;
    }
    .sidebar-modern {
        background: linear-gradient(180deg, #667eea 0%, #e7edfb 100%);
        padding: 0.5rem 0.8rem 1.5rem 0.8rem;
        border-radius: 14px;
    }
    .summary-row {
        display: flex;
        justify-content: start;
        gap: 2.2rem;
        margin: 0.7rem 0 2.2rem 0.2rem;
    }
    .summary-card {
        background: #fff;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(44,62,80,0.06);
        padding: 1.1rem 2rem 1.1rem 1.2rem;
        min-width: 170px;
        max-width: 230px;
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .summary-label { font-size: 15px; color: #6c80a9; margin-bottom: 0.3rem; font-weight: 400; }
    .summary-value { font-size: 2rem; font-weight: 700; color: #667eea; margin-bottom: 0rem;}
    .summary-sub { font-size: 12px; color: #aab8d4; font-weight: 500;}
    .section-card {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(44,62,80,0.07);
        padding: 1.5rem 1.2rem 1.5rem 1.2rem;
        margin-bottom: 1.2rem;
    }
    .footer-modern {
        text-align: center;
        color: #aab8d4;
        padding: 1.2rem 0 0.5rem 0;
        font-size: 13px;
    }
    .stDataFrame { background: #fff; border-radius: 12px; }
    .stTabs [role=tablist] { background: #e8f0fb; border-radius: 9px; }
    .stTabs [role=tab] { font-weight: 500; }
    .progress-circle {
        width: 105px;
        height: 105px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# DATA LOADING
# ========================================================================================

@st.cache_data(ttl=300)
def load_data():
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
# MODERN SIDEBAR
# ========================================================================================

with st.sidebar:
    st.markdown('<div class="sidebar-modern">', unsafe_allow_html=True)
    st.markdown("### 🌳 ลิตาการยาง")
    st.markdown("#### 📊 Dashboard")
    st.markdown("---")
    df = load_data()
    if df.empty:
        st.error("ไม่สามารถโหลดข้อมูลได้")
        st.stop()
    st.markdown("#### วันที่")
    selected_date = st.date_input(
        "เลือกวันที่", value=date.today(),
        help="เลือกวันที่ที่ต้องการดูข้อมูล"
    )
    st.markdown("#### สาขา")
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect(
        "เลือกสาขา", options=branches, default=branches,
        help="เลือกสาขาที่ต้องการดูข้อมูล"
    )
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================================
# HEADER
# ========================================================================================

st.markdown("""
<div class="main-header">
    <h1 style="margin-bottom: 0.3rem;">แดชบอร์ดยางพารา</h1>
    <span style="font-weight:400;opacity:0.98;font-size:1.1rem;">ข้อมูลรายวันสรุปภาพรวม · อัปเดตล่าสุด {}</span>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)

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
    # STATISTICS
    total_rubber_today = df_filtered['จำนวนยาง'].sum()
    total_money_today = df_filtered['จำนวนเงิน'].sum()
    total_customers_today = df_filtered['ชื่อลูกค้า'].count()
    avg_price = df_filtered['ราคา'].mean() if len(df_filtered) > 0 else 0
    percent_target = min(100, (total_rubber_today / 2500) * 100)  # sample target: 2500kg

    # SUMMARY ROW (metrics)
    st.markdown("""
    <div class="summary-row">
        <div class="summary-card">
            <span class="summary-label">จำนวนยางรวม</span>
            <span class="summary-value">{:,.1f} กก.</span>
            <span class="summary-sub">วันนี้</span>
        </div>
        <div class="summary-card">
            <span class="summary-label">รายได้รวม</span>
            <span class="summary-value">฿{:,.0f}</span>
            <span class="summary-sub">บาท</span>
        </div>
        <div class="summary-card">
            <span class="summary-label">จำนวนลูกค้า</span>
            <span class="summary-value">{:,.0f}</span>
            <span class="summary-sub">ราย</span>
        </div>
        <div class="summary-card">
            <span class="summary-label">ราคาเฉลี่ย</span>
            <span class="summary-value">{:,.2f}</span>
            <span class="summary-sub">บาท/กก.</span>
        </div>
    </div>
    """.format(total_rubber_today, total_money_today, total_customers_today, avg_price), unsafe_allow_html=True)

    # ====================================================================================
    # MODERN CARDS GRID: Chart, Progress, Calendar, Donut
    # ====================================================================================

    # Layout: [Line Chart] [Progress/Calendar] [Bar/Donut]
    col1, col2, col3 = st.columns([2,1,1])

    # Line chart: Rubber amount vs sales
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("##### ปริมาณยางและยอดขายวันนี้")
        df_filtered_sorted = df_filtered.sort_values("จำนวนยาง", ascending=False)
        if not df_filtered_sorted.empty:
            fig_line = px.line(
                df_filtered_sorted,
                x='ชื่อลูกค้า',
                y=['จำนวนยาง', 'จำนวนเงิน'],
                labels={"value":"ค่า", "variable":"ประเภท"},
                color_discrete_map={"จำนวนยาง": "#667eea", "จำนวนเงิน": "#6ed0fa"},
                markers=True
            )
            fig_line.update_layout(showlegend=True, height=270, font=dict(size=13), margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Progress/Calendar card
    with col2:
        st.markdown('<div class="section-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("##### เป้าหมายวันนี้")
        st.markdown(f"""
        <div class="progress-circle">
            <svg width="90" height="90">
              <circle r="42" cx="45" cy="45" fill="transparent" stroke="#e6e6e6" stroke-width="8"/>
              <circle r="42" cx="45" cy="45"
                fill="transparent"
                stroke="#667eea"
                stroke-width="8"
                stroke-dasharray="{2*3.1416*42}"
                stroke-dashoffset="{2*3.1416*42*(1-percent_target/100)}"
                transform="rotate(-90 45 45)"
              />
              <text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="#667eea" font-size="1.5em">{percent_target:.1f}%</text>
            </svg>
        </div>
        <div class="summary-sub" style="margin-top:0.5rem;">{total_rubber_today:,.1f} / 2,500 กก.</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bar/Donut chart
    with col3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("##### สัดส่วนรายได้แต่ละสาขา")
        money_summary = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
        if not money_summary.empty:
            fig_donut = px.pie(
                money_summary, values='จำนวนเงิน', names='สาขา',
                hole=0.55, color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig_donut.update_layout(
                showlegend=True, height=265,
                margin=dict(l=10, r=10, t=20, b=10),
                font=dict(size=13)
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ====================================================================================
    # MINI GRID: Horizontal Bar & Calendar
    # ====================================================================================
    col4, col5 = st.columns([2,1])
    with col4:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("##### จำนวนยางตามกอง")
        grouped_by_gong = df_filtered.groupby('กอง')['จำนวนยาง'].sum().sort_values().reset_index()
        if not grouped_by_gong.empty:
            fig_bar = px.bar(
                grouped_by_gong,
                x='จำนวนยาง', y='กอง', orientation='h',
                labels={"จำนวนยาง": "จำนวนยาง (กก.)", "กอง": "กอง"},
                color='จำนวนยาง', color_continuous_scale='Blues'
            )
            fig_bar.update_layout(showlegend=False, height=220, font=dict(size=13), margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("##### ปฏิทินเลือกวัน")
        st.date_input("เลือกวันใหม่", key="calendar2", value=selected_date)
        st.markdown('</div>', unsafe_allow_html=True)

    # ====================================================================================
    # DATA TABLES WITH MODERN TABS
    # ====================================================================================
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
    f'<div class="footer-modern">ลิตาการยาง Dashboard | อัพเดท: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div>',
    unsafe_allow_html=True
)
