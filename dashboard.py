import streamlit as st
import pandas as pd

# ลิงก์ข้อมูล CSV จาก Google Sheets ชีตชื่อ streamlit-data (gid = 2026341208)
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"

# อ่านข้อมูล โดยใช้แถวที่ 2 ของชีตเป็น header (เพราะแถวแรกมีสูตร REF!)
df = pd.read_csv(sheet_url, header=1)

# แสดงข้อมูลทั้งหมด
st.subheader("🧾 ข้อมูลทั้งหมด")
st.dataframe(df)

# แปลงคอลัมน์วันที่ให้เป็น datetime
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# กรองเฉพาะข้อมูลของวันที่วันนี้
today = pd.Timestamp.today().normalize()
df_today = df[df['วันที่'] == today]

# แสดงข้อมูลวันนี้
st.subheader("📅 ข้อมูลของวันนี้")
st.dataframe(df_today)

# สรุปจำนวนยางรวมต่อสาขา
summary = df_today.groupby('สาขา')['จำนวนยาง'].sum().reset_index()

# แสดงกราฟแท่ง
st.title("📊 สรุปจำนวนยางแต่ละสาขา (วันนี้)")
st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')
