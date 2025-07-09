import streamlit as st
import pandas as pd

# ลิงก์ข้อมูลจาก Google Sheets (gid = 2026341208 -> ชีต streamlit-data)
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"

# อ่านข้อมูลแบบไม่มี header แล้วตั้งชื่อคอลัมน์เอง
df = pd.read_csv(sheet_url, header=None)
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# แสดงข้อมูลทั้งหมด
st.subheader("📋 ข้อมูลทั้งหมด")
st.dataframe(df)

# แปลงคอลัมน์วันที่ให้เป็น datetime
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# กรองเฉพาะข้อมูลของวันนี้
today = pd.Timestamp.today().normalize()
df_today = df[df['วันที่'] == today]

# แสดงข้อมูลวันนี้
st.subheader("📅 ข้อมูลของวันนี้")
st.dataframe(df_today)

# สรุปจำนวนยางต่อสาขา
summary = df_today.groupby('สาขา')['จำนวนยาง'].sum().reset_index()

# แสดงกราฟ
st.title("📊 สรุปจำนวนยางแต่ละสาขา (วันนี้)")
st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')
