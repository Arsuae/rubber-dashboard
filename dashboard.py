import streamlit as st
import pandas as pd

# ลิงก์ดึงข้อมูลจากชีตชื่อ "หน้าหลัก"
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/gviz/tq?tqx=out:csv&sheet=หน้าหลัก"
df = pd.read_csv(sheet_url)

# แสดงข้อมูลทั้งหมด (debug ชั่วคราว)
st.subheader("📄 ข้อมูลทั้งหมด")
st.write(df)

# แปลงวันที่ให้เป็น datetime
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# กรองเฉพาะวันนี้
today = pd.Timestamp.today().normalize()
df_today = df[df['วันที่'] == today]

st.subheader("📆 ข้อมูลของวันนี้")
st.write(df_today)

# รวมจำนวนยางตามสาขา
summary = df_today.groupby('สาขา')['จำนวนยาง'].sum().reset_index()

# แสดงกราฟ
st.title("📊 สรุปจำนวนยางแต่ละสาขา (วันนี้)")
st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')
