import streamlit as st
import pandas as pd

st.set_page_config(page_title="ลิตตากาการยาง", page_icon="💧", layout="wide")

st.title("💧 ลิตตากาการยาง")
st.header("ข้อมูลยางพาราก่อนถ้วยวันนี้")

# โหลดข้อมูลจาก Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
df = pd.read_csv(sheet_url, header=None)
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# แปลงวันที่ให้เป็น datetime
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# วันที่และสาขาที่เลือก
selected_date = st.date_input("เลือกวันที่", pd.Timestamp.today())
selected_branches = st.multiselect("เลือกสาขา", options=df['สาขา'].unique().tolist(), default=df['สาขา'].unique().tolist())

# กรองข้อมูลตามวันที่และสาขา
df_filtered = df[(df['วันที่'].dt.date == selected_date) & (df['สาขา'].isin(selected_branches))]

# แสดงผลรวม
st.subheader("🧾 จำนวนยางทั้งหมดที่เลือก")
st.metric("จำนวนยางรวม", f"{df_filtered['จำนวนยาง'].sum():,.0f}")

# สรุปผลรวมต่อกอง
st.subheader("📊 สรุปจำนวนยางแต่ละกอง")
summary = df_filtered.groupby('กอง')['จำนวนยาง'].sum().reset_index()
st.dataframe(summary, use_container_width=True)

# ตารางข้อมูลแบบคอลัมน์ที่เลือก
st.subheader("📄 ข้อมูลที่กรองแล้ว")
if df_filtered.empty:
    st.warning("⚠️ ไม่มีข้อมูลตามวันที่และสาขาที่เลือก")
else:
    columns_to_show = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
    st.dataframe(df_filtered[columns_to_show], use_container_width=True)
