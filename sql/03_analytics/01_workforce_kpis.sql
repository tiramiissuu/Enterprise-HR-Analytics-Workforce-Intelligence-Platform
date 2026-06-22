USE enterprise_hr_dw;

-- 1. Executive Workforce KPI Summary
SELECT
    COUNT(DISTINCT CASE WHEN fws.is_active = TRUE THEN fws.employee_key END) AS active_employees,
    ROUND(AVG(CASE WHEN fws.is_active = TRUE THEN fws.salary END), 2) AS avg_salary,
    ROUND(AVG(CASE WHEN fws.is_active = TRUE THEN fws.tenure_months END), 2) AS avg_tenure_months,
    ROUND(
        COUNT(DISTINCT fa.employee_key) * 100.0 /
        NULLIF(COUNT(DISTINCT fws.employee_key), 0),
        2
    ) AS attrition_rate_percent
FROM fact_workforce_snapshot fws
JOIN dim_date dd ON dd.date_key = fws.date_key
LEFT JOIN fact_attrition fa ON fa.employee_key = fws.employee_key
WHERE dd.full_date = (
    SELECT MAX(full_date)
    FROM dim_date
);

-- 2. Monthly Headcount Trend
SELECT
    dd.year_number,
    dd.month_number,
    dd.month_name,
    COUNT(DISTINCT fws.employee_key) AS active_headcount
FROM fact_workforce_snapshot fws
JOIN dim_date dd ON dd.date_key = fws.date_key
WHERE fws.is_active = TRUE
GROUP BY
    dd.year_number,
    dd.month_number,
    dd.month_name
ORDER BY
    dd.year_number,
    dd.month_number;

-- 3. Department Workforce Summary
SELECT
    d.department_name,
    d.business_unit,
    COUNT(DISTINCT fws.employee_key) AS active_headcount,
    ROUND(AVG(fws.salary), 2) AS avg_salary,
    ROUND(AVG(fws.tenure_months), 2) AS avg_tenure_months
FROM fact_workforce_snapshot fws
JOIN dim_department d ON d.department_key = fws.department_key
JOIN dim_date dd ON dd.date_key = fws.date_key
WHERE fws.is_active = TRUE
  AND dd.full_date = (
      SELECT MAX(full_date)
      FROM dim_date
  )
GROUP BY
    d.department_name,
    d.business_unit
ORDER BY active_headcount DESC;

-- 4. Attrition by Department
SELECT
    d.department_name,
    COUNT(*) AS attrition_count,
    SUM(CASE WHEN fa.attrition_type = 'Voluntary' THEN 1 ELSE 0 END) AS voluntary_attrition,
    SUM(CASE WHEN fa.attrition_type = 'Involuntary' THEN 1 ELSE 0 END) AS involuntary_attrition,
    ROUND(AVG(fa.tenure_months), 2) AS avg_tenure_at_exit
FROM fact_attrition fa
JOIN dim_department d ON d.department_key = fa.department_key
GROUP BY d.department_name
ORDER BY attrition_count DESC;

-- 5. Recruitment Funnel
SELECT
    dd.year_number,
    dd.month_number,
    dd.month_name,
    SUM(fr.applications_count) AS applications,
    SUM(fr.interviews_count) AS interviews,
    SUM(fr.offers_count) AS offers,
    SUM(fr.hires_count) AS hires,
    ROUND(SUM(fr.recruitment_cost) / NULLIF(SUM(fr.hires_count), 0), 2) AS cost_per_hire,
    ROUND(AVG(fr.avg_time_to_hire_days), 2) AS avg_time_to_hire_days
FROM fact_recruitment fr
JOIN dim_date dd ON dd.date_key = fr.date_key
GROUP BY
    dd.year_number,
    dd.month_number,
    dd.month_name
ORDER BY
    dd.year_number,
    dd.month_number;

-- 6. Performance Distribution
SELECT
    pr.rating_label,
    COUNT(*) AS rating_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS rating_percent
FROM fact_performance fp
JOIN dim_performance_rating pr
    ON pr.performance_rating_key = fp.performance_rating_key
GROUP BY pr.rating_label
ORDER BY rating_count DESC;

-- 7. Training Investment by Category
SELECT
    training_category,
    COUNT(*) AS training_records,
    ROUND(SUM(training_hours), 2) AS total_training_hours,
    ROUND(SUM(training_cost), 2) AS total_training_cost,
    ROUND(AVG(training_hours), 2) AS avg_training_hours
FROM fact_training
GROUP BY training_category
ORDER BY total_training_hours DESC;

-- 8. Attendance Summary by Department
SELECT
    d.department_name,
    SUM(fa.scheduled_days) AS scheduled_days,
    SUM(fa.present_days) AS present_days,
    SUM(fa.leave_days) AS leave_days,
    SUM(fa.absence_days) AS absence_days,
    ROUND(SUM(fa.present_days) * 100.0 / NULLIF(SUM(fa.scheduled_days), 0), 2) AS attendance_percent
FROM fact_attendance fa
JOIN fact_workforce_snapshot fws
    ON fws.employee_key = fa.employee_key
   AND fws.date_key = fa.date_key
JOIN dim_department d
    ON d.department_key = fws.department_key
GROUP BY d.department_name
ORDER BY attendance_percent DESC;

-- 9. Gender Diversity
SELECT
    e.gender,
    COUNT(DISTINCT fws.employee_key) AS active_headcount,
    ROUND(COUNT(DISTINCT fws.employee_key) * 100.0 / SUM(COUNT(DISTINCT fws.employee_key)) OVER (), 2) AS percentage
FROM fact_workforce_snapshot fws
JOIN dim_employee e ON e.employee_key = fws.employee_key
JOIN dim_date dd ON dd.date_key = fws.date_key
WHERE fws.is_active = TRUE
  AND dd.full_date = (
      SELECT MAX(full_date)
      FROM dim_date
  )
GROUP BY e.gender
ORDER BY active_headcount DESC;

-- 10. Manager Workforce Performance
SELECT
    m.manager_name,
    m.manager_level,
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
  AND dd.full_date = (
      SELECT MAX(full_date)
      FROM dim_date
  )
GROUP BY
    m.manager_name,
    m.manager_level
ORDER BY avg_performance_rating DESC;