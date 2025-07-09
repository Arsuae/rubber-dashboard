import streamlit as st
import pandas as pd

st.set_page_config(page_title="ลิตตากรยาง", layout="wide")

st.title("💧 ลิตตากรยาง")
st.header("ข้อมูลยางพาราก่อนถ้วยวันนี้")

# โหลดข้อมูลจาก Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
df = pd.read_csv(sheet_url, header=None)
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# แปลงวันที่
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')

# 🗓 ตัวเลือกวันที่
available_dates = df['วันที่'].dropna().dt.date.unique()
selected_date = st.date_input("เลือกวันที่", pd.Timestamp.today().date())

# 🏢 ตัวเลือกสาขา
branches = df['สาขา'].dropna().unique().tolist()
selected_branches = st.multiselect("เลือกสาขา", options=branches, default=branches)

# 🔍 กรองข้อมูลตามที่เลือก
filtered_df = df[
    (df['วันที่'].dt.date == selected_date) &
    (df['สาขา'].isin(selected_branches))
]

# 🔢 แสดงจำนวนยางรวม
total_rubber = filtered_df['จำนวนยาง'].sum()
st.subheader("📊 จำนวนยางทั้งหมดที่เลือก")
st.metric(label="จำนวนยางรวม", value=f"{total_rubber:,.0f}")

# ⚠️ ถ้าไม่มีข้อมูล
if filtered_df.empty:
    st.warning("⚠️ ไม่มีข้อมูลตามวันที่และสาขาที่เลือก")
else:
    # 📋 ตารางข้อมูลที่กรองแล้ว
    st.subheader("📄 ข้อมูลที่กรองแล้ว")
    st.dataframe(filtered_df, use_container_width=True)

    # 🧮 สรุปตามสาขา
    summary = filtered_df.groupby('สาขา')[['จำนวนยาง', 'จำนวนเงิน']].sum().reset_index()
    st.subheader("📌 สรุปจำนวนยางและจำนวนเงินต่อสาขา")
    st.dataframe(summary, use_container_width=True)

    # 📊 แสดงกราฟ
    st.subheader("📈 กราฟจำนวนยางตามสาขา")
    st.bar_chart(data=summary, x='สาขา', y='จำนวนยาง')
