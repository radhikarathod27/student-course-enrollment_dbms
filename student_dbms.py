import mysql.connector
import random
from datetime import datetime, timedelta

# -------------------------------
# MYSQL CONNECTION
# -------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aarohi@2005",      # change if needed
    auth_plugin="mysql_native_password"
)
cursor = conn.cursor()

# -------------------------------
# CREATE DATABASE
# -------------------------------
cursor.execute("CREATE DATABASE IF NOT EXISTS schema_demo")
cursor.execute("USE schema_demo")

# -------------------------------
# DROP TABLES (CLEAN RUN)
# -------------------------------
cursor.execute("DROP TABLE IF EXISTS Enrollment")
cursor.execute("DROP TABLE IF EXISTS Course")
cursor.execute("DROP TABLE IF EXISTS Student")

# -------------------------------
# STUDENT TABLE
# -------------------------------
cursor.execute("""
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Age INT CHECK (Age >= 18),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# -------------------------------
# COURSE TABLE
# -------------------------------
cursor.execute("""
CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL,
    Credits INT CHECK (Credits > 0)
)
""")

# -------------------------------
# ENROLLMENT TABLE
# -------------------------------
cursor.execute("""
CREATE TABLE Enrollment (
    EnrollmentID INT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    EnrollDate DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
)
""")

# -------------------------------
# DATA FOR GENERATION
# -------------------------------
first_names = ["Rahul","Amit","Sneha","Priya","Anjali","Ravi","Kiran","Neha","Pooja","Arjun"]
last_names = ["Sharma","Reddy","Patel","Singh","Verma","Gupta","Iyer","Rao"]

course_names = [
    "DBMS","Python","Data Structures","Operating Systems",
    "Computer Networks","AI","ML","Web Development","Cloud Computing","Cyber Security"
]

# -------------------------------
# INSERT COURSES (10)
# -------------------------------
for cid, cname in enumerate(course_names, start=1):
    cursor.execute(
        "INSERT INTO Course VALUES (%s,%s,%s)",
        (cid, cname, random.randint(2, 5))
    )

# -------------------------------
# INSERT 1000 STUDENTS
# -------------------------------
for sid in range(1, 1001):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"student{sid}@college.com"
    age = random.randint(18, 25)

    cursor.execute("""
        INSERT INTO Student
        (StudentID, Name, Email, Age)
        VALUES (%s,%s,%s,%s)
    """, (sid, name, email, age))

# -------------------------------
# INSERT 1000 ENROLLMENTS
# -------------------------------
for eid in range(1, 1001):
    enroll_date = datetime.now() - timedelta(days=random.randint(1, 365))

    cursor.execute("""
        INSERT INTO Enrollment
        (EnrollmentID, StudentID, CourseID, EnrollDate)
        VALUES (%s,%s,%s,%s)
    """, (
        eid,
        eid,                        # one student → one enrollment
        random.randint(1, 10),
        enroll_date.date()
    ))

# -------------------------------
# CREATE VIEW
# -------------------------------
cursor.execute("""
CREATE OR REPLACE VIEW Student_Enrollment_View AS
SELECT
    s.StudentID,
    s.Name AS StudentName,
    c.CourseName,
    e.EnrollDate
FROM Student s
JOIN Enrollment e ON s.StudentID = e.StudentID
JOIN Course c ON c.CourseID = e.CourseID
""")

# -------------------------------
# CREATE INDEX
# -------------------------------
cursor.execute("CREATE INDEX idx_student_name ON Student(Name)")

conn.commit()

# -------------------------------
# VERIFY COUNTS
# -------------------------------
cursor.execute("SELECT COUNT(*) FROM Student")
print("Students:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM Enrollment")
print("Enrollments:", cursor.fetchone()[0])

cursor.close()
conn.close()

print("✅ 1000 synthetic Student–Course–Enrollment records created successfully")


