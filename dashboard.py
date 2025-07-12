<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ลิตาการยาง - Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans Thai', sans-serif;
            background: linear-gradient(135deg, #faf7f4 0%, #f9f5f2 100%);
            color: #4a4a4a;
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header */
        .header {
            background: linear-gradient(135deg, #e8f4f8 0%, #d4e9f2 100%);
            padding: 2rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            border: 1px solid rgba(255,255,255,0.8);
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 600;
            color: #2c5aa0;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .header p {
            font-size: 1.1rem;
            color: #5a7ba8;
            font-weight: 300;
        }

        /* Navigation */
        .nav {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 2rem;
            background: rgba(255,255,255,0.7);
            padding: 0.5rem;
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }

        .nav-item {
            flex: 1;
            text-align: center;
            padding: 1rem;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            color: #6a7b8a;
            background: transparent;
            border: none;
            font-size: 0.95rem;
        }

        .nav-item:hover {
            background: rgba(255,255,255,0.8);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }

        .nav-item.active {
            background: linear-gradient(135deg, #b8e6d3 0%, #a8dcc6 100%);
            color: #2d5a3d;
            box-shadow: 0 4px 12px rgba(168,220,198,0.3);
        }

        /* Cards */
        .card {
            background: rgba(255,255,255,0.8);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            border: 1px solid rgba(255,255,255,0.9);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c5aa0;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            border: 1px solid rgba(255,255,255,0.9);
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        }

        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            opacity: 0.8;
        }

        .stat-card:nth-child(1) .stat-icon { color: #f4a6a6; }
        .stat-card:nth-child(2) .stat-icon { color: #a6d4f4; }
        .stat-card:nth-child(3) .stat-icon { color: #a6f4c4; }

        .stat-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: #2c5aa0;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            font-size: 1rem;
            color: #6a7b8a;
            font-weight: 400;
        }

        /* Filters */
        .filters {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .filter-label {
            font-weight: 500;
            color: #4a4a4a;
            font-size: 0.9rem;
        }

        .filter-select {
            padding: 0.75rem 1rem;
            border-radius: 12px;
            border: 1px solid #e0e6ed;
            background: rgba(255,255,255,0.9);
            color: #4a4a4a;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            min-width: 140px;
        }

        .filter-select:focus {
            outline: none;
            border-color: #b8e6d3;
            box-shadow: 0 0 0 3px rgba(184,230,211,0.2);
        }

        .refresh-btn {
            background: linear-gradient(135deg, #b8e6d3 0%, #a8dcc6 100%);
            color: #2d5a3d;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .refresh-btn:hover {
            background: linear-gradient(135deg, #a8dcc6 0%, #98d2b8 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(168,220,198,0.3);
        }

        /* Table */
        .table-container {
            background: rgba(255,255,255,0.9);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }

        .table {
            width: 100%;
            border-collapse: collapse;
        }

        .table th {
            background: linear-gradient(135deg, #e8f4f8 0%, #d4e9f2 100%);
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: #2c5aa0;
            border-bottom: 1px solid rgba(255,255,255,0.5);
        }

        .table td {
            padding: 1rem;
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }

        .table tr:hover {
            background: rgba(184,230,211,0.1);
        }

        /* Search */
        .search-container {
            margin-bottom: 1.5rem;
        }

        .search-input {
            width: 100%;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #e0e6ed;
            background: rgba(255,255,255,0.9);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: #b8e6d3;
            box-shadow: 0 0 0 3px rgba(184,230,211,0.2);
        }

        /* Employee Status */
        .employee-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }

        .employee-card {
            background: rgba(255,255,255,0.8);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid #b8e6d3;
            transition: all 0.3s ease;
        }

        .employee-card:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }

        .employee-card.late { border-left-color: #f4d6a6; }
        .employee-card.absent { border-left-color: #f4a6a6; }
        .employee-card.leave { border-left-color: #d4a6f4; }

        .employee-name {
            font-weight: 600;
            color: #2c5aa0;
            margin-bottom: 0.3rem;
        }

        .employee-status {
            font-size: 0.9rem;
            color: #6a7b8a;
        }

        /* Chart placeholder */
        .chart-placeholder {
            height: 300px;
            background: linear-gradient(135deg, #f9f5f2 0%, #f4f0ed 100%);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #6a7b8a;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
        }

        /* Tab Content */
        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .nav {
                flex-direction: column;
                gap: 0.3rem;
            }
            
            .filters {
                flex-direction: column;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            animation: fadeIn 0.5s ease-out;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>
                <i class="fas fa-leaf"></i>
                ลิตาการยาง
            </h1>
            <p>แดชบอร์ดข้อมูลยางพาราแบบเรียลไทม์</p>
        </div>

        <!-- Navigation -->
        <div class="nav">
            <button class="nav-item active" onclick="showTab('overview')">
                <i class="fas fa-chart-pie"></i> ภาพรวม
            </button>
            <button class="nav-item" onclick="showTab('summary')">
                <i class="fas fa-clipboard-list"></i> สรุป
            </button>
            <button class="nav-item" onclick="showTab('list')">
                <i class="fas fa-list"></i> รายการ
            </button>
            <button class="nav-item" onclick="showTab('employees')">
                <i class="fas fa-users"></i> พนักงาน
            </button>
        </div>

        <!-- Filters -->
        <div class="filters">
            <div class="filter-group">
                <label class="filter-label">วันที่</label>
                <input type="date" class="filter-select" id="dateFilter">
            </div>
            <div class="filter-group">
                <label class="filter-label">สาขา</label>
                <select class="filter-select" id="branchFilter">
                    <option value="">ทั้งหมด</option>
                    <option value="สาขา1">สาขา 1</option>
                    <option value="สาขา2">สาขา 2</option>
                    <option value="สาขา3">สาขา 3</option>
                </select>
            </div>
            <div class="filter-group">
                <label class="filter-label">กอง</label>
                <select class="filter-select" id="groupFilter">
                    <option value="">ทั้งหมด</option>
                    <option value="กอง1">กอง 1</option>
                    <option value="กอง2">กอง 2</option>
                    <option value="กอง3">กอง 3</option>
                </select>
            </div>
            <button class="refresh-btn" onclick="refreshData()">
                <i class="fas fa-sync-alt"></i> รีเฟรช
            </button>
        </div>

        <!-- Tab Contents -->
        
        <!-- Overview Tab -->
        <div id="overview" class="tab-content active">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-weight"></i>
                    </div>
                    <div class="stat-value" id="totalWeight">2,450.5</div>
                    <div class="stat-label">กิโลกรัม</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-coins"></i>
                    </div>
                    <div class="stat-value" id="totalRevenue">฿125,000</div>
                    <div class="stat-label">รายได้รวม</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="stat-value" id="totalCustomers">48</div>
                    <div class="stat-label">ลูกค้าทั้งหมด</div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">
                    <i class="fas fa-chart-bar"></i>
                    จำนวนยางตามสาขา
                </div>
                <div class="chart-placeholder">
                    <i class="fas fa-chart-bar" style="font-size: 3rem; opacity: 0.3;"></i>
                </div>
            </div>

            <div class="card">
                <div class="card-title">
                    <i class="fas fa-chart-pie"></i>
                    สัดส่วนรายได้
                </div>
                <div class="chart-placeholder">
                    <i class="fas fa-chart-pie" style="font-size: 3rem; opacity: 0.3;"></i>
                </div>
            </div>
        </div>

        <!-- Summary Tab -->
        <div id="summary" class="tab-content">
            <div class="card">
                <div class="card-title">
                    <i class="fas fa-boxes"></i>
                    สรุปข้อมูลตามกอง
                </div>
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>กอง</th>
                                <th>จำนวนยาง (กก.)</th>
                                <th>รายได้ (บาท)</th>
                                <th>จำนวนลูกค้า</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>กอง 1</td>
                                <td>850.2</td>
                                <td>42,500</td>
                                <td>16</td>
                            </tr>
                            <tr>
                                <td>กอง 2</td>
                                <td>920.8</td>
                                <td>46,000</td>
                                <td>18</td>
                            </tr>
                            <tr>
                                <td>กอง 3</td>
                                <td>679.5</td>
                                <td>36,500</td>
                                <td>14</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <div class="card-title">
                    <i class="fas fa-building"></i>
                    สรุปข้อมูลตามสาขา
                </div>
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>สาขา</th>
                                <th>จำนวนยาง (กก.)</th>
                                <th>รายได้ (บาท)</th>
                                <th>จำนวนลูกค้า</th>
                                <th>ราคาเฉลี่ย</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>สาขา 1</td>
                                <td>1,200.5</td>
                                <td>60,000</td>
                                <td>22</td>
                                <td>50.0</td>
                            </tr>
                            <tr>
                                <td>สาขา 2</td>
                                <td>800.0</td>
                                <td>40,000</td>
                                <td>16</td>
                                <td>50.0</td>
                            </tr>
                            <tr>
                                <td>สาขา 3</td>
                                <td>450.0</td>
                                <td>25,000</td>
                                <td>10</td>
                                <td>55.6</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- List Tab -->
        <div id="list" class="tab-content">
            <div class="card">
                <div class="card-title">
                    <i class="fas fa-list"></i>
                    รายการลูกค้าทั้งหมด
                </div>
                
                <div class="search-container">
                    <input type="text" class="search-input" placeholder="🔍 ค้นหาชื่อลูกค้า..." id="customerSearch">
                </div>

                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>สาขา</th>
                                <th>กอง</th>
                                <th>ชื่อลูกค้า</th>
                                <th>จำนวนยาง (กก.)</th>
                                <th>ราคา (บาท/กก.)</th>
                                <th>จำนวนเงิน (บาท)</th>
                            </tr>
                        </thead>
                        <tbody id="customerTableBody">
                            <tr>
                                <td>สาขา 1</td>
                                <td>กอง 1</td>
                                <td>นายสมชาย ใจดี</td>
                                <td>150.5</td>
                                <td>50.0</td>
                                <td>7,525</td>
                            </tr>
                            <tr>
                                <td>สาขา 1</td>
                                <td>กอง 2</td>
                                <td>นางสาววิไล สุขใส</td>
                                <td>200.0</td>
                                <td>52.0</td>
                                <td>10,400</td>
                            </tr>
                            <tr>
                                <td>สาขา 2</td>
                                <td>กอง 1</td>
                                <td>นายประยุทธ์ ขยันงาน</td>
                                <td>180.2</td>
                                <td>48.0</td>
                                <td>8,650</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Employees Tab -->
        <div id="employees" class="tab-content">
            <div class="card">
                <div class="card-title">
                    <i class="fas fa-users"></i>
                    สถานะพนักงาน
                </div>
                
                <div class="employee-grid">
                    <div class="employee-card">
                        <div class="employee-name">นายสมศักดิ์ ทำงาน</div>
                        <div class="employee-status">🟢 มาทำงาน 08:00</div>
                    </div>
                    <div class="employee-card">
                        <div class="employee-name">นางสาวมณี ขยัน</div>
                        <div class="employee-status">🟢 มาทำงาน 07:45</div>
                    </div>
                    <div class="employee-card late">
                        <div class="employee-name">นายสุชาติ ช้าหน่อย</div>
                        <div class="employee-status">🟡 มาสาย 08:30</div>
                    </div>
                    <div class="employee-card absent">
                        <div class="employee-name">นายพิชิต ป่วย</div>
                        <div class="employee-status">🔴 ขาดงาน</div>
                    </div>
                    <div class="employee-card leave">
                        <div class="employee-name">นางวิภา ลางาน</div>
                        <div class="employee-status">🟣 ลางาน</div>
                    </div>
                    <div class="employee-card">
                        <div class="employee-name">นายอานนท์ ตรงเวลา</div>
                        <div class="employee-status">🟢 มาทำงาน 07:50</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Tab switching
        function showTab(tabName) {
            // Hide all tab contents
            const tabContents = document.querySelectorAll('.tab-content');
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            
            // Remove active class from all nav items
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => {
                item.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked nav item
            event.target.classList.add('active');
        }

        // Search functionality
        document.getElementById('customerSearch').addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('#customerTableBody tr');
            
            tableRows.forEach(row => {
                const customerName = row.children[2].textContent.toLowerCase();
                if (customerName.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });

        // Refresh data
        function refreshData() {
            // Simulate data refresh
            const refreshBtn = document.querySelector('.refresh-btn');
            const icon = refreshBtn.querySelector('i');
            
            icon.style.animation = 'spin 1s linear infinite';
            
            setTimeout(() => {
                icon.style.animation = '';
                // Update stats with random values
                document.getElementById('totalWeight').textContent = (Math.random() * 3000 + 2000).toFixed(1);
                document.getElementById('totalRevenue').textContent = '฿' + (Math.random() * 50000 + 100000).toFixed(0);
                document.getElementById('totalCustomers').textContent = Math.floor(Math.random() * 20 + 40);
            }, 1000);
        }

        // Set today's date
        document.getElementById('dateFilter').value = new Date().toISOString().split('T')[0];

        // Add spin animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
