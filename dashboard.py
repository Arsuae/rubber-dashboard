import streamlit as st
import pandas as pd

st.set_page_config(page_title="ลิตตาการยาง", page_icon="💧", layout="wide")

# โหลดข้อมูลจาก Google Sheets (ต้องตั้งค่าสาธารณะให้ export ได้)
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
df = pd.read_csv(sheet_url, header=None)
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# แปลงวันที่
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# ส่วนหัว
st.title("💧 ลิตตาการยาง")
st.markdown("## ข้อมูลยางพาราก่อนถ้วยวันนี้")

# เลือกวันที่
selected_date = st.date_input("เลือกวันที่", pd.Timestamp.today())

# เลือกสาขา
branches = df['สาขา'].dropna().unique().tolist()
selected_branches = st.multiselect("เลือกสาขา", options=branches, default=branches)

# กรองข้อมูล
df_filtered = df[(df['วันที่'].dt.date == selected_date) & (df['สาขา'].isin(selected_branches))]

# แสดงจำนวนรวม
st.subheader("📋 จำนวนยางทั้งหมดที่เลือก")
total_rubber = df_filtered['จำนวนยาง'].sum()
st.metric(label="จำนวนยางรวม", value=f"{total_rubber:,.0f}")

# รวมตามกอง
st.markdown("### 🧮 รวมตามกอง")
group_sum = df_filtered.groupby('กอง')['จำนวนยาง'].sum().reset_index()

for k in ['กอง1', 'กอง2', 'กอง3']:
    amount = group_sum[group_sum['กอง'] == k]['จำนวนยาง'].sum()
    st.write(f"- **{k}**: {amount:,.0f} กิโล")

# แสดงตารางเฉพาะคอลัมน์
if df_filtered.empty:
    st.warning("⚠️ ไม่มีข้อมูลตามวันที่และสาขาที่เลือก")
else:
    show_cols = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
    st.dataframe(df_filtered[show_cols], use_container_width=True)
