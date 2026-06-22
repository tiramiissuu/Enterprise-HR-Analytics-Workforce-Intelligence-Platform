import os
import sys

import pandas as pd
import mysql.connector


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "230623",
    "database": "enterprise_hr_dw",
}


TABLE_FILES = {
    "stg_employee_master": "employee_master.csv",
    "stg_workforce_monthly": "workforce_monthly.csv",
    "stg_attendance_monthly": "attendance_monthly.csv",
    "stg_performance_monthly": "performance_monthly.csv",
    "stg_training_monthly": "training_monthly.csv",
    "stg_recruitment_monthly": "recruitment_monthly.csv",
    "stg_attrition_events": "attrition_events.csv",
}


def clean_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp,)):
        return value.date()
    return value


def load_csv_to_table(cursor, table_name, file_name):
    file_path = os.path.join(RAW_DIR, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing file: {file_path}")

    df = pd.read_csv(file_path)
    df = df.where(pd.notnull(df), None)

    columns = list(df.columns)
    placeholders = ", ".join(["%s"] * len(columns))
    column_list = ", ".join(columns)

    insert_sql = f"""
        INSERT INTO {table_name} ({column_list})
        VALUES ({placeholders})
    """

    rows = [
        tuple(clean_value(value) for value in row)
        for row in df.itertuples(index=False, name=None)
    ]

    cursor.execute(f"TRUNCATE TABLE {table_name}")

    if rows:
        cursor.executemany(insert_sql, rows)

    print(f"Loaded {table_name}: {len(rows):,} rows")


def main():
    if DB_CONFIG["password"] == "YOUR_MYSQL_PASSWORD":
        print("ERROR: Update YOUR_MYSQL_PASSWORD in src/etl/load_to_mysql.py first.")
        sys.exit(1)

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        for table_name, file_name in TABLE_FILES.items():
            load_csv_to_table(cursor, table_name, file_name)

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
        print("All staging tables loaded successfully.")

    except Exception as error:
        connection.rollback()
        print(f"ETL load failed: {error}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()