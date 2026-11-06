# 🏥 Hospital Management System Database & ETL Pipeline

## 📌 Overview
A comprehensive relational database architecture designed for a hospital management system, coupled with a fully automated Python ETL pipeline. This project demonstrates end-to-end data engineering, from conceptual database design (ERD) to generating and ingesting over 115,000 synthetic records while strictly maintaining referential integrity.

## 🚀 Key Features
- **Robust Architecture:** Designed 8 normalized tables with complex relationships (1:1, 1:N, M:N) and strict constraints (e.g., `UNIQUE` index for Ward Supervision).
- **Automated Data Ingestion (ETL):** Built a custom Python script using `Pandas`, `SQLAlchemy`, and `Faker` to generate and load realistic synthetic healthcare data.
- **Large-Scale Processing:** Successfully generated and loaded **115,000+ records** (including 5,000 patients and 100,000 drug transaction logs) into the database in seconds.
- **Advanced SQL Analytics:** Developed advanced T-SQL queries (including Window Functions like `RANK()` and complex `JOIN`s) to extract meaningful business insights, such as top drug consumption.

## 🛠️ Tech Stack
- **Database:** Microsoft SQL Server, T-SQL, SSMS
- **Programming Language:** Python
- **Libraries:** Pandas, SQLAlchemy, PyODBC, Faker
- **Core Concepts:** Relational Database Design, Data Pipeline (ETL), Referential Integrity, Conceptual & Logical Mapping

## 📂 Database Schema (Core Tables)
`Patient` | `Ward` | `Consultant` | `Nurses` | `Drug` | `Drug_Brand` | `Examin_Consultant` | `N_G_P_D` (Drug Movement)

## ⚙️ How to Explore This Project
1. **ERD & Mapping:** Check the attached diagrams to understand the conceptual and logical design of the database.
2. **SQL Scripts:** Review the T-SQL scripts used for table creation and advanced querying.
3. **Python Pipeline:** Explore the Python script to see how the synthetic data was generated and ingested into SQL Server using `SQLAlchemy`.
