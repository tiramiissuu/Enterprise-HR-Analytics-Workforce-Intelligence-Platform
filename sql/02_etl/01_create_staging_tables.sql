USE enterprise_hr_dw;

DROP TABLE IF EXISTS stg_employee_master;
DROP TABLE IF EXISTS stg_workforce_monthly;
DROP TABLE IF EXISTS stg_attendance_monthly;
DROP TABLE IF EXISTS stg_performance_monthly;
DROP TABLE IF EXISTS stg_training_monthly;
DROP TABLE IF EXISTS stg_recruitment_monthly;
DROP TABLE IF EXISTS stg_attrition_events;

CREATE TABLE stg_employee_master (
    employee_id VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(20),
    birth_date DATE,
    hire_date DATE,
    employment_status VARCHAR(30),
    department_name VARCHAR(100),
    business_unit VARCHAR(100),
    job_title VARCHAR(100),
    job_level VARCHAR(50),
    job_family VARCHAR(100),
    salary_band_min DECIMAL(12,2),
    salary_band_max DECIMAL(12,2),
    city VARCHAR(80),
    state VARCHAR(80),
    country VARCHAR(80),
    region VARCHAR(80),
    manager_id VARCHAR(20),
    manager_name VARCHAR(120),
    manager_level VARCHAR(50),
    education_level VARCHAR(80)
);

CREATE TABLE stg_workforce_monthly (
    snapshot_date DATE,
    employee_id VARCHAR(20),
    department_name VARCHAR(100),
    job_title VARCHAR(100),
    job_level VARCHAR(50),
    city VARCHAR(80),
    state VARCHAR(80),
    country VARCHAR(80),
    manager_id VARCHAR(20),
    education_level VARCHAR(80),
    salary DECIMAL(12,2),
    tenure_months INT,
    is_active BOOLEAN
);

CREATE TABLE stg_attendance_monthly (
    attendance_date DATE,
    employee_id VARCHAR(20),
    scheduled_days INT,
    present_days INT,
    leave_days INT,
    absence_days INT,
    overtime_hours DECIMAL(8,2)
);

CREATE TABLE stg_performance_monthly (
    performance_date DATE,
    employee_id VARCHAR(20),
    rating_code INT,
    goals_completed INT,
    promotion_flag BOOLEAN,
    bonus_amount DECIMAL(12,2)
);

CREATE TABLE stg_training_monthly (
    training_date DATE,
    employee_id VARCHAR(20),
    training_category VARCHAR(100),
    training_hours DECIMAL(8,2),
    training_cost DECIMAL(12,2),
    completion_status VARCHAR(30)
);

CREATE TABLE stg_recruitment_monthly (
    recruitment_date DATE,
    department_name VARCHAR(100),
    job_title VARCHAR(100),
    job_level VARCHAR(50),
    city VARCHAR(80),
    state VARCHAR(80),
    country VARCHAR(80),
    applications_count INT,
    interviews_count INT,
    offers_count INT,
    hires_count INT,
    recruitment_cost DECIMAL(12,2),
    avg_time_to_hire_days DECIMAL(8,2)
);

CREATE TABLE stg_attrition_events (
    attrition_date DATE,
    employee_id VARCHAR(20),
    department_name VARCHAR(100),
    job_title VARCHAR(100),
    job_level VARCHAR(50),
    city VARCHAR(80),
    state VARCHAR(80),
    country VARCHAR(80),
    attrition_type VARCHAR(50),
    attrition_reason VARCHAR(120),
    final_salary DECIMAL(12,2),
    tenure_months INT
);