USE enterprise_hr_dw;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE fact_attrition;
TRUNCATE TABLE fact_recruitment;
TRUNCATE TABLE fact_training;
TRUNCATE TABLE fact_performance;
TRUNCATE TABLE fact_attendance;
TRUNCATE TABLE fact_workforce_snapshot;

SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO fact_workforce_snapshot (
    date_key,
    employee_key,
    department_key,
    job_key,
    location_key,
    manager_key,
    education_key,
    salary,
    tenure_months,
    is_active
)
SELECT
    dd.date_key,
    de.employee_key,
    dp.department_key,
    dj.job_key,
    dl.location_key,
    dm.manager_key,
    ded.education_key,
    sw.salary,
    sw.tenure_months,
    sw.is_active
FROM stg_workforce_monthly sw
JOIN dim_date dd ON dd.full_date = sw.snapshot_date
JOIN dim_employee de ON de.employee_id = sw.employee_id
JOIN dim_department dp ON dp.department_name = sw.department_name
JOIN dim_job dj ON dj.job_title = sw.job_title AND dj.job_level = sw.job_level
JOIN dim_location dl ON dl.city = sw.city AND dl.state = sw.state AND dl.country = sw.country
JOIN dim_manager dm ON dm.manager_id = sw.manager_id
JOIN dim_education ded ON ded.education_level = sw.education_level;

INSERT INTO fact_attendance (
    date_key,
    employee_key,
    scheduled_days,
    present_days,
    leave_days,
    absence_days,
    overtime_hours
)
SELECT
    dd.date_key,
    de.employee_key,
    sa.scheduled_days,
    sa.present_days,
    sa.leave_days,
    sa.absence_days,
    sa.overtime_hours
FROM stg_attendance_monthly sa
JOIN dim_date dd ON dd.full_date = sa.attendance_date
JOIN dim_employee de ON de.employee_id = sa.employee_id;

INSERT INTO fact_performance (
    date_key,
    employee_key,
    performance_rating_key,
    goals_completed,
    promotion_flag,
    bonus_amount
)
SELECT
    dd.date_key,
    de.employee_key,
    dpr.performance_rating_key,
    sp.goals_completed,
    sp.promotion_flag,
    sp.bonus_amount
FROM stg_performance_monthly sp
JOIN dim_date dd ON dd.full_date = sp.performance_date
JOIN dim_employee de ON de.employee_id = sp.employee_id
JOIN dim_performance_rating dpr ON dpr.rating_code = sp.rating_code;

INSERT INTO fact_training (
    date_key,
    employee_key,
    training_category,
    training_hours,
    training_cost,
    completion_status
)
SELECT
    dd.date_key,
    de.employee_key,
    st.training_category,
    st.training_hours,
    st.training_cost,
    st.completion_status
FROM stg_training_monthly st
JOIN dim_date dd ON dd.full_date = st.training_date
JOIN dim_employee de ON de.employee_id = st.employee_id;

INSERT INTO fact_recruitment (
    date_key,
    department_key,
    job_key,
    location_key,
    applications_count,
    interviews_count,
    offers_count,
    hires_count,
    recruitment_cost,
    avg_time_to_hire_days
)
SELECT
    dd.date_key,
    dp.department_key,
    dj.job_key,
    dl.location_key,
    sr.applications_count,
    sr.interviews_count,
    sr.offers_count,
    sr.hires_count,
    sr.recruitment_cost,
    sr.avg_time_to_hire_days
FROM stg_recruitment_monthly sr
JOIN dim_date dd ON dd.full_date = sr.recruitment_date
JOIN dim_department dp ON dp.department_name = sr.department_name
JOIN dim_job dj ON dj.job_title = sr.job_title AND dj.job_level = sr.job_level
JOIN dim_location dl ON dl.city = sr.city AND dl.state = sr.state AND dl.country = sr.country;

INSERT INTO fact_attrition (
    date_key,
    employee_key,
    department_key,
    job_key,
    location_key,
    attrition_type,
    attrition_reason,
    final_salary,
    tenure_months
)
SELECT
    dd.date_key,
    de.employee_key,
    dp.department_key,
    dj.job_key,
    dl.location_key,
    sa.attrition_type,
    sa.attrition_reason,
    sa.final_salary,
    sa.tenure_months
FROM stg_attrition_events sa
JOIN dim_date dd ON dd.full_date = sa.attrition_date
JOIN dim_employee de ON de.employee_id = sa.employee_id
JOIN dim_department dp ON dp.department_name = sa.department_name
JOIN dim_job dj ON dj.job_title = sa.job_title AND dj.job_level = sa.job_level
JOIN dim_location dl ON dl.city = sa.city AND dl.state = sa.state AND dl.country = sa.country;