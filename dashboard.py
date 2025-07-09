import streamlit as st
import pandas as pd

# ลิงก์ Google Sheet (CSV export) ต้องเปิดสิทธิ์ดูได้
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/edit?gid=2026341208#gid=2026341208"

# อ่านโดยไม่ใช้แถวแรกเป็นหัวตาราง
df = pd.read_csv(sheet_url, header=None)

# ตั้งชื่อคอลัมน์เอง
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# แสดงข้อมูลทั้งหมด
st.subheader("📋 ข้อมูลทั้งหมด")
st.write(df)

# แปลงคอลัมน์วันที่
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# กรองเฉพาะวันนี้
today = pd.Timestamp.today().normalize()
df_today = df[df['วันที่'] == today]

st.subheader("📅 ข้อมูลของวันนี้")
st.write(df_today)

# รวมจำนวนยางต่อสาขา
summary = df_today.groupby('สาขา')['จำนวนยาง'].sum().reset_index()

# แสดงกราฟ
st.title("📊 สรุปจำนวนยางแต่ละสาขา (วันนี้)")
st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')
