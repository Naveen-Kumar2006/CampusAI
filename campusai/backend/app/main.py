from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field
from . import models, schemas
from .database import engine, get_db
from .services.chat_service import ask_campus_ai

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CampusAI College Portal API",
    description="College portal API with a RAG-powered AI assistant",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/college")
def get_college_info():
    return {
        "name": "CampusAI Institute of Engineering",
        "location": "Tamil Nadu, India",
        "established": 2001,
        "description": (
            "Empowering the Engineers of Tomorrow "
            "with cutting-edge technology and research."
        ),
        "email": "contact@campusai.edu.in",
        "phone": "+91 9876543210"
    }

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Question asked by the user"
    )


@app.post("/api/chat")
def chat(request: ChatRequest):
    """
    Answer questions using college documents,
    FAISS retrieval, and Gemini.
    """

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    result = ask_campus_ai(message)

    return result
@app.get(
    "/api/departments",
    response_model=List[schemas.Department]
)
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Department)
        .offset(skip)
        .limit(limit)
        .all()
    )

@app.get(
    "/api/departments/{id}",
    response_model=schemas.Department
)
def read_department(
    id: int,
    db: Session = Depends(get_db)
):
    department = (
        db.query(models.Department)
        .filter(models.Department.id == id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department
@app.post(
    "/api/admin/departments",
    response_model=schemas.Department
)
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db)
):
    db_department = models.Department(
        **department.model_dump()
    )

    db.add(db_department)
    db.commit()
    db.refresh(db_department)

    return db_department
@app.get(
    "/api/announcements",
    response_model=List[schemas.Announcement]
)
def read_announcements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Announcement)
        .offset(skip)
        .limit(limit)
        .all()
    )
@app.post(
    "/api/admin/announcements",
    response_model=schemas.Announcement
)
def create_announcement(
    announcement: schemas.AnnouncementCreate,
    db: Session = Depends(get_db)
):
    db_announcement = models.Announcement(
        **announcement.model_dump()
    )

    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)

    return db_announcement
@app.get(
    "/api/events",
    response_model=List[schemas.Event]
)
def read_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Event)
        .offset(skip)
        .limit(limit)
        .all()
    )
@app.post(
    "/api/admin/events",
    response_model=schemas.Event
)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db)
):
    db_event = models.Event(
        **event.model_dump()
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event
@app.get(
    "/api/faculty",
    response_model=List[schemas.Faculty]
)
def read_faculty(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Faculty)
        .offset(skip)
        .limit(limit)
        .all()
    )
@app.get(
    "/api/courses",
    response_model=List[schemas.Course]
)
def read_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Course)
        .offset(skip)
        .limit(limit)
        .all()
    )
class LoginRequest(BaseModel):
    username: str
    password: str
@app.post("/api/auth/login")
def login(request: LoginRequest):

    # DEMO ONLY — replace with secure authentication
    if (
        request.username == "admin"
        and request.password == "admin"
    ):
        return {
            "token": "dummy-admin-token",
            "role": "admin"
        }
    elif request.username.startswith("student"):
        return {
            "token": "dummy-student-token",
            "role": "student"
        }
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )