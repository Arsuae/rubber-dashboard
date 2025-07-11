import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

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
# LOAD DATA
# ========================================================================================
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
    df = pd.read_csv(url, header=None)
    df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
    df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')
    df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df['ราคา'] = pd.to_numeric(df['ราคา'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df['จำนวนเงิน'] = pd.to_numeric(df['จำนวนเงิน'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    return df

# ========================================================================================
# STATE HANDLING
# ========================================================================================
if 'tab' not in st.session_state:
    st.session_state.tab = "📑 รายการ"
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
    st.markdown("## 🎛️ ตัวกรองข้อมูล")
    selected_date = st.date_input("เลือกวันที่", value=st.session_state.selected_date)
    st.session_state.selected_date = selected_date

    df = load_data()
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect("เลือกสาขา", options=branches, default=st.session_state.selected_branches or branches)
    st.session_state.selected_branches = selected_branches

    groups = df['กอง'].dropna().unique().tolist()
    if "กอง3" not in groups:
        groups.append("กอง3")
    selected_groups = st.multiselect("เลือกกอง", options=groups, default=st.session_state.selected_groups or groups)
    st.session_state.selected_groups = selected_groups

    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        df = load_data()

# ========================================================================================
# FILTERED DATA
# ========================================================================================
df_filtered = df[
    (df['วันที่'].dt.date == st.session_state.selected_date) &
    (df['สาขา'].isin(st.session_state.selected_branches)) &
    (df['กอง'].isin(st.session_state.selected_groups))
]

# ========================================================================================
# HEADER
# ========================================================================================
st.markdown("""
<div style="background: #2a4d69; padding: 1.5rem; border-radius: 12px; color: white;">
    <h2 style="margin: 0;">ลิตาการยาง</h2>
    <p style="margin: 0;">แดชบอร์ดข้อมูลยางพาราแบบเรียลไทม์</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# TABS
# ========================================================================================
selected_tab = st.radio("เลือกหมวดหมู่", ["📊 ภาพรวม", "📋 สรุป", "📑 รายการ"], horizontal=True, index=["📊 ภาพรวม", "📋 สรุป", "📑 รายการ"].index(st.session_state.tab))
st.session_state.tab = selected_tab

# ========================================================================================
# TAB: ภาพรวม
# ========================================================================================
if selected_tab == "📊 ภาพรวม":
    if df_filtered.empty:
        st.warning("ไม่มีข้อมูลในวันที่ สาขา หรือกองที่เลือก")
        st.stop()

    col1, col2, col3 = st.columns(3)
    col1.metric("จำนวนยางรวม", f"{df_filtered['จำนวนยาง'].sum():,.1f} กก.")
    col2.metric("จำนวนเงิน", f"฿{df_filtered['จำนวนเงิน'].sum():,.0f}")
    col3.metric("จำนวนลูกค้า", f"{df_filtered['ชื่อลูกค้า'].count():,.0f} ราย")

    st.markdown("---")
    st.subheader("🏢 จำนวนยางตามสาขา")
    bar_data = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
    fig_bar = px.bar(bar_data, x='สาขา', y='จำนวนยาง', text='จำนวนยาง', color='จำนวนยาง')
    fig_bar.update_traces(texttemplate='%{text:.1f} กก.', textposition='outside')
    fig_bar.update_layout(font_family="Noto Sans Thai")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("💰 สัดส่วนรายได้")
    pie_data = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
    fig_pie = px.pie(pie_data, values='จำนวนเงิน', names='สาขา', hole=0.4)
    fig_pie.update_traces(textinfo='percent+label')
    fig_pie.update_layout(font_family="Noto Sans Thai")
    st.plotly_chart(fig_pie, use_container_width=True)

# ========================================================================================
# TAB: สรุป
# ========================================================================================
elif selected_tab == "📋 สรุป":
    st.subheader("📦 สรุปข้อมูลตามกอง")
    by_gong = df_filtered.groupby('กอง').agg({'จำนวนยาง': 'sum', 'จำนวนเงิน': 'sum', 'ชื่อลูกค้า': 'count'}).reset_index()
    st.dataframe(by_gong.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า'}), use_container_width=True)

    st.subheader("🏢 สรุปข้อมูลตามสาขา")
    by_branch = df_filtered.groupby('สาขา').agg({'จำนวนยาง': 'sum', 'จำนวนเงิน': 'sum', 'ชื่อลูกค้า': 'count', 'ราคา': 'mean'}).reset_index()
    by_branch = by_branch.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า', 'ราคา': 'ราคาเฉลี่ย'})
    st.dataframe(by_branch, use_container_width=True)

# ========================================================================================
# TAB: รายการ
# ========================================================================================
elif selected_tab == "📑 รายการ":
    st.subheader("📋 รายการลูกค้าทั้งหมด")
    keyword = st.text_input("🔍 ค้นหาชื่อลูกค้า")
    if keyword:
        result_df = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(keyword, case=False, na=False)]
    else:
        result_df = df_filtered

    if result_df.empty:
        st.info("ไม่พบข้อมูลลูกค้าที่ค้นหา")
    else:
        result_df = result_df.reset_index(drop=True)
        display_df = result_df[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']]
        st.dataframe(display_df, use_container_width=True)

        csv = display_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 ดาวน์โหลด", csv, "data.csv", "text/csv", use_container_width=True)

# ========================================================================================
# FOOTER
# ========================================================================================
st.markdown("""
---
<div style="text-align: center; color: gray; font-size: 0.85rem;">
    ลิตาการยาง Dashboard © อัปเดตล่าสุด: {}
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
