from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models
from . import schemas
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Функции для новостей
def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.News).filter(models.News.is_published == True)\
        .order_by(models.News.created_at.desc())\
        .offset(skip).limit(limit).all()

def get_news_item(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()

def create_news(db: Session, news: schemas.NewsCreate, author_id: int):
    db_news = models.News(**news.dict(), author_id=author_id)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def get_dance_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DanceClass).filter(models.DanceClass.is_active == True).offset(skip).limit(limit).all()

def get_dance_class(db: Session, dance_class_id: int):
    return db.query(models.DanceClass).filter(models.DanceClass.id == dance_class_id).first()

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).filter(models.Teacher.is_active == True).offset(skip).limit(limit).all()

def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()

def get_schedule(db: Session):
    return db.query(models.Schedule).all()

def get_class_schedule(db: Session, dance_class_id: int):
    return db.query(models.Schedule).filter(models.Schedule.dance_class_id == dance_class_id).all()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

def create_registration(db: Session, registration: schemas.RegistrationCreate):
    db_registration = models.Registration(**registration.dict())
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration

def get_registrations_by_student(db: Session, student_id: int):
    return db.query(models.Registration).filter(models.Registration.student_id == student_id).all()