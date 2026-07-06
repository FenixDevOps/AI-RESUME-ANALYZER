import streamlit as st
from typing import List, Dict
from .job_portals import JobPortal
from .suggestions import (
    JOB_SUGGESTIONS, 
    LOCATION_SUGGESTIONS, 
    EXPERIENCE_RANGES,
    SALARY_RANGES,
    JOB_TYPES,
    get_cities_by_state,
    get_all_states
)
from .companies import get_featured_companies, get_market_insights
from .linkedin_scraper import render_linkedin_scraper
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu

def filter_suggestions(query: str, suggestions: List[Dict]) -> List[Dict]:
    """Filter suggestions based on user input"""
    if not query:
        return []
    return [
        s for s in suggestions 
        if query.lower() in s["text"].lower()
    ][:5]

def filter_location_suggestions(query: str, suggestions: List[Dict]) -> List[Dict]:
    """Filter location suggestions based on user input with smart categorization"""
    if not query or len(query) < 2:
        return []
        
    # First check if query matches any state
    matching_states = [s for s in suggestions if s.get("type") == "state" and query.lower() in s["text"].lower()]
    
    # Then check cities
    matching_cities = [s for s in suggestions if s.get("type") == "city" and query.lower() in s["text"].lower()]
    
    # Then check work modes
    matching_work_modes = [s for s in suggestions if s.get("type") == "work_mode" and query.lower() in s["text"].lower()]
    
    # Combine results with states first, then major cities, then other matches
    results = matching_states + matching_cities + matching_work_modes
    return results[:7]  # Return top 7 matches

def get_filter_options():
    """Get filter options for job search"""
    return {
        "experience_levels": [
            {"id": "all", "text": "All Levels"},
            {"id": "fresher", "text": "Fresher"},
            {"id": "0-1", "text": "0-1 years"},
            {"id": "1-3", "text": "1-3 years"},
            {"id": "3-5", "text": "3-5 years"},
            {"id": "5-7", "text": "5-7 years"},
            {"id": "7-10", "text": "7-10 years"},
            {"id": "10+", "text": "10+ years"}
        ],
        "salary_ranges": [
            {"id": "all", "text": "All Ranges"},
            {"id": "0-3", "text": "0-3 LPA"},
            {"id": "3-6", "text": "3-6 LPA"},
            {"id": "6-10", "text": "6-10 LPA"},
            {"id": "10-15", "text": "10-15 LPA"},
            {"id": "15+", "text": "15+ LPA"}
        ],
        "job_types": [
            {"id": "all", "text": "All Types"},
            {"id": "full-time", "text": "Full Time"},
            {"id": "part-time", "text": "Part Time"},
            {"id": "contract", "text": "Contract"},
            {"id": "remote", "text": "Remote"}
        ]
    }

def render_company_section():
    """Render the featured companies section with premium cards"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        * { font-family: 'Inter', sans-serif; }

        /* ── Company Section ── */
        .company-section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #4FD1C5;
            margin: 2rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(79,209,197,0.2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .company-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 1.1rem;
            padding: 0.5rem 0 1rem;
        }
        .company-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            overflow: hidden;
            transition: transform 0.26s ease, box-shadow 0.26s ease, background 0.26s ease;
            cursor: pointer;
        }
        .company-card:hover {
            transform: translateY(-6px);
            background: rgba(255,255,255,0.08);
            box-shadow: 0 14px 36px rgba(0,0,0,0.35);
        }
        .company-card-banner {
            height: 6px;
        }
        .company-card-body {
            padding: 1.1rem 1.2rem;
        }
        .company-header {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 0.55rem;
        }
        .company-icon {
            font-size: 1.7rem;
            line-height: 1;
        }
        .company-name {
            font-size: 1.05rem;
            font-weight: 700;
            color: #fff;
            margin: 0;
        }
        .company-desc {
            font-size: 0.82rem;
            color: rgba(255,255,255,0.5);
            margin: 0 0 0.75rem;
            line-height: 1.45;
        }
        .company-categories {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-bottom: 0.85rem;
        }
        .company-category {
            background: rgba(79,209,197,0.1);
            color: #4FD1C5;
            border: 1px solid rgba(79,209,197,0.25);
            padding: 0.18rem 0.55rem;
            border-radius: 20px;
            font-size: 0.74rem;
            font-weight: 500;
        }
        .company-cta {
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 600;
            color: rgba(255,255,255,0.6);
            text-decoration: none;
        }
        .company-cta:hover { color: #4FD1C5; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="company-section-title">🏢 Featured Companies</div>', unsafe_allow_html=True)

    # Banner gradient per tab
    banners = [
        'linear-gradient(90deg,#4FD1C5,#63b3ed)',
        'linear-gradient(90deg,#63b3ed,#4299e1)',
        'linear-gradient(90deg,#f6ad55,#ed8936)',
        'linear-gradient(90deg,#b794f4,#9f7aea)'
    ]
    tabs = st.tabs(["All Companies", "Tech Giants", "Indian Tech", "Global Corps"])
    categories = [None, "tech", "indian_tech", "global_corps"]

    for tab, category, banner in zip(tabs, categories, banners):
        with tab:
            companies = get_featured_companies(category)
            html = '<div class="company-grid">'
            for company in companies:
                cats_html = ''.join(
                    f'<span class="company-category">{cat}</span>'
                    for cat in company['categories']
                )
                html += f"""
                <a href="{company['careers_url']}" target="_blank" style="text-decoration:none;color:inherit;">
                    <div class="company-card">
                        <div class="company-card-banner" style="background:{banner};"></div>
                        <div class="company-card-body">
                            <div class="company-header">
                                <span class="company-icon">{company.get('emoji', '🏢')}</span>
                                <p class="company-name">{company['name']}</p>
                            </div>
                            <p class="company-desc">{company['description']}</p>
                            <div class="company-categories">{cats_html}</div>
                            <span class="company-cta">View Careers →</span>
                        </div>
                    </div>
                </a>"""
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

def render_market_insights():
    """Render job market insights section with premium cards"""
    insights = get_market_insights()

    st.markdown("""
        <style>
        .insights-section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #4FD1C5;
            margin: 1.5rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(79,209,197,0.2);
        }
        /* Trending Skills */
        .skill-insight-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            margin-bottom: 0.7rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: background 0.2s ease, transform 0.2s ease;
        }
        .skill-insight-card:hover {
            background: rgba(255,255,255,0.07);
            transform: translateX(4px);
        }
        .skill-icon-badge {
            font-size: 1.8rem;
            min-width: 2.5rem;
            text-align: center;
        }
        .skill-info { flex: 1; }
        .skill-name {
            font-size: 0.95rem;
            font-weight: 700;
            color: #fff;
            margin: 0 0 0.4rem;
        }
        .skill-bar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            height: 6px;
            overflow: hidden;
        }
        .skill-bar-fill {
            height: 6px;
            border-radius: 20px;
            background: linear-gradient(90deg, #4FD1C5, #63b3ed);
            transition: width 0.6s ease;
        }
        .skill-growth {
            font-size: 0.8rem;
            font-weight: 700;
            color: #68d391;
            white-space: nowrap;
        }
        /* Locations */
        .location-insight-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.65rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: background 0.2s ease, transform 0.2s ease;
        }
        .location-insight-card:hover {
            background: rgba(255,255,255,0.07);
            transform: translateX(4px);
        }
        .location-left {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }
        .location-icon { font-size: 1.5rem; }
        .location-name {
            font-size: 0.95rem;
            font-weight: 600;
            color: #fff;
            margin: 0;
        }
        .location-jobs-badge {
            background: rgba(79,209,197,0.12);
            border: 1px solid rgba(79,209,197,0.28);
            color: #4FD1C5;
            font-size: 0.78rem;
            font-weight: 700;
            padding: 0.2rem 0.65rem;
            border-radius: 20px;
        }
        /* Salary */
        .salary-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 1.2rem 1.3rem;
            margin-bottom: 0.75rem;
            border-left: 4px solid #4FD1C5;
            transition: background 0.2s ease, transform 0.2s ease;
        }
        .salary-card:hover {
            background: rgba(255,255,255,0.07);
            transform: translateX(6px);
        }
        .salary-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.7rem;
        }
        .salary-role {
            font-size: 1rem;
            font-weight: 700;
            color: #fff;
            margin: 0 0 0.25rem;
        }
        .salary-exp-tag {
            font-size: 0.75rem;
            color: rgba(255,255,255,0.5);
        }
        .salary-amount {
            font-size: 1.15rem;
            font-weight: 800;
            color: #4FD1C5;
            white-space: nowrap;
        }
        .salary-range-bar {
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .salary-range-track {
            flex: 1;
            background: rgba(255,255,255,0.09);
            border-radius: 20px;
            height: 5px;
            overflow: hidden;
        }
        .salary-range-fill {
            height: 5px;
            border-radius: 20px;
            background: linear-gradient(90deg, #4FD1C5, #68d391);
        }
        .salary-min, .salary-max {
            font-size: 0.72rem;
            color: rgba(255,255,255,0.45);
            white-space: nowrap;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="insights-section-title">📊 Job Market Insights</div>', unsafe_allow_html=True)

    tabs = st.tabs(["🔥 Trending Skills", "📍 Top Locations", "💰 Salary Insights"])

    with tabs[0]:
        for skill in insights["trending_skills"]:
            # Parse growth % for bar width (e.g. "+45%" → 45)
            growth_str = str(skill.get('growth', '0%'))
            try:
                growth_num = int(''.join(filter(str.isdigit, growth_str)))
            except Exception:
                growth_num = 30
            bar_w = min(growth_num, 100)
            st.markdown(f"""
                <div class="skill-insight-card">
                    <div class="skill-icon-badge">{skill.get('emoji', '⚡')}</div>
                    <div class="skill-info">
                        <p class="skill-name">{skill['name']}</p>
                        <div class="skill-bar-track">
                            <div class="skill-bar-fill" style="width:{bar_w}%;"></div>
                        </div>
                    </div>
                    <span class="skill-growth">↑ {skill['growth']}</span>
                </div>
            """, unsafe_allow_html=True)

    with tabs[1]:
        for location in insights["top_locations"]:
            st.markdown(f"""
                <div class="location-insight-card">
                    <div class="location-left">
                        <span class="location-icon">{location.get('emoji', '📍')}</span>
                        <p class="location-name">{location['name']}</p>
                    </div>
                    <span class="location-jobs-badge">{location['jobs']} Jobs</span>
                </div>
            """, unsafe_allow_html=True)

    with tabs[2]:
        salary_colors = ['#4FD1C5','#63b3ed','#b794f4','#68d391','#f6ad55']
        for i, insight in enumerate(insights["salary_insights"]):
            border_color = salary_colors[i % len(salary_colors)]
            st.markdown(f"""
                <div class="salary-card" style="border-left-color:{border_color};">
                    <div class="salary-top">
                        <div>
                            <p class="salary-role">{insight['role']}</p>
                            <span class="salary-exp-tag">⏱ {insight['experience']}</span>
                        </div>
                        <span class="salary-amount">₹ {insight['range']}</span>
                    </div>
                    <div class="salary-range-bar">
                        <span class="salary-min">Entry</span>
                        <div class="salary-range-track">
                            <div class="salary-range-fill" style="width:{55 + i*8}%;"></div>
                        </div>
                        <span class="salary-max">Senior</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def render_job_search():
    """Render job search page with enhanced features"""

    # ── Hero Banner ────────────────────────────────────────────────────────────
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        * { font-family: 'Inter', sans-serif; }

        /* Hero */
        .jobs-hero {
            background: linear-gradient(135deg, #0d1b2a 0%, #0f3460 60%, #16213e 100%);
            border-radius: 20px;
            padding: 2.2rem 2.6rem;
            margin-bottom: 1.8rem;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(79,209,197,0.16);
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }
        .jobs-hero::before {
            content: '';
            position: absolute;
            top: -60%; right: -10%;
            width: 55%; height: 240%;
            background: radial-gradient(ellipse, rgba(79,209,197,0.1) 0%, transparent 65%);
            pointer-events: none;
        }
        .jobs-hero h1 {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #4FD1C5 0%, #63b3ed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 0.4rem;
            letter-spacing: -0.5px;
        }
        .jobs-hero p {
            color: rgba(255,255,255,0.5);
            font-size: 1rem;
            margin: 0;
        }
        .jobs-hero-badges {
            display: flex;
            gap: 0.7rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }
        .jobs-badge {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 20px;
            padding: 0.3rem 0.8rem;
            font-size: 0.78rem;
            color: rgba(255,255,255,0.65);
        }

        /* Search container */
        .search-container {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1.6rem 1.8rem;
            margin-bottom: 1.5rem;
        }
        .search-section-label {
            font-size: 1.1rem;
            font-weight: 700;
            color: #fff;
            margin: 0 0 0.25rem;
        }
        .search-section-sub {
            font-size: 0.84rem;
            color: rgba(255,255,255,0.45);
            margin: 0 0 1.2rem;
        }

        /* Result cards */
        .result-cards-grid { display: flex; flex-direction: column; gap: 0.85rem; margin-top: 1.2rem; }
        .result-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 16px;
            padding: 1.2rem 1.4rem;
            display: flex;
            align-items: center;
            gap: 1.1rem;
            transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.22s ease;
        }
        .result-card:hover {
            transform: translateX(5px);
            background: rgba(255,255,255,0.08);
            box-shadow: 0 8px 28px rgba(0,0,0,0.28);
        }
        .result-portal-dot {
            width: 4px;
            min-height: 60px;
            border-radius: 4px;
            flex-shrink: 0;
        }
        .result-body { flex: 1; }
        .result-portal-name {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin: 0 0 0.3rem;
        }
        .result-title {
            font-size: 0.95rem;
            color: rgba(255,255,255,0.7);
            margin: 0;
        }
        .result-cta {
            display: inline-block;
            padding: 0.45rem 1rem;
            border-radius: 10px;
            font-size: 0.8rem;
            font-weight: 700;
            text-decoration: none;
            color: #0d1b2a;
            white-space: nowrap;
            transition: opacity 0.2s ease, transform 0.2s ease;
        }
        .result-cta:hover { opacity: 0.85; transform: scale(1.03); }

        /* Search CTA button */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #4FD1C5 0%, #38b2ac 100%) !important;
            color: #0d1b2a !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            padding: 0.75rem 2rem !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 20px rgba(79,209,197,0.3) !important;
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            box-shadow: 0 8px 30px rgba(79,209,197,0.5) !important;
            transform: translateY(-2px) !important;
        }

        /* option_menu nav overrides */
        .nav-link-selected { background-color: #4FD1C5 !important; color: #0d1b2a !important; }
        </style>

        <div class="jobs-hero">
            <h1>🔍 Smart Job Search</h1>
            <p>Discover opportunities across top platforms — curated for your resume</p>
            <div class="jobs-hero-badges">
                <span class="jobs-badge">🌐 LinkedIn</span>
                <span class="jobs-badge">💼 Indeed</span>
                <span class="jobs-badge">📋 Naukri</span>
                <span class="jobs-badge">🚀 Foundit</span>
                <span class="jobs-badge">🤖 AI-Matched</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Market Insights Section (Above Search)
    render_market_insights()

    # Job Search Section
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)

        # Portal tabs
        tabs = option_menu(
            menu_title=None,
            options=["Job Portal", "LinkedIn"],
            icons=["search", "linkedin"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0px", "margin-bottom": "1.2rem", "background": "transparent"},
                "icon": {"font-size": "17px"},
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "center",
                    "padding": "10px 20px",
                    "border-radius": "10px",
                    "color": "rgba(255,255,255,0.65)",
                    "font-weight": "600"
                },
                "nav-link-selected": {
                    "background-color": "#4FD1C5",
                    "color": "#0d1b2a",
                    "font-weight": "700"
                },
            }
        )

        if tabs == "Job Portal":
            st.markdown('<p class="search-section-label">🌐 Search Jobs Across Multiple Platforms</p>', unsafe_allow_html=True)
            st.markdown('<p class="search-section-sub">Find opportunities from LinkedIn, Indeed, Naukri, and Foundit</p>', unsafe_allow_html=True)

            col1, col2 = st.columns([2, 1])
            with col1:
                job_query = st.text_input(
                    "Job Title / Skills",
                    value="",
                    placeholder="e.g. Software Engineer, Data Scientist"
                )
                if job_query and len(job_query) >= 2:
                    filtered_jobs = [s["text"] for s in JOB_SUGGESTIONS if job_query.lower() in s["text"].lower()]
                    if filtered_jobs:
                        job_query = st.selectbox("Select Job Title", filtered_jobs)

            with col2:
                location = st.text_input(
                    "Location",
                    value="",
                    placeholder="e.g. Bangalore, Karnataka"
                )
                if location and len(location) >= 2:
                    filtered_locations = filter_location_suggestions(location, LOCATION_SUGGESTIONS)
                    if filtered_locations:
                        location_options = []
                        location_display = {}
                        for loc in filtered_locations:
                            display_text = loc["text"]
                            if loc.get("type") == "state":
                                display_text = f"{loc['text']} (State)"
                            elif loc.get("type") == "city":
                                display_text = f"{loc['text']}, {loc.get('state', '')}"
                            elif loc.get("type") == "work_mode":
                                display_text = f"{loc['text']} (Work Mode)"
                            location_options.append(loc["text"])
                            location_display[loc["text"]] = display_text

                        selected_location = st.selectbox(
                            "Select Location",
                            options=location_options,
                            format_func=lambda x: location_display.get(x, x)
                        )
                        location = selected_location

                        selected_loc_type = next(
                            (loc.get("type") for loc in filtered_locations if loc["text"] == selected_location),
                            None
                        )
                        if selected_loc_type == "state":
                            st.markdown(f"**Cities in {selected_location}:**")
                            cities = get_cities_by_state(selected_location)
                            city_cols = st.columns(3)
                            for i, city in enumerate(cities):
                                with city_cols[i % 3]:
                                    if st.button(f"{city['icon']} {city['text']}", key=f"city_{i}"):
                                        location = city['text']

            # Advanced Filters
            with st.expander("🎯 Advanced Filters"):
                filter_cols = st.columns(3)
                with filter_cols[0]:
                    experience = st.selectbox(
                        "Experience Level",
                        options=get_filter_options()["experience_levels"],
                        format_func=lambda x: x["text"]
                    )
                with filter_cols[1]:
                    salary_range = st.selectbox(
                        "Salary Range",
                        options=get_filter_options()["salary_ranges"],
                        format_func=lambda x: x["text"]
                    )
                with filter_cols[2]:
                    job_type = st.selectbox(
                        "Job Type",
                        options=get_filter_options()["job_types"],
                        format_func=lambda x: x["text"]
                    )

            # Search button
            if st.button("🔍 SEARCH JOBS", type="primary", use_container_width=True):
                if job_query:
                    job_portal = JobPortal()
                    results = job_portal.search_jobs(job_query, location, experience)

                    if results:
                        # Per-portal color map
                        portal_colors = {
                            'LinkedIn':  {'border': '#0A66C2', 'cta_bg': '#0A66C2'},
                            'Indeed':    {'border': '#003A9B', 'cta_bg': '#003A9B'},
                            'Naukri':    {'border': '#4FD1C5', 'cta_bg': '#4FD1C5'},
                            'Foundit':   {'border': '#b794f4', 'cta_bg': '#9f7aea'},
                        }
                        default_colors = {'border': '#4FD1C5', 'cta_bg': '#4FD1C5'}

                        st.markdown('<div class="result-cards-grid">', unsafe_allow_html=True)
                        for result in results:
                            pc = portal_colors.get(result.get('portal', ''), default_colors)
                            st.markdown(f"""
                            <div class="result-card">
                                <div class="result-portal-dot" style="background:{pc['border']};"></div>
                                <div class="result-body">
                                    <p class="result-portal-name" style="color:{pc['border']};">{result['portal']}</p>
                                    <p class="result-title">{result['title']}</p>
                                </div>
                                <a href="{result['url']}" target="_blank"
                                   class="result-cta"
                                   style="background:{pc['cta_bg']};">
                                    View Jobs →
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No results found. Try different search terms or filters.")
                else:
                    st.warning("Please enter a job title or skills to search.")

        else:
            st.markdown('<p class="search-section-label">💼 LinkedIn Job Scraper</p>', unsafe_allow_html=True)
            st.markdown('<p class="search-section-sub">Find real-time job listings directly from LinkedIn</p>', unsafe_allow_html=True)
            render_linkedin_scraper()

        st.markdown('</div>', unsafe_allow_html=True)

    # Featured Companies Section
    render_company_section()

# Removed render_job_search() call to prevent automatic rendering