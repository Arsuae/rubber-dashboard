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

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;600;700&display=swap');
    html, body, [class*="st-emotion"] {
        font-family: 'Noto Sans Thai', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# 🗂️ DATA LOADING
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
        st.error(f"❌ โหลดข้อมูลไม่สำเร็จ: {e}")
        return pd.DataFrame()

# ========================================================================================
# 🔧 SIDEBAR FILTERS
# ========================================================================================

df = load_data()

with st.sidebar:
    st.markdown("## ⚙️ ตัวกรองข้อมูล")
    today = date.today()
    selected_date = st.date_input("เลือกวันที่", value=today)
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect("เลือกสาขา", options=branches, default=branches)
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ========================================================================================
# 🔍 DATA FILTERING
# ========================================================================================

df_filtered = df[(df['วันที่'].dt.date == selected_date) & (df['สาขา'].isin(selected_branches))]

# ========================================================================================
# 🧭 NAVIGATION BAR
# ========================================================================================

st.markdown("""
<div style="display: flex; align-items: center; gap: 1rem; background: #2a4d69; padding: 1rem 2rem; border-radius: 12px; color: white;">
    <div style="font-size: 2.5rem;">🌳</div>
    <div>
        <div style="font-size: 1.5rem; font-weight: bold;">ลิตาการยาง</div>
        <div style="font-size: 0.95rem;">แดชบอร์ดข้อมูลยางพาราแบบเรียลไทม์</div>
    </div>
</div>
""", unsafe_allow_html=True)

selected_tab = st.radio("เลือกหมวดหมู่", ["📊 ภาพรวม", "📋 สรุป", "📑 รายการ"], horizontal=True)

# ========================================================================================
# 📊 OVERVIEW TAB
# ========================================================================================

if selected_tab == "📊 ภาพรวม":
    if df_filtered.empty:
        st.warning("ไม่พบข้อมูลในวันที่และสาขาที่เลือก")
        st.stop()

    st.markdown("### 🔢 สรุปข้อมูลวันนี้")
    col1, col2, col3 = st.columns(3)
    col1.metric("จำนวนยางรวม", f"{df_filtered['จำนวนยาง'].sum():,.1f} กก.")
    col2.metric("จำนวนเงิน", f"฿{df_filtered['จำนวนเงิน'].sum():,.0f}")
    col3.metric("จำนวนลูกค้า", f"{df_filtered['ชื่อลูกค้า'].count():,.0f} ราย")

    st.markdown("---")
    st.markdown("#### 🏢 จำนวนยางตามสาขา")
    branch_summary = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
    fig1 = px.bar(branch_summary, x='สาขา', y='จำนวนยาง', text='จำนวนยาง', color='จำนวนยาง')
    fig1.update_traces(texttemplate='%{text:.1f} กก.', textposition='outside')
    fig1.update_layout(margin=dict(t=30), font_family="Noto Sans Thai")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("#### 💰 สัดส่วนรายได้")
    money_summary = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
    fig2 = px.pie(money_summary, values='จำนวนเงิน', names='สาขา', hole=0.4)
    fig2.update_traces(textinfo='percent+label')
    fig2.update_layout(font_family="Noto Sans Thai")
    st.plotly_chart(fig2, use_container_width=True)

# ========================================================================================
# 📋 SUMMARY TAB
# ========================================================================================

elif selected_tab == "📋 สรุป":
    st.markdown("### 📦 สรุปตามกอง")
    by_gong = df_filtered.groupby('กอง').agg({'จำนวนยาง': 'sum', 'จำนวนเงิน': 'sum', 'ชื่อลูกค้า': 'count'}).reset_index()
    st.dataframe(by_gong.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า'}), use_container_width=True)

    st.markdown("### 🏢 สรุปตามสาขา")
    by_branch = df_filtered.groupby('สาขา').agg({'จำนวนยาง': 'sum', 'จำนวนเงิน': 'sum', 'ชื่อลูกค้า': 'count', 'ราคา': 'mean'}).reset_index()
    by_branch = by_branch.rename(columns={'ชื่อลูกค้า': 'จำนวนลูกค้า', 'ราคา': 'ราคาเฉลี่ย'})
    st.dataframe(by_branch, use_container_width=True)

# ========================================================================================
# 📑 DETAIL TAB
# ========================================================================================

elif selected_tab == "📑 รายการ":
    st.markdown("### 🔍 ค้นหารายชื่อลูกค้า")
    keyword = st.text_input("ค้นหาชื่อลูกค้า")
    if keyword:
        df_search = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(keyword, case=False, na=False)]
    else:
        df_search = df_filtered

    if df_search.empty:
        st.info("ไม่พบข้อมูลลูกค้าที่ค้นหา")
    else:
        st.dataframe(df_search[['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']], use_container_width=True)

    csv = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 ดาวน์โหลดข้อมูลทั้งหมด", csv, "data.csv", "text/csv", use_container_width=True)

# ========================================================================================
# 📌 FOOTER
# ========================================================================================

st.markdown("""
---
<div style="text-align: center; color: gray; padding: 1rem; font-size: 0.85rem;">
    ลิตาการยาง Dashboard © อัพเดตล่าสุด: {}
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
