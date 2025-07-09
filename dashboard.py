# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Google Sheet CSV URL (ใช้ export เป็น CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"

# โหลดข้อมูลจาก Google Sheet
@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
    df['วันที่'] = pd.to_datetime(df['วันที่']).dt.date
    today_data = df[df['วันที่'] == today]
    return df.dropna(subset=['วันที่'])

# โหลดข้อมูล
st.set_page_config(page_title="ลิตตาการยาง", layout="wide")
st.title("💧 ลิตตาการยาง")
st.markdown("### ข้อมูลยางพาราก่อนถ้วยวันนี้")

df = load_data()
today = pd.Timestamp.now(tz='Asia/Bangkok').normalize().date()
df_today = df[df['วันที่'] == today]

# ---------------------- Summary Section ----------------------
total_today = df_today['จำนวนยาง'].sum()

st.metric("📊 จำนวนยางวันนี้", f"{total_today:,.0f}")

if df_today.empty:
    st.warning("⚠️ ไม่มีข้อมูลของวันนี้")
    st.stop()

# ---------------------- สรุปแยกสาขา ----------------------
st.markdown("### 🗂 รายชื่อลูกค้าแยกตามสาขา")
branches = df_today['สาขา'].unique()
cols = st.columns(len(branches))

for i, branch in enumerate(branches):
    df_branch = df_today[df_today['สาขา'] == branch]
    total_kg = df_branch['จำนวนยาง'].sum()
    total_money = df_branch['จำนวนเงิน'].sum()
    total_customers = df_branch.shape[0]

    with cols[i]:
        st.subheader(f"สาขา {branch}")
        st.metric("จำนวนยาง", f"{total_kg:,.0f}")
        st.metric("จำนวนเงิน", f"{total_money:,.0f}")
        st.metric("รายชื่อ", f"{total_customers}")

# ---------------------- Bar Chart ----------------------
st.markdown("### 📈 จำนวนยางวันนี้")
branch_summary = df_today.groupby('สาขา')[['จำนวนยาง']].sum().reset_index()
fig = px.bar(branch_summary, x='สาขา', y='จำนวนยาง', color='สาขา', text='จำนวนยาง')
fig.update_layout(showlegend=False, height=400)
st.plotly_chart(fig, use_container_width=True)

# ---------------------- ตารางรายชื่อลูกค้า ----------------------
st.markdown("### 📋 รายชื่อลูกค้าแต่ละสาขา")
branch_tabs = st.tabs(branches)
for i, branch in enumerate(branches):
    df_branch = df_today[df_today['สาขา'] == branch][['ชื่อลูกค้า', 'จำนวนยาง', 'ราคา']]
    df_branch = df_branch.sort_values(by='จำนวนยาง', ascending=False).reset_index(drop=True)
    df_branch.index += 1
    branch_tabs[i].dataframe(df_branch, use_container_width=True, hide_index=False)
