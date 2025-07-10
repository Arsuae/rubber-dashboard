import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================ DARK THEME CSS FOR MODERN DASHBOARD ======================
st.markdown("""
<style>
body, .stApp { background: #10131a !important; color: #e5e7ef;}
.main-header {
    background: linear-gradient(90deg, #22243b 0%, #2c3254 100%);
    padding: 2rem 1rem 1.2rem 1rem;
    border-radius: 18px;
    text-align: left;
    color: #fff !important;
    margin-bottom: 1.8rem;
    box-shadow: 0 3px 22px rgba(10,10,15,0.18);
    font-family: 'Inter', sans-serif;
}
.section-card {
    background: #181c26;
    border-radius: 14px;
    box-shadow: 0 2px 16px rgba(25,30,40,0.13);
    padding: 1.3rem 1.2rem 1.5rem 1.2rem;
    margin-bottom: 1.5rem;
}
.dashboard-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1.3rem;
    margin-bottom: 1rem;
}
.dashboard-col {
    flex: 1 1 0px;
    min-width: 350px;
    max-width: 49%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}
.dashboard-col-wide {
    flex: 2 1 0px;
    min-width: 600px;
    max-width: 72%;
    display: flex;
    flex-direction: column;
}
.metric-card {
    border-radius: 12px;
    margin: 0.3rem 0;
    padding: 1.2rem 0.9rem;
    font-size: 1.7rem;
    font-weight: 700;
    text-align: center;
    background: #1e222f;
    color: #fff;
    box-shadow: 0 2px 8px rgba(44,62,80,0.07);
}
.metric-title {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #7ee787;
}
.metric-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: #ffd700;
}
.metric-value2 { color: #34b4eb; }
.metric-value3 { color: #ffc107; }
.metric-label { font-size: 1rem; color: #aab8d4; font-weight: 400;}
.stTabs [role=tablist] { background: #1e222f; border-radius: 9px; }
.stTabs [role=tab] { font-weight: 500; color: #bbb; }
.stTabs [aria-selected="true"] { color: #FF6161; }
.stDataFrame { background: #181c26; border-radius: 12px; color: #fff; }
.footer-modern {
    text-align: center;
    color: #888;
    padding: 1.2rem 0 0.5rem 0;
    font-size: 13px;
}
.summary-title {
    font-size: 1.55rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 1.2rem;
    margin-top: 0.5rem;
    letter-spacing: 0.01em;
}
.stat-card {
    background: #28a745;
    border-radius: 11px;
    padding: 0.8rem 1.2rem;
    color: #fff;
    text-align: center;
    margin: 0.3rem 0.1rem;
    font-size: 1.3rem;
    font-weight: bold;
}
.stat-card2 { background: #17a2b8; }
.stat-card3 { background: #ffc107; color: #222;}
hr {border-top: 1px solid #22243b;}
</style>
""", unsafe_allow_html=True)

# ============================ DATA LOADING ============================
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

# ============================ SIDEBAR ============================
with st.sidebar:
    st.header("🌳 ลิตาการยาง")
    df = load_data()
    if df.empty:
        st.error("ไม่สามารถโหลดข้อมูลได้")
        st.stop()
    st.subheader("เลือกวันที่")
    selected_date = st.date_input("เลือกวันที่", value=date.today(), help="เลือกวันที่ที่ต้องการดูข้อมูล")
    st.subheader("เลือกสาขา")
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect("เลือกสาขา", options=branches, default=branches, help="เลือกสาขาที่ต้องการดูข้อมูล")
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ============================ HEADER ============================
st.markdown("""
<div class="main-header">
    <h1>ลิตาการยาง · Dashboard</h1>
    <span>แดชบอร์ดสรุปข้อมูลยางพารา · <b>อัปเดต {}</b></span>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)

# ============================ DATA FILTERING ============================
df_filtered = df[
    (df['วันที่'].dt.date == selected_date) &
    (df['สาขา'].isin(selected_branches))
]

# ============================ MAIN DASHBOARD ============================
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

    # ============================ TOP CARDS ROW ============================
    st.markdown('<div class="dashboard-row">', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-col"></div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-col"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ============================ MIDDLE CARDS (3 cols) ============================
    st.markdown('<div class="dashboard-row">', unsafe_allow_html=True)

    # ----- ปริมาณยางและยอดขายวันนี้ (Line Chart) -----
    st.markdown('<div class="dashboard-col-wide section-card">', unsafe_allow_html=True)
    st.markdown('<div class="summary-title">ปริมาณยางและยอดขายวันนี้</div>', unsafe_allow_html=True)
    df_filtered_sorted = df_filtered.sort_values("จำนวนยาง", ascending=False)
    if not df_filtered_sorted.empty:
        fig_line = px.line(
            df_filtered_sorted,
            x='ชื่อลูกค้า',
            y=['จำนวนยาง', 'จำนวนเงิน'],
            labels={"value":"ค่า", "variable":"ประเภท"},
            color_discrete_map={"จำนวนยาง": "#7ee787", "จำนวนเงิน": "#34b4eb"},
            markers=True,
            template="plotly_dark"
        )
        fig_line.update_layout(
            showlegend=True, height=350, font=dict(size=13),
            margin=dict(l=10, r=10, t=20, b=10),
            plot_bgcolor='#181c26', paper_bgcolor='#181c26',
        )
        fig_line.update_xaxes(tickangle=45)
        st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ----- เป้าหมายวันนี้ (Progress Circle) -----
    st.markdown('<div class="dashboard-col section-card" style="align-items:center;text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="summary-title">เป้าหมายวันนี้</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <svg width="120" height="120" style="display:block;margin:auto;">
      <circle r="50" cx="60" cy="60" fill="transparent" stroke="#22243b" stroke-width="12"/>
      <circle r="50" cx="60" cy="60"
        fill="transparent"
        stroke="#7ee787"
        stroke-width="12"
        stroke-dasharray="{2*3.1416*50}"
        stroke-dashoffset="{2*3.1416*50*(1-percent_target/100)}"
        transform="rotate(-90 60 60)"
        style="transition:stroke-dashoffset 1s;"
      />
      <text x="60" y="70" text-anchor="middle" fill="#7ee787" font-size="1.8em" font-family="Arial" font-weight="bold">{percent_target:.1f}%</text>
    </svg>
    <div class="metric-label" style="margin-top:0.5rem;">{total_rubber_today:,.1f} / 2,500 กก.</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ----- สัดส่วนรายได้แต่ละสาขา (Donut Chart) -----
    st.markdown('<div class="dashboard-col section-card">', unsafe_allow_html=True)
    st.markdown('<div class="summary-title">สัดส่วนรายได้แต่ละสาขา</div>', unsafe_allow_html=True)
    money_summary = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
    if not money_summary.empty:
        fig_donut = px.pie(
            money_summary, values='จำนวนเงิน', names='สาขา',
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Blues_r,
            template="plotly_dark"
        )
        fig_donut.update_layout(
            showlegend=True, height=350,
            margin=dict(l=10, r=10, t=20, b=10),
            font=dict(size=13),
            plot_bgcolor='#181c26', paper_bgcolor='#181c26',
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ============================ LOWER CARDS (2 cols) ============================
    st.markdown('<div class="dashboard-row">', unsafe_allow_html=True)
    # ----- จำนวนยางตามกอง (Horizontal Bar) -----
    st.markdown('<div class="dashboard-col-wide section-card">', unsafe_allow_html=True)
    st.markdown('<div class="summary-title">จำนวนยางตามกอง</div>', unsafe_allow_html=True)
    grouped_by_gong = df_filtered.groupby('กอง')['จำนวนยาง'].sum().sort_values().reset_index()
    if not grouped_by_gong.empty:
        fig_bar = px.bar(
            grouped_by_gong,
            x='จำนวนยาง', y='กอง', orientation='h',
            labels={"จำนวนยาง": "จำนวนยาง (กก.)", "กอง": "กอง"},
            color='จำนวนยาง', color_continuous_scale='Blues',
            template="plotly_dark"
        )
        fig_bar.update_layout(
            showlegend=False, height=250, font=dict(size=13),
            margin=dict(l=10, r=10, t=20, b=10),
            plot_bgcolor='#181c26', paper_bgcolor='#181c26',
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # ----- ปฏิทินเลือกวัน -----
    st.markdown('<div class="dashboard-col section-card">', unsafe_allow_html=True)
    st.markdown('<div class="summary-title">ปฏิทินเลือกวัน</div>', unsafe_allow_html=True)
    st.date_input("เลือกวันใหม่", key="calendar2", value=selected_date)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ============================ BRANCH STATISTIC CARDS ============================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="summary-title">🏬 สถิติแยกตามสาขา</div>', unsafe_allow_html=True)
    branch_stats = df_filtered.groupby('สาขา').agg({
        'จำนวนยาง': 'sum', 'จำนวนเงิน': 'sum', 'ชื่อลูกค้า': 'count'
    }).reset_index()
    for i, row in branch_stats.iterrows():
        st.markdown(f"##### สาขา {row['สาขา']}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="stat-card">
                <div>จำนวนยาง</div>
                <div class="metric-value">{row['จำนวนยาง']:,.1f} กก.</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="stat-card stat-card2">
                <div>จำนวนเงิน</div>
                <div class="metric-value2">฿{row['จำนวนเงิน']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="stat-card stat-card3">
                <div>จำนวนรายการ</div>
                <div class="metric-value3">{row['ชื่อลูกค้า']:,.0f} ราย</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

    # ============================ TABS FOR DATA TABLES ============================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📋 ข้อมูลทั้งหมด", "📦 สรุปตามกอง", "🏬 สรุปตามสาขา"])
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

# ============================ FOOTER ============================
st.markdown(
    f'<div class="footer-modern">ลิตาการยาง Dashboard | อัพเดท: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div>',
    unsafe_allow_html=True
)
