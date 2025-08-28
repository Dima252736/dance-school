document.addEventListener('DOMContentLoaded', function() {
    // Фильтрация расписания
    const filterButtons = document.querySelectorAll('.filter-btn');
    const scheduleDays = document.querySelectorAll('.schedule-day');

    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Убираем активный класс у всех кнопок
                filterButtons.forEach(btn => btn.classList.remove('active'));
                // Добавляем активный класс текущей кнопке
                this.classList.add('active');

                const day = this.getAttribute('data-day');

                // Показываем/скрываем дни
                scheduleDays.forEach(dayElement => {
                    if (day === 'all' || dayElement.getAttribute('data-day') === day) {
                        dayElement.style.display = 'block';
                    } else {
                        dayElement.style.display = 'none';
                    }
                });
            });
        });
    }

    // Валидация формы регистрации
    const registrationForm = document.querySelector('.registration-form form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(e) {
            const phoneInput = document.getElementById('phone');
            const phoneRegex = /^(\+7|8)[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/;

            if (!phoneRegex.test(phoneInput.value)) {
                e.preventDefault();
                alert('Пожалуйста, введите корректный номер телефона');
                phoneInput.focus();
            }
        });
    }
});