import os
import urllib
import pandas as pd
from sqlalchemy import create_engine, text

# ==========================================
# 1. إعدادات الاتصال بـ SQL Server
# ==========================================
# ⚠️ غير اسم السيرفر هنا باسم سيرفرك (مثلاً: localhost أو . أو اسم جهازك)
SERVER_NAME = r"."  
DATABASE_NAME = "Hospital System"

# بناء جملة الاتصال باستخدام Windows Authentication
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# ==========================================
# 2. قائمة الجداول والملفات بالترتيب
# ==========================================
output_dir = "hospital_csv_data"

tables_files = [
    ("Consultant", "Consultant.csv"),
    ("Drugs", "Drugs.csv"),
    ("Drug_Brand", "Drug_Brand.csv"),
    ("Ward", "Ward.csv"),
    ("Nurses", "Nurses.csv"),
    ("Patient", "Patient.csv"),
    ("Examin_Consultant", "Examin_Consultant.csv"),
    ("N_G_P_D", "N_G_P_D.csv")
]

print("🚀 جاري بدء عملية شحن البيانات (Data Ingestion)...")

with engine.begin() as connection:
    # أ) إيقاف قيود المفاتيح الأجنبية مؤقتاً لتسريع وتسهيل الرفع
    print("⏳ إيقاف قيود الـ Foreign Keys مؤقتاً...")
    connection.execute(text("EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL';"))

    # ب) قراءة كل ملف CSV وشحنه للجدول المناظر
    for table_name, file_name in tables_files:
        file_path = os.path.join(output_dir, file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            
            # رفع البيانات للجدول
            df.to_sql(
                name=table_name,
                con=connection,
                if_exists='append',  # إضافة البيانات للجدول الموجود
                index=False,
                chunksize=5000       # رفع البيانات على دفعات لتسريع العملية
            )
            print(f"  ✅ تم شحن {len(df):,} صف إلى جدول [{table_name}] بنجاح.")
        else:
            print(f"  ⚠️ الملف {file_name} غير موجود!")

    # ج) إعادة تفعيل القيود مرة أخرى والتأكد من سلامتها
    print("⏳ إعادة تفعيل قيود الـ Foreign Keys...")
    connection.execute(text("EXEC sp_MSforeachtable 'ALTER TABLE ? WITH CHECK CHECK CONSTRAINT ALL';"))

print("\n🎉 تمت عملية رفع البيانات للـ 8 جداول بنجاح تام!")