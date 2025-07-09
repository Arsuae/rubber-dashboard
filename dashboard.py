import streamlit as st
import pandas as pd

# โหลดข้อมูลจาก Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
df = pd.read_csv(sheet_url, header=None)

# ตั้งชื่อคอลัมน์
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# แสดงข้อมูลทั้งหมด
st.subheader("📋 ข้อมูลทั้งหมด")
st.dataframe(df)

# แปลงวันที่ให้เป็น datetime แล้วเลือกเฉพาะข้อมูลของวันนี้
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# ใช้ .dt.date เปรียบเทียบแค่วันที่ (ไม่เอาเวลา)
today = pd.Timestamp.today().date()
df_today = df[df['วันที่'].dt.date == today]

# แสดงข้อมูลวันนี้
st.subheader("📅 ข้อมูลของวันนี้")
st.dataframe(df_today)

# สรุปจำนวนยางต่อสาขา
summary = df_today.groupby('สาขา')['จำนวนยาง'].sum().reset_index()

# แสดงกราฟ
st.title("📊 สรุปจำนวนยางแต่ละสาขา (วันนี้)")
st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')
