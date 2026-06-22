USE enterprise_hr_dw;

DROP TABLE IF EXISTS dim_performance_rating;
DROP TABLE IF EXISTS dim_education;
DROP TABLE IF EXISTS dim_manager;
DROP TABLE IF EXISTS dim_location;
DROP TABLE IF EXISTS dim_job;
DROP TABLE IF EXISTS dim_department;
DROP TABLE IF EXISTS dim_employee;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_of_month INT NOT NULL,
    month_number INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter_number INT NOT NULL,
    year_number INT NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

CREATE TABLE dim_employee (
    employee_key INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    hire_date DATE NOT NULL,
    employment_status VARCHAR(30) NOT NULL
);

CREATE TABLE dim_department (
    department_key INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    business_unit VARCHAR(100) NOT NULL
);

CREATE TABLE dim_job (
    job_key INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    job_level VARCHAR(50) NOT NULL,
    job_family VARCHAR(100) NOT NULL,
    salary_band_min DECIMAL(12,2) NOT NULL,
    salary_band_max DECIMAL(12,2) NOT NULL,
    UNIQUE(job_title, job_level)
);

CREATE TABLE dim_location (
    location_key INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(80) NOT NULL,
    state VARCHAR(80) NOT NULL,
    country VARCHAR(80) NOT NULL,
    region VARCHAR(80) NOT NULL,
    UNIQUE(city, state, country)
);

CREATE TABLE dim_manager (
    manager_key INT AUTO_INCREMENT PRIMARY KEY,
    manager_id VARCHAR(20) NOT NULL UNIQUE,
    manager_name VARCHAR(120) NOT NULL,
    manager_level VARCHAR(50) NOT NULL
);

CREATE TABLE dim_education (
    education_key INT AUTO_INCREMENT PRIMARY KEY,
    education_level VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE dim_performance_rating (
    performance_rating_key INT AUTO_INCREMENT PRIMARY KEY,
    rating_code INT NOT NULL UNIQUE,
    rating_label VARCHAR(80) NOT NULL,
    rating_description VARCHAR(255) NOT NULL
);