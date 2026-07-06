import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config.database import get_database_connection
import io
import uuid
from plotly.subplots import make_subplots
from io import BytesIO
from config.database import delete_resume

class DashboardManager:
    def __init__(self):
        self.conn = get_database_connection()
        self.colors = {
            'primary': '#4CAF50',
            'secondary': '#2196F3',
            'warning': '#FFA726',
            'danger': '#F44336',
            'info': '#00BCD4',
            'success': '#66BB6A',
            'purple': '#9C27B0',
            'background': '#1E1E1E',
            'card': '#2D2D2D',
            'text': '#FFFFFF',
            'subtext': '#B0B0B0'
        }
        
    def apply_dashboard_style(self):
        """Apply custom styling for dashboard"""
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

                /* ── Base ── */
                html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

                /* ── Keyframes ── */
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(24px); }
                    to   { opacity: 1; transform: translateY(0); }
                }
                @keyframes shimmer {
                    0%   { background-position: -400px 0; }
                    100% { background-position: 400px 0; }
                }
                @keyframes pulseGlow {
                    0%, 100% { box-shadow: 0 0 12px rgba(79,209,197,0.3); }
                    50%       { box-shadow: 0 0 28px rgba(79,209,197,0.65); }
                }
                @keyframes countUp {
                    from { opacity: 0; transform: scale(0.8); }
                    to   { opacity: 1; transform: scale(1); }
                }

                /* ── Dashboard hero ── */
                .dash-hero {
                    background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 40%, #0f3460 100%);
                    border-radius: 20px;
                    padding: 2.4rem 2.8rem;
                    margin-bottom: 2rem;
                    position: relative;
                    overflow: hidden;
                    border: 1px solid rgba(79,209,197,0.18);
                    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
                    animation: fadeInUp 0.6s ease-out;
                }
                .dash-hero::before {
                    content: '';
                    position: absolute;
                    top: -50%; left: -50%;
                    width: 200%; height: 200%;
                    background: radial-gradient(ellipse at 70% 30%, rgba(79,209,197,0.08) 0%, transparent 65%);
                    pointer-events: none;
                }
                .dash-hero-grid {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 1rem;
                }
                .dash-hero-left h1 {
                    font-size: 2.4rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, #4FD1C5 0%, #63b3ed 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin: 0 0 0.4rem 0;
                    letter-spacing: -0.5px;
                }
                .dash-hero-left p {
                    color: rgba(255,255,255,0.55);
                    font-size: 1rem;
                    margin: 0;
                }
                .dash-timestamp {
                    background: rgba(79,209,197,0.12);
                    border: 1px solid rgba(79,209,197,0.3);
                    border-radius: 40px;
                    padding: 0.45rem 1.1rem;
                    font-size: 0.82rem;
                    color: #4FD1C5;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    white-space: nowrap;
                }

                /* ── Stats grid ── */
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 1.2rem;
                    margin-top: 1.8rem;
                }
                @media (max-width: 900px) {
                    .stats-grid { grid-template-columns: repeat(2, 1fr); }
                }

                /* ── Stat card ── */
                .stat-card {
                    background: rgba(255,255,255,0.04);
                    backdrop-filter: blur(14px);
                    border-radius: 18px;
                    padding: 1.6rem 1.4rem;
                    border: 1px solid rgba(255,255,255,0.08);
                    transition: transform 0.28s ease, box-shadow 0.28s ease, background 0.28s ease;
                    position: relative;
                    overflow: hidden;
                    animation: fadeInUp 0.5s ease-out both;
                }
                .stat-card::before {
                    content: '';
                    position: absolute;
                    top: 0; left: 0; right: 0;
                    height: 3px;
                    border-radius: 18px 18px 0 0;
                }
                .stat-card:hover {
                    transform: translateY(-6px);
                    background: rgba(255,255,255,0.08);
                    box-shadow: 0 16px 40px rgba(0,0,0,0.3);
                }
                .stat-card.teal::before   { background: linear-gradient(90deg,#4FD1C5,#38b2ac); }
                .stat-card.blue::before   { background: linear-gradient(90deg,#63b3ed,#4299e1); }
                .stat-card.purple::before { background: linear-gradient(90deg,#b794f4,#9f7aea); }
                .stat-card.green::before  { background: linear-gradient(90deg,#68d391,#48bb78); }

                .stat-icon {
                    font-size: 1.6rem;
                    margin-bottom: 0.7rem;
                    display: block;
                }
                .stat-value {
                    font-size: 2.6rem;
                    font-weight: 800;
                    margin: 0;
                    line-height: 1;
                    animation: countUp 0.5s ease-out;
                }
                .stat-card.teal   .stat-value { color: #4FD1C5; }
                .stat-card.blue   .stat-value { color: #63b3ed; }
                .stat-card.purple .stat-value { color: #b794f4; }
                .stat-card.green  .stat-value { color: #68d391; }

                .stat-label {
                    font-size: 0.85rem;
                    color: rgba(255,255,255,0.55);
                    margin: 0.45rem 0 0.8rem;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.6px;
                }
                .trend-indicator {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.28rem;
                    padding: 0.25rem 0.65rem;
                    border-radius: 20px;
                    font-size: 0.78rem;
                    font-weight: 600;
                }
                .trend-up   { background: rgba(72,187,120,0.15); color: #68d391; }
                .trend-down { background: rgba(245,101,101,0.15); color: #fc8181; }
                .trend-neutral { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.5); }

                /* ── Section title ── */
                .section-title {
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: #4FD1C5;
                    margin: 2rem 0 1rem;
                    padding-bottom: 0.6rem;
                    border-bottom: 2px solid rgba(79,209,197,0.2);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    letter-spacing: -0.2px;
                }

                /* ── Chart container ── */
                .chart-container {
                    background: rgba(255,255,255,0.03);
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 18px;
                    padding: 1.2rem;
                    margin-bottom: 1.2rem;
                    transition: box-shadow 0.3s ease;
                }
                .chart-container:hover {
                    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
                }

                /* ── Insight cards ── */
                .insights-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 1.2rem;
                    margin-top: 1rem;
                }
                @media (max-width: 900px) {
                    .insights-grid { grid-template-columns: 1fr; }
                }
                .insight-card {
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 16px;
                    padding: 1.5rem;
                    position: relative;
                    transition: transform 0.25s ease, box-shadow 0.25s ease;
                    animation: fadeInUp 0.5s ease-out both;
                }
                .insight-card:hover {
                    transform: translateY(-4px);
                    box-shadow: 0 12px 30px rgba(0,0,0,0.28);
                }
                .insight-card.trophy { border-left: 4px solid #f6e05e; }
                .insight-card.trend  { border-left: 4px solid #68d391; }
                .insight-card.skills { border-left: 4px solid #4FD1C5; }
                .insight-card h3 {
                    font-size: 1rem;
                    font-weight: 700;
                    color: #fff;
                    margin: 0 0 0.6rem;
                    display: flex;
                    align-items: center;
                    gap: 0.4rem;
                }
                .insight-card p {
                    font-size: 0.88rem;
                    color: rgba(255,255,255,0.6);
                    line-height: 1.55;
                    margin: 0 0 0.9rem;
                }

                /* ── Admin table ── */
                .resume-data, .admin-logs {
                    background: rgba(255,255,255,0.03);
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 16px;
                    padding: 1.4rem;
                    margin-bottom: 1.2rem;
                }
                .stDataFrame {
                    border-radius: 12px;
                    overflow: hidden;
                }

                /* ── Delete / download buttons ── */
                .stButton > button {
                    border-radius: 10px;
                    font-weight: 600;
                    transition: all 0.2s ease;
                }
                .stButton > button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
                }
                .stDownloadButton > button {
                    background: linear-gradient(135deg,#4FD1C5,#38b2ac) !important;
                    color: #0d1b2a !important;
                    border: none !important;
                    border-radius: 10px !important;
                    font-weight: 700 !important;
                    transition: all 0.2s ease !important;
                }
                .stDownloadButton > button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(79,209,197,0.4) !important;
                }

                [data-testid="stMetricValue"] { font-size: 2rem !important; }
                [data-testid="stMetricLabel"] { font-size: 1rem !important; }
            </style>
        """, unsafe_allow_html=True)

    def get_resume_metrics(self):
        """Get resume-related metrics from database"""
        cursor = self.conn.cursor()
        
        # Get current date
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week = now - timedelta(days=now.weekday())
        start_of_month = now.replace(day=1)
        
        # Fetch metrics for different time periods
        metrics = {}
        for period, start_date in [
            ('Today', start_of_day),
            ('This Week', start_of_week),
            ('This Month', start_of_month),
            ('All Time', datetime(2000, 1, 1))
        ]:
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT rd.id) as total_resumes,
                    ROUND(AVG(ra.ats_score), 1) as avg_ats_score,
                    ROUND(AVG(ra.keyword_match_score), 1) as avg_keyword_score,
                    COUNT(DISTINCT CASE WHEN ra.ats_score >= 70 THEN rd.id END) as high_scoring
                FROM resume_data rd
                LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
                WHERE rd.created_at >= ?
            """, (start_date.strftime('%Y-%m-%d %H:%M:%S'),))
            
            row = cursor.fetchone()
            if row:
                metrics[period] = {
                    'total': row[0] or 0,
                    'ats_score': row[1] or 0,
                    'keyword_score': row[2] or 0,
                    'high_scoring': row[3] or 0
                }
            else:
                metrics[period] = {
                    'total': 0,
                    'ats_score': 0,
                    'keyword_score': 0,
                    'high_scoring': 0
                }
        
        return metrics

    def get_skill_distribution(self):
        """Get skill distribution data"""
        cursor = self.conn.cursor()
        cursor.execute("""
            WITH RECURSIVE split(skill, rest) AS (
                SELECT '', skills || ','
                FROM resume_data
                UNION ALL
                SELECT
                    substr(rest, 0, instr(rest, ',')),
                    substr(rest, instr(rest, ',') + 1)
                FROM split
                WHERE rest <> ''
            ),
            SkillCategories AS (
                SELECT 
                    CASE 
                        WHEN LOWER(TRIM(skill, '[]" ')) LIKE '%python%' OR LOWER(TRIM(skill, '[]" ')) LIKE '%java%' OR 
                             LOWER(TRIM(skill, '[]" ')) LIKE '%javascript%' OR LOWER(TRIM(skill, '[]" ')) LIKE '%c++%' OR 
                             LOWER(TRIM(skill, '[]" ')) LIKE '%programming%' THEN 'Programming'
                        WHEN LOWER(TRIM(skill, '[]" ')) LIKE '%sql%' OR LOWER(TRIM(skill, '[]" ')) LIKE '%database%' OR 
                             LOWER(TRIM(skill, '[]" ')) LIKE '%mongodb%' THEN 'Database'
                        WHEN LOWER(TRIM(skill, '[]" ')) LIKE '%aws%' OR LOWER(TRIM(skill, '[]" ')) LIKE '%cloud%' OR 
                             LOWER(TRIM(skill, '[]" ')) LIKE '%azure%' THEN 'Cloud'
                        WHEN LOWER(TRIM(skill, '[]" ')) LIKE '%agile%' OR LOWER(TRIM(skill, '[]" ')) LIKE '%scrum%' OR 
                             LOWER(TRIM(skill, '[]" ')) LIKE '%management%' THEN 'Management'
                        ELSE 'Other'
                    END as category,
                    COUNT(*) as count
                FROM split
                WHERE skill <> ''
                GROUP BY category
            )
            SELECT category, count
            FROM SkillCategories
            ORDER BY count DESC
        """)
        
        categories, counts = [], []
        for row in cursor.fetchall():
            categories.append(row[0])
            counts.append(row[1])
            
        return categories, counts

    def get_weekly_trends(self):
        """Get weekly submission trends"""
        cursor = self.conn.cursor()
        now = datetime.now()
        dates = [(now - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(6, -1, -1)]
        
        submissions = []
        for date in dates:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM resume_data 
                WHERE DATE(created_at) = DATE(?)
            """, (date,))
            submissions.append(cursor.fetchone()[0])
            
        return [d[-3:] for d in dates], submissions  # Return shortened date format (e.g., 'Mon', 'Tue')

    def get_job_category_stats(self):
        """Get statistics by job category"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                COALESCE(target_category, 'Other') as category,
                COUNT(*) as count,
                ROUND(AVG(CASE WHEN ra.ats_score >= 70 THEN 1 ELSE 0 END) * 100, 1) as success_rate
            FROM resume_data rd
            LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
            GROUP BY category
            ORDER BY count DESC
            LIMIT 5
        """)
        
        categories, success_rates = [], []
        for row in cursor.fetchall():
            categories.append(row[0])
            success_rates.append(row[2] or 0)
            
        return categories, success_rates

    def render_admin_panel(self):
        """Render admin panel with data management tools"""
        st.sidebar.markdown("### 👋 Welcome Admin!")
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🚪 Logout"):
            st.session_state.is_admin = False
            st.rerun()
            
        st.sidebar.markdown("### 🛠️ Admin Tools")
        
        # Data Export Options
        export_format = st.sidebar.selectbox(
            "Export Format",
            ["Excel", "CSV", "JSON"],
            key="export_format"
        )
        
        if st.sidebar.button("📥 Export Data"):
            if export_format == "Excel":
                excel_data = self.export_to_excel()
                if excel_data:
                    st.sidebar.download_button(
                        "⬇️ Download Excel",
                        data=excel_data,
                        file_name=f"resume_data_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            elif export_format == "CSV":
                csv_data = self.export_to_csv()
                if csv_data:
                    st.sidebar.download_button(
                        "⬇️ Download CSV",
                        data=csv_data,
                        file_name=f"resume_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
            else:
                json_data = self.export_to_json()
                if json_data:
                    st.sidebar.download_button(
                        "⬇️ Download JSON",
                        data=json_data,
                        file_name=f"resume_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                        mime="application/json"
                    )

        # Database Stats
        st.sidebar.markdown("### 📊 Database Stats")
        stats = self.get_database_stats()
        st.sidebar.markdown(f"""
            - Total Resumes: {stats['total_resumes']}
            - Today's Submissions: {stats['today_submissions']}
            - Storage Used: {stats['storage_size']}
        """)

    def get_resume_data(self):
        """Get all resume data"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            SELECT 
                r.id,
                r.name,
                r.email,
                r.phone,
                r.linkedin,
                r.github,
                r.portfolio,
                r.target_role,
                r.target_category,
                r.created_at,
                a.ats_score,
                a.keyword_match_score,
                a.format_score,
                a.section_score
            FROM resume_data r
            LEFT JOIN resume_analysis a ON r.id = a.resume_id
            ORDER BY r.created_at DESC
            ''')
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching resume data: {str(e)}")
            return []

    def render_resume_data_section(self):
        """Render resume data section with Excel download"""
        st.markdown("<h2 class='section-title'>Resume Submissions</h2>", unsafe_allow_html=True)
        
        # Get resume data
        resume_data = self.get_resume_data()
        
        if resume_data:
            # Convert to DataFrame
            columns = [
                'ID', 'Name', 'Email', 'Phone', 'LinkedIn', 'GitHub', 
                'Portfolio', 'Target Role', 'Target Category', 'Submission Date',
                'ATS Score', 'Keyword Match', 'Format Score', 'Section Score'
            ]
            df = pd.DataFrame(resume_data, columns=columns)
            
            # Format scores as percentages
            score_columns = ['ATS Score', 'Keyword Match', 'Format Score', 'Section Score']
            for col in score_columns:
                df[col] = df[col].apply(lambda x: f"{x*100:.1f}%" if pd.notnull(x) else "N/A")
            
            # Style the dataframe
            st.markdown("""
            <style>
            .resume-data {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 1rem;
                margin-bottom: 1rem;
            }
            </style>
            """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="resume-data">', unsafe_allow_html=True)
                
                # Add filters
                col1, col2 = st.columns(2)
                with col1:
                    target_role = st.selectbox(
                        "Filter by Target Role",
                        options=["All"] + list(df['Target Role'].unique()),
                        key="role_filter"
                    )
                with col2:
                    target_category = st.selectbox(
                        "Filter by Category",
                        options=["All"] + list(df['Target Category'].unique()),
                        key="category_filter"
                    )
                
                # Apply filters
                filtered_df = df.copy()
                if target_role != "All":
                    filtered_df = filtered_df[filtered_df['Target Role'] == target_role]
                if target_category != "All":
                    filtered_df = filtered_df[filtered_df['Target Category'] == target_category]
                
                # Display filtered data
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    hide_index=True
                )
                st.markdown("### 🗑 Delete Resume")

                resume_ids = filtered_df["ID"].tolist()

                selected_resume = st.selectbox("Select Resume to Delete",resume_ids)

                if st.button("Delete Selected Resume"):
                    delete_resume(selected_resume)
                    st.success("Resume deleted successfully!")
                    st.rerun()
                
                # Add download buttons
                col1, col2 = st.columns(2)
                with col1:
                    # Download filtered data
                    excel_buffer = BytesIO()
                    filtered_df.to_excel(excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label="📥 Download Filtered Data",
                        data=excel_buffer,
                        file_name=f"resume_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_filtered_data"
                    )
                
                with col2:
                    # Download all data
                    excel_buffer_all = BytesIO()
                    df.to_excel(excel_buffer_all, index=False, engine='openpyxl')
                    excel_buffer_all.seek(0)
                    
                    st.download_button(
                        label="📥 Download All Data",
                        data=excel_buffer_all,
                        file_name=f"resume_data_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_all_data"
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No resume submissions available")

    def render_admin_section(self):
        """Render admin section with logs and Excel download"""
        # Render resume data section
        self.render_resume_data_section()
        
        # Render admin logs section
        st.markdown("<h2 class='section-title'>Admin Activity Logs</h2>", unsafe_allow_html=True)
        
        # Get admin logs
        admin_logs = self.get_admin_logs()
        
        if admin_logs:
            # Convert to DataFrame
            df = pd.DataFrame(admin_logs, columns=['Admin Email', 'Action', 'Timestamp'])
            
            # Style the dataframe
            st.markdown("""
            <style>
            .admin-logs {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 1rem;
            }
            </style>
            """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="admin-logs">', unsafe_allow_html=True)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Add download button
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Admin Logs as Excel",
                    data=excel_buffer,
                    file_name=f"admin_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_admin_logs"
                )
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No admin activity logs available")

    def export_to_excel(self):
        """Export data to Excel format"""
        query = """
            SELECT 
                rd.name, rd.email, rd.phone, rd.linkedin, rd.github, rd.portfolio,
                rd.summary, rd.target_role, rd.target_category,
                rd.education, rd.experience, rd.projects, rd.skills,
                ra.ats_score, ra.keyword_match_score, ra.format_score, ra.section_score,
                ra.missing_skills, ra.recommendations,
                rd.created_at
            FROM resume_data rd
            LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
        """
        try:
            df = pd.read_sql_query(query, self.conn)
            
            # Create Excel writer object
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Write main data
                df.to_excel(writer, sheet_name='Resume Data', index=False)
                
                # Get the workbook and the worksheet
                workbook = writer.book
                worksheet = writer.sheets['Resume Data']
                
                # Add formatting
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',
                    'border': 1
                })
                
                # Write headers with formatting
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    
                # Auto-adjust columns' width
                for i, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(str(col))
                    ) + 2
                    worksheet.set_column(i, i, min(max_length, 50))
            
            # Return the Excel file
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            st.error(f"Error exporting to Excel: {str(e)}")
            return None

    def export_to_csv(self):
        """Export data to CSV format"""
        query = """
            SELECT 
                rd.name, rd.email, rd.phone, rd.linkedin, rd.github, rd.portfolio,
                rd.summary, rd.target_role, rd.target_category,
                rd.education, rd.experience, rd.projects, rd.skills,
                ra.ats_score, ra.keyword_match_score, ra.format_score, ra.section_score,
                ra.missing_skills, ra.recommendations,
                rd.created_at
            FROM resume_data rd
            LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
        """
        try:
            df = pd.read_sql_query(query, self.conn)
            return df.to_csv(index=False).encode('utf-8')
        except Exception as e:
            st.error(f"Error exporting to CSV: {str(e)}")
            return None

    def export_to_json(self):
        """Export data to JSON format"""
        query = """
            SELECT 
                rd.*, ra.*
            FROM resume_data rd
            LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
        """
        try:
            df = pd.read_sql_query(query, self.conn)
            return df.to_json(orient='records', date_format='iso')
        except Exception as e:
            st.error(f"Error exporting to JSON: {str(e)}")
            return None

    def get_database_stats(self):
        """Get database statistics"""
        cursor = self.conn.cursor()
        stats = {}
        
        # Total resumes
        cursor.execute("SELECT COUNT(*) FROM resume_data")
        stats['total_resumes'] = cursor.fetchone()[0]
        
        # Today's submissions
        cursor.execute("""
            SELECT COUNT(*) 
            FROM resume_data 
            WHERE DATE(created_at) = DATE('now')
        """)
        stats['today_submissions'] = cursor.fetchone()[0]
        
        # Database size (approximate)
        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        size_bytes = page_count * page_size
        
        if size_bytes < 1024:
            stats['storage_size'] = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            stats['storage_size'] = f"{size_bytes/1024:.1f} KB"
        else:
            stats['storage_size'] = f"{size_bytes/(1024*1024):.1f} MB"
        
        return stats

    def get_admin_logs(self):
        """Get admin logs"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            SELECT admin_email, action, timestamp
            FROM admin_logs
            ORDER BY timestamp DESC
            ''')
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching admin logs: {str(e)}")
            return []

    def render_dashboard(self):
        """Main dashboard rendering function"""
        self.apply_dashboard_style()

        # ── Hero Banner ──────────────────────────────────────────────────────
        st.markdown(f"""
            <div class="dash-hero">
                <div class="dash-hero-grid">
                    <div class="dash-hero-left">
                        <h1>📊 Resume Analytics Dashboard</h1>
                        <p>Real-time insights into resume performance, skills & hiring trends</p>
                    </div>
                    <div class="dash-timestamp">
                        🕐 {datetime.now().strftime('%B %d, %Y &nbsp;·&nbsp; %I:%M %p')}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ── Quick Stats ──────────────────────────────────────────────────────
        stats = self.get_quick_stats()
        trend_indicators = self.get_trend_indicators()

        cards = [
            {
                'color': 'teal',
                'icon': '📄',
                'value': stats['Total Resumes'],
                'label': 'Total Resumes',
                'trend': trend_indicators['resumes'],
            },
            {
                'color': 'blue',
                'icon': '🎯',
                'value': stats['Avg ATS Score'],
                'label': 'Avg ATS Score',
                'trend': trend_indicators['ats'],
            },
            {
                'color': 'purple',
                'icon': '🏆',
                'value': stats['High Performing'],
                'label': 'High Performing',
                'trend': trend_indicators['high_performing'],
            },
            {
                'color': 'green',
                'icon': '✅',
                'value': stats['Success Rate'],
                'label': 'Success Rate',
                'trend': trend_indicators['success_rate'],
            },
        ]

        cards_html = '<div class="stats-grid">'
        for delay, c in enumerate(cards):
            t = c['trend']
            cards_html += f"""
            <div class="stat-card {c['color']}" style="animation-delay:{delay*0.1}s">
                <span class="stat-icon">{c['icon']}</span>
                <p class="stat-value">{c['value']}</p>
                <p class="stat-label">{c['label']}</p>
                <span class="trend-indicator {t['class']}">{t['icon']} {t['value']}%</span>
            </div>"""
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        # ── Performance Analytics ─────────────────────────────────────────────
        st.markdown('<div class="section-title">📈 Performance Analytics</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig = self.create_enhanced_ats_gauge(float(stats['Avg ATS Score'].rstrip('%')))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig = self.create_skill_distribution_chart()
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig = self.create_submission_trends_chart()
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig = self.create_job_category_chart()
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Key Insights ──────────────────────────────────────────────────────
        st.markdown('<div class="section-title">🎯 Key Insights</div>', unsafe_allow_html=True)
        insights = self.get_detailed_insights()

        # Map icon to card accent class
        _accent_map = {'🏆': 'trophy', '📈': 'trend', '💡': 'skills'}

        insights_html = '<div class="insights-grid">'
        for i, ins in enumerate(insights):
            accent = _accent_map.get(ins['icon'], 'trend')
            insights_html += f"""
            <div class="insight-card {accent}" style="animation-delay:{i*0.12}s">
                <h3>{ins['icon']} {ins['title']}</h3>
                <p>{ins['description']}</p>
                <span class="trend-indicator {ins['trend_class']}">
                    {ins['trend_icon']} {ins['trend_value']}
                </span>
            </div>"""
        insights_html += '</div>'
        st.markdown(insights_html, unsafe_allow_html=True)

        # ── Admin section ─────────────────────────────────────────────────────
        if st.session_state.get('is_admin', False):
            self.render_admin_section()

    def get_trend_indicators(self):
        """Get trend indicators for stats"""
        cursor = self.conn.cursor()
        indicators = {}
        
        # Compare with last week's data
        for metric in ['resumes', 'ats', 'high_performing', 'success_rate']:
            try:
                if metric == 'resumes':
                    cursor.execute("""
                        SELECT 
                            (COUNT(*) - (
                                SELECT COUNT(*) 
                                FROM resume_data 
                                WHERE created_at < date('now', '-7 days')
                            )) * 100.0 / 
                            NULLIF((
                                SELECT COUNT(*) 
                                FROM resume_data 
                                WHERE created_at < date('now', '-7 days')
                            ), 0)
                        FROM resume_data
                    """)
                elif metric == 'ats':
                    cursor.execute("""
                        SELECT 
                            (AVG(ats_score) - (
                                SELECT AVG(ats_score) 
                                FROM resume_analysis 
                                WHERE created_at < date('now', '-7 days')
                            )) * 100.0 / 
                            NULLIF((
                                SELECT AVG(ats_score) 
                                FROM resume_analysis 
                                WHERE created_at < date('now', '-7 days')
                            ), 0)
                        FROM resume_analysis
                    """)
                
                change = cursor.fetchone()[0] or 0
                indicators[metric] = {
                    'value': abs(round(change, 1)),
                    'icon': '↑' if change >= 0 else '↓',
                    'class': 'trend-up' if change >= 0 else 'trend-down'
                }
            except Exception:
                indicators[metric] = {
                    'value': 0,
                    'icon': '→',
                    'class': 'trend-neutral'
                }
        
        return indicators

    def get_detailed_insights(self):
        """Get detailed insights from the database"""
        cursor = self.conn.cursor()
        insights = []
        
        # Most Successful Job Category
        cursor.execute("""
            SELECT target_category, AVG(ats_score) as avg_score,
                   COUNT(*) as submission_count
            FROM resume_data rd
            JOIN resume_analysis ra ON rd.id = ra.resume_id
            GROUP BY target_category
            ORDER BY avg_score DESC
            LIMIT 1
        """)
        top_category = cursor.fetchone()
        if top_category:
            insights.append({
                'title': 'Top Performing Category',
                'icon': '🏆',
                'description': f"{top_category[0]} leads with {top_category[1]:.1f}% average ATS score across {top_category[2]} submissions",
                'trend_class': 'trend-up',
                'trend_icon': '↑',
                'trend_value': f"{top_category[1]:.1f}%"
            })
        
        # Recent Improvement
        cursor.execute("""
            SELECT 
                (SELECT AVG(ats_score) FROM resume_analysis 
                 WHERE created_at >= date('now', '-7 days')) as recent_score,
                (SELECT AVG(ats_score) FROM resume_analysis 
                 WHERE created_at < date('now', '-7 days')) as old_score
        """)
        scores = cursor.fetchone()
        if scores and scores[0] and scores[1]:
            change = scores[0] - scores[1]
            insights.append({
                'title': 'Weekly Trend',
                'icon': '📈',
                'description': f"ATS scores have {'improved' if change >= 0 else 'decreased'} by {abs(change):.1f}% in the last week",
                'trend_class': 'trend-up' if change >= 0 else 'trend-down',
                'trend_icon': '↑' if change >= 0 else '↓',
                'trend_value': f"{abs(change):.1f}%"
            })
        
        # Most Common Skills
        cursor.execute("""
            WITH RECURSIVE
            split(skill, rest) AS (
                SELECT '', skills || ',' 
                FROM resume_data 
                WHERE skills IS NOT NULL
                UNION ALL
                SELECT
                    substr(rest, 0, instr(rest, ',')),
                    substr(rest, instr(rest, ',') + 1)
                FROM split 
                WHERE rest <> ''
            ),
            cleaned_skills AS (
                SELECT TRIM(REPLACE(REPLACE(skill, '[', ''), ']', '')) as skill
                FROM split 
                WHERE skill <> ''
            )
            SELECT skill, COUNT(*) as count
            FROM cleaned_skills
            GROUP BY skill
            ORDER BY count DESC
            LIMIT 3
        """)
        top_skills = cursor.fetchall()
        if top_skills:
            skills_text = f"Most in-demand skills: Python ({top_skills[0][1]} resumes), Java ({top_skills[1][1]} resumes), Express ({top_skills[2][1]} resumes)"
            insights.append({
                'title': 'Top Skills',
                'icon': '💡',
                'description': f"Most in-demand skills: {skills_text}",
                'trend_class': 'trend-up',
                'trend_icon': '🔝',
                'trend_value': f"Top {len(top_skills)}"
            })
        
        return insights

    def get_quick_stats(self):
        """Get quick statistics for the dashboard"""
        cursor = self.conn.cursor()
        
        # Total Resumes
        cursor.execute("SELECT COUNT(*) FROM resume_data")
        total_resumes = cursor.fetchone()[0]
        
        # Average ATS Score
        cursor.execute("SELECT AVG(ats_score) FROM resume_analysis")
        avg_ats = cursor.fetchone()[0] or 0
        
        # High Performing Resumes
        cursor.execute("SELECT COUNT(*) FROM resume_analysis WHERE ats_score >= 70")
        high_performing = cursor.fetchone()[0]
        
        # Success Rate
        success_rate = (high_performing / total_resumes * 100) if total_resumes > 0 else 0
        
        return {
            "Total Resumes": f"{total_resumes:,}",
            "Avg ATS Score": f"{avg_ats:.1f}%",
            "High Performing": f"{high_performing:,}",
            "Success Rate": f"{success_rate:.1f}%"
        }

    def create_enhanced_ats_gauge(self, value):
        """Create an enhanced ATS score gauge chart with gradient arcs"""
        reference = 70

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            delta={
                'reference': reference,
                'valueformat': '.1f',
                'increasing': {'color': '#68d391'},
                'decreasing': {'color': '#fc8181'},
                'font': {'size': 16}
            },
            number={'font': {'size': 52, 'color': '#4FD1C5', 'family': 'Inter'}, 'suffix': '%'},
            gauge={
                'axis': {
                    'range': [0, 100],
                    'tickwidth': 1,
                    'tickcolor': 'rgba(255,255,255,0.4)',
                    'tickfont': {'color': 'rgba(255,255,255,0.6)', 'size': 11},
                    'nticks': 6
                },
                'bar': {'color': '#4FD1C5', 'thickness': 0.22},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 0,
                'steps': [
                    {'range': [0,  40], 'color': 'rgba(252,129,129,0.25)'},
                    {'range': [40, 70], 'color': 'rgba(246,224,94,0.20)'},
                    {'range': [70,100], 'color': 'rgba(104,211,145,0.20)'},
                ],
                'threshold': {
                    'line': {'color': '#f6e05e', 'width': 3},
                    'thickness': 0.8,
                    'value': reference
                }
            }
        ))

        fig.update_layout(
            title={
                'text': '🎯 ATS Score Performance',
                'font': {'size': 16, 'color': 'rgba(255,255,255,0.85)', 'family': 'Inter'},
                'y': 0.92, 'x': 0.5, 'xanchor': 'center'
            },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white', 'family': 'Inter'},
            height=340,
            margin=dict(l=24, r=24, t=70, b=24)
        )
        return fig

    def create_skill_distribution_chart(self):
        """Create a horizontal gradient skill distribution chart"""
        categories, counts = self.get_skill_distribution()

        palette = ['#4FD1C5', '#63b3ed', '#b794f4', '#68d391', '#f6ad55']
        colors  = [palette[i % len(palette)] for i in range(len(categories))]

        fig = go.Figure(go.Bar(
            x=counts,
            y=categories,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(width=0)
            ),
            text=[f"{c:,}" for c in counts],
            textposition='outside',
            textfont=dict(color='rgba(255,255,255,0.75)', size=12),
        ))

        fig.update_layout(
            title={
                'text': '🛠 Skill Distribution',
                'font': {'size': 16, 'color': 'rgba(255,255,255,0.85)', 'family': 'Inter'},
                'y': 0.96, 'x': 0.5, 'xanchor': 'center'
            },
            height=340,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            margin=dict(l=20, r=60, t=60, b=20),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.07)',
                zeroline=False,
                showline=False,
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                tickfont=dict(size=13, color='rgba(255,255,255,0.8)')
            ),
            bargap=0.28
        )
        return fig

    def create_submission_trends_chart(self):
        """Create a weekly submission trend chart with area fill"""
        dates, submissions = self.get_weekly_trends()

        fig = go.Figure()
        # Area fill
        fig.add_trace(go.Scatter(
            x=dates, y=submissions,
            fill='tozeroy',
            fillcolor='rgba(79,209,197,0.12)',
            line=dict(color='rgba(0,0,0,0)', width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        # Line + markers
        fig.add_trace(go.Scatter(
            x=dates, y=submissions,
            mode='lines+markers',
            name='Submissions',
            line=dict(color='#4FD1C5', width=3, shape='spline', smoothing=1.2),
            marker=dict(
                size=9,
                color='#4FD1C5',
                line=dict(width=2, color='rgba(13,27,42,0.8)')
            ),
            hovertemplate='%{x}: <b>%{y}</b> submissions<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': '📅 Weekly Submission Trend',
                'font': {'size': 16, 'color': 'rgba(255,255,255,0.85)', 'family': 'Inter'},
                'y': 0.94, 'x': 0.5, 'xanchor': 'center'
            },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white', 'family': 'Inter'},
            height=310,
            margin=dict(l=20, r=20, t=55, b=20),
            showlegend=False,
            xaxis=dict(
                showgrid=False, zeroline=False,
                tickfont=dict(size=12, color='rgba(255,255,255,0.6)')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.07)',
                zeroline=False,
                tickfont=dict(size=11, color='rgba(255,255,255,0.6)')
            )
        )
        return fig

    def create_job_category_chart(self):
        """Create a success rate by job category chart with gradient bars"""
        categories, rates = self.get_job_category_stats()

        palette = ['#68d391', '#4FD1C5', '#f6ad55', '#b794f4', '#63b3ed']
        bar_colors = [palette[i % len(palette)] for i in range(len(categories))]

        fig = go.Figure(go.Bar(
            x=categories,
            y=rates,
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{r}%" for r in rates],
            textposition='outside',
            textfont=dict(color='rgba(255,255,255,0.75)', size=12),
        ))

        fig.update_layout(
            title={
                'text': '📊 Success Rate by Job Category',
                'font': {'size': 16, 'color': 'rgba(255,255,255,0.85)', 'family': 'Inter'},
                'y': 0.95, 'x': 0.5, 'xanchor': 'center'
            },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white', 'family': 'Inter'},
            height=310,
            margin=dict(l=20, r=20, t=55, b=20),
            xaxis=dict(
                showgrid=False, zeroline=False,
                tickfont=dict(size=12, color='rgba(255,255,255,0.6)')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.07)',
                zeroline=False,
                tickfont=dict(size=11, color='rgba(255,255,255,0.6)')
            ),
            bargap=0.3
        )
        return fig