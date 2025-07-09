import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ลิตตากรยาง", layout="wide")

st.markdown("<h1 style='text-align: center; color: #00BFFF;'>💧 ลิตตากรยาง</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>ข้อมูลยางพาราก่อนถ้วยวันนี้</h3>", unsafe_allow_html=True)

# โหลดข้อมูลจาก Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
df = pd.read_csv(sheet_url, header=None)
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# แปลงวันที่
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# ข้อมูลวันนี้
today = pd.Timestamp.today().date()
df_today = df[df['วันที่'].dt.date == today]

# ====== CARD SECTION ======
st.subheader("📅 จำนวนยางวันนี้")

total_today = df_today['จำนวนยาง'].sum() if not df_today.empty else 0
st.metric("จำนวนยางวันนี้", f"{total_today:,.0f}")

# ====== ถ้าไม่มีข้อมูล ======
if df_today.empty:
    st.warning("⚠️ ไม่มีข้อมูลของวันนี้")
else:
    # ====== รายชื่อลูกค้าแยกตามสาขา ======
    st.subheader("📋 รายชื่อลูกค้าแยกตามสาขา")
    branches = df_today['สาขา'].unique()

    for branch in branches:
        st.markdown(f"### 🏠 {branch}")
        df_branch = df_today[df_today['สาขา'] == branch][['ชื่อลูกค้า', 'จำนวนยาง', 'ราคา']]
        st.dataframe(df_branch, use_container_width=True)

    # ====== รวมยอดสาขา ======
    st.subheader("📊 สรุปจำนวนยางแต่ละสาขา (วันนี้)")
    summary = df_today.groupby('สาขา').agg({
        'จำนวนยาง': 'sum',
        'จำนวนเงิน': 'sum',
        'ชื่อลูกค้า': 'count'
    }).reset_index()
    summary.columns = ['สาขา', 'จำนวนยาง', 'จำนวนเงิน', 'รายชื่อ']

    col1, col2, col3 = st.columns(3)
    for i, row in summary.iterrows():
        with [col1, col2, col3][i % 3]:
            st.metric(f"📦 {row['สาขา']}", f"{row['จำนวนยาง']:,.0f} ยาง", f"{row['จำนวนเงิน']:,.0f} บาท | {row['รายชื่อ']} ราย")

    # ====== แสดงกราฟแท่ง ======
    st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')

# ====== แสดงตารางข้อมูลทั้งหมด (ย้อนหลัง) ======
with st.expander("🗂 ดูข้อมูลย้อนหลังทั้งหมด"):
    st.dataframe(df.sort_values(by='วันที่', ascending=False), use_container_width=True)
