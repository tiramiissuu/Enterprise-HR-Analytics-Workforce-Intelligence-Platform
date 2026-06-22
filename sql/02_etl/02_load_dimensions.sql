USE enterprise_hr_dw;

INSERT INTO dim_date (
    date_key,
    full_date,
    day_of_month,
    month_number,
    month_name,
    quarter_number,
    year_number,
    is_weekend
)
SELECT DISTINCT
    CAST(DATE_FORMAT(full_date, '%Y%m%d') AS UNSIGNED),
    full_date,
    DAY(full_date),
    MONTH(full_date),
    MONTHNAME(full_date),
    QUARTER(full_date),
    YEAR(full_date),
    CASE WHEN DAYOFWEEK(full_date) IN (1, 7) THEN TRUE ELSE FALSE END
FROM (
    SELECT snapshot_date AS full_date FROM stg_workforce_monthly
    UNION
    SELECT attendance_date FROM stg_attendance_monthly
    UNION
    SELECT performance_date FROM stg_performance_monthly
    UNION
    SELECT training_date FROM stg_training_monthly
    UNION
    SELECT recruitment_date FROM stg_recruitment_monthly
    UNION
    SELECT attrition_date FROM stg_attrition_events
) d
WHERE full_date IS NOT NULL
ON DUPLICATE KEY UPDATE
    full_date = VALUES(full_date);

INSERT INTO dim_employee (
    employee_id,
    first_name,
    last_name,
    gender,
    birth_date,
    hire_date,
    employment_status
)
SELECT DISTINCT
    employee_id,
    first_name,
    last_name,
    gender,
    birth_date,
    hire_date,
    employment_status
FROM stg_employee_master
ON DUPLICATE KEY UPDATE
    first_name = VALUES(first_name),
    last_name = VALUES(last_name),
    gender = VALUES(gender),
    birth_date = VALUES(birth_date),
    hire_date = VALUES(hire_date),
    employment_status = VALUES(employment_status);

INSERT INTO dim_department (
    department_name,
    business_unit
)
SELECT DISTINCT
    department_name,
    business_unit
FROM stg_employee_master
WHERE department_name IS NOT NULL
ON DUPLICATE KEY UPDATE
    business_unit = VALUES(business_unit);

INSERT INTO dim_job (
    job_title,
    job_level,
    job_family,
    salary_band_min,
    salary_band_max
)
SELECT DISTINCT
    job_title,
    job_level,
    job_family,
    salary_band_min,
    salary_band_max
FROM stg_employee_master
WHERE job_title IS NOT NULL
ON DUPLICATE KEY UPDATE
    job_family = VALUES(job_family),
    salary_band_min = VALUES(salary_band_min),
    salary_band_max = VALUES(salary_band_max);

INSERT INTO dim_location (
    city,
    state,
    country,
    region
)
SELECT DISTINCT
    city,
    state,
    country,
    region
FROM stg_employee_master
WHERE city IS NOT NULL
ON DUPLICATE KEY UPDATE
    region = VALUES(region);

INSERT INTO dim_manager (
    manager_id,
    manager_name,
    manager_level
)
SELECT DISTINCT
    manager_id,
    manager_name,
    manager_level
FROM stg_employee_master
WHERE manager_id IS NOT NULL
ON DUPLICATE KEY UPDATE
    manager_name = VALUES(manager_name),
    manager_level = VALUES(manager_level);

INSERT INTO dim_education (
    education_level
)
SELECT DISTINCT
    education_level
FROM stg_employee_master
WHERE education_level IS NOT NULL
ON DUPLICATE KEY UPDATE
    education_level = VALUES(education_level);

INSERT INTO dim_performance_rating (
    rating_code,
    rating_label,
    rating_description
)
VALUES
    (1, 'Needs Improvement', 'Performance is below expectations'),
    (2, 'Developing', 'Performance meets some expectations'),
    (3, 'Meets Expectations', 'Performance consistently meets expectations'),
    (4, 'Exceeds Expectations', 'Performance is above expectations'),
    (5, 'Outstanding', 'Performance is exceptional')
ON DUPLICATE KEY UPDATE
    rating_label = VALUES(rating_label),
    rating_description = VALUES(rating_description);