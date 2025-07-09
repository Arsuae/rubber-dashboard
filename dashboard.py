import streamlit as st
import pandas as pd
import numpy as np

# ====== CONFIG ======
st.set_page_config(
    page_title="ลิตตาการยาง",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== LOAD DATA FROM GOOGLE SHEETS ======
sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
df = pd.read_csv(sheet_url, header=None)
df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
df['วันที่'] = pd.to_datetime(df['วันที่'], errors='coerce')
today = pd.Timestamp.today().date()
df_today = df[df['วันที่'].dt.date == today]

# ====== SUMMARY BY BRANCH ======
branches = df_today['สาขา'].unique()
branch_summary = df_today.groupby('สาขา').agg({
    'จำนวนยาง': 'sum',
    'จำนวนเงิน': 'sum',
    'ชื่อลูกค้า': 'nunique'
}).reset_index().rename(columns={'ชื่อลูกค้า': 'รายชื่อ'})

# ====== UI ======
st.markdown("""
<h1 style='text-align:center; color:#00AEEF;'>ลิตตาการยาง</h1>
<h3 style='text-align:center;'>ข้อมูลยางพาราก้อนถ้วยวันนี้</h3>
""", unsafe_allow_html=True)

# ====== TOP SUMMARY ======
total_rubber = int(df_today['จำนวนยาง'].sum())
st.markdown("""
<div style='text-align:center;'>
    <div style='display:inline-block; background-color:#444; padding:20px 40px; border-radius:10px;'>
        <h4 style='color:#ddd;'>จำนวนยางวันนี้</h4>
        <h2 style='color:white;'> {:,} </h2>
    </div>
</div>
""".format(total_rubber), unsafe_allow_html=True)

# ====== BRANCH BOXES ======
st.write("\n")
cols = st.columns(len(branches))
for i, row in branch_summary.iterrows():
    with cols[i]:
        st.markdown(f"""
        <div style='background-color:#999; padding:15px; border-radius:10px;'>
            <h4>สาขา {row['สาขา']}</h4>
            <p>จำนวนยาง: <b>{int(row['จำนวนยาง']):,}</b></p>
            <p>จำนวนเงิน: <b>{int(row['จำนวนเงิน']):,}</b></p>
            <p>รายชื่อ: <b>{int(row['รายชื่อ'])}</b></p>
        </div>
        """, unsafe_allow_html=True)

# ====== BAR CHART ======
st.write("\n")
st.subheader("จำนวนยางวันนี้")
st.bar_chart(data=branch_summary, x='สาขา', y='จำนวนยาง', color="#3399ff")

# ====== TABLES PER BRANCH ======
st.write("\n")
st.markdown("""<h3 style='margin-top:30px;'>รายละเอียดต่อสาขา</h3>""", unsafe_allow_html=True)

branch_cols = st.columns(len(branches))
for i, branch in enumerate(branches):
    df_branch = df_today[df_today['สาขา'] == branch][['ชื่อลูกค้า', 'จำนวนยาง', 'ราคา']].sort_values(by='จำนวนยาง', ascending=False)
    with branch_cols[i]:
        st.markdown(f"<h4 style='text-align:center;'>{branch}</h4>", unsafe_allow_html=True)
        st.dataframe(df_branch.reset_index(drop=True), use_container_width=True)
