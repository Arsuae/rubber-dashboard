import streamlit as st
import pandas as pd

# URL ของ Google Sheet ของคุณ (เปลี่ยนตรงนี้)
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv"
df = pd.read_csv(sheet_url)

# แปลงวันที่เป็น datetime
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# กรองเฉพาะวันนี้
today = pd.Timestamp.today().normalize()
df_today = df[df['วันที่'] == today]

# รวมจำนวนยางตามสาขา
summary = df_today.groupby('สาขา')['จำนวนยาง'].sum().reset_index()

# แสดง Dashboard
st.title("📊 สรุปจำนวนยางแต่ละสาขา (วันนี้)")
st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')
