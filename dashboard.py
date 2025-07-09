import streamlit as st
import pandas as pd

# -------------------------------
# 1. โหลดข้อมูลจาก Google Sheets
# -------------------------------
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
df = pd.read_csv(sheet_url, header=None)

# ตั้งชื่อคอลัมน์
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# -------------------------------
# 2. แปลงคอลัมน์วันที่ให้เป็น datetime
# -------------------------------
df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')

# -------------------------------
# 3. UI หน้าเว็บ
# -------------------------------
st.set_page_config(page_title="ลิตตาการยาง", layout="wide")
st.title("💧 ลิตตาการยาง")
st.header("ข้อมูลยางพาราก่อนถ้วยวันนี้")

selected_date = st.date_input("เลือกวันที่", pd.Timestamp.today())
branches = df['สาขา'].dropna().unique().tolist()
selected_branches = st.multiselect("เลือกสาขา", branches, default=branches)

# -------------------------------
# 4. กรองข้อมูลตามวันที่และสาขา
# -------------------------------
df_filtered = df[
    (df['วันที่'].dt.date == selected_date) &
    (df['สาขา'].isin(selected_branches))
]

# -------------------------------
# 5. สรุปจำนวนยางรวม
# -------------------------------
st.subheader("📋 จำนวนยางทั้งหมดที่เลือก")
total_amount = df_filtered['จำนวนยาง'].sum()
st.metric("จำนวนยางรวม", f"{total_amount:,.0f}")

if df_filtered.empty:
    st.warning("⚠️ ไม่มีข้อมูลตามวันที่และสาขาที่เลือก")
else:
# แสดงเฉพาะคอลัมน์ที่ต้องการ
columns_to_show = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
st.dataframe(df_filtered[columns_to_show], use_container_width=True)

# -------------------------------
# 6. สรุปจำนวนยางแยกตามกอง
# -------------------------------
st.subheader("📦 สรุปจำนวนยางแยกตามกอง")
grouped_by_gong = df_filtered.groupby('กอง')['จำนวนยาง'].sum().reset_index()
st.dataframe(grouped_by_gong, use_container_width=True)

# -------------------------------
# 7. สรุปกราฟจำนวนยางต่อสาขา
# -------------------------------
st.subheader("📊 สรุปจำนวนยางต่อสาขา")
summary = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
if not summary.empty:
    st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')
