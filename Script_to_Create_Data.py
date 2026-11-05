import os
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

fake = Faker()

# إنشاء الفولدر المخصص
output_dir = "hospital_csv_data"
os.makedirs(output_dir, exist_ok=True)

print("⏳ جاري توليد البيانات الاصطناعية بنجاح...")

# 1. Consultants
NUM_CONSULTANTS = 50
consultants = [
    {"Consultant_id": i, "Name": f"Dr. {fake.name()}"}
    for i in range(1, NUM_CONSULTANTS + 1)
]
pd.DataFrame(consultants).to_csv(f"{output_dir}/Consultant.csv", index=False)

# 2. Drugs & Brands
NUM_DRUGS = 200
dosages = ["500mg", "250mg", "100mg", "10mg/ml", "2 tablets/day", "1 injection/12h"]
drugs, drug_brands = [], []

for i in range(1, NUM_DRUGS + 1):
    drug_code = 1000 + i
    drugs.append(
        {"Drug_Code": drug_code, "Recommande_Dossage": random.choice(dosages)}
    )
    for _ in range(random.randint(1, 3)):
        drug_brands.append(
            {"Drug_Code": drug_code, "Brand_Name": f"{fake.company()} Pharm"}
        )

pd.DataFrame(drugs).to_csv(f"{output_dir}/Drugs.csv", index=False)
pd.DataFrame(drug_brands).drop_duplicates().to_csv(
    f"{output_dir}/Drug_Brand.csv", index=False
)

# 3. Ward & Nurses
NUM_WARDS = 20
NUM_NURSES = 100

nurses = [
    {
        "Nurs_id": i,
        "Name": fake.name(),
        "Address": fake.city(),
        "Ward_id": ((i - 1) % NUM_WARDS) + 1,
    }
    for i in range(1, NUM_NURSES + 1)
]

# تخصيص الممرضات من 1 إلى 20 كمشرفات فريدات على الأجنحة (1:1)
wards = [
    {
        "Ward_id": w_id,
        "Name": f"Ward {w_id} - {fake.job()[:15]}",
        "Supervis_Nurs_id": w_id,
    }
    for w_id in range(1, NUM_WARDS + 1)
]

pd.DataFrame(wards).to_csv(f"{output_dir}/Ward.csv", index=False)
pd.DataFrame(nurses).to_csv(f"{output_dir}/Nurses.csv", index=False)

# 4. Patient (5,000 مريض)
NUM_PATIENTS = 5000
patients = [
    {
        "Patient_id": i,
        "Name": fake.name(),
        "DOB": fake.date_of_birth(
            minimum_age=1, maximum_age=85
        ).strftime("%Y-%m-%d"),
        "Ward_id": random.randint(1, NUM_WARDS),
        "Consultant_id": random.randint(1, NUM_CONSULTANTS),
    }
    for i in range(1, NUM_PATIENTS + 1)
]
pd.DataFrame(patients).to_csv(f"{output_dir}/Patient.csv", index=False)

# 5. Examin_Consultant
examinations = []
for p_id in range(1, NUM_PATIENTS + 1):
    c_ids = random.sample(
        range(1, NUM_CONSULTANTS + 1), k=random.randint(1, 3)
    )
    for c_id in c_ids:
        examinations.append({"Consultant_id": c_id, "Patient_id": p_id})

pd.DataFrame(examinations).drop_duplicates().to_csv(
    f"{output_dir}/Examin_Consultant.csv", index=False
)

# 6. N_G_P_D (100,000 سجل حركة أدوية)
NUM_LOGS = 100000
start_date = datetime.now() - timedelta(days=90)
ngpd_logs = []

for _ in range(NUM_LOGS):
    given_time = start_date + timedelta(
        minutes=random.randint(0, 90 * 24 * 60)
    )
    ngpd_logs.append(
        {
            "Nurs_id": random.randint(1, NUM_NURSES),
            "Drug_Code": 1000 + random.randint(1, NUM_DRUGS),
            "Patient_id": random.randint(1, NUM_PATIENTS),
            "Dossage": random.choice(dosages),
            "Given_At": given_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        }
    )

pd.DataFrame(ngpd_logs).to_csv(f"{output_dir}/N_G_P_D.csv", index=False)

print(f"✨ تم توليد كافة البيانات بنجاح داخل فولدر: {output_dir}")