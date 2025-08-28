from fastapi import FastAPI, Request, Depends, HTTPException, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from .database import SessionLocal, engine, get_db
from . import models, crud, schemas
from .dependencies import get_current_user, get_current_admin_user
import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dance_school.db")

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dance School", version="1.0.0")

# Setup templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Frontend routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    classes = crud.get_dance_classes(db)
    teachers = crud.get_teachers(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "classes": classes,
        "teachers": teachers
    })


@app.get("/classes", response_class=HTMLResponse)
async def read_classes(request: Request, db: Session = Depends(get_db)):
    classes = crud.get_dance_classes(db)
    return templates.TemplateResponse("classes.html", {
        "request": request,
        "classes": classes
    })


@app.get("/teachers", response_class=HTMLResponse)
async def read_teachers(request: Request, db: Session = Depends(get_db)):
    teachers = crud.get_teachers(db)
    return templates.TemplateResponse("teachers.html", {
        "request": request,
        "teachers": teachers
    })


@app.get("/schedule", response_class=HTMLResponse)
async def read_schedule(request: Request, db: Session = Depends(get_db)):
    schedule = crud.get_schedule(db)
    classes = crud.get_dance_classes(db)
    teachers = crud.get_teachers(db)

    class_map = {cls.id: cls.name for cls in classes}
    teacher_map = {teacher.id: teacher.name for teacher in teachers}

    return templates.TemplateResponse("schedule.html", {
        "request": request,
        "schedule": schedule,
        "class_map": class_map,
        "teacher_map": teacher_map
    })


@app.get("/contacts", response_class=HTMLResponse)
async def read_contacts(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})


@app.get("/registration", response_class=HTMLResponse)
async def registration_form(request: Request, db: Session = Depends(get_db)):
    classes = crud.get_dance_classes(db)
    return templates.TemplateResponse("registration.html", {
        "request": request,
        "classes": classes
    })


@app.post("/registration", response_class=HTMLResponse)
async def create_registration(
        request: Request,
        name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        level: str = Form(...),
        dance_class_id: int = Form(...),
        db: Session = Depends(get_db)
):
    student = crud.get_student_by_email(db, email)
    if not student:
        student_data = schemas.StudentCreate(
            name=name,
            email=email,
            phone=phone,
            level=level
        )
        student = crud.create_student(db, student_data)

    registration_data = schemas.RegistrationCreate(
        student_id=student.id,
        dance_class_id=dance_class_id
    )
    crud.create_registration(db, registration_data)

    return RedirectResponse(url="/registration/success", status_code=303)


@app.get("/registration/success", response_class=HTMLResponse)
async def registration_success(request: Request):
    return templates.TemplateResponse("registration_success.html", {"request": request})


# API endpoints
@app.get("/api/classes", response_model=List[schemas.DanceClass])
def read_classes_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    classes = crud.get_dance_classes(db, skip=skip, limit=limit)
    return classes


@app.get("/api/teachers", response_model=List[schemas.Teacher])
def read_teachers_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teachers = crud.get_teachers(db, skip=skip, limit=limit)
    return teachers


@app.post("/api/students/", response_model=schemas.Student)
def create_student_api(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db, student)


@app.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


# Admin routes
@app.get("/admin")
async def admin_panel(
        request: Request,
        current_user: models.User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    classes = crud.get_dance_classes(db)
    teachers = crud.get_teachers(db)
    students = db.query(models.Student).all()
    registrations = db.query(models.Registration).all()

    return templates.TemplateResponse("admin.html", {
        "request": request,
        "user": current_user,
        "classes": classes,
        "teachers": teachers,
        "students": students,
        "registrations": registrations
    })


# News routes
@app.get("/news")
async def news_list(
        request: Request,
        db: Session = Depends(get_db)
):
    news_items = crud.get_news(db)
    return templates.TemplateResponse("news.html", {
        "request": request,
        "news_items": news_items
    })


@app.get("/news/{news_id}")
async def news_detail(
        request: Request,
        news_id: int,
        db: Session = Depends(get_db)
):
    news_item = crud.get_news_item(db, news_id)
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")

    return templates.TemplateResponse("news_detail.html", {
        "request": request,
        "news_item": news_item
    })


# API endpoints для новостей
@app.get("/api/news", response_model=List[schemas.News])
def get_news_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_news(db, skip=skip, limit=limit)


@app.post("/api/news", response_model=schemas.News)
def create_news_api(
        news: schemas.NewsCreate,
        current_user: models.User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    return crud.create_news(db, news, current_user.id)

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/gallery", response_class=HTMLResponse)
async def gallery_page(request: Request, db: Session = Depends(get_db)):
    # Здесь можно добавить логику для галереи
    return templates.TemplateResponse("gallery.html", {"request": request})

@app.get("/prices", response_class=HTMLResponse)
async def prices_page(request: Request, db: Session = Depends(get_db)):
    classes = crud.get_dance_classes(db)
    return templates.TemplateResponse("prices.html", {
        "request": request,
        "classes": classes
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@app.post("/contact")
async def contact_form(
        request: Request,
        name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(None),
        message: str = Form(...)
):
    # Здесь можно добавить логику обработки формы (отправка email, сохранение в БД и т.д.)
    print(f"Новое сообщение от {name} ({email}): {message}")

    # Пока просто редиректим на страницу благодарности
    return RedirectResponse(url="/contact/success", status_code=303)


@app.get("/contact/success")
async def contact_success(request: Request):
    return templates.TemplateResponse("contact_success.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)