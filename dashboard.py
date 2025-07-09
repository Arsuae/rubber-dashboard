import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ลิตตาการยาง Dashboard",
    layout="wide"
)

# โหลดข้อมูลจาก Google Sheets (CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
df = pd.read_csv(sheet_url, header=None)

# ตั้งชื่อคอลัมน์ให้ตรงกับ Google Sheet
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']

# แปลงคอลัมน์เป็นชนิดที่ถูกต้อง
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')
df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'], errors='coerce')
df['จำนวนเงิน'] = df['จำนวนเงิน'].replace(",", "", regex=True).astype(float)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1 style='color:#00BFFF;'>💧 ลิตตาการยาง</h1>", unsafe_allow_html=True)
st.markdown("### 🧾 ข้อมูลยางพาราก้อนถ้วยวันนี้")

# -------------------------------
# ดึงข้อมูลของวันนี้
# -------------------------------
today = pd.Timestamp.today().date()
df_today = df[df['วันที่'].dt.date == today]

# -------------------------------
# แสดงยอดรวมวันนี้
# -------------------------------
total_rubber = df_today['จำนวนยาง'].sum()
total_money = df_today['จำนวนเงิน'].sum()
total_customers = df_today['ชื่อลูกค้า'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("🧪 จำนวนยางรวมวันนี้", f"{total_rubber:,.0f} กิโล")
col2.metric("💰 จำนวนเงินรวมวันนี้", f"{total_money:,.0f} บาท")
col3.metric("👥 รายชื่อลูกค้า", f"{total_customers} ราย")

# -------------------------------
# สรุปกราฟจำนวนยางต่อสาขา
# -------------------------------
if not df_today.empty:
    summary_rubber = df_today.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
    summary_money = df_today.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()

    st.markdown("### 📊 กราฟจำนวนยางและเงินต่อสาขา")

    col4, col5 = st.columns(2)

    with col4:
        st.bar_chart(data=summary_rubber, x='สาขา', y='จำนวนยาง', use_container_width=True)

    with col5:
        st.bar_chart(data=summary_money, x='สาขา', y='จำนวนเงิน', use_container_width=True)
else:
    st.warning("⚠️ ไม่มีข้อมูลของวันนี้")

# -------------------------------
# ตารางลูกค้าแยกตามสาขา
# -------------------------------
st.markdown("### 📋 รายชื่อลูกค้าแยกตามสาขา")

branches = df_today['สาขา'].unique()
for branch in branches:
    st.markdown(f"#### 🏠 สาขา {branch}")
    branch_data = df_today[df_today['สาขา'] == branch][['ชื่อลูกค้า', 'จำนวนยาง', 'ราคา']]
    st.dataframe(branch_data, use_container_width=True)
