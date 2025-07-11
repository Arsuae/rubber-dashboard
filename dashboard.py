import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, time as datetime_time
import json
import os

# ========================================================================================
# 📊 CONFIGURATION & STYLING
# ========================================================================================

st.set_page_config(
    page_title="ลิตาการยาง Dashboard",
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
    
    .employee-attendance-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .employee-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .employee-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .employee-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .status-working {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        border-left: 4px solid #155724;
    }
    
    .status-off-work {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        border-left: 4px solid #856404;
        color: #212529;
    }
    
    .status-absent {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        border-left: 4px solid #721c24;
    }
    
    .employee-name {
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 0.5rem;
    }
    
    .employee-status {
        font-size: 12px;
        opacity: 0.9;
        margin-bottom: 0.25rem;
    }
    
    .employee-time {
        font-size: 11px;
        opacity: 0.8;
    }
    
    .total-summary {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .attendance-stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 14px;
        opacity: 0.9;
    }
    
    .debug-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #007bff;
    }
    
    .credentials-section {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================================
# 🗂️ DATA LOADING & PROCESSING
# ========================================================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_rubber_data():
    """Load rubber data from Google Sheets with caching"""
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
        st.error(f"❌ ไม่สามารถโหลดข้อมูลยางได้: {str(e)}")
        return pd.DataFrame()

def create_sample_attendance_data():
    """สร้างข้อมูลตัวอย่างสำหรับการลงเวลา"""
    today = datetime.now()
    sample_data = []
    
    employees = [
        ("001", "สมชาย ใจดี"),
        ("002", "สมหญิง รักงาน"),
        ("003", "สมศักดิ์ ขยัน"),
        ("004", "สมใจ มาตรง"),
        ("005", "สมปอง ซื่อสัตย์"),
        ("006", "สมหมาย ภักดี"),
        ("007", "สมหวัง สู้งาน"),
        ("008", "สมพงษ์ ตั้งใจ"),
        ("009", "สมบัติ มั่นคง"),
        ("010", "สมร เข็มแข็ง")
    ]
    
    # สุ่มสร้างข้อมูลการลงเวลา
    import random
    for i, (emp_id, emp_name) in enumerate(employees):
        # สุ่มว่าพนักงานคนนี้มาทำงานหรือไม่ (85% โอกาสมาทำงาน)
        if random.random() < 0.85:
            # เวลาเข้างาน (7:00-9:00)
            check_in_hour = random.randint(7, 8)
            check_in_minute = random.randint(0, 59)
            check_in_time = today.replace(hour=check_in_hour, minute=check_in_minute, second=0, microsecond=0)
            
            sample_data.append({
                'ID': f"{emp_id}_{today.strftime('%Y%m%d')}_{check_in_time.strftime('%H%M%S')}",
                'User ID': emp_id,
                'Name': emp_name,
                'Timestamp': check_in_time,
                'Status': 0,  # Check-in
                'Punch': 1,
                'Date': today.date(),
                'Time': check_in_time.time(),
                'Device IP': '192.168.1.3'
            })
            
            # ถ้าเกิน 4 โมงเย็นแล้ว หรือสุ่มให้บางคนออกงาน
            if today.hour >= 16 or (today.hour >= 12 and random.random() < 0.3):
                check_out_hour = random.randint(max(16, today.hour-2), max(18, today.hour))
                check_out_minute = random.randint(0, 59)
                check_out_time = today.replace(hour=check_out_hour, minute=check_out_minute, second=0, microsecond=0)
                
                sample_data.append({
                    'ID': f"{emp_id}_{today.strftime('%Y%m%d')}_{check_out_time.strftime('%H%M%S')}",
                    'User ID': emp_id,
                    'Name': emp_name,
                    'Timestamp': check_out_time,
                    'Status': 1,  # Check-out
                    'Punch': 1,
                    'Date': today.date(),
                    'Time': check_out_time.time(),
                    'Device IP': '192.168.1.3'
                })
    
    df = pd.DataFrame(sample_data)
    if not df.empty:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Date'] = pd.to_datetime(df['Date'])
        
    return df

@st.cache_data(ttl=60)  # Cache for 1 minute for more frequent updates
def load_attendance_data_with_credentials(uploaded_credentials=None, use_sample=False):
    """Load attendance data from ZKTeco Google Sheets with proper credentials handling"""
    
    if use_sample:
        st.info("🔧 ใช้ข้อมูลตัวอย่างสำหรับการทดสอบ")
        return create_sample_attendance_data()
    
    if uploaded_credentials is None:
        st.warning("⚠️ ไม่พบไฟล์ credentials.json - ใช้ข้อมูลตัวอย่าง")
        return create_sample_attendance_data()
    
    try:
        # ใช้ credentials ที่อัปโหลด
        import gspread
        from google.oauth2.service_account import Credentials
        
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        credentials = Credentials.from_service_account_info(uploaded_credentials, scopes=scope)
        gc = gspread.authorize(credentials)
        
        # เชื่อมต่อกับ Google Sheets สำหรับข้อมูลการลงเวลา
        spreadsheet = gc.open("ZKTeco Attendance")
        worksheet = spreadsheet.worksheet("Attendance")
        
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        if not df.empty and 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Date'] = pd.to_datetime(df['Date'])
            st.success("✅ เชื่อมต่อ Google Sheets สำเร็จ!")
            return df
        else:
            st.warning("⚠️ ไม่มีข้อมูลใน Google Sheets - ใช้ข้อมูลตัวอย่าง")
            return create_sample_attendance_data()
            
    except Exception as e:
        st.warning(f"⚠️ ไม่สามารถเชื่อมต่อ Google Sheets ได้: {str(e)} - ใช้ข้อมูลตัวอย่าง")
        return create_sample_attendance_data()

def get_employee_status(attendance_df):
    """คำนวณสถานะของพนักงานแต่ละคน"""
    today = datetime.now().date()
    current_time = datetime.now().time()
    
    # กรองข้อมูลเฉพาะวันนี้
    today_attendance = attendance_df[attendance_df['Date'].dt.date == today]
    
    if today_attendance.empty:
        return []
    
    # จัดกลุ่มตาม User ID และหาข้อมูลการเข้า-ออก
    employee_status = []
    
    for user_id in today_attendance['User ID'].unique():
        user_records = today_attendance[today_attendance['User ID'] == user_id].sort_values('Timestamp')
        
        if user_records.empty:
            continue
            
        name = user_records['Name'].iloc[0]
        first_record = user_records.iloc[0]
        last_record = user_records.iloc[-1]
        
        # กำหนดสถานะ
        status = "ไม่มาทำงาน"
        status_class = "status-absent"
        time_info = ""
        
        # ตรวจสอบว่ามีการสแกนหรือไม่
        if len(user_records) > 0:
            first_time = first_record['Timestamp'].time()
            
            # ตรวจสอบเวลาปัจจุบัน
            afternoon_cutoff = datetime_time(16, 0)  # 4 โมงเย็น
            
            if current_time < afternoon_cutoff:
                # ก่อน 4 โมงเย็น = กำลังทำงาน
                status = "กำลังทำงาน"
                status_class = "status-working"
                time_info = f"เข้างาน: {first_time.strftime('%H:%M')}"
            else:
                # หลัง 4 โมงเย็น
                if len(user_records) >= 2:
                    # มีการสแกนออก
                    last_time = last_record['Timestamp'].time()
                    status = "เลิกงานแล้ว"
                    status_class = "status-off-work"
                    time_info = f"เข้า: {first_time.strftime('%H:%M')} | ออก: {last_time.strftime('%H:%M')}"
                else:
                    # ยังไม่ได้สแกนออก
                    status = "กำลังทำงาน"
                    status_class = "status-working"
                    time_info = f"เข้างาน: {first_time.strftime('%H:%M')} | ยังไม่ออก"
        
        employee_status.append({
            'user_id': user_id,
            'name': name,
            'status': status,
            'status_class': status_class,
            'time_info': time_info,
            'records_count': len(user_records)
        })
    
    return employee_status

# ========================================================================================
# 🎨 HEADER SECTION
# ========================================================================================

st.markdown("""
<div class="main-header">
    <h1>🌳 ลิตาการยาง</h1>
    <p>ระบบจัดการข้อมูลยางพาราและการลงเวลาทำงาน</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================================
# 📊 SIDEBAR CONTROLS
# ========================================================================================

with st.sidebar:
    st.markdown("### ⚙️ ตัวควบคุม")
    
    # Google Credentials Upload
    st.markdown("#### 🔐 Google Credentials")
    uploaded_credentials = None
    
    credentials_file = st.file_uploader(
        "อัปโหลด credentials.json",
        type=['json'],
        help="อัปโหลดไฟล์ credentials.json สำหรับเชื่อมต่อ Google Sheets"
    )
    
    if credentials_file is not None:
        try:
            uploaded_credentials = json.load(credentials_file)
            st.success("✅ โหลดไฟล์ credentials สำเร็จ!")
        except Exception as e:
            st.error(f"❌ ไม่สามารถอ่านไฟล์ credentials ได้: {str(e)}")
    else:
        st.markdown("""
        <div class="credentials-section">
            <h5>⚠️ ไม่พบไฟล์ credentials.json</h5>
            <p>กรุณาอัปโหลดไฟล์ credentials.json เพื่อเชื่อมต่อกับ Google Sheets หรือใช้ข้อมูลตัวอย่าง</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Debug mode
    st.markdown("#### 🔧 โหมดแก้ไขปัญหา")
    debug_mode = st.checkbox("เปิดโหมด Debug", value=False)
    use_sample_data = st.checkbox("ใช้ข้อมูลตัวอย่าง", value=True)
    
    # Load data
    rubber_df = load_rubber_data()
    attendance_df = load_attendance_data_with_credentials(uploaded_credentials, use_sample_data)
    
    if rubber_df.empty:
        st.error("ไม่สามารถโหลดข้อมูลยางได้")
    
    # Date selector
    st.markdown("#### 📅 เลือกวันที่")
    selected_date = st.date_input(
        "วันที่",
        value=date.today(),
        help="เลือกวันที่ที่ต้องการดูข้อมูล"
    )
    
    # Branch selector
    if not rubber_df.empty:
        st.markdown("#### 🏢 เลือกสาขา")
        branches = rubber_df['สาขา'].dropna().unique().tolist()
        selected_branches = st.multiselect(
            "สาขา",
            options=branches,
            default=branches,
            help="เลือกสาขาที่ต้องการดูข้อมูล"
        )
    else:
        selected_branches = []
    
    # Data refresh button
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # Attendance settings
    st.markdown("---")
    st.markdown("#### 👥 การตั้งค่าการลงเวลา")
    show_attendance = st.checkbox("แสดงข้อมูลการลงเวลา", value=True)
    
    if show_attendance:
        st.info("📌 สถานะอัตโนมัติ:\n- เช้า-บ่าย: กำลังทำงาน\n- หลัง 16:00: เลิกงานแล้ว")

# Debug information
if debug_mode:
    st.markdown("---")
    st.markdown("### 🔧 ข้อมูลการแก้ไขปัญหา")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="debug-section">
            <h4>📊 สถานะข้อมูลยางพารา</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not rubber_df.empty:
            st.success(f"✅ โหลดข้อมูลยางสำเร็จ: {len(rubber_df)} รายการ")
            st.write("ตัวอย่างข้อมูล 3 แถวแรก:")
            st.dataframe(rubber_df.head(3))
        else:
            st.error("❌ ไม่สามารถโหลดข้อมูลยางได้")
    
    with col2:
        st.markdown("""
        <div class="debug-section">
            <h4>👥 สถานะข้อมูลการลงเวลา</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not attendance_df.empty:
            st.success(f"✅ โหลดข้อมูลการลงเวลาสำเร็จ: {len(attendance_df)} รายการ")
            st.write("ตัวอย่างข้อมูล 3 แถวแรก:")
            st.dataframe(attendance_df.head(3))
            
            # แสดงข้อมูลวันนี้
            today = datetime.now().date()
            today_data = attendance_df[attendance_df['Date'].dt.date == today]
            st.info(f"📅 ข้อมูลวันนี้: {len(today_data)} รายการ")
        else:
            st.error("❌ ไม่สามารถโหลดข้อมูลการลงเวลาได้")

# ========================================================================================
# 👥 EMPLOYEE ATTENDANCE SECTION
# ========================================================================================

if show_attendance:
    employee_status = get_employee_status(attendance_df)
    
    if employee_status:
        # คำนวณสถิติ
        total_employees = len(employee_status)
        working = len([e for e in employee_status if e['status'] == 'กำลังทำงาน'])
        off_work = len([e for e in employee_status if e['status'] == 'เลิกงานแล้ว'])
        absent = len([e for e in employee_status if e['status'] == 'ไม่มาทำงาน'])
        
        st.markdown(f"""
        <div class="employee-attendance-section">
            <h2>👥 สถานะการลงเวลาทำงาน</h2>
            <div class="attendance-stats">
                <div class="stat-item">
                    <div class="stat-number" style="color: #28a745;">{working}</div>
                    <div class="stat-label">กำลังทำงาน</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" style="color: #ffc107;">{off_work}</div>
                    <div class="stat-label">เลิกงานแล้ว</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" style="color: #dc3545;">{absent}</div>
                    <div class="stat-label">ไม่มาทำงาน</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{total_employees}</div>
                    <div class="stat-label">รวมทั้งหมด</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # แสดงรายการพนักงาน
        if employee_status:
            cols_per_row = 4
            rows = [employee_status[i:i + cols_per_row] for i in range(0, len(employee_status), cols_per_row)]
            
            for row in rows:
                cols = st.columns(cols_per_row)
                for i, employee in enumerate(row):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="employee-card {employee['status_class']}">
                            <div class="employee-name">{employee['name']}</div>
                            <div class="employee-status">{employee['status']}</div>
                            <div class="employee-time">{employee['time_info']}</div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="employee-attendance-section">
            <h2>👥 สถานะการลงเวลาทำงาน</h2>
            <p style="text-align: center; margin-top: 1rem;">ไม่มีข้อมูลการลงเวลาสำหรับวันนี้</p>
            <p style="text-align: center; font-size: 14px; opacity: 0.8;">กรุณาเปิด "ใช้ข้อมูลตัวอย่าง" ในแถบข้างเพื่อดูตัวอย่าง</p>
        </div>
        """, unsafe_allow_html=True)

# ========================================================================================
# 📈 RUBBER DATA PROCESSING
# ========================================================================================

if not rubber_df.empty and selected_branches:
    # Filter rubber data
    rubber_df_filtered = rubber_df[
        (rubber_df['วันที่'].dt.date == selected_date) &
        (rubber_df['สาขา'].isin(selected_branches))
    ]
    
    # ========================================================================================
    # 📊 RUBBER DASHBOARD
    # ========================================================================================
    
    if rubber_df_filtered.empty:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6c757d 0%, #495057 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 2rem 0;">
            <h3>⚠️ ไม่มีข้อมูลยางพารา</h3>
            <p>ไม่พบข้อมูลยางพาราตามวันที่และสาขาที่เลือก</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Calculate totals for today
        total_rubber_today = rubber_df_filtered['จำนวนยาง'].sum()
        total_money_today = rubber_df_filtered['จำนวนเงิน'].sum()
        total_customers_today = rubber_df_filtered['ชื่อลูกค้า'].count()
        
        # ========================================================================================
        # 📊 TOTAL SUMMARY SECTION
        # ========================================================================================
        
        st.markdown(f"""
        <div class="total-summary">
            <h2>📊 สรุปยางพาราวันนี้</h2>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                <div>
                    <div style="font-size: 14px; opacity: 0.9;">จำนวนยางรวม</div>
                    <div style="font-size: 28px; font-weight: bold;">{total_rubber_today:,.1f} กก.</div>
                </div>
                <div>
                    <div style="font-size: 14px; opacity: 0.9;">รายได้รวม</div>
                    <div style="font-size: 28px; font-weight: bold;">฿{total_money_today:,.0f}</div>
                </div>
                <div>
                    <div style="font-size: 14px; opacity: 0.9;">จำนวนลูกค้า</div>
                    <div style="font-size: 28px; font-weight: bold;">{total_customers_today:,.0f} ราย</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ========================================================================================
        # 📊 CHARTS SECTION
        # ========================================================================================
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 จำนวนยางตามสาขา")
            branch_summary = rubber_df_filtered.groupby('สาขา')['จำนวนยาง'].sum().reset_index()
            
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
            money_summary = rubber_df_filtered.groupby('สาขา')['จำนวนเงิน'].sum().reset_index()
            
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
        # BRANCH STATISTICS SECTION
        # ========================================================================================

        # Calculate branch statistics
        branch_stats = rubber_df_filtered.groupby('สาขา').agg({
            'จำนวนยาง': 'sum',
            'จำนวนเงิน': 'sum',
            'ชื่อลูกค้า': 'count'
        }).reset_index()

        st.markdown("#### 🏢 สถิติแยกตามสาขา")
        
        # Display branch statistics in cards
        for i, row in branch_stats.iterrows():
            st.markdown(f"##### สาขา {row['สาขา']}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="background: #28a745; padding: 1rem; border-radius: 8px; text-align: center; color: white;">
                    <div style="font-size: 12px;">จำนวนยาง</div>
                    <div style="font-size: 24px; font-weight: bold;">{row['จำนวนยาง']:,.1f} กก.</div>
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
                    <div style="font-size: 24px; font-weight: bold;">{row['ชื่อลูกค้า']:,.0f} ราย</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
        # ========================================================================================
        # 📋 DATA TABLES SECTION
        # ========================================================================================
        
        st.markdown("---")
        
        # Data tables
        tab1, tab2, tab3, tab4 = st.tabs(["📋 ข้อมูลทั้งหมด", "📦 สรุปตามกอง", "🏢 สรุปตามสาขา", "👥 ข้อมูลการลงเวลา"])
        
        with tab1:
            st.markdown("#### 📋 ข้อมูลรายละเอียดยางพารา")
            columns_to_show = ['สาขา', 'กอง', 'ชื่อลูกค้า', 'จำนวนยาง', 'ราคา', 'จำนวนเงิน']
            
            # Add search functionality
            search_term = st.text_input("🔍 ค้นหาลูกค้า", placeholder="พิมพ์ชื่อลูกค้าที่ต้องการค้นหา...")
            
            if search_term:
                df_display = rubber_df_filtered[rubber_df_filtered['ชื่อลูกค้า'].str.contains(search_term, case=False, na=False)]
            else:
                df_display = rubber_df_filtered
            
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
            grouped_by_gong = rubber_df_filtered.groupby('กอง').agg({
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
            grouped_by_branch = rubber_df_filtered.groupby('สาขา').agg({
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
        
        with tab4:
            st.markdown("#### 👥 ข้อมูลการลงเวลาทำงานวันนี้")
            
            if not attendance_df.empty:
                today = datetime.now().date()
                today_attendance = attendance_df[attendance_df['Date'].dt.date == today]
                
                if not today_attendance.empty:
                    # จัดรูปแบบข้อมูลสำหรับแสดง
                    display_attendance = today_attendance.copy()
                    display_attendance['เวลา'] = display_attendance['Timestamp'].dt.strftime('%H:%M:%S')
                    display_attendance['สถานะ'] = display_attendance['Status'].map({0: 'เข้างาน', 1: 'ออกงาน'})
                    
                    # เลือกคอลัมน์ที่จะแสดง
                    columns_to_show = ['User ID', 'Name', 'เวลา', 'สถานะ']
                    
                    st.dataframe(
                        display_attendance[columns_to_show].sort_values('เวลา', ascending=False),
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            'User ID': st.column_config.TextColumn('รหัสพนักงาน'),
                            'Name': st.column_config.TextColumn('ชื่อพนักงาน'),
                            'เวลา': st.column_config.TextColumn('เวลา'),
                            'สถานะ': st.column_config.TextColumn('สถานะ')
                        }
                    )
                else:
                    st.info("ไม่มีข้อมูลการลงเวลาสำหรับวันนี้")
            else:
                st.warning("ไม่สามารถโหลดข้อมูลการลงเวลาได้")

else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6c757d 0%, #495057 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 2rem 0;">
        <h3>⚠️ ไม่มีข้อมูลยางพารา</h3>
        <p>กรุณาเลือกสาขาเพื่อดูข้อมูล</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================================================================
# 📋 INSTRUCTIONS SECTION
# ========================================================================================

if not show_attendance or not uploaded_credentials:
    st.markdown("---")
    st.markdown("### 📋 คำแนะนำการใช้งาน")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🔐 การเชื่อมต่อ Google Sheets จริง:
        1. **สร้าง Service Account** ใน Google Cloud Console
        2. **Download ไฟล์ credentials.json**
        3. **แชร์ Google Sheets** ชื่อ "ZKTeco Attendance" ให้กับ Service Account
        4. **อัปโหลดไฟล์ credentials.json** ในแถบข้าง
        5. **ปิด "ใช้ข้อมูลตัวอย่าง"** เพื่อใช้ข้อมูลจริง
        """)
    
    with col2:
        st.markdown("""
        #### 🧪 การใช้ข้อมูลตัวอย่าง:
        1. **เปิด "ใช้ข้อมูลตัวอย่าง"** ในแถบข้าง
        2. **เปิด "แสดงข้อมูลการลงเวลา"**
        3. **ดูข้อมูลพนักงาน 10 คน** พร้อมสถานะต่างๆ
        4. **ทดสอบฟีเจอร์ต่างๆ** ได้ทันที
        """)

# ========================================================================================
# 📊 FOOTER
# ========================================================================================

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌳 ลิตาการยาง Dashboard | อัพเดทล่าสุด: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
    <p>💼 ระบบจัดการข้อมูลยางพาราและการลงเวลาทำงาน</p>
    <p style="font-size: 12px;">📁 ใช้ข้อมูลตัวอย่าง: {"✅" if use_sample_data else "❌"} | Google Sheets: {"✅" if uploaded_credentials else "❌"}</p>
</div>
""", unsafe_allow_html=True)
