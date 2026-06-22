USE enterprise_hr_dw;

DROP TABLE IF EXISTS fact_attrition;
DROP TABLE IF EXISTS fact_recruitment;
DROP TABLE IF EXISTS fact_training;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_attendance;
DROP TABLE IF EXISTS fact_workforce_snapshot;

CREATE TABLE fact_workforce_snapshot (
    snapshot_key INT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL,
    employee_key INT NOT NULL,
    department_key INT NOT NULL,
    job_key INT NOT NULL,
    location_key INT NOT NULL,
    manager_key INT NOT NULL,
    education_key INT NOT NULL,
    salary DECIMAL(12,2) NOT NULL,
    tenure_months INT NOT NULL,
    is_active BOOLEAN NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (employee_key) REFERENCES dim_employee(employee_key),
    FOREIGN KEY (department_key) REFERENCES dim_department(department_key),
    FOREIGN KEY (job_key) REFERENCES dim_job(job_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key),
    FOREIGN KEY (manager_key) REFERENCES dim_manager(manager_key),
    FOREIGN KEY (education_key) REFERENCES dim_education(education_key)
);

CREATE TABLE fact_attendance (
    attendance_key INT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL,
    employee_key INT NOT NULL,
    scheduled_days INT NOT NULL,
    present_days INT NOT NULL,
    leave_days INT NOT NULL,
    absence_days INT NOT NULL,
    overtime_hours DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (employee_key) REFERENCES dim_employee(employee_key)
);

CREATE TABLE fact_performance (
    performance_key INT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL,
    employee_key INT NOT NULL,
    performance_rating_key INT NOT NULL,
    goals_completed INT NOT NULL,
    promotion_flag BOOLEAN NOT NULL,
    bonus_amount DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (employee_key) REFERENCES dim_employee(employee_key),
    FOREIGN KEY (performance_rating_key) REFERENCES dim_performance_rating(performance_rating_key)
);

CREATE TABLE fact_training (
    training_key INT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL,
    employee_key INT NOT NULL,
    training_category VARCHAR(100) NOT NULL,
    training_hours DECIMAL(8,2) NOT NULL,
    training_cost DECIMAL(12,2) NOT NULL,
    completion_status VARCHAR(30) NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (employee_key) REFERENCES dim_employee(employee_key)
);

CREATE TABLE fact_recruitment (
    recruitment_key INT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL,
    department_key INT NOT NULL,
    job_key INT NOT NULL,
    location_key INT NOT NULL,
    applications_count INT NOT NULL,
    interviews_count INT NOT NULL,
    offers_count INT NOT NULL,
    hires_count INT NOT NULL,
    recruitment_cost DECIMAL(12,2) NOT NULL,
    avg_time_to_hire_days DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (department_key) REFERENCES dim_department(department_key),
    FOREIGN KEY (job_key) REFERENCES dim_job(job_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key)
);

CREATE TABLE fact_attrition (
    attrition_key INT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL,
    employee_key INT NOT NULL,
    department_key INT NOT NULL,
    job_key INT NOT NULL,
    location_key INT NOT NULL,
    attrition_type VARCHAR(50) NOT NULL,
    attrition_reason VARCHAR(120) NOT NULL,
    final_salary DECIMAL(12,2) NOT NULL,
    tenure_months INT NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (employee_key) REFERENCES dim_employee(employee_key),
    FOREIGN KEY (department_key) REFERENCES dim_department(department_key),
    FOREIGN KEY (job_key) REFERENCES dim_job(job_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key)
);