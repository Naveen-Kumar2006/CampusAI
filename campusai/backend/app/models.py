from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Date, Time, Float
from sqlalchemy.orm import relationship
from .database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    hod = Column(String)
    faculty_count = Column(Integer)
    contact_email = Column(String)
    
    faculties = relationship("Faculty", back_populates="department")
    courses = relationship("Course", back_populates="department")

class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    designation = Column(String)
    qualification = Column(String)
    email = Column(String, unique=True, index=True)
    specialization = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    department = relationship("Department", back_populates="faculties")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(Text)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    department = relationship("Department", back_populates="courses")

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    date = Column(Date)
    category = Column(String)
    is_important = Column(Boolean, default=False)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    date = Column(Date)
    time = Column(Time)
    location = Column(String)
    organizer = Column(String)
    category = Column(String)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    roll_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    year = Column(Integer)
