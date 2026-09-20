from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

class CourseBase(BaseModel):
    name: str
    code: str
    description: str
    credits: int
    department_id: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    class Config:
        from_attributes = True

class FacultyBase(BaseModel):
    name: str
    designation: str
    qualification: str
    email: str
    specialization: str
    department_id: int

class FacultyCreate(FacultyBase):
    pass

class Faculty(FacultyBase):
    id: int
    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    description: str
    hod: str
    faculty_count: int
    contact_email: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    faculties: List[Faculty] = []
    courses: List[Course] = []
    class Config:
        from_attributes = True

class AnnouncementBase(BaseModel):
    title: str
    description: str
    date: date
    category: str
    is_important: bool = False

class AnnouncementCreate(AnnouncementBase):
    pass

class Announcement(AnnouncementBase):
    id: int
    class Config:
        from_attributes = True

class EventBase(BaseModel):
    title: str
    description: str
    date: date
    time: time
    location: str
    organizer: str
    category: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    roll_number: str
    email: str
    department_id: int
    year: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    class Config:
        from_attributes = True
