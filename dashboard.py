import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytz
from datetime import datetime
import plotly.express as px

# ------------------ CONFIG ------------------
st.set_page_config(page_title="ลิตตาการยาง", layout="wide")

st.markdown("<h1 style='color: #00BFFF;'>💧 ลิตตาการยาง</h1>", unsafe_allow_html=True)
st.markdown("### 🧾 ข้อมูลยางพาราก้อนถ้วยวันนี้")

# ------------------ TIMEZONE ------------------
bangkok = pytz.timezone('Asia/Bangkok')
today = datetime.now(bangkok).date()

# ------------------ GOOGLE SHEET ------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)

spreadsheet = client.open_by_key("1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU")  # <== เปลี่ยนเป็นของคุณ
worksheet = spreadsheet.get_worksheet_by_id(2026341208)  # <== gid ของ sheet

data = worksheet.get_all_values()
headers = data[0]
rows = data[1:]
df = pd.DataFrame(rows, columns=headers)

# ------------------ CLEAN DATA ------------------
df = df.replace("", pd.NA).dropna()
df["จำนวนยาง"] = df["จำนวนยาง"].astype(float)
df["ราคา"] = df["ราคา"].astype(float)
df["จำนวนเงิน"] = df["จำนวนเงิน"].str.replace(",", "").astype(float)
df["วันที่"] = pd.to_datetime(df["วันที่"], dayfirst=False).dt.date

# ------------------ FILTER TODAY ------------------
today_df = df[df["วันที่"] == today]

# ------------------ DISPLAY ------------------
col1, col2 = st.columns([1, 3])

with col1:
    st.metric("📊 จำนวนยางวันนี้", f"{int(today_df['จำนวนยาง'].sum()):,}")
    if today_df.empty:
        st.warning("⚠️ ไม่มีข้อมูลของวันนี้")

# ------------------ SUMMARY BY BRANCH ------------------
branch_summary = today_df.groupby("สาขา").agg({
    "จำนวนยาง": "sum",
    "จำนวนเงิน": "sum",
    "ชื่อลูกค้า": "count"
}).rename(columns={"ชื่อลูกค้า": "รายชื่อ"}).reset_index()

with col2:
    st.markdown("### 🔎 สรุปตามสาขา")
    st.dataframe(branch_summary, use_container_width=True)

# ------------------ CHART ------------------
fig = px.bar(branch_summary, x="สาขา", y="จำนวนยาง", color="สาขา",
             title="📈 จำนวนยางตามสาขาวันนี้", text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# ------------------ CUSTOMER TABLE ------------------
st.markdown("### 📋 รายชื่อลูกค้าแยกตามสาขา")

branches = today_df["สาขา"].unique()
for b in branches:
    sub = today_df[today_df["สาขา"] == b][["ชื่อลูกค้า", "จำนวนยาง", "ราคา"]].reset_index(drop=True)
    sub.index += 1
    st.markdown(f"#### 🏠 {b}")
    st.dataframe(sub, use_container_width=True)
