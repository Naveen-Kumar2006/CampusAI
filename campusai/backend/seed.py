import os
from datetime import date, time
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Departments
        if not db.query(models.Department).first():
            depts = [
                models.Department(name="Artificial Intelligence & Data Science", description="Focuses on AI, ML, and Data Science.", hod="Dr. Alan Turing", faculty_count=15, contact_email="ai@campusai.edu.in"),
                models.Department(name="Computer Science & Engineering", description="Core computer science principles.", hod="Dr. Ada Lovelace", faculty_count=20, contact_email="cse@campusai.edu.in"),
                models.Department(name="Electronics & Communication Engineering", description="Hardware and communication systems.", hod="Dr. Claude Shannon", faculty_count=18, contact_email="ece@campusai.edu.in"),
            ]
            db.add_all(depts)
            db.commit()
            
            # Re-query for IDs
            ai_dept = db.query(models.Department).filter_by(name="Artificial Intelligence & Data Science").first()
            
            # Faculty
            db.add(models.Faculty(name="Dr. Geoffrey Hinton", designation="Professor", qualification="PhD", email="geoffrey@campusai.edu.in", specialization="Deep Learning", department_id=ai_dept.id))
            
            # Courses
            db.add(models.Course(name="Introduction to Machine Learning", code="AI101", description="Basics of ML.", credits=4, department_id=ai_dept.id))
            
            # Announcements
            db.add(models.Announcement(title="Semester Examination Schedule", description="The odd semester exams will begin next month.", date=date.today(), category="Academic", is_important=True))
            db.add(models.Announcement(title="Placement Training", description="Mandatory placement training for final year students.", date=date.today(), category="Placements", is_important=True))
            
            # Events
            db.add(models.Event(title="TechFest 2026", description="Annual technical symposium.", date=date.today(), time=time(9, 0), location="Main Auditorium", organizer="Student Council", category="Cultural"))
            
            db.commit()
            print("Database successfully seeded with dummy data!")
        else:
            print("Data already exists. Skipping seeding.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
