import os
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd
from faker import Faker


fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)
np.random.seed(42)


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)


START_DATE = date(2022, 1, 1)
END_DATE = date(2024, 12, 31)
EMPLOYEE_COUNT = 650


DEPARTMENTS = [
    ("Human Resources", "Corporate Services"),
    ("Finance", "Corporate Services"),
    ("Information Technology", "Technology"),
    ("Data Analytics", "Technology"),
    ("Sales", "Commercial"),
    ("Marketing", "Commercial"),
    ("Operations", "Business Operations"),
    ("Customer Support", "Business Operations"),
    ("Legal", "Corporate Services"),
]

JOBS = [
    ("HR Executive", "Associate", "Human Resources", 350000, 650000),
    ("HR Manager", "Manager", "Human Resources", 900000, 1600000),
    ("Financial Analyst", "Associate", "Finance", 450000, 800000),
    ("Finance Manager", "Manager", "Finance", 1000000, 1800000),
    ("Software Engineer", "Associate", "Engineering", 600000, 1200000),
    ("Senior Software Engineer", "Senior", "Engineering", 1200000, 2200000),
    ("Data Analyst", "Associate", "Data", 500000, 1000000),
    ("Data Engineer", "Senior", "Data", 1000000, 2000000),
    ("Sales Executive", "Associate", "Sales", 350000, 900000),
    ("Sales Manager", "Manager", "Sales", 900000, 1800000),
    ("Marketing Specialist", "Associate", "Marketing", 400000, 850000),
    ("Operations Executive", "Associate", "Operations", 350000, 750000),
    ("Operations Manager", "Manager", "Operations", 900000, 1600000),
    ("Customer Support Associate", "Associate", "Support", 300000, 600000),
    ("Legal Associate", "Associate", "Legal", 600000, 1200000),
]

LOCATIONS = [
    ("Pune", "Maharashtra", "India", "West"),
    ("Mumbai", "Maharashtra", "India", "West"),
    ("Bengaluru", "Karnataka", "India", "South"),
    ("Hyderabad", "Telangana", "India", "South"),
    ("Delhi", "Delhi", "India", "North"),
    ("Gurugram", "Haryana", "India", "North"),
    ("Chennai", "Tamil Nadu", "India", "South"),
    ("Kolkata", "West Bengal", "India", "East"),
]

EDUCATION_LEVELS = [
    "Diploma",
    "Bachelor's Degree",
    "Master's Degree",
    "MBA",
    "PhD",
]

MANAGER_LEVELS = ["Manager", "Senior Manager", "Director"]

PERFORMANCE_RATINGS = [
    (1, "Needs Improvement", "Performance is below expectations"),
    (2, "Developing", "Performance meets some expectations"),
    (3, "Meets Expectations", "Performance consistently meets expectations"),
    (4, "Exceeds Expectations", "Performance is above expectations"),
    (5, "Outstanding", "Performance is exceptional"),
]


def month_ends(start_date: date, end_date: date):
    dates = pd.date_range(start=start_date, end=end_date, freq="ME")
    return [d.date() for d in dates]


def random_date(start: date, end: date):
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def build_date_dimension():
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")
    records = []

    for d in dates:
        current = d.date()
        records.append({
            "date_key": int(current.strftime("%Y%m%d")),
            "full_date": current,
            "day_of_month": current.day,
            "month_number": current.month,
            "month_name": current.strftime("%B"),
            "quarter_number": ((current.month - 1) // 3) + 1,
            "year_number": current.year,
            "is_weekend": current.weekday() >= 5,
        })

    return pd.DataFrame(records)


def build_managers():
    records = []

    for i in range(1, 46):
        records.append({
            "manager_id": f"MGR{i:04d}",
            "manager_name": fake.name(),
            "manager_level": random.choice(MANAGER_LEVELS),
        })

    return records


def build_employees(managers):
    records = []

    for i in range(1, EMPLOYEE_COUNT + 1):
        employee_id = f"EMP{i:05d}"
        gender = random.choices(
            ["Male", "Female", "Other"],
            weights=[0.54, 0.44, 0.02],
            k=1
        )[0]

        first_name = fake.first_name_male() if gender == "Male" else fake.first_name_female()
        last_name = fake.last_name()

        hire_date = random_date(date(2016, 1, 1), date(2024, 10, 1))
        birth_date = random_date(date(1970, 1, 1), date(2001, 12, 31))

        department_name, business_unit = random.choice(DEPARTMENTS)
        job_title, job_level, job_family, salary_min, salary_max = random.choice(JOBS)
        city, state, country, region = random.choice(LOCATIONS)
        manager = random.choice(managers)
        education_level = random.choice(EDUCATION_LEVELS)

        salary = round(random.uniform(salary_min, salary_max), 2)

        records.append({
            "employee_id": employee_id,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "birth_date": birth_date,
            "hire_date": hire_date,
            "employment_status": "Active",
            "department_name": department_name,
            "business_unit": business_unit,
            "job_title": job_title,
            "job_level": job_level,
            "job_family": job_family,
            "salary_band_min": salary_min,
            "salary_band_max": salary_max,
            "city": city,
            "state": state,
            "country": country,
            "region": region,
            "manager_id": manager["manager_id"],
            "manager_name": manager["manager_name"],
            "manager_level": manager["manager_level"],
            "education_level": education_level,
            "salary": salary,
        })

    return pd.DataFrame(records)


def build_monthly_facts(employee_df):
    snapshot_records = []
    attendance_records = []
    performance_records = []
    training_records = []
    attrition_records = []

    months = month_ends(START_DATE, END_DATE)
    attrited_employees = set()

    for _, emp in employee_df.iterrows():
        possible_attrition = random.random() < 0.18

        attrition_date = None
        if possible_attrition and emp["hire_date"] < date(2024, 6, 1):
            attrition_date = random_date(max(emp["hire_date"], date(2022, 3, 1)), END_DATE)

        for snapshot_date in months:
            if snapshot_date < emp["hire_date"]:
                continue

            is_active = True
            if attrition_date and snapshot_date >= attrition_date:
                is_active = False

            tenure_months = max(
                0,
                (snapshot_date.year - emp["hire_date"].year) * 12
                + (snapshot_date.month - emp["hire_date"].month)
            )

            snapshot_records.append({
                "snapshot_date": snapshot_date,
                "employee_id": emp["employee_id"],
                "department_name": emp["department_name"],
                "job_title": emp["job_title"],
                "job_level": emp["job_level"],
                "city": emp["city"],
                "state": emp["state"],
                "country": emp["country"],
                "manager_id": emp["manager_id"],
                "education_level": emp["education_level"],
                "salary": emp["salary"],
                "tenure_months": tenure_months,
                "is_active": is_active,
            })

            if is_active:
                scheduled_days = random.randint(20, 23)
                leave_days = random.choices([0, 1, 2, 3, 4], weights=[35, 30, 20, 10, 5], k=1)[0]
                absence_days = random.choices([0, 1, 2], weights=[80, 15, 5], k=1)[0]
                present_days = max(0, scheduled_days - leave_days - absence_days)
                overtime_hours = round(max(0, np.random.normal(8, 5)), 2)

                attendance_records.append({
                    "attendance_date": snapshot_date,
                    "employee_id": emp["employee_id"],
                    "scheduled_days": scheduled_days,
                    "present_days": present_days,
                    "leave_days": leave_days,
                    "absence_days": absence_days,
                    "overtime_hours": overtime_hours,
                })

                if snapshot_date.month in [3, 6, 9, 12]:
                    rating_code = random.choices([1, 2, 3, 4, 5], weights=[5, 12, 48, 25, 10], k=1)[0]
                    goals_completed = random.randint(3, 12)
                    promotion_flag = rating_code >= 4 and random.random() < 0.08
                    bonus_amount = round(emp["salary"] * random.uniform(0.02, 0.12), 2) if rating_code >= 3 else 0

                    performance_records.append({
                        "performance_date": snapshot_date,
                        "employee_id": emp["employee_id"],
                        "rating_code": rating_code,
                        "goals_completed": goals_completed,
                        "promotion_flag": promotion_flag,
                        "bonus_amount": bonus_amount,
                    })

                if random.random() < 0.35:
                    training_category = random.choice([
                        "Leadership",
                        "Technical Skills",
                        "Compliance",
                        "Communication",
                        "Data Literacy",
                        "Cybersecurity",
                    ])

                    training_hours = round(random.uniform(2, 24), 2)
                    training_cost = round(training_hours * random.uniform(600, 2200), 2)

                    training_records.append({
                        "training_date": snapshot_date,
                        "employee_id": emp["employee_id"],
                        "training_category": training_category,
                        "training_hours": training_hours,
                        "training_cost": training_cost,
                        "completion_status": random.choices(
                            ["Completed", "In Progress", "Dropped"],
                            weights=[82, 14, 4],
                            k=1
                        )[0],
                    })

        if attrition_date:
            attrited_employees.add(emp["employee_id"])

            tenure_months = max(
                0,
                (attrition_date.year - emp["hire_date"].year) * 12
                + (attrition_date.month - emp["hire_date"].month)
            )

            attrition_records.append({
                "attrition_date": attrition_date,
                "employee_id": emp["employee_id"],
                "department_name": emp["department_name"],
                "job_title": emp["job_title"],
                "job_level": emp["job_level"],
                "city": emp["city"],
                "state": emp["state"],
                "country": emp["country"],
                "attrition_type": random.choice(["Voluntary", "Involuntary"]),
                "attrition_reason": random.choice([
                    "Career Growth",
                    "Compensation",
                    "Relocation",
                    "Performance",
                    "Role Misfit",
                    "Higher Studies",
                    "Personal Reasons",
                ]),
                "final_salary": emp["salary"],
                "tenure_months": tenure_months,
            })

    employee_df.loc[employee_df["employee_id"].isin(attrited_employees), "employment_status"] = "Inactive"

    return (
        employee_df,
        pd.DataFrame(snapshot_records),
        pd.DataFrame(attendance_records),
        pd.DataFrame(performance_records),
        pd.DataFrame(training_records),
        pd.DataFrame(attrition_records),
    )


def build_recruitment():
    records = []
    months = month_ends(START_DATE, END_DATE)

    for recruitment_date in months:
        for _ in range(random.randint(8, 18)):
            department_name, _ = random.choice(DEPARTMENTS)
            job_title, job_level, _, _, _ = random.choice(JOBS)
            city, state, country, _ = random.choice(LOCATIONS)

            applications = random.randint(30, 420)
            interviews = random.randint(8, min(90, applications))
            offers = random.randint(2, min(25, interviews))
            hires = random.randint(0, min(offers, 8))

            records.append({
                "recruitment_date": recruitment_date,
                "department_name": department_name,
                "job_title": job_title,
                "job_level": job_level,
                "city": city,
                "state": state,
                "country": country,
                "applications_count": applications,
                "interviews_count": interviews,
                "offers_count": offers,
                "hires_count": hires,
                "recruitment_cost": round(random.uniform(25000, 350000), 2),
                "avg_time_to_hire_days": round(random.uniform(14, 75), 2),
            })

    return pd.DataFrame(records)


def main():
    print("Generating HR warehouse source data...")

    managers = build_managers()
    employees = build_employees(managers)

    (
        employee_master,
        workforce_monthly,
        attendance_monthly,
        performance_monthly,
        training_monthly,
        attrition_events,
    ) = build_monthly_facts(employees)

    date_dim = build_date_dimension()
    recruitment_monthly = build_recruitment()
    performance_ratings = pd.DataFrame(
        PERFORMANCE_RATINGS,
        columns=["rating_code", "rating_label", "rating_description"]
    )

    employee_master_export = employee_master.drop(columns=["salary"])

    outputs = {
        "dim_date.csv": date_dim,
        "performance_ratings.csv": performance_ratings,
        "employee_master.csv": employee_master_export,
        "workforce_monthly.csv": workforce_monthly,
        "attendance_monthly.csv": attendance_monthly,
        "performance_monthly.csv": performance_monthly,
        "training_monthly.csv": training_monthly,
        "recruitment_monthly.csv": recruitment_monthly,
        "attrition_events.csv": attrition_events,
    }

    for filename, df in outputs.items():
        path = os.path.join(RAW_DIR, filename)
        df.to_csv(path, index=False)
        print(f"Created {filename}: {len(df):,} rows")

    print("Data generation completed successfully.")


if __name__ == "__main__":
    main()