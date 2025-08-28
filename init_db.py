from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from passlib.context import CryptContext
from datetime import time

# Создаем экземпляр CryptContext для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def init_db():
    # Создаем таблицы
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Очищаем существующие данные (для тестов)
        db.query(models.Registration).delete()
        db.query(models.Student).delete()
        db.query(models.Schedule).delete()
        db.query(models.DanceClass).delete()
        db.query(models.Teacher).delete()
        db.query(models.News).delete()
        db.query(models.User).delete()

        # Добавляем тестовые классы
        classes = [
            models.DanceClass(
                name="Бальные танцы",
                description="Изучение классических бальных танцев: вальс, танго, фокстрот. Идеально для начинающих и продолжающих. Развиваем грацию, пластику и чувство ритма.",
                level="Начинающий",
                duration=60,
                price=1500,
                image_url="/static/images/ballroom.jpg"
            ),
            models.DanceClass(
                name="Хип-хоп",
                description="Современные уличные танцы в стиле хип-хоп. Динамичные движения, работа над стилем и импровизация. Для тех, кто любит современную музыку и хочет научиться двигаться уверенно.",
                level="Средний",
                duration=90,
                price=2000,
                image_url="/static/images/hiphop.jpg"
            ),
            models.DanceClass(
                name="Балет",
                description="Классическая хореография и балетная техника. Постановка корпуса, работа у станка, развитие гибкости и силы. Для детей и взрослых с любым уровнем подготовки.",
                level="Продвинутый",
                duration=120,
                price=2500,
                image_url="/static/images/ballet.jpg"
            ),
            models.DanceClass(
                name="Сальса",
                description="Зажигательные латиноамериканские танцы. Изучение базовых шагов, парные комбинации и вращения. Отличный способ познакомиться с латинской культурой и найти новых друзей.",
                level="Начинающий",
                duration=60,
                price=1700,
                image_url="/static/images/salsa.jpg"
            ),
            models.DanceClass(
                name="Танго",
                description="Страстный аргентинский танец. Изучение близкого контакта, импровизации и музыкальности. Для романтичных натур и тех, кто хочет погрузиться в атмосферу Аргентины.",
                level="Средний",
                duration=75,
                price=2200,
                image_url="/static/images/tango.jpg"
            ),
            models.DanceClass(
                name="Contemporary",
                description="Современный танец, сочетающий элементы классического балета, джаза и модерна. Развитие выразительности тела и эмоциональной подачи.",
                level="Продвинутый",
                duration=90,
                price=2300,
                image_url="/static/images/contemporary.jpg"
            )
        ]

        for dance_class in classes:
            db.add(dance_class)

        # Добавляем преподавателей
        teachers = [
            models.Teacher(
                name="Анна Иванова",
                bio="Профессиональная балерина с 15-летним опытом, выпускница Академии русского балета им. Вагановой. Участница международных конкурсов и фестивалей. Специализируется на классическом балете и contemporary.",
                specialization="Балет, Contemporary",
                experience=15,
                photo_url="/static/images/teacher1.jpg"
            ),
            models.Teacher(
                name="Михаил Петров",
                bio="Чемпион России по бальным танцам, международный инструктор IDSF. Тренер победителей всероссийских конкурсов. Специализируется на европейской и латиноамериканской программах.",
                specialization="Бальные танцы",
                experience=10,
                photo_url="/static/images/teacher2.jpg"
            ),
            models.Teacher(
                name="Елена Смирнова",
                bio="Профессиональный хореограф в стиле хип-хоп, участница международных баттлов. Работала с известными артистами российской эстрады. Специализируется на уличных танцах и современных направлениях.",
                specialization="Хип-хоп, Уличные танцы",
                experience=8,
                photo_url="/static/images/teacher3.jpg"
            ),
            models.Teacher(
                name="Карлос Родригес",
                bio="Носитель латиноамериканской культуры, профессиональный танцор сальсы и бачаты. Уроженец Кубы, с 10-летним опытом преподавания. Специализируется на латинских танцах и социальных вечеринках.",
                specialization="Сальса, Бачата",
                experience=12,
                photo_url="/static/images/teacher4.jpg"
            ),
            models.Teacher(
                name="Ольга Козлова",
                bio="Сертифицированный инструктор аргентинского танго, участница международных фестивалей в Буэнос-Айресе. Специализируется на технике ведения и импровизации в танго.",
                specialization="Аргентинское танго",
                experience=9,
                photo_url="/static/images/teacher5.jpg"
            )
        ]

        for teacher in teachers:
            db.add(teacher)

        # Добавляем расписание
        schedule = [
            # Понедельник
            models.Schedule(dance_class_id=1, teacher_id=2, day_of_week="Понедельник", start_time="18:00",
                            end_time="19:00", room="Зал 1"),
            models.Schedule(dance_class_id=4, teacher_id=4, day_of_week="Понедельник", start_time="19:00",
                            end_time="20:00", room="Зал 2"),
            models.Schedule(dance_class_id=2, teacher_id=3, day_of_week="Понедельник", start_time="20:00",
                            end_time="21:30", room="Зал 1"),

            # Вторник
            models.Schedule(dance_class_id=3, teacher_id=1, day_of_week="Вторник", start_time="17:00", end_time="19:00",
                            room="Зал 1"),
            models.Schedule(dance_class_id=5, teacher_id=5, day_of_week="Вторник", start_time="19:00", end_time="20:15",
                            room="Зал 2"),
            models.Schedule(dance_class_id=6, teacher_id=1, day_of_week="Вторник", start_time="20:30", end_time="22:00",
                            room="Зал 1"),

            # Среда
            models.Schedule(dance_class_id=1, teacher_id=2, day_of_week="Среда", start_time="18:00", end_time="19:00",
                            room="Зал 1"),
            models.Schedule(dance_class_id=4, teacher_id=4, day_of_week="Среда", start_time="19:00", end_time="20:00",
                            room="Зал 2"),
            models.Schedule(dance_class_id=2, teacher_id=3, day_of_week="Среда", start_time="20:00", end_time="21:30",
                            room="Зал 1"),

            # Четверг
            models.Schedule(dance_class_id=3, teacher_id=1, day_of_week="Четверг", start_time="17:00", end_time="19:00",
                            room="Зал 1"),
            models.Schedule(dance_class_id=5, teacher_id=5, day_of_week="Четверг", start_time="19:00", end_time="20:15",
                            room="Зал 2"),
            models.Schedule(dance_class_id=6, teacher_id=1, day_of_week="Четверг", start_time="20:30", end_time="22:00",
                            room="Зал 1"),

            # Пятница
            models.Schedule(dance_class_id=1, teacher_id=2, day_of_week="Пятница", start_time="18:00", end_time="19:00",
                            room="Зал 1"),
            models.Schedule(dance_class_id=4, teacher_id=4, day_of_week="Пятница", start_time="19:00", end_time="20:00",
                            room="Зал 2"),

            # Суббота
            models.Schedule(dance_class_id=2, teacher_id=3, day_of_week="Суббота", start_time="11:00", end_time="12:30",
                            room="Зал 1"),
            models.Schedule(dance_class_id=3, teacher_id=1, day_of_week="Суббота", start_time="13:00", end_time="15:00",
                            room="Зал 1"),
            models.Schedule(dance_class_id=5, teacher_id=5, day_of_week="Суббота", start_time="15:30", end_time="16:45",
                            room="Зал 2"),
            models.Schedule(dance_class_id=6, teacher_id=1, day_of_week="Суббота", start_time="17:00", end_time="18:30",
                            room="Зал 1"),

            # Воскресенье
            models.Schedule(dance_class_id=4, teacher_id=4, day_of_week="Воскресенье", start_time="12:00",
                            end_time="13:00", room="Зал 2"),
            models.Schedule(dance_class_id=1, teacher_id=2, day_of_week="Воскресенье", start_time="14:00",
                            end_time="15:00", room="Зал 1")
        ]

        for item in schedule:
            db.add(item)

        # Добавляем администратора
        admin_user = db.query(models.User).filter(models.User.email == "admin@dancestudio.ru").first()
        if not admin_user:
            hashed_password = get_password_hash("admin123")
            admin_user = models.User(
                email="admin@dancestudio.ru",
                hashed_password=hashed_password,
                full_name="Администратор",
                is_admin=True
            )
            db.add(admin_user)

        # Добавляем тестовые новости
        news_items = [
            models.News(
                title="Открытие нового танцевального зала",
                content="Мы рады сообщить об открытии нового современного танцевального зала, оборудованного по последнему слову техники. Новый зал площадью 150 кв.м. оснащен профессиональными зеркалами, системой вентиляции и современным звуковым оборудованием. Приходите на пробное занятие и оцените новые возможности!",
                author_id=1,
                image_url="/static/images/news1.jpg"
            ),
            models.News(
                title="Летний интенсив по хип-хопу",
                content="Приглашаем всех на летний интенсив по хип-хопу с профессиональными хореографами. Интенсив пройдет с 1 по 15 июля. За две недели вы освоите базовые движения, научитесь импровизировать и подготовите полноценный танец. Отличная возможность провести лето с пользой и научиться чему-то новому!",
                author_id=1,
                image_url="/static/images/news2.jpg"
            ),
            models.News(
                title="Набор в детские группы",
                content="Объявляем набор в детские танцевальные группы для детей от 4 до 12 лет. Занятия проходят в игровой форме, способствуют развитию координации, музыкальности и творческих способностей. Первое пробное занятие - бесплатно! Записывайтесь заранее, количество мест ограничено.",
                author_id=1,
                image_url="/static/images/news3.jpg"
            )
        ]

        for news in news_items:
            db.add(news)

        db.commit()
        print("Тестовые данные успешно добавлены в базу данных!")

    except Exception as e:
        db.rollback()
        print(f"Ошибка при добавлении данных: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()