from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class DanceClassBase(BaseModel):
    name: str
    description: Optional[str] = None
    level: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    image_url: Optional[str] = None


class DanceClassCreate(DanceClassBase):
    pass


class DanceClass(DanceClassBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TeacherBase(BaseModel):
    name: str
    bio: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[int] = None
    photo_url: Optional[str] = None


class TeacherCreate(TeacherBase):
    pass


class Teacher(TeacherBase):
    id: int

    class Config:
        from_attributes = True


class ScheduleBase(BaseModel):
    dance_class_id: int
    teacher_id: int
    day_of_week: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    room: Optional[str] = None


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    id: int

    class Config:
        from_attributes = True


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    level: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RegistrationBase(BaseModel):
    student_id: int
    dance_class_id: int


class RegistrationCreate(RegistrationBase):
    pass


class Registration(RegistrationBase):
    id: int
    registration_date: datetime
    status: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class NewsBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True