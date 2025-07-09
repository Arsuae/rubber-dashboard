import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="ลิตตาการยาง", layout="wide")

# -----------------------------
# 1. ดึงข้อมูลจาก Google Sheets
# -----------------------------
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"

df = pd.read_csv(sheet_url)

# ตั้งชื่อคอลัมน์ให้ตรงกับ Google Sheets
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# -----------------------------
# 2. แปลงค่าวันที่เป็น datetime
# -----------------------------
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce').dt.normalize()
today = pd.Timestamp.today().normalize()
df_today = df[df['วันที่'] == today]

# -----------------------------
# 3. กรองข้อมูลเฉพาะ "วันนี้"
# -----------------------------
today = pd.Timestamp.today().normalize()
df_today = df[df['วันที่'] == today]

# -----------------------------
# 4. Header
# -----------------------------
st.markdown("<h1 style='text-align: center; color: #00b4d8;'>ลิตตาการยาง</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>ข้อมูลยางพาราก่อนถ้วยวันนี้</h3>", unsafe_allow_html=True)

# -----------------------------
# 5. จำนวนยางรวมทั้งหมดวันนี้
# -----------------------------
total_rubber = df_today["จำนวนยาง"].sum()
st.markdown("### 🧮 จำนวนยางวันนี้")
st.metric(label="จำนวนยางวันนี้", value=f"{total_rubber:,.0f}")

# -----------------------------
# 6. แสดงค่าสรุปของแต่ละสาขา
# -----------------------------
branches = df_today['สาขา'].dropna().unique().tolist()

if len(branches) > 0:
    st.markdown("### 🏪 รายงานแยกตามสาขา")
    cols = st.columns(len(branches))
    for i, branch in enumerate(branches):
        branch_df = df_today[df_today["สาขา"] == branch]
        total_rubber = branch_df["จำนวนยาง"].sum()
        total_money = branch_df["จำนวนเงิน"].sum()
        buyer_count = branch_df.shape[0]

        with cols[i]:
            st.markdown(f"**สาขา {branch}**")
            st.metric("จำนวนยาง", f"{total_rubber:,.0f}")
            st.metric("จำนวนเงิน", f"{total_money:,.0f}")
            st.metric("รายชื่อ", f"{buyer_count}")
else:
    st.warning("⚠️ ไม่มีข้อมูลของวันนี้")

# -----------------------------
# 7. กราฟ bar ยางแยกตามสาขา
# -----------------------------
if not df_today.empty:
    summary = df_today.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
    fig = px.bar(summary, x='สาขา', y='จำนวนยาง', title='จำนวนยางวันนี้', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 8. ตารางรายชื่อแยกตามสาขา
# -----------------------------
st.markdown("### 📋 รายชื่อลูกค้าแยกตามสาขา")

cols = st.columns(len(branches)) if len(branches) > 0 else []
for i, branch in enumerate(branches):
    with cols[i]:
        st.markdown(f"**{branch}**")
        branch_df = df_today[df_today["สาขา"] == branch][['ชื่อลูกค้า', 'จำนวนยาง', 'ราคา']].reset_index(drop=True)
        branch_df.index += 1
        st.dataframe(branch_df, use_container_width=True)
