import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ========================================================================================
# 📊 CONFIGURATION & STYLING
# ========================================================================================

st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;600;700&display=swap');

    html, body, [class*="st-emotion"] { /* Target Streamlit's main content wrapper */
        font-family: 'Noto Sans Thai', sans-serif;
        color: #333; /* Darker text for better readability */
    }

    .main-header {
        background: linear-gradient(135deg, #2a4d69 0%, #4b86b4 100%);
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Slightly stronger shadow for header */
        animation: fadeIn 1s ease-out; /* Add a subtle fade-in animation */
    }
    
    .main-header h1 {
        font-size: 2.8rem; /* Slightly larger heading */
        font-weight: 700;
        margin-bottom: 0.75rem; /* Increased margin */
        letter-spacing: 1.5px; /* Added letter spacing for visual appeal */
    }
    
    .main-header p {
        font-size: 1.3rem; /* Slightly larger paragraph */
        font-weight: 300;
        opacity: 0.95; /* Slightly less opaque */
    }

    .branch-section { /* This class doesn't seem to be explicitly used, but good to have */
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #6ab04c 0%, #55efc4 100%);
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease; /* Added box-shadow transition */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Default subtle shadow */
    }
    
    .stats-card:hover {
        transform: translateY(-7px); /* Slightly more pronounced lift */
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Stronger shadow on hover */
    }
    
    .metric-card { /* This class is also not directly used, but good for reference */
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4b86b4;
        margin: 1rem 0;
        transition: box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .info-card {
        background: linear-gradient(135deg, #4834d4 0%, #686de0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Added shadow for info card */
    }
    
    .sidebar .sidebar-content {
        background: #ffffff;
        border-right: 1px solid #e9ecef;
        padding: 1rem;
    }
    
    .stMetric {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08); /* Slightly lighter shadow */
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #e0e0e0; /* Subtle border */
    }
    
    .stMetric:hover {
        transform: translateY(-5px); /* Slightly more pronounced lift */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12); /* Stronger shadow on hover */
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .company-title { /* Not explicitly used, but a good style */
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #2a4d69;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }
    
    .total-summary {
        background: linear-gradient(135deg, #1dd1a1 0%, #00b894 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Stronger shadow for total summary */
    }
    
    .stButton>button {
        background: #4b86b4;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem; /* Slightly larger padding for buttons */
        font-weight: 600;
        transition: background 0.3s ease, transform 0.2s ease; /* Added transform transition */
        border: none; /* Remove default border */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        background: #2a4d69;
        transform: translateY(-2px); /* Subtle lift on hover */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stTextInput>div>div>input { /* More specific target for text input */
        border-radius: 8px;
        border: 1px solid #ced4da; /* More defined border color */
        padding: 0.6rem 1rem; /* Adjusted padding */
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05); /* Inner shadow for depth */
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #4b86b4; /* Highlight border on focus */
        box-shadow: 0 0 0 0.2rem rgba(75, 134, 180, 0.25); /* Focus ring */
        outline: none;
    }
    
    h1, h2, h3, h4, h5, h6 { /* Apply Noto Sans Thai to all headings */
        font-family: 'Noto Sans Thai', sans-serif;
        color: #2a4d69;
        font-weight: 600;
    }

    h3 {
        font-size: 1.75rem; /* Slightly larger h3 */
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 1.25rem; /* Larger tabs for better clickability */
        border-radius: 8px;
        color: #4b86b4; /* Color for inactive tabs */
        transition: background 0.2s ease, color 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e9ecef;
        color: #2a4d69; /* Darker text on hover */
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #4b86b4; /* Active tab background */
        color: white; /* Active tab text color */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Shadow for active tab */
    }

    /* Keyframe for fade-in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Apply fade-in to main content elements */
    .stBlock, .stColumn {
        animation: fadeIn 0.8s ease-out forwards;
        animation-delay: var(--animation-delay, 0s); /* Use a CSS variable for staggered delays */
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# 🗂️ DATA LOADING & PROCESSING
# ========================================================================================

@st.cache_data(ttl=300)
def load_data():
    """Load data from Google Sheets with caching"""
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
        df = pd.read_csv(sheet_url, header=None)
        
        df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
        df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')
        df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['ราคา'] = pd.to_numeric(df['ราคา'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['จำนวนเงิน'] = pd.to_numeric(df['จำนวนเงิน'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดข้อมูลได้: {str(e)}")
        return pd.DataFrame()

# ========================================================================================
# 🎨 HEADER SECTION
# ========================================================================================

st.markdown("""
<div class="main-header">
    <h1>ลิตาการยาง</h1>
    <p>แดชบอร์ดข้อมูลยางพาราแบบเรียลไทม์</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# 📊 SIDEBAR CONTROLS
# ========================================================================================

with st.sidebar:
    st.markdown("### ⚙️ การควบคุม")
    
    df = load_data()
    
    if df.empty:
        st.error("ไม่สามารถโหลดข้อมูลได้ โปรดตรวจสอบการเชื่อมต่อหรือแหล่งข้อมูล")
        st.stop()
    
    st.markdown("#### 📅 ตัวเลือกวันที่")
    selected_date = st.date_input(
        "เลือกวันที่",
        value=date.today(),
        help="เลือกวันที่ที่ต้องการดูข้อมูล"
    )
    
    st.markdown("#### 🏢 ตัวเลือกสาขา")
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect(
        "เลือกสาขา",
        options=branches,
        default=branches,
        help="เลือกสาขาที่ต้องการดูข้อมูล"
    )
    
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ========================================================================================
# 📈 DATA FILTERING & PROCESSING
# ========================================================================================

df_filtered = df[
    (df['วันที่'].dt.date == selected_date) &
    (df['สาขา'].isin(selected_branches))
]

# ========================================================================================
# 📊 MAIN DASHBOARD
# ========================================================================================

if df_filtered.empty:
    st.markdown("""
    <div class="info-card">
        <h3>⚠️ ไม่มีข้อมูล</h3>
        <p>ไม่พบข้อมูลสำหรับวันที่และสาขาที่เลือก กรุณาเลือกวันที่หรือสาขาอื่น</p>
    </div>
    """, unsafe_allow_html=True)
else:
    branch_stats = df_filtered.groupby('สาขา').agg({
        'จำนวนยาง': 'sum',
        'จำนวนเงิน': 'sum',
        'ชื่อลูกค้า': 'count'
    }).reset_index()
    
    total_rubber_today = df_filtered['จำนวนยาง'].sum()
    total_money_today = df_filtered['จำนวนเงิน'].sum()
    total_customers_today = df_filtered['ชื่อลูกค้า'].count()
    
    # ========================================================================================
    # 📊 TOTAL SUMMARY SECTION
    # ========================================================================================
    
    st.markdown(f"""
    <div class="total-summary">
        <h2>📊 สรุปข้อมูลวันนี้</h2>
        <div style="display: flex; justify-content: center; gap: 2.5rem; margin-top: 1.5rem;">
            <div class="stats-card" style="background: linear-gradient(135deg, #6ab04c 0%, #55efc4 100%);">
                <div style="font-size: 1.1rem; font-weight: 400;">จำนวนยางรวม</div>
                <div style="font-size: 2.2rem; font-weight: 700;">{total_rubber_today:,.1f} กก.</div>
            </div>
            <div class="stats-card" style="background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);">
                <div style="font-size: 1.1rem; font-weight: 400;">จำนวนเงิน</div>
                <div style="font-size: 2.2rem; font-weight: 700;">฿{total_money_today:,.0f}</div>
            </div>
            <div class="stats-card" style="background: linear-gradient(135deg, #fdcb6e 0%, #ffeaa7 100%);">
                <div style="font-size: 1.1rem; font-weight: 400;">จำนวนลูกค้า</div>
                <div style="font-size: 2.2rem; font-weight: 700;">{total_customers_today:,.0f} ราย</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================================================
    # 📊 CHARTS SECTION
    # ========================================================================================
    
    st.markdown("---")
    st.markdown("### 📈 ภาพรวมการดำเนินงาน")

    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### 📊 จำนวนยางตามสาขา")
        branch_summary = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
        
        if not branch_summary.empty:
            fig_branch = px.bar(
                branch_summary,
                x='สาขา',
                y='จำนวนยาง',
                title="จำนวนยางแยกตามสาขา",
                color='จำนวนยาง',
                color_continuous_scale='teal', # Retained a good color scale
                text='จำนวนยาง'
            )
            fig_branch.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, family='Noto Sans Thai'),
                title_font=dict(size=18, family='Noto Sans Thai', weight='bold', color='#2a4d69'), # Larger, bolder chart title
                margin=dict(t=70, b=50), # Adjust margin for title
                hoverlabel=dict(font_family='Noto Sans Thai') # Ensure hover text is also Thai font
            )
            fig_branch.update_traces(texttemplate='%{text:,.1f} กก.', textposition='outside') # More descriptive text
            st.plotly_chart(fig_branch, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### 💰 สัดส่วนรายได้ตามสาขา")
        money_summary = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
        
        if not money_summary.empty:
            fig_money = px.pie(
                money_summary,
                values='จำนวนเงิน',
                names='สาขา',
                title="สัดส่วนรายได้ตามสาขา",
                color_discrete_sequence=px.colors.qualitative.Pastel # Good choice
            )
            fig_money.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, family='Noto Sans Thai'),
                title_font=dict(size=18, family='Noto Sans Thai', weight='bold', color='#2a4d69'), # Larger, bolder chart title
                margin=dict(t=70, b=50), # Adjust margin for title
                hoverlabel=dict(font_family='Noto Sans Thai')
            )
            fig_money.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=1))) # White border for slices
            st.plotly_chart(fig_money, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================================================
    # BRANCH STATISTICS SECTION
    # ========================================================================================

    st.markdown("---")
    st.markdown("### 🏢 สถิติแยกตามสาขา")
    
    for i, row in branch_stats.iterrows():
        st.markdown(f"#### สาขา **{row['สาขา']}**") # Bold the branch name for emphasis
        col_b1, col_b2, col_b3 = st.columns(3)
        
        with col_b1:
            st.markdown(f"""
            <div class="stats-card" style="background: linear-gradient(135deg, #6ab04c 0%, #55efc4 100%);">
                <div style="font-size: 1rem;">จำนวนยาง</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{row['จำนวนยาง']:,.1f} กก.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b2:
            st.markdown(f"""
            <div class="stats-card" style="background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);">
                <div style="font-size: 1rem;">จำนวนเงิน</div>
                <div style="font-size: 1.8rem; font-weight: 700;">฿{row['จำนวนเงิน']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b3:
            st.markdown(f"""
            <div class="stats-card" style="background: linear-gradient(135deg, #fdcb6e 0%, #ffeaa7 100%);">
                <div style="font-size: 1rem;">จำนวนลูกค้า</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{row['ชื่อลูกค้า']:,.0f} ราย</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---") # Add a separator after each branch

    # ========================================================================================
    # 📋 DATA TABLES SECTION
    # ========================================================================================
    
    st.markdown("### 📊 รายละเอียดข้อมูลและสรุป")
    
    tab1, tab2, tab3 = st.tabs(["📋 ข้อมูลทั้งหมด", "📦 สรุปตามกอง", "🏢 สรุปตามสาขา"])
    
    with tab1:
        st.markdown("#### 📋 รายละเอียดการซื้อขายทั้งหมด")
        columns_to_show = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
        
        search_term = st.text_input("🔍 ค้นหาลูกค้า", placeholder="พิมพ์ชื่อลูกค้าที่ต้องการค้นหา...", key="customer_search")
        
        if search_term:
            df_display = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(search_term, case=False, na=False)]
        else:
            df_display = df_filtered
        
        if df_display.empty:
            st.info("ไม่พบข้อมูลลูกค้าที่ค้นหา.")
        else:
            st.dataframe(
                df_display[columns_to_show],
                use_container_width=True,
                hide_index=True,
                column_config={
                    'จำนวนยาง': st.column_config.NumberColumn(
                        'จำนวนยาง (กก.)',
                        help='ปริมาณยางที่ซื้อ (กิโลกรัม)',
                        format='%.1f'
                    ),
                    'ราคา': st.column_config.NumberColumn(
                        'ราคา (บาท/กก.)',
                        help='ราคาต่อกิโลกรัม (บาท)',
                        format='%.2f'
                    ),
                    'จำนวนเงิน': st.column_config.NumberColumn(
                        'จำนวนเงิน (บาท)',
                        help='รวมจำนวนเงินที่ชำระ (บาท)',
                        format='%.0f'
                    )
                }
            )
    
    with tab2:
        st.markdown("#### 📦 สรุปข้อมูลตามกอง")
        grouped_by_gong = df_filtered.groupby('กอง').agg({
            'จำนวนยาง': 'sum',
            'จำนวนเงิน': 'sum',
            'ชื่อลูกค้า': 'count'
        }).reset_index()
        grouped_by_gong.columns = ['กอง', 'จำนวนยาง', 'จำนวนเงิน', 'จำนวนลูกค้า']
        
        if grouped_by_gong.empty:
            st.info("ไม่พบข้อมูลสรุปตามกอง.")
        else:
            st.dataframe(
                grouped_by_gong,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'จำนวนยาง': st.column_config.NumberColumn(
                        'จำนวนยาง (กก.)',
                        format='%.1f'
                    ),
                    'จำนวนเงิน': st.column_config.NumberColumn(
                        'จำนวนเงิน (บาท)',
                        format='%.0f'
                    )
                }
            )
    
    with tab3:
        st.markdown("#### 🏢 สรุปข้อมูลตามสาขา")
        grouped_by_branch = df_filtered.groupby('สาขา').agg({
            'จำนวนยาง': 'sum',
            'จำนวนเงิน': 'sum',
            'ชื่อลูกค้า': 'count',
            'ราคา': 'mean'
        }).reset_index()
        grouped_by_branch.columns = ['สาขา', 'จำนวนยาง', 'จำนวนเงิน', 'จำนวนลูกค้า', 'ราคาเฉลี่ย']
        
        if grouped_by_branch.empty:
            st.info("ไม่พบข้อมูลสรุปตามสาขา.")
        else:
            st.dataframe(
                grouped_by_branch,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'จำนวนยาง': st.column_config.NumberColumn(
                        'จำนวนยาง (กก.)',
                        format='%.1f'
                    ),
                    'จำนวนเงิน': st.column_config.NumberColumn(
                        'จำนวนเงิน (บาท)',
                        format='%.0f'
                    ),
                    'ราคาเฉลี่ย': st.column_config.NumberColumn(
                        'ราคาเฉลี่ย (บาท/กก.)',
                        format='%.2f'
                    )
                }
            )

# ========================================================================================
# 📊 FOOTER
# ========================================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1.5rem; font-size: 0.9rem;">
    <p>🌳 ลิตาการยาง Dashboard | อัพเดทล่าสุด: {}</p>
    <p>สร้างสรรค์ด้วย ❤️ โดยทีมงาน</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
