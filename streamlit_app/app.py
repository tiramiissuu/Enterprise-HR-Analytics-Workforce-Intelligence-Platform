import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import mysql.connector


st.set_page_config(
    page_title="Enterprise HR Intelligence Studio",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "230623",
    "database": "enterprise_hr_dw",
}


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg: #05070A;
    --sidebar: #090D14;
    --surface: rgba(13, 18, 28, 0.90);
    --surface2: rgba(18, 26, 39, 0.94);
    --border: rgba(148, 163, 184, 0.13);
    --text: #F4F7FB;
    --muted: #9BA7B8;
    --muted2: #6F7F93;
    --purple: #8B7CF6;
    --cyan: #5EEAD4;
    --mint: #7DD3FC;
    --violet: #C084FC;
    --rose: #F0ABFC;
    --blue: #93C5FD;
}

.stApp {
    background:
        radial-gradient(circle at 14% 8%, rgba(167,139,250,0.22), transparent 26%),
        radial-gradient(circle at 92% 12%, rgba(103,232,249,0.14), transparent 24%),
        radial-gradient(circle at 80% 88%, rgba(110,231,183,0.10), transparent 26%),
        linear-gradient(180deg, #05070A 0%, #0A0F18 52%, #060912 100%);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(13,15,23,0.96), rgba(8,10,16,0.98));
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif;
    letter-spacing: -0.055em;
}

.hero {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(167,139,250,0.20), rgba(103,232,249,0.08)),
        rgba(18,21,32,0.86);
    border: 1px solid var(--border);
    border-radius: 34px;
    padding: 38px 42px;
    margin-bottom: 26px;
    box-shadow: 0 28px 80px rgba(0,0,0,0.35);
}

.hero::after {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(125,211,252,0.18), transparent 62%);
    right: -120px;
    top: -130px;
}

.kicker {
    font-family: 'JetBrains Mono', monospace;
    color: var(--cyan);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: .16em;
    font-weight: 700;
}

.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 66px;
    line-height: .9;
    font-weight: 800;
    letter-spacing: -0.085em;
    margin-top: 16px;
    color: var(--text);
}

.hero-subtitle {
    max-width: 820px;
    color: var(--muted);
    font-size: 16px;
    line-height: 1.65;
    margin-top: 18px;
}

.page-title {
    font-family: 'Sora', sans-serif;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -0.06em;
    margin-bottom: 6px;
}

.page-caption {
    color: var(--muted);
    font-size: 15px;
    margin-bottom: 22px;
}

.metric-card {
    background:
        linear-gradient(180deg, rgba(25,29,44,0.95), rgba(14,17,27,0.95));
    border: 1px solid var(--border);
    border-radius: 26px;
    padding: 24px;
    min-height: 145px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.22);
}

.metric-card:hover {
    border-color: rgba(167,139,250,0.55);
    transform: translateY(-2px);
    transition: .22s ease;
}

.metric-label {
    font-family: 'JetBrains Mono', monospace;
    color: var(--muted);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: .13em;
}

.metric-value {
    font-family: 'Sora', sans-serif;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.06em;
    margin-top: 16px;
    color: var(--text);
}

.metric-note {
    color: var(--muted2);
    margin-top: 8px;
    font-size: 13px;
}

.card {
    background:
        linear-gradient(180deg, rgba(18,21,32,0.94), rgba(12,14,22,0.96));
    border: 1px solid var(--border);
    border-radius: 28px;
    padding: 24px;
    margin-bottom: 22px;
    box-shadow: 0 18px 55px rgba(0,0,0,0.22);
}

.section-label {
    font-family: 'JetBrains Mono', monospace;
    color: var(--cyan);
    font-size: 12px;
    letter-spacing: .15em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 6px;
}

[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid var(--border);
}

div[data-testid="stRadio"] > label {
    display: none;
}

div[data-testid="stRadio"] label {
    background: rgba(18,21,32,0.75);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 11px 14px;
    margin-bottom: 8px;
}

div[data-testid="stRadio"] label:hover {
    border-color: rgba(103,232,249,0.6);
    background: rgba(25,29,44,0.98);
}

.stSelectbox div {
    border-radius: 16px;
}

hr {
    border-color: var(--border);
}

.footer-note {
    color: var(--muted2);
    font-size: 13px;
    margin-top: 16px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def run_query(query):
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def chart_style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,15,24,0.94)",
        font=dict(family="Inter", color="#F4F7FB"),
        title=dict(font=dict(size=23, family="Sora", color="#F4F7FB")),
        margin=dict(l=35, r=35, t=75, b=45),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(255,255,255,0.08)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
    )
    return fig


def metric_card(label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


if DB_CONFIG["password"] == "YOUR_MYSQL_PASSWORD":
    st.error("Replace YOUR_MYSQL_PASSWORD in app.py first.")
    st.stop()


st.sidebar.markdown("## ◆ HR Intelligence")
st.sidebar.caption("")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Workforce",
        "Attrition",
        "Recruitment",
        "Performance",
        "Training",
        "Managers",
        "Data Tables"
    ]
)

kpi_query = """
SELECT
COUNT(DISTINCT CASE WHEN fws.is_active = TRUE THEN fws.employee_key END) AS active_employees,
ROUND(AVG(CASE WHEN fws.is_active = TRUE THEN fws.salary END), 2) AS avg_salary,
ROUND(AVG(CASE WHEN fws.is_active = TRUE THEN fws.tenure_months END), 2) AS avg_tenure_months,
ROUND(COUNT(DISTINCT fa.employee_key) * 100.0 / NULLIF(COUNT(DISTINCT fws.employee_key), 0), 2) AS attrition_rate_percent
FROM fact_workforce_snapshot fws
JOIN dim_date dd ON dd.date_key = fws.date_key
LEFT JOIN fact_attrition fa ON fa.employee_key = fws.employee_key
WHERE dd.full_date = (SELECT MAX(full_date) FROM dim_date);
"""

headcount_query = """
SELECT dd.year_number, dd.month_number, dd.month_name,
COUNT(DISTINCT fws.employee_key) AS active_headcount
FROM fact_workforce_snapshot fws
JOIN dim_date dd ON dd.date_key = fws.date_key
WHERE fws.is_active = TRUE
GROUP BY dd.year_number, dd.month_number, dd.month_name
ORDER BY dd.year_number, dd.month_number;
"""

department_query = """
SELECT d.department_name, d.business_unit,
COUNT(DISTINCT fws.employee_key) AS active_headcount,
ROUND(AVG(fws.salary), 2) AS avg_salary,
ROUND(AVG(fws.tenure_months), 2) AS avg_tenure_months
FROM fact_workforce_snapshot fws
JOIN dim_department d ON d.department_key = fws.department_key
JOIN dim_date dd ON dd.date_key = fws.date_key
WHERE fws.is_active = TRUE
AND dd.full_date = (SELECT MAX(full_date) FROM dim_date)
GROUP BY d.department_name, d.business_unit
ORDER BY active_headcount DESC;
"""

attrition_query = """
SELECT d.department_name,
COUNT(*) AS attrition_count,
SUM(CASE WHEN fa.attrition_type = 'Voluntary' THEN 1 ELSE 0 END) AS voluntary_attrition,
SUM(CASE WHEN fa.attrition_type = 'Involuntary' THEN 1 ELSE 0 END) AS involuntary_attrition,
ROUND(AVG(fa.tenure_months), 2) AS avg_tenure_at_exit
FROM fact_attrition fa
JOIN dim_department d ON d.department_key = fa.department_key
GROUP BY d.department_name
ORDER BY attrition_count DESC;
"""

recruitment_query = """
SELECT dd.year_number, dd.month_number, dd.month_name,
SUM(fr.applications_count) AS applications,
SUM(fr.interviews_count) AS interviews,
SUM(fr.offers_count) AS offers,
SUM(fr.hires_count) AS hires,
ROUND(SUM(fr.recruitment_cost) / NULLIF(SUM(fr.hires_count), 0), 2) AS cost_per_hire,
ROUND(AVG(fr.avg_time_to_hire_days), 2) AS avg_time_to_hire_days
FROM fact_recruitment fr
JOIN dim_date dd ON dd.date_key = fr.date_key
GROUP BY dd.year_number, dd.month_number, dd.month_name
ORDER BY dd.year_number, dd.month_number;
"""

performance_query = """
SELECT pr.rating_label,
COUNT(*) AS rating_count,
ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS rating_percent
FROM fact_performance fp
JOIN dim_performance_rating pr ON pr.performance_rating_key = fp.performance_rating_key
GROUP BY pr.rating_label
ORDER BY rating_count DESC;
"""

training_query = """
SELECT training_category,
COUNT(*) AS training_records,
ROUND(SUM(training_hours), 2) AS total_training_hours,
ROUND(SUM(training_cost), 2) AS total_training_cost,
ROUND(AVG(training_hours), 2) AS avg_training_hours
FROM fact_training
GROUP BY training_category
ORDER BY total_training_hours DESC;
"""

attendance_query = """
SELECT d.department_name,
SUM(fa.scheduled_days) AS scheduled_days,
SUM(fa.present_days) AS present_days,
SUM(fa.leave_days) AS leave_days,
SUM(fa.absence_days) AS absence_days,
ROUND(SUM(fa.present_days) * 100.0 / NULLIF(SUM(fa.scheduled_days), 0), 2) AS attendance_percent
FROM fact_attendance fa
JOIN fact_workforce_snapshot fws ON fws.employee_key = fa.employee_key AND fws.date_key = fa.date_key
JOIN dim_department d ON d.department_key = fws.department_key
GROUP BY d.department_name
ORDER BY attendance_percent DESC;
"""

gender_query = """
SELECT e.gender,
COUNT(DISTINCT fws.employee_key) AS active_headcount,
ROUND(COUNT(DISTINCT fws.employee_key) * 100.0 / SUM(COUNT(DISTINCT fws.employee_key)) OVER (), 2) AS percentage
FROM fact_workforce_snapshot fws
JOIN dim_employee e ON e.employee_key = fws.employee_key
JOIN dim_date dd ON dd.date_key = fws.date_key
WHERE fws.is_active = TRUE
AND dd.full_date = (SELECT MAX(full_date) FROM dim_date)
GROUP BY e.gender
ORDER BY active_headcount DESC;
"""

manager_query = """
SELECT m.manager_name, m.manager_level,
COUNT(DISTINCT fws.employee_key) AS team_size,
ROUND(AVG(fws.salary), 2) AS avg_team_salary,
ROUND(AVG(fws.tenure_months), 2) AS avg_team_tenure_months,
ROUND(AVG(pr.rating_code), 2) AS avg_performance_rating
FROM fact_workforce_snapshot fws
JOIN dim_manager m ON m.manager_key = fws.manager_key
LEFT JOIN fact_performance fp ON fp.employee_key = fws.employee_key
LEFT JOIN dim_performance_rating pr ON pr.performance_rating_key = fp.performance_rating_key
JOIN dim_date dd ON dd.date_key = fws.date_key
WHERE fws.is_active = TRUE
AND dd.full_date = (SELECT MAX(full_date) FROM dim_date)
GROUP BY m.manager_name, m.manager_level
ORDER BY avg_performance_rating DESC
LIMIT 15;
"""

kpi = run_query(kpi_query).iloc[0]
headcount_df = run_query(headcount_query)
department_df = run_query(department_query)
attrition_df = run_query(attrition_query)
recruitment_df = run_query(recruitment_query)
performance_df = run_query(performance_query)
training_df = run_query(training_query)
attendance_df = run_query(attendance_query)
gender_df = run_query(gender_query)
manager_df = run_query(manager_query)

headcount_df["period"] = headcount_df["month_name"] + " " + headcount_df["year_number"].astype(str)
recruitment_df["period"] = recruitment_df["month_name"] + " " + recruitment_df["year_number"].astype(str)


st.markdown("""
<div class="hero">
    <div class="kicker">Enterprise HR Analytics Warehouse</div>
    <div class="hero-title">Workforce Intelligence Studio</div>
</div>
""", unsafe_allow_html=True)

if page == "Executive Overview":
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Active Employees", f"{int(kpi['active_employees']):,}", "Current active workforce")
    with c2:
        metric_card("Average Salary", f"₹{kpi['avg_salary']:,.0f}", "Across active employees")
    with c3:
        metric_card("Average Tenure", f"{kpi['avg_tenure_months']:.1f} mo", "Current workforce tenure")
    with c4:
        metric_card("Attrition Rate", f"{kpi['attrition_rate_percent']:.2f}%", "Overall exit percentage")

    st.markdown('<div class="card"><div class="section-label">Executive Pulse</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=headcount_df["period"],
        y=headcount_df["active_headcount"],
        mode="lines+markers",
        line=dict(color="#8B7CF6", width=4, shape="spline"),
        marker=dict(size=8, color="#5EEAD4"),
        fill="tozeroy",
        fillcolor="rgba(167,139,250,0.14)"
    ))
    fig.update_layout(title="Monthly Active Headcount Trend")
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


elif page == "Workforce":
    st.markdown('<div class="page-title">Workforce Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-caption">Explore department structure, headcount distribution and workforce diversity.</div>', unsafe_allow_html=True)

    left, right = st.columns([1.2, 0.8])

    with left:
        st.markdown('<div class="card"><div class="section-label">Department Distribution</div>', unsafe_allow_html=True)

        fig = px.bar(
            department_df,
            x="active_headcount",
            y="department_name",
            orientation="h",
            title="Active Headcount by Department",
            color="active_headcount",
            color_continuous_scale=["#5EEAD4", "#8B7CF6", "#F0ABFC"]
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><div class="section-label">Diversity View</div>', unsafe_allow_html=True)

        fig = px.pie(
            gender_df,
            names="gender",
            values="active_headcount",
            hole=0.62,
            title="Gender Diversity",
            color_discrete_sequence=["#8B7CF6", "#5EEAD4", "#7DD3FC"]
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(department_df, use_container_width=True)


elif page == "Attrition":
    st.markdown('<div class="page-title">Attrition Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-caption">Understand employee exits across departments and exit categories.</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="section-label">Exit Breakdown</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=attrition_df["department_name"],
        y=attrition_df["voluntary_attrition"],
        name="Voluntary",
        marker_color="#F0ABFC"
    ))
    fig.add_trace(go.Bar(
        x=attrition_df["department_name"],
        y=attrition_df["involuntary_attrition"],
        name="Involuntary",
        marker_color="#7DD3FC"
    ))
    fig.update_layout(title="Voluntary vs Involuntary Attrition", barmode="group")
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(attrition_df, use_container_width=True)

elif page == "Recruitment":
    st.markdown('<div class="page-title">Recruitment Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-caption">Track hiring funnel efficiency, monthly hires, cost per hire and time to hire.</div>', unsafe_allow_html=True)

    funnel = pd.DataFrame({
        "stage": ["Applications", "Interviews", "Offers", "Hires"],
        "count": [
            recruitment_df["applications"].sum(),
            recruitment_df["interviews"].sum(),
            recruitment_df["offers"].sum(),
            recruitment_df["hires"].sum()
        ]
    })

    st.markdown('<div class="card"><div class="section-label">Hiring Funnel</div>', unsafe_allow_html=True)

    fig = px.funnel(
        funnel,
        x="count",
        y="stage",
        title="Recruitment Funnel",
        color_discrete_sequence=["#A78BFA"]
    )
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="card"><div class="section-label">Hiring Trend</div>', unsafe_allow_html=True)
        fig = px.line(
            recruitment_df,
            x="period",
            y="hires",
            markers=True,
            title="Monthly Hires",
            color_discrete_sequence=["#67E8F9"]
        )
        fig.update_traces(line=dict(width=4, shape="spline"))
        st.plotly_chart(chart_style(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="section-label">Speed</div>', unsafe_allow_html=True)
        fig = px.line(
            recruitment_df,
            x="period",
            y="avg_time_to_hire_days",
            markers=True,
            title="Average Time to Hire",
            color_discrete_sequence=["#7DD3FC"]
        )
        fig.update_traces(line=dict(width=4, shape="spline"))
        st.plotly_chart(chart_style(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(recruitment_df, use_container_width=True)


elif page == "Performance":
    st.markdown('<div class="page-title">Performance Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-caption">Analyze employee performance rating distribution across the organization.</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="section-label">Ratings</div>', unsafe_allow_html=True)

    fig = px.bar(
        performance_df,
        x="rating_label",
        y="rating_count",
        title="Performance Rating Distribution",
        color="rating_count",
        color_continuous_scale=["#5EEAD4", "#8B7CF6", "#F0ABFC"]
    )
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(performance_df, use_container_width=True)


elif page == "Training":
    st.markdown('<div class="page-title">Learning & Attendance</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-caption">Review training investment, learning hours and department attendance health.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="card"><div class="section-label">Learning Investment</div>', unsafe_allow_html=True)

        fig = px.bar(
            training_df,
            x="training_category",
            y="total_training_hours",
            title="Training Hours by Category",
            color="total_training_hours",
            color_continuous_scale=["#7DD3FC", "#5EEAD4", "#8B7CF6"]
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="section-label">Attendance Health</div>', unsafe_allow_html=True)

        fig = px.bar(
            attendance_df,
            x="department_name",
            y="attendance_percent",
            title="Attendance % by Department",
            color="attendance_percent",
            color_continuous_scale=["#C084FC", "#7DD3FC", "#5EEAD4"]
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(training_df, use_container_width=True)


elif page == "Managers":
    st.markdown('<div class="page-title">Leadership Lens</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-caption">Compare team size, salary profile, tenure and average performance by manager.</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="section-label">Manager Performance</div>', unsafe_allow_html=True)

    fig = px.bar(
        manager_df,
        x="avg_performance_rating",
        y="manager_name",
        orientation="h",
        title="Top Managers by Average Team Performance",
        color="avg_performance_rating",
        color_continuous_scale=["#F0ABFC", "#8B7CF6", "#5EEAD4"]
    )
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(manager_df, use_container_width=True)


elif page == "Data Tables":
    st.markdown('<div class="page-title">Warehouse Data Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-caption">Browse curated analytical datasets generated from the HR warehouse.</div>', unsafe_allow_html=True)

    table = st.selectbox(
        "Choose dataset",
        [
            "Department Summary",
            "Attrition Summary",
            "Recruitment Summary",
            "Performance Summary",
            "Training Summary",
            "Attendance Summary",
            "Manager Summary"
        ]
    )

    tables = {
        "Department Summary": department_df,
        "Attrition Summary": attrition_df,
        "Recruitment Summary": recruitment_df,
        "Performance Summary": performance_df,
        "Training Summary": training_df,
        "Attendance Summary": attendance_df,
        "Manager Summary": manager_df,
    }

    st.markdown('<div class="card"><div class="section-label">Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(tables[table], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown(
    '<div class="footer-note">Built on a MySQL dimensional warehouse with synthetic enterprise HR data, ETL staging, fact tables and analytical marts.</div>',
    unsafe_allow_html=True
)
