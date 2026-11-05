use [Hospital System]

create table Patient (
	Patient_id int primary key,
	Name Varchar(100),
	DOB Date ,
	Ward_id int  not null ,  -- المريض لازم يكون ليه جناح امال هيبقي قاعد في الشارع, موجود كده طبعا في المتطلبات 
	Consultant_id int ,
	FOREIGN KEY (Ward_id) REFERENCES Ward(Ward_id),
    FOREIGN KEY (Consultant_id) REFERENCES Cnosultant(Consultant_id)
)

create table Ward(
	Ward_id int primary key,
	Name Varchar(50),
	Supervis_Nurs_id int  not null   -- لازم يكون ليه ممرضة 
)

-------
alter table Ward 
add constraint FK_Ward_Supervisor foreign key (Supervis_Nurs_id) references Nurses(Nurs_id)

ALTER TABLE Ward 
ADD CONSTRAINT UQ_Ward_Supervis_Nurs UNIQUE (Supervis_Nurs_id);


-------

create table Cnosultant(
	Consultant_id int primary key,
	Name Varchar(30),
)

---- جدول العلاقة المتعددة بين المريض والاستشاري 
create table Examin_Consultant(
	Consultant_id int not null,
	Patient_id int not null ,
	primary key(Consultant_id,Patient_id),  --composit primary key
	----- ربط بقا العلاقة(M:N) دي 
	foreign key(Consultant_id) references Cnosultant(Consultant_id),
	foreign key (Patient_id) references Patient(Patient_id)
)


create table Nurses(
	Nurs_id int primary key,
	Name varchar(20),
	Address Varchar(50),
	Ward_id int not null,   -- لازم يكون ليها جناح كان في المتطلبات بردوا 
	-- ربط علشان اعرف الممرضة دي شغالة فين  في انهي جناح
	foreign key(Ward_id) references Ward(Ward_id)
);




create table Drugs(
	Drug_Code int primary key,
	Recommande_Dossage varchar(50),
)

CREATE TABLE Drug_Brand (
    Drug_Code INT,
    Brand_Name VARCHAR(50) NOT NULL, 
    PRIMARY KEY (Drug_Code, Brand_Name),
    FOREIGN KEY(Drug_Code) REFERENCES Drugs(Drug_Code) 
)

-- اهم جدول --
-- IMPORTANT TABLE -- 
-- =======================================
-- الجدول الي بيربط المريض مع الجرعة مع الممرضة الي بتديلوا جرعة محددة في وقت محددة --
-- =======================================

Create Table N_G_P_D(  -- N Standerd for Nurs , G => Gives , P => Patient , D => Dossage (or Druge)
	Nurs_id int ,
	Drug_Code int ,
	Patient_id int ,
	Dossage varchar(50),
	-- بدل عمل وقت و تاريخ وتخزين كبير غملت تخزين ل الاتنين مع بعض 
	Given_At DATETIME2 DEFAULT SYSUTCDATETIME(),    -- بيسجل وقت النظام تلقائياً بالدقة المتناهية 
	primary key (Nurs_id,Drug_Code,Patient_id),      -- Composit Primary Key
	-------------------------------------------------
	Foreign key(Nurs_id) References Nurses(Nurs_id),
	Foreign key(Drug_Code) References Drugs(Drug_Code),
	Foreign key(Patient_id) References Patient(Patient_id)
	-------------------------------------------------
)                

------------
-- تعديلات --

alter table Patient
alter column Consultant_id int  NOT NULL

----- لاني نسيت عمود اضيفه ل البريمري كي  في الجدول الوسيط ده 
-- فا لازم اضيفه ف هتعمل : 
-- أولاً: حذف المفتاح القديم
ALTER TABLE N_G_P_D
DROP CONSTRAINT Your_Auto_Generated_PK_Name;

---
alter table N_G_P_D 
alter column Given_At Datetime2  not null

-- ثانياً: إنشاء المفتاح الجديد وإضافة الوقت معاه
ALTER TABLE N_G_P_D
ADD CONSTRAINT PK_N_G_P_D 
PRIMARY KEY (Nurs_id, Drug_Code, Patient_id, Given_At);
