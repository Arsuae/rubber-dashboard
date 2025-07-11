import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# ========================================================================================
# 📊 CONFIGURATION & STYLING
# ========================================================================================

st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start collapsed for mobile
)

# Enhanced CSS for mobile-responsive design
st.markdown("""
<style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }
        
        .main-header {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
        }
        
        .main-header h1 {
            font-size: 1.8rem !important;
        }
        
        .total-summary {
            padding: 1rem !important;
        }
        
        .total-summary .summary-grid {
            flex-direction: column !important;
            gap: 1rem !important;
        }
        
        .summary-item {
            text-align: center !important;
        }
        
        .summary-value {
            font-size: 1.5rem !important;
        }
        
        .branch-card {
            margin-bottom: 1rem !important;
        }
        
        .branch-stats {
            flex-direction: column !important;
            gap: 0.5rem !important;
        }
        
        .stat-item {
            margin-bottom: 0.5rem !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.9rem;
            padding: 0.5rem 0.8rem;
        }
    }
    
    /* Base styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .total-summary {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .summary-grid {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .summary-item {
        text-align: center;
        flex: 1;
        min-width: 150px;
    }
    
    .summary-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .summary-value {
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .branch-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .branch-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    .branch-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3498db;
    }
    
    .branch-stats {
        display: flex;
        justify-content: space-around;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
        flex: 1;
        min-width: 120px;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        font-weight: 500;
    }
    
    .stat-rubber {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stat-money {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .stat-customers {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .stat-label {
        font-size: 0.8rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .search-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }
    
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid #eee;
    }
    
    /* Mobile sidebar improvements */
    @media (max-width: 768px) {
        .sidebar .sidebar-content {
            width: 100% !important;
        }
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
        
        return df
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดข้อมูลได้: {str(e)}")
        return pd.DataFrame()

# ========================================================================================
# 🎨 HEADER SECTION
# ========================================================================================

st.markdown("""
<div class="main-header">
    <h1>🌳 ลิตาการยาง</h1>
    <p>ระบบจัดการข้อมูลยางพารา</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# 📊 SIDEBAR CONTROLS (Mobile-Optimized)
# ========================================================================================

with st.sidebar:
    st.markdown("### 🎛️ ตัวควบคุม")
    
    # Load data
    with st.spinner("กำลังโหลดข้อมูล..."):
        df = load_data()
    
    if df.empty:
        st.error("❌ ไม่สามารถโหลดข้อมูลได้")
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
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    # Info section
    st.markdown("---")
    st.markdown("### 📊 ข้อมูลทั่วไป")
    st.info(f"📈 ข้อมูลทั้งหมด: {len(df)} รายการ")
    st.info(f"🏢 จำนวนสาขา: {len(branches)} สาขา")

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
    <div class="chart-container" style="text-align: center; padding: 3rem;">
        <h3>⚠️ ไม่มีข้อมูล</h3>
        <p>ไม่พบข้อมูลตามวันที่และสาขาที่เลือก</p>
        <p>กรุณาเลือกวันที่หรือสาขาอื่น หรือเปิด sidebar เพื่อปรับแต่งการค้นหา</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Calculate statistics for each branch
    branch_stats = df_filtered.groupby('สาขา').agg({
        'จำนวนยาง': 'sum',
        'จำนวนเงิน': 'sum',
        'ชื่อลูกค้า': 'count'
    }).reset_index()
    
    # Calculate totals for today
    total_rubber_today = df_filtered['จำนวนยาง'].sum()
    total_money_today = df_filtered['จำนวนเงิน'].sum()
    total_customers_today = df_filtered['ชื่อลูกค้า'].count()
    
    # ========================================================================================
    # 📊 TOTAL SUMMARY SECTION (Mobile-Optimized)
    # ========================================================================================
    
    st.markdown(f"""
    <div class="total-summary">
        <h2>📊 สรุปรวม {selected_date.strftime('%d/%m/%Y')}</h2>
        <div class="summary-grid">
            <div class="summary-item">
                <div class="summary-label">จำนวนยางรวม</div>
                <div class="summary-value">{total_rubber_today:,.1f} กก.</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">รายได้รวม</div>
                <div class="summary-value">฿{total_money_today:,.0f}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">จำนวนลูกค้า</div>
                <div class="summary-value">{total_customers_today:,.0f} ราย</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================================================
    # 📊 CHARTS SECTION (Mobile-Optimized)
    # ========================================================================================
    
    # Mobile-responsive chart layout
    st.markdown("### 📈 กราฟสรุปข้อมูล")
    
    # Create responsive columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
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
                font=dict(size=10),
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            fig_branch.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig_branch, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 💰 สัดส่วนรายได้ตามสาขา")
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
                font=dict(size=10),
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            fig_money.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_money, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================================
    # BRANCH STATISTICS SECTION (Mobile-Optimized Cards)
    # ========================================================================================

    st.markdown("### 🏢 สถิติแยกตามสาขา")
    
    # Display branch statistics in modern cards
    for i, row in branch_stats.iterrows():
        st.markdown(f"""
        <div class="branch-card">
            <div class="branch-title">สาขา {row['สาขา']}</div>
            <div class="branch-stats">
                <div class="stat-item stat-rubber">
                    <div class="stat-label">จำนวนยาง</div>
                    <div class="stat-value">{row['จำนวนยาง']:,.1f} กก.</div>
                </div>
                <div class="stat-item stat-money">
                    <div class="stat-label">จำนวนเงิน</div>
                    <div class="stat-value">฿{row['จำนวนเงิน']:,.0f}</div>
                </div>
                <div class="stat-item stat-customers">
                    <div class="stat-label">จำนวนรายการ</div>
                    <div class="stat-value">{row['ชื่อลูกค้า']:,.0f} ราย</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # ========================================================================================
    # 📋 DATA TABLES SECTION (Mobile-Optimized)
    # ========================================================================================
    
    st.markdown("---")
    st.markdown("### 📋 ข้อมูลรายละเอียด")
    
    # Mobile-optimized tabs
    tab1, tab2, tab3 = st.tabs(["📋 ข้อมูลทั้งหมด", "📦 ตามกอง", "🏢 ตามสาขา"])
    
    with tab1:
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        search_term = st.text_input("🔍 ค้นหาลูกค้า", placeholder="พิมพ์ชื่อลูกค้าที่ต้องการค้นหา...")
        st.markdown('</div>', unsafe_allow_html=True)
        
        columns_to_show = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
        
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

st.markdown("""
<div class="footer">
    <p>🌳 <strong>ลิตาการยาง Dashboard</strong></p>
    <p>อัพเดทล่าสุด: {}</p>
    <p>💡 <em>เคล็ดลับ: ใช้ sidebar เพื่อปรับแต่งข้อมูล</em></p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
