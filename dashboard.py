import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# ========================================================================================
# 📊 CONFIGURATION & STYLING
# ========================================================================================

st.set_page_config(
    page_title="ลิตตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4472C4 0%, #5B9BD5 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .branch-section {
        background: #2F3349;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    
    .stats-card {
        background: #6c757d;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4472C4;
        margin: 1rem 0;
    }
    
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .company-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #4472C4;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# 🗂️ DATA LOADING & PROCESSING
# ========================================================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    """Load data from Google Sheets with caching"""
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1S1x1No7A_kS7tVDKd52Y5DIQkoKtE14GBlQDcUvSICU/export?format=csv&gid=2026341208"
        df = pd.read_csv(sheet_url, header=None)
        
        # Set column names
        df.columns = ['ลำดับ', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน', 'วันที่', 'กอง', 'สาขา']
        
        # Convert date column
        df['วันที่'] = pd.to_datetime(df['วันที่'], format="%d/%m/%Y", errors='coerce')
        
        # Clean numeric columns with more robust conversion
        df['จำนวนยาง'] = pd.to_numeric(df['จำนวนยาง'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['ราคา'] = pd.to_numeric(df['ราคา'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['จำนวนเงิน'] = pd.to_numeric(df['จำนวนเงิน'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        
        # Debug: Show data types and sample values
        st.sidebar.write("Debug Info:")
        st.sidebar.write(f"Total rows: {len(df)}")
        st.sidebar.write(f"จำนวนเงิน sum: {df['จำนวนเงิน'].sum():,.2f}")
        st.sidebar.write(f"จำนวนเงิน type: {df['จำนวนเงิน'].dtype}")
        
        return df
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดข้อมูลได้: {str(e)}")
        return pd.DataFrame()

# ========================================================================================
# 🎨 HEADER SECTION - MOVED UP
# ========================================================================================

st.markdown('<div class="company-title">ลิตตาการยาง</div>', unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>สถิติการยาง</h1>
    <p>ข้อมูลสำคัญการค้อนด้วยวันนี้</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# 📊 SIDEBAR CONTROLS
# ========================================================================================

with st.sidebar:
    st.markdown("### 🎛️ ตัวควบคุม")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.error("ไม่สามารถโหลดข้อมูลได้")
        st.stop()
    
    # Date selector
    st.markdown("#### 📅 เลือกวันที่")
    selected_date = st.date_input(
        "วันที่",
        value=date.today(),
        help="เลือกวันที่ที่ต้องการดูข้อมูล"
    )
    
    # Branch selector
    st.markdown("#### 🏢 เลือกสาขา")
    branches = df['สาขา'].dropna().unique().tolist()
    selected_branches = st.multiselect(
        "สาขา",
        options=branches,
        default=branches,
        help="เลือกสาขาที่ต้องการดูข้อมูล"
    )
    
    # Data refresh button
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ========================================================================================
# 📈 DATA FILTERING & PROCESSING
# ========================================================================================

# Filter data
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
        <p>ไม่พบข้อมูลตามวันที่และสาขาที่เลือก กรุณาเลือกวันที่หรือสาขาอื่น</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Summary statistics by branch
    st.markdown("## สถิติการยาง")
    st.markdown("### ข้อมูลสำคัญการค้อนด้วยวันนี้")
    
    # Calculate statistics for each branch
    branch_stats = df_filtered.groupby('สาขา').agg({
        'จำนวนยาง': 'sum',
        'จำนวนเงิน': 'sum',
        'ชื่อลูกค้า': 'count'
    }).reset_index()
    
    # Calculate totals for today
    total_rubber_today = df_filtered['จำนวนยาง'].sum()
    total_money_today = df_filtered['จำนวนเงิน'].sum()
    
    # ========================================================================================
    # 📊 CHARTS SECTION - MOVED UP
    # ========================================================================================
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 จำนวนยางตามสาขา")
        branch_summary = df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
        
        if not branch_summary.empty:
            fig_branch = px.bar(
                branch_summary,
                x='สาขา',
                y='จำนวนยาง',
                title="จำนวนยางแยกตามสาขา",
                color='จำนวนยาง',
                color_continuous_scale='viridis',
                text='จำนวนยาง'
            )
            fig_branch.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            fig_branch.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig_branch, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 จำนวนเงินตามสาขา")
        money_summary = df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
        
        if not money_summary.empty:
            fig_money = px.pie(
                money_summary,
                values='จำนวนเงิน',
                names='สาขา',
                title="สัดส่วนรายได้ตามสาขา",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_money.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            fig_money.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_money, use_container_width=True)

    # ========================================================================================
    # BRANCH STATISTICS - MOVED BELOW CHARTS
    # ========================================================================================
    
    # Display branch statistics in cards
    for i, row in branch_stats.iterrows():
        st.markdown(f"#### สาขา {row['สาขา']}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: #28a745; padding: 1rem; border-radius: 8px; text-align: center; color: white;">
                <div style="font-size: 12px;">จำนวนยาง</div>
                <div style="font-size: 24px; font-weight: bold;">{row['จำนวนยาง']:,.1f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: #17a2b8; padding: 1rem; border-radius: 8px; text-align: center; color: white;">
                <div style="font-size: 12px;">จำนวนเงิน</div>
                <div style="font-size: 24px; font-weight: bold;">฿{row['จำนวนเงิน']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: #ffc107; padding: 1rem; border-radius: 8px; text-align: center; color: black;">
                <div style="font-size: 12px;">จำนวนรายการ</div>
                <div style="font-size: 24px; font-weight: bold;">{row['ชื่อลูกค้า']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if i == 0:  # Show total only once
            with col4:
                st.markdown(f"""
                <div style="background: #dc3545; padding: 1rem; border-radius: 8px; text-align: center; color: white;">
                    <div style="font-size: 12px;">รวมทั้งหมดวันนี้</div>
                    <div style="font-size: 18px; font-weight: bold;">
                        {total_rubber_today:,.1f} กก.<br>
                        ฿{total_money_today:,.0f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ========================================================================================
    # 📋 DATA TABLES SECTION
    # ========================================================================================
    
    st.markdown("---")
    
    # Data tables
    tab1, tab2, tab3 = st.tabs(["📋 ข้อมูลทั้งหมด", "📦 สรุปตามกอง", "🏢 สรุปตามสาขา"])
    
    with tab1:
        st.markdown("#### 📋 ข้อมูลรายละเอียด")
        columns_to_show = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
        
        # Add search functionality
        search_term = st.text_input("🔍 ค้นหาลูกค้า", placeholder="พิมพ์ชื่อลูกค้าที่ต้องการค้นหา...")
        
        if search_term:
            df_display = df_filtered[df_filtered['ชื่อลูกค้า'].str.contains(search_term, case=False, na=False)]
        else:
            df_display = df_filtered
        
        st.dataframe(
            df_display[columns_to_show],
            use_container_width=True,
            hide_index=True,
            column_config={
                'จำนวนยาง': st.column_config.NumberColumn(
                    'จำนวนยาง (กก.)',
                    help='จำนวนยาง (กิโลกรัม)',
                    format='%.1f'
                ),
                'ราคา': st.column_config.NumberColumn(
                    'ราคา (บาท/กก.)',
                    help='ราคาต่อหน่วย (บาท)',
                    format='%.2f'
                ),
                'จำนวนเงิน': st.column_config.NumberColumn(
                    'จำนวนเงิน (บาท)',
                    help='รายได้รวม (บาท)',
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
        grouped_by_gong.columns = ['กอง', 'จำนวนยาง', 'จำนวนเงิน', 'จำนวนรายการ']
        
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
        grouped_by_branch.columns = ['สาขา', 'จำนวนยาง', 'จำนวนเงิน', 'จำนวนรายการ', 'ราคาเฉลี่ย']
        
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
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📊 ลิตตาการยาง Dashboard | อัพเดทล่าสุด: {}</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
